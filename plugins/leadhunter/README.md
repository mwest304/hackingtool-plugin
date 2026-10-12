# Blackridge Lead Hunter

A lead-generation **agent + program** for **Blackridge Builders** (home
improvement, Bruceton Mills WV).

It finds homeowners who are **publicly asking** for home-improvement work —
across local Facebook groups, Nextdoor, Craigslist, Marketplace, Reddit, job
boards, forums, and the open web — then **qualifies, scores, drafts a
branded first reply, and tracks every lead to close.**

- **Agent** (`skills/leadhunter/SKILL.md`): Claude runs the searches, reads the
  posts, judges each lead, and writes the outreach.
- **Program** (`scripts/leadhunter.py`): stores, scores (hot/warm/cold), and
  tracks every lead. Pure Python stdlib — nothing to install.

## Compliant by design

It works **public buy-intent posts only** — people openly asking for the
service. It does **not** scrape private contact data, cold-blast strangers, or
violate any site's terms. That keeps Blackridge legal, off the spam lists, and
in good standing on every platform.

## Quick start

Just talk to Claude with the skill active:

> "Find me some roofing leads around Kingwood."
> "Work the follow-up list."
> "Who do I need to call today?"

Or drive the program directly from `scripts/`:

```bash
python leadhunter.py config                 # show service area, trades, contact info
python leadhunter.py queries --trade roofing --max-towns 3   # build the search list
python leadhunter.py add --source reddit --need "roof leaking, need a roofer" \
    --location "Kingwood, WV" --url "https://..." --intent explicit --age 2 --contact-path dm
python leadhunter.py next                    # the follow-up queue, best first
python leadhunter.py draft <id>              # branded first-contact message
python leadhunter.py update <id> --status contacted --touch
python leadhunter.py stats                   # pipeline summary
python leadhunter.py export                  # CSV for your phone / Google Sheets
```

Run `python leadhunter.py <command> -h` for full options.

## Tuning it

Everything lives in **`config/blackridge.json`** — edit the town list (how far
you'll drive), the trades you want work in, the intent phrases, and the
sources. Run `python leadhunter.py rescore` after big changes.

## Your data stays yours

Real leads are written to `leads/leads.jsonl` and `leads/leads.csv`, which are
**git-ignored** — customer info never leaves your machine.

---

*Built for Michael West / Blackridge Builders. (304) 405-2106 · blackridgebuilderswv.com*
