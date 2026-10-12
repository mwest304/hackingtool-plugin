# Where Preston County / Morgantown homeowners actually post

Read this to know *where* to hunt and *how* to read each channel. Ranked by how
often real, local, ready-to-hire leads show up.

## Tier 1 — highest-intent, local

### Local Facebook groups  `[check in browser]`
The #1 source for small-town WV home-improvement leads. People post
"anyone know a good roofer near Kingwood?" constantly.
- **Where:** "Preston County Buy Sell Trade", "Morgantown WV Community",
  "Kingwood / Terra Alta" groups, county yard-sale groups.
- **Read it:** look for a *homeowner* asking, not a contractor advertising.
  Comments often already have competitors — reply fast and local wins.
- **Search blocks indexing**, so `site:facebook.com` web searches miss most of
  it. Check the groups directly in a browser. This is worth the manual time.

### Nextdoor recommendation requests  `[check in browser]`
"Looking for recommendations for..." is literally a built-in post type.
Hyper-local by design. Browser only.

### Facebook Marketplace — services  `[check in browser]`
Homeowners post jobs under services/requests. Browser only.

## Tier 2 — searchable, good signal

### Craigslist  `[web-search]`
- Morgantown CL covers Preston County. Check **"gigs"** and **"services"** and
  anything in housing/wanted where someone needs repair work.
- `site:craigslist.org ("wanted" OR "services") <trade> "<town>"`

### Reddit  `[web-search]`
- `r/Morgantown`, `r/WestVirginia`, `r/HomeImprovement`, `r/Preston County` if active.
- People ask for contractor recs and post DIY-gone-wrong "need a pro now" threads.
- `site:reddit.com ("need a contractor" OR "anyone recommend") <trade> "<town>"`

### Thumbtack / Angi / HomeAdvisor  `[web-search]`
- Open request pages sometimes surface in search. These are pay-to-quote
  marketplaces — a lead here may mean Michael signs up to bid. Flag it as a
  lead but note the platform cost in `--notes`.

## Tier 3 — slower, but real jobs

### Local forums & community boards  `[web-search]`
County/town boards, church and school community pages, HOA boards.

### Open-web signals  `[web-search]`
Indirect but powerful — people with a *reason* to need work soon:
- **Storm/weather news** in the area → roofing, siding, gutters, water damage.
  (`"Preston County" storm damage` / hail / wind.)
- **FSBO & fixer-upper listings** → the buyer or seller often needs work done.
- **Public building-permit notices** (county sites) → an active project; the
  owner may still need trades. Public record, fair game.

## Reading any lead — the 10-second gut check

1. **Homeowner, or competitor/spam?** Skip other contractors and lead-broker pages.
2. **In the service radius?** Town in the config list = yes. Unknown WV/MD/PA = maybe (log it warm). Far away = skip.
3. **A trade we do?** Match the config; skip plumbing/HVAC/electrical-rewire.
4. **Fresh?** Today–this week = hot. Last month = warm. Older = cold or skip.
5. **Can we reply publicly?** If yes → log with the right `--contact-path` and draft. If the only way to reach them is private info they didn't post → log `contact_path none`, don't message.
