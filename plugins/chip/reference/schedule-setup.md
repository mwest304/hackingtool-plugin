# Making follow-up near-real-time

The lead loop works three ways, cheapest/fastest first. Pick what fits.

## 1. On-demand (works right now, $0 setup)

Say **"Chip, handle my leads"** — or forward/paste an inquiry — and Chip runs the
full sweep → qualify → draft → page → log loop immediately. Use this the moment a
lead comes in or a few times a day. Nothing to connect beyond Gmail (already live).

## 2. Scheduled sweep (near-real-time, closes the overnight gap)

A scheduled task wakes Chip every N minutes, sweeps the lead channels, drafts and
sorts anything new, pages hot leads, and leaves the batch waiting for approval. On
a 10–15 minute cadence a lead that lands at 2am has a reply drafted and the owner
paged before coffee.

**To arm it, Chip needs four facts** (then it sets the scheduled task):
1. **Lead inbox** — which Gmail address / label the inquiries land in.
2. **Cadence** — how often to sweep (default: every 15 min during the day, hourly overnight).
3. **Hot-lead page** — where a hot lead alert should go (owner's email? phone via text? a channel?).
4. **Confirm**: drafts stay held for approval — yes (there is no auto-send).

Mechanism (Chip handles this — documented so it's not a black box): a recurring
scheduled task fires the `chip-leads` loop. Chip sets it only on the owner's
explicit go, because it's a standing, recurring action. It drafts and pages; it
never sends.

## 3. Truly instant (seconds — the moment a form is submitted)

A reply that goes out within seconds of a web-form submit, with no wait for a
sweep, needs a real-time trigger wired to the lead source (a webhook or a texting
service like a Twilio/▪ SMS connector). That's a `small-business:build-connector`
job:
- Connect the lead platform (website form, Angi/Thumbtack/Facebook Leads) so a new
  lead fires an event instead of waiting to be polled.
- Connect SMS so first contact can be a text, not just email — texts get read in
  minutes, email in hours.

Even here, "send" still waits for the owner's approval unless the owner explicitly
sets an auto-reply template for a known-safe first touch — and that's the owner's
call to make, on the record.

## Honest expectation-setting

- Option 1 and 2 are available today with the connected tools. Option 2 is
  "minutes," not "seconds."
- Option 3 ("seconds, fully automatic") depends on connectors that aren't wired
  yet. It's a real next step, not a promise Chip can keep today.
