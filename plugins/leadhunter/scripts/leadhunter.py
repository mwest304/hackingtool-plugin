#!/usr/bin/env python3
"""
Blackridge Lead Hunter — the program half of the lead-gen agent.

Stdlib only. No external deps, no network calls, no scraping. The hunting
(web search) is done by the Claude agent per SKILL.md; this program turns the
agent's work into concrete search queries, then stores, scores, and tracks the
leads it finds.

Subcommands:
  queries   Build the web-search query list the agent runs (the "scan" map).
  add       Record a found lead; auto-scores and tiers it.
  list      Show leads (filter by tier/status/trade/source).
  next      The follow-up queue: who to contact next, best first.
  update    Change a lead's status / notes / last-touch.
  rescore   Recompute scores (after editing config).
  draft     Print a Blackridge-branded first-contact message for a lead.
  stats     Pipeline summary.
  export    Write all leads to CSV (open on your phone / import to Sheets).
  config    Show the active config.

Run `python leadhunter.py <subcommand> -h` for details.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "blackridge.json"
LEADS_DIR = ROOT / "leads"
LEADS_FILE = LEADS_DIR / "leads.jsonl"

INTENT_LEVELS = ("explicit", "implied", "mention")
CONTACTABLE = ("comment", "dm", "phone", "email", "form")
STATUSES = ("new", "contacted", "replied", "quoted", "won", "lost", "dead")


# --------------------------------------------------------------------------- #
# IO helpers
# --------------------------------------------------------------------------- #
def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        die(f"config not found: {CONFIG_PATH}")
    with CONFIG_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_leads() -> list[dict]:
    if not LEADS_FILE.exists():
        return []
    leads = []
    with LEADS_FILE.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                leads.append(json.loads(line))
    return leads


def save_leads(leads: list[dict]) -> None:
    LEADS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = LEADS_FILE.with_suffix(".jsonl.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        for lead in leads:
            fh.write(json.dumps(lead, ensure_ascii=False) + "\n")
    tmp.replace(LEADS_FILE)


def die(msg: str) -> "NoReturn":  # type: ignore[name-defined]
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def emit(payload, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))


# --------------------------------------------------------------------------- #
# Scoring
# --------------------------------------------------------------------------- #
def detect_trade(text: str, cfg: dict) -> str | None:
    text_l = text.lower()
    for trade, words in cfg["trades"]["offered"].items():
        for w in words:
            if w.lower() in text_l:
                return trade
    return None


def in_service_area(location: str, cfg: dict) -> str:
    """Return 'in', 'out', or 'unknown'."""
    if not location:
        return "unknown"
    loc_l = location.lower()
    for town in cfg["service_area"]["towns"]:
        if town.lower() in loc_l:
            return "in"
    # State match without a known town = uncertain but plausible.
    for st in cfg["service_area"]["states"]:
        if re.search(rf"\b{re.escape(st.lower())}\b", loc_l):
            return "unknown"
    return "out"


def score_lead(lead: dict, cfg: dict) -> tuple[int, str]:
    score = 0

    # Buy-intent strength — the single biggest factor.
    score += {"explicit": 45, "implied": 25, "mention": 10}.get(lead.get("intent", "mention"), 10)

    # Recency — a fresh post is a live lead.
    age = lead.get("posted_age_days")
    if isinstance(age, (int, float)):
        if age <= 2:
            score += 20
        elif age <= 7:
            score += 12
        elif age <= 30:
            score += 5

    # Location. Known in-area town is a strong plus; a confirmed out-of-area
    # town is a strong minus; anything we can't place stays neutral so it lands
    # in 'warm' for a human to eyeball rather than faking a hot score.
    area = in_service_area(lead.get("location", ""), cfg)
    score += {"in": 20, "unknown": 0, "out": -15}[area]

    # Trade match.
    if lead.get("trade") in cfg["trades"]["offered"]:
        score += 10

    # Can we actually reach them?
    if lead.get("contact_path") in CONTACTABLE:
        score += 5

    score = max(0, min(100, score))
    tier = "hot" if score >= 70 else "warm" if score >= 40 else "cold"
    return score, tier


# --------------------------------------------------------------------------- #
# queries — the "scan everywhere" map
# --------------------------------------------------------------------------- #
SOURCE_OPERATORS = {
    "craigslist": 'site:craigslist.org ("wanted" OR "services") {trade} {town}',
    "reddit": 'site:reddit.com ({intent}) {trade} {town}',
    "thumbtack": '("thumbtack" OR "angi" OR "homeadvisor") {trade} {town} request',
    "forums": '{intent} {trade} {town} forum OR board',
    "web": '{intent} {trade} near {town}',
    "facebook_groups": 'site:facebook.com {intent} {trade} {town}',
    "marketplace": 'site:facebook.com/marketplace {trade} {town}',
    "nextdoor": 'site:nextdoor.com {intent} {trade} {town}',
}


def cmd_queries(args, cfg):
    trades = cfg["trades"]["offered"]
    towns = cfg["service_area"]["towns"]
    intents = cfg["intent_phrases"]["explicit"]

    sel_trades = [args.trade] if args.trade else list(trades.keys())
    sel_towns = [args.town] if args.town else towns[: args.max_towns]
    channels = cfg["sources"]["channels"]
    if args.source:
        channels = [c for c in channels if c["id"] == args.source]

    # A representative intent phrase keeps the query list short but potent.
    intent_sample = args.intent or (intents[0] if intents else "need a contractor")

    out = []
    for ch in channels:
        tmpl = SOURCE_OPERATORS.get(ch["id"])
        if not tmpl:
            continue
        for trade in sel_trades:
            # Use the plainest keyword for the trade in the query.
            trade_word = trades.get(trade, [trade])[0] if trade in trades else trade
            for town in sel_towns:
                q = tmpl.format(
                    trade=trade_word,
                    town=f'"{town}"',
                    intent=f'"{intent_sample}"',
                ).strip()
                q = re.sub(r"\s+", " ", q)
                out.append(
                    {
                        "source": ch["id"],
                        "mode": ch["mode"],
                        "label": ch["label"],
                        "trade": trade,
                        "town": town,
                        "query": q,
                    }
                )

    if args.json:
        emit(out, True)
        return
    print(f"# {len(out)} search queries for the Lead Hunter to run\n")
    current = None
    for item in out:
        if item["source"] != current:
            current = item["source"]
            tag = "[web-search]" if item["mode"] == "search" else "[check in browser]"
            print(f"\n## {item['label']} {tag}")
        print(f"  ({item['trade']} / {item['town']})  {item['query']}")
    print(
        "\nHow to use: run the [web-search] queries with your web search tool, "
        "open the [check in browser] sources directly, then record each real lead with:\n"
        "  python leadhunter.py add --source <id> --need '...' --location '...' --url '...' --intent explicit"
    )


# --------------------------------------------------------------------------- #
# add
# --------------------------------------------------------------------------- #
def make_id(lead: dict) -> str:
    basis = (lead.get("url") or "") + (lead.get("need") or "") + (lead.get("name") or "")
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:10]


def cmd_add(args, cfg):
    leads = load_leads()
    text_for_trade = " ".join(filter(None, [args.need, args.notes]))
    trade = args.trade or detect_trade(text_for_trade, cfg)

    lead = {
        "id": "",
        "created": now_iso(),
        "source": args.source,
        "channel_detail": args.channel_detail or "",
        "url": args.url or "",
        "name": args.name or "",
        "location": args.location or "",
        "need": args.need,
        "trade": trade,
        "posted_age_days": args.age,
        "intent": args.intent,
        "contact_path": args.contact_path,
        "notes": args.notes or "",
        "status": "new",
        "score": 0,
        "tier": "",
        "last_touch": None,
    }
    lead["id"] = make_id(lead)

    # Dedupe on url (if present) else on generated id.
    for existing in leads:
        same = (args.url and existing.get("url") == args.url) or existing["id"] == lead["id"]
        if same:
            if args.json:
                emit({"status": "duplicate", "id": existing["id"]}, True)
            else:
                print(f"duplicate — already tracked as {existing['id']} ({existing['status']})")
            return

    lead["score"], lead["tier"] = score_lead(lead, cfg)
    leads.append(lead)
    save_leads(leads)

    if args.json:
        emit(lead, True)
    else:
        print(f"added {lead['id']}  [{lead['tier'].upper()} {lead['score']}]  "
              f"{lead['trade'] or 'untagged'} — {lead['need']}")


# --------------------------------------------------------------------------- #
# list / next
# --------------------------------------------------------------------------- #
def _filter(leads, args):
    out = leads
    if getattr(args, "tier", None):
        out = [l for l in out if l["tier"] == args.tier]
    if getattr(args, "status", None):
        out = [l for l in out if l["status"] == args.status]
    if getattr(args, "trade", None):
        out = [l for l in out if l.get("trade") == args.trade]
    if getattr(args, "source", None):
        out = [l for l in out if l["source"] == args.source]
    return out


def _print_table(leads):
    if not leads:
        print("(no leads)")
        return
    print(f"{'ID':<11}{'TIER':<6}{'SCR':<5}{'STATUS':<10}{'TRADE':<14}{'LOCATION':<20}NEED")
    print("-" * 100)
    for l in leads:
        print(
            f"{l['id']:<11}{l['tier']:<6}{l['score']:<5}{l['status']:<10}"
            f"{(l.get('trade') or '-'):<14}{(l.get('location') or '-')[:19]:<20}"
            f"{(l.get('need') or '')[:40]}"
        )


def cmd_list(args, cfg):
    leads = _filter(load_leads(), args)
    leads.sort(key=lambda l: (-l["score"], l["created"]))
    if args.json:
        emit(leads, True)
    else:
        _print_table(leads)


def cmd_next(args, cfg):
    leads = load_leads()
    # The follow-up queue: anything not yet closed, hot/warm first.
    live = [l for l in leads if l["status"] in ("new", "contacted", "replied", "quoted")]
    live.sort(key=lambda l: (-l["score"], l.get("last_touch") or "", l["created"]))
    live = live[: args.limit]
    if args.json:
        emit(live, True)
        return
    if not live:
        print("queue empty — go run the hunter: python leadhunter.py queries")
        return
    print("FOLLOW-UP QUEUE (work top to bottom)\n")
    for i, l in enumerate(live, 1):
        print(f"{i}. [{l['tier'].upper()} {l['score']}] {l['id']}  {l['status']}")
        print(f"   {l.get('trade') or 'untagged'} | {l.get('location') or 'location?'} | "
              f"{l['source']}{(' — ' + l['channel_detail']) if l['channel_detail'] else ''}")
        print(f"   NEED: {l.get('need')}")
        if l.get("url"):
            print(f"   LINK: {l['url']}")
        print()


# --------------------------------------------------------------------------- #
# update / rescore
# --------------------------------------------------------------------------- #
def cmd_update(args, cfg):
    leads = load_leads()
    found = None
    for l in leads:
        if l["id"] == args.id:
            found = l
            break
    if not found:
        die(f"no lead with id {args.id}")
    if args.status:
        if args.status not in STATUSES:
            die(f"status must be one of {STATUSES}")
        found["status"] = args.status
    if args.notes is not None:
        found["notes"] = (found.get("notes", "") + " | " + args.notes).strip(" |")
    if args.touch:
        found["last_touch"] = now_iso()
    save_leads(leads)
    if args.json:
        emit(found, True)
    else:
        print(f"updated {found['id']}: status={found['status']} "
              f"last_touch={found['last_touch'] or '-'}")


def cmd_rescore(args, cfg):
    leads = load_leads()
    for l in leads:
        l["score"], l["tier"] = score_lead(l, cfg)
    save_leads(leads)
    if args.json:
        emit({"rescored": len(leads)}, True)
    else:
        print(f"rescored {len(leads)} leads")


# --------------------------------------------------------------------------- #
# draft — Blackridge-branded first contact (plain text)
# --------------------------------------------------------------------------- #
def cmd_draft(args, cfg):
    leads = load_leads()
    lead = next((l for l in leads if l["id"] == args.id), None)
    if not lead:
        die(f"no lead with id {args.id}")
    b = cfg["business"]
    trade = (lead.get("trade") or "that project").replace("_", " ")
    town = lead.get("location") or "your area"

    msg = (
        f"Hey — saw your post about {lead.get('need') or trade}. "
        f"I'm Michael with {b['name']} out of {b['home_base']}. "
        f"We handle {trade} work all over {town.split(',')[0]} and the area, and we show up when we say we will.\n\n"
        f"Happy to swing by, take a look, and give you a straight, no-pressure quote — free. "
        f"If it's something we can knock out, great; if not, I'll point you to the right person.\n\n"
        f"Best way to reach me is {b['phone']} or {b['email']}. "
        f"What's your timeline looking like?\n\n"
        f"— Michael West\n{b['name']} | {b['tagline']}\n{b['phone']} | {b['website']}"
    )
    if args.json:
        emit({"id": lead["id"], "draft": msg}, True)
    else:
        print("NOTE: public post? Reply in the thread first, keep it short, move to DM/phone.\n")
        print(msg)
        print("\n(Reminder: no pre-checked boxes, no unsolicited texts to a number they "
              "didn't post publicly — keep it compliant.)")


# --------------------------------------------------------------------------- #
# stats / export / config
# --------------------------------------------------------------------------- #
def cmd_stats(args, cfg):
    leads = load_leads()
    by_tier = {}
    by_status = {}
    by_source = {}
    for l in leads:
        by_tier[l["tier"]] = by_tier.get(l["tier"], 0) + 1
        by_status[l["status"]] = by_status.get(l["status"], 0) + 1
        by_source[l["source"]] = by_source.get(l["source"], 0) + 1
    payload = {
        "total": len(leads),
        "by_tier": by_tier,
        "by_status": by_status,
        "by_source": by_source,
    }
    if args.json:
        emit(payload, True)
        return
    print(f"LEADS: {len(leads)} total")
    print(f"  tier:   {dict(sorted(by_tier.items()))}")
    print(f"  status: {dict(sorted(by_status.items()))}")
    print(f"  source: {dict(sorted(by_source.items()))}")
    hot_new = len([l for l in leads if l["tier"] == "hot" and l["status"] == "new"])
    if hot_new:
        print(f"\n>>> {hot_new} HOT lead(s) untouched — run: python leadhunter.py next")


def cmd_export(args, cfg):
    leads = load_leads()
    path = Path(args.csv) if args.csv else (LEADS_DIR / "leads.csv")
    cols = ["id", "created", "tier", "score", "status", "trade", "location",
            "need", "source", "channel_detail", "url", "name", "intent",
            "contact_path", "posted_age_days", "last_touch", "notes"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for l in leads:
            w.writerow(l)
    if args.json:
        emit({"exported": len(leads), "path": str(path)}, True)
    else:
        print(f"exported {len(leads)} leads -> {path}")


def cmd_config(args, cfg):
    if args.json:
        emit(cfg, True)
    else:
        b = cfg["business"]
        print(f"{b['name']} — {b['home_base']}")
        print(f"  contact: {b['phone']} | {b['email']} | {b['website']}")
        print(f"  towns ({len(cfg['service_area']['towns'])}): "
              f"{', '.join(cfg['service_area']['towns'][:8])} ...")
        print(f"  trades: {', '.join(cfg['trades']['offered'].keys())}")
        print(f"  sources: {', '.join(c['id'] for c in cfg['sources']['channels'])}")
        print(f"\n  edit: {CONFIG_PATH}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(description="Blackridge Lead Hunter")
    # Shared flag available on every subcommand (so `list --json` works, not
    # just `--json list`).
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", help="machine-readable JSON output")
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("queries", parents=[common], help="build the web-search query list")
    q.add_argument("--trade", help="limit to one trade key")
    q.add_argument("--town", help="limit to one town")
    q.add_argument("--source", help="limit to one source id")
    q.add_argument("--intent", help="override the intent phrase used")
    q.add_argument("--max-towns", type=int, default=5, help="cap towns per trade (default 5)")
    q.set_defaults(func=cmd_queries)

    a = sub.add_parser("add", parents=[common], help="record a found lead")
    a.add_argument("--source", required=True, help="source id (craigslist, reddit, ...)")
    a.add_argument("--need", required=True, help="what they're asking for")
    a.add_argument("--location", default="", help="town, state")
    a.add_argument("--url", default="", help="link to the public post")
    a.add_argument("--name", default="", help="poster display name (if public)")
    a.add_argument("--trade", help="trade key (auto-detected if omitted)")
    a.add_argument("--intent", choices=INTENT_LEVELS, default="mention")
    a.add_argument("--age", type=int, help="how many days old the post is")
    a.add_argument("--contact-path", dest="contact_path", choices=CONTACTABLE + ("none",),
                   default="none", help="how you can reach them")
    a.add_argument("--channel-detail", dest="channel_detail", default="",
                   help="e.g. the group/sub name")
    a.add_argument("--notes", default="")
    a.set_defaults(func=cmd_add)

    ls = sub.add_parser("list", parents=[common], help="show leads")
    ls.add_argument("--tier", choices=("hot", "warm", "cold"))
    ls.add_argument("--status", choices=STATUSES)
    ls.add_argument("--trade")
    ls.add_argument("--source")
    ls.set_defaults(func=cmd_list)

    nx = sub.add_parser("next", parents=[common], help="follow-up queue")
    nx.add_argument("--limit", type=int, default=10)
    nx.set_defaults(func=cmd_next)

    up = sub.add_parser("update", parents=[common], help="update a lead")
    up.add_argument("id")
    up.add_argument("--status", choices=STATUSES)
    up.add_argument("--notes")
    up.add_argument("--touch", action="store_true", help="stamp last_touch = now")
    up.set_defaults(func=cmd_update)

    rs = sub.add_parser("rescore", parents=[common], help="recompute all scores")
    rs.set_defaults(func=cmd_rescore)

    dr = sub.add_parser("draft", parents=[common], help="print a branded first-contact message")
    dr.add_argument("id")
    dr.set_defaults(func=cmd_draft)

    st = sub.add_parser("stats", parents=[common], help="pipeline summary")
    st.set_defaults(func=cmd_stats)

    ex = sub.add_parser("export", parents=[common], help="write leads to CSV")
    ex.add_argument("--csv", help="output path (default leads/leads.csv)")
    ex.set_defaults(func=cmd_export)

    cf = sub.add_parser("config", parents=[common], help="show active config")
    cf.set_defaults(func=cmd_config)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    cfg = load_config()
    args.func(args, cfg)


if __name__ == "__main__":
    main()
