# The get-found funnel — make leads come to you

Hunting is one half. The other half is making homeowners who are *already
searching* ("remodeler near Morgantown") find Blackridge and call. For a local
contractor this is the highest-ROI, lowest-cost thing you can do, and it
compounds — set it once, it works forever.

Two pieces: **Google Business Profile** (free, do this first) and the
**lead-capture page** (`landing/blackridge-free-estimate.html`).

---

## 1. Google Business Profile (GBP) — free, do this first

A GBP is what puts you on Google Maps and in the "remodeler / roofer near me"
results. Blackridge already has one — but a public web check turned up **nothing**,
which means it isn't ranking. The fix is below.

> ### ⚠️ FIX FIRST — NAP consistency (the #1 reason you're invisible)
> Google only ranks a local business it *trusts*, and trust comes from your
> **Name + Address + Phone being identical everywhere**. Right now your website
> says Fairmont while other records said Bruceton Mills — that mismatch alone can
> bury you. Lock in ONE of each and make it match on the GBP, the website, and
> every directory:
> - **Name:** Blackridge Builders
> - **Address:** 107 Highland Ave, Fairmont, WV 26554 (your business address of record)
> - **Phone:** (304) 405-2106
> - **Email:** blackridgewv@outlook.com
> - **Website:** blackridgebuilderswv.com
>
> Do this before anything else. Then claim the free directory listings below so
> every site on the web points the same way.

**Check / complete your GBP (you, on your Google account):**
1. Go to **google.com/business** → sign in → open your Blackridge Builders listing.
   Confirm it says **Verified** and **published** (nothing shows publicly until it's
   verified). If it isn't verified, finish verification first — that alone could be
   why nobody finds you.
2. Category: **General Contractor** (add secondary: Siding Contractor, Remodeler,
   Flooring Contractor, Painter, Roofing Contractor, Handyman). Lead with your core
   work; roofing is secondary.
3. Set it as a **service-area business** and list your real area: Fairmont,
   Morgantown, Clarksburg, Bridgeport, and out through Preston County
   (Kingwood/Bruceton Mills) + the MD/PA edge — north-central WV.
4. Confirm Phone **(304) 405-2106** and Website **blackridgebuilderswv.com** match
   the NAP box above exactly.
5. Fill it fully: hours, services (list every trade), a real description in your
   voice, and **photos of finished jobs** (before/after sells hardest). Add new
   photos monthly — Google rewards active profiles.

**The move that wins local: reviews.** After every job, text the customer:
> "Thanks again — if you've got 30 seconds, a quick Google review really helps a
> small local shop like mine. Here's the link: [your GBP review link]"

5+ recent reviews and you outrank the big franchise names in your towns.

**Build citations (free, ~1 hour total).** Claim a free listing on each of these
and enter the **exact same** Name / Address / Phone from the NAP box — this is how
Google learns to trust and rank you:
- Bing Places, Apple Business Connect, Facebook (business page), Yelp, BBB,
  Angi, Nextdoor (business page), YellowPages.
A dozen consistent listings moves the needle more than any single one.

---

## 2. The lead-capture page (`landing/blackridge-free-estimate.html`)

A one-page site that turns a click into a call or a form submission. Built
Blackridge-branded, mobile-first (most of your traffic is phones off Facebook).

**What it does:**
- Giant **Call** and **Text** buttons at the top (most people just want to call).
- A short **Free Estimate** form (name, phone, town, what they need).
- The post-storm free-inspection offer baked in.

**Deploy it (you):**
1. **Wire the form to your inbox.** Open the file, find the `FORMSPREE_ENDPOINT`
   placeholder, and replace it with a free form endpoint from **formspree.io**
   (sign up free → new form → paste its URL). Submissions then email you at
   blackridgewv@outlook.com. *(Or tell me your site's stack — WordPress, etc. — and
   I'll wire it to that instead.)*
2. **Add your logo:** drop `blackridge_logo.png` in the same folder (the page
   already has a slot for it; it looks clean without it too).
3. **Host it:** upload to blackridgebuilderswv.com (as the homepage or a
   `/free-estimate` page). If you're on WordPress, I can push it there directly
   once your site's connected.
4. **Point everything at it:** put the link in your GBP, your Facebook page's
   button, and every post. One link, everywhere.

---

## How the funnel feeds the tracker

Every call and form submission is a lead. Log them so nothing slips:
```
python leadhunter.py add --source web --need "<what they asked for>" \
    --location "<town>" --intent explicit --contact-path phone --name "<name>"
```
Then `python leadhunter.py next` keeps your follow-ups straight.
