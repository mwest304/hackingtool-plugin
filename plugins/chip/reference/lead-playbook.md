# Lead Playbook — Blackridge Builders

Qualification criteria and routing that `chip-leads` / `speed-to-lead` use to sort
every inbound. Tune the ‹confirm› lines once; they become the rules.

## The SLA (the whole point)

- **First reply drafted: within 5 minutes** of a lead landing (on a scheduled run,
  within the run interval).
- **Hot lead paged to owner: immediately**, not in a digest.
- Why: in home improvement, the homeowner is messaging 3–4 contractors in one
  sitting. First clear, human reply with real appointment times usually books the
  estimate. Slow = lost, even if you're the better builder.

## The four buckets

Every inbound sorts into exactly one:

| Bucket | What it looks like | Action |
|---|---|---|
| **Hot** | Owns the home, in service area, clear scope, mentions a budget or a date, urgency ("need it before winter"), came from a referral/ad | Page owner now + draft reply offering the soonest two slots |
| **Qualified** | Fits, no urgency | Draft reply, offer times, book the estimate |
| **Unclear** | Vague scope / no location / "just prices" | Draft reply with the ONE question that resolves it (usually: address + what's the project?) |
| **Out of scope** | Outside area, work we don't do, cheapest-bid-only | Honest reply, refer out if we can |

## Qualification inputs

The live values live in `../../config/blackridge-profile.md` (read it first).
Summary:

- **Service area:** Fairmont / Morgantown / Clarksburg / Bridgeport / Bruceton Mills
  (Marion, Monongalia, Harrison, Preston counties). Radius **30 mi** (site says 50 — ‹confirm›).
  Outside it = out of scope unless the job is big enough to travel for.
- **Work we do:** kitchen & bath remodels, comprehensive remodeling, drywall (incl.
  single patches), interior painting, flooring, tile, siding.
- **Work we decline:** additions, roofing, decks, standalone electrical/plumbing,
  new-construction builds (unless the owner says otherwise).
- **Small jobs welcome** — a single drywall patch is still a lead, not a brush-off.
- **Red flags → out-of-scope/unclear:** won't give an address, wants a firm price
  with no site visit, a trade we don't do, insurance-only scope-shoppers.

## First-reply structure (home improvement)

1. **Answer their actual question** (price range, availability, "do you do X?").
2. **Confirm we can help** — or honestly say we can't and who can.
3. **Offer two or three real appointment times** for a free estimate / site visit,
   pulled live from Google Calendar — respect drive time between jobs.
4. **One next step** — "Reply with the one that works and I'll lock it in."

Under 100 words. Plain. In Mike's voice once it's captured.

## Routing after the reply

- Needs a multi-touch sequence → `outreach-composer`
- Log every touch → `crm-autopilot`
- Rank today's qualified into a call list → `lead-triage` → `call-list`
- Ready to quote a qualified job → `proposal-builder`

## What kills leads (don't do it)

- Generic "thanks, we'll be in touch" — buys nothing, they expected it.
- Offering a slot that's already booked — costs a second exchange at the worst moment.
- Ignoring out-of-scope — a 30-second referral comes back as goodwill and repeat work.
- Replying under a human who already answered.
- Making the homeowner wait overnight for a hot lead.
