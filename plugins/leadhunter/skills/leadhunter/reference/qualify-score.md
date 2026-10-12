# Qualifying, scoring & outreach

## The scoring model (what `leadhunter.py` computes)

Each lead gets 0–100, summed from five signals, then tiered.

| Signal | Points | Why |
|--------|--------|-----|
| **Intent** | explicit **+45** · implied **+25** · mention **+10** | Someone asking to hire beats someone musing. The biggest factor. |
| **Recency** | ≤2d **+20** · ≤7d **+12** · ≤30d **+5** · older **0** | A live post is a live lead. |
| **Location** | in-area **+20** · unknown **0** · out-of-area **−15** | Local wins; far away is a time sink. |
| **Trade match** | **+10** | It's work Blackridge actually does. |
| **Reachable** | **+5** | There's a public way to respond. |

**Tiers:** hot ≥ 70 · warm 40–69 · cold < 40.

### Set the inputs honestly
- `--intent explicit` only when they're clearly trying to hire ("need a roofer", "getting quotes", "ISO contractor"). `implied` for problems ("roof's leaking"). `mention` for everything softer. **Don't inflate intent to fake a hot score — it just wastes Michael's time on a cold call.**
- `--age` in days from when they posted. Guess conservatively if unsure.
- `--location "Town, ST"` — the town match is what earns the +20.
- `--contact-path` — `comment`/`dm`/`form`/`email`/`phone` if public, else `none`.

Re-run `python leadhunter.py rescore` after editing the config (new towns/trades shift scores).

## The Blackridge outreach playbook

`leadhunter.py draft <id>` gives you the skeleton. Before sending, make it
*yours* and *theirs*:

**Do:**
- Reference their actual words ("saw your roof's leaking after Tuesday's storm").
- Lead with identity + local: "Michael with Blackridge Builders, out of Bruceton Mills."
- Offer a free, no-pressure look. Low commitment gets the yes.
- Keep it to 3–4 short sentences. Trades talk, not essays.
- End with the phone number and one easy question ("What's your timeline?").

**Don't:**
- Paste a wall of text or a corporate pitch.
- Send the same message twice to the same thread.
- Over-promise price before seeing the job.
- Message anyone who didn't publicly ask.

**Voice (from the brand-identity skill — this is non-negotiable):**
> Straight-talking. Blue-collar. No fluff. "We show up, we do the work, we do it right."
> NEVER: "We leverage synergistic home improvement solutions."

**Channel manners:**
- Public thread (FB group, Reddit, Nextdoor): a short, friendly public reply
  builds trust and lets the asker DM you. Don't dump your life story in public.
- Then move to DM/phone to talk specifics.

## Working the pipeline

- `new` → you found it, haven't reached out.
- `contacted` → you replied/messaged. Always `--touch` so follow-up timing is tracked.
- `replied` → they answered. Hot — respond same day.
- `quoted` → you gave a number. Follow up in 2–3 days if quiet.
- `won` / `lost` → closed. Log it; the stats teach us which sources pay.
- `dead` → went cold or not real. Clear it out of `next`.

**The rule:** no hot lead sits at `new` overnight. If Michael can't get to it,
that's the one thing to flag to him by name.
