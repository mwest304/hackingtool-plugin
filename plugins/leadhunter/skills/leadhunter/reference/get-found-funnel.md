# The get-found funnel — make leads come to you

Hunting is one half. The other half is making homeowners who are *already
searching* ("roofer near Kingwood") find Blackridge and call. For a local
contractor this is the highest-ROI, lowest-cost thing you can do, and it
compounds — set it once, it works forever.

Two pieces: **Google Business Profile** (free, do this first) and the
**lead-capture page** (`landing/blackridge-free-estimate.html`).

---

## 1. Google Business Profile (GBP) — free, ~30 minutes, do it first

A GBP is what puts you on Google Maps and in the "roofers near me" results. Most
small contractors either don't have one or never finish it. Finishing yours beats
any paid ad.

**Setup steps (you, on your Google account):**
1. Go to **google.com/business** → sign in → **Add your business**.
2. Business name: **Blackridge Builders**. Category: **General Contractor** (add
   secondary categories: Roofing Contractor, Siding Contractor, Deck Builder,
   Handyman).
3. Choose **"I serve customers at their locations"** (service-area business — no
   storefront). Add your service area: Bruceton Mills, Kingwood, Terra Alta,
   Masontown, Reedsville, Morgantown, Cheat Lake, and the MD/PA edge towns.
4. Phone: **(304) 405-2106**. Website: **blackridgebuilderswv.com**.
5. **Verify** (Google mails a postcard or does phone/video verification). Nothing
   shows publicly until verified — don't skip this.
6. Fill it fully: hours, services (list every trade), a real description in your
   voice, and **photos of finished jobs** (before/after sells hardest). Add new
   photos monthly — Google rewards active profiles.

**The move that wins local: reviews.** After every job, text the customer:
> "Thanks again — if you've got 30 seconds, a quick Google review really helps a
> small local shop like mine. Here's the link: [your GBP review link]"

5+ recent reviews and you outrank the big franchise names in your towns.

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
   mwest304@outlook.com. *(Or tell me your site's stack — WordPress, etc. — and
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
