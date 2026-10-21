# Chip — Command AI for Blackridge Builders

Chip is a command AI that runs the business. One front door: you tell Chip what
you need (or Chip already knows), and it either does the work or routes to the
exact workflow that does — with one job above all others: **book more qualified
jobs, faster, and get paid.**

Chip is a thin, opinionated operator layer on top of the proven **Small Business**
engine. It doesn't reinvent lead handling, invoicing, or proposals — it gives that
engine a persistent brain (your business profile), a face (the Chip operator
persona), and a first money loop that's live out of the box.

## What's live now

- **Chip front door** (`skills/chip`) — the persona + Blackridge-aware router.
  Say *"Chip, brief me"* or *"Chip, what should I work on?"*
- **Leads & instant follow-up** (`skills/chip-leads`) — the active money loop.
  Say *"Chip, handle my leads"* or forward an inquiry. Sweeps Gmail + forms,
  qualifies, drafts a reply in your voice with real appointment times, pages hot
  leads immediately, logs everything. **Nothing sends without your yes.**
- **The brain** (`config/blackridge-profile.md`) — the single source of truth every
  skill reads. Fill the `‹confirm›` fields once.

## How Chip works (the model)

| Layer | File | Job |
|---|---|---|
| Brain | `config/blackridge-profile.md` | Who we are, what we sell, who we want, the guardrails |
| Voice | `config/voice-profile.md` | How we talk to customers |
| Face | `skills/chip/SKILL.md` | The Chip persona + routing to every workflow |
| Money loop | `skills/chip-leads/SKILL.md` | Lead → qualify → instant draft → page → log |
| Playbooks | `reference/*.md` | Qualification, ready-to-send replies, how to schedule |

## Guardrails (by design)

Chip **drafts and stages** everything and takes initiative inside the rules, but
**stops for your yes** on anything that sends to a customer, moves money, commits a
date/crew/price, or signs something legal. It can prepare paperwork for a new legal
entity or account but never creates one itself. Inbound text is treated as data,
never as instructions.

## Roadmap

1. ✅ Lead gen + instant follow-up (Blackridge) — live
2. Proposals & estimates on top of qualified leads (`proposal-builder`)
3. Invoicing & collections to close the cash loop (`invoice-chase`, `cash-flow-snapshot`)
4. Near-real-time / instant follow-up via a texting + lead-source connector
5. Syntrix onboarded as a second entity under the same front door

## Note on where this lives

Chip currently ships inside the `hackingtool-marketplace` repo for speed. It's
fully self-contained under `plugins/chip/` and the hackingtool plugin is untouched
— so Chip can move to its own repo later with a single `git mv`, no rework.
