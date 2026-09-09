# Lotus Foreign Exchange — evidence

Date checked: 2026-09-09

## Site
https://au.lotusfx.com/ — branches in Australia, New Zealand and Fiji per site content; "no-commission" FX and money-transfer positioning; also acts as a MoneyGram agent per site content.

## robots.txt
`https://au.lotusfx.com/robots.txt` → HTTP 404 Not Found. No robots.txt present at this path.

## Homepage — WebFetch summary
- Confirms transfers to Fiji, and describes an "eWire" remittance service between NZ, Australia and Fiji.
- Also offers MoneyGram-branded transfers (in association with MoneyGram) "to the Pacific and worldwide" — this makes Lotus FX partly a MoneyGram agent front-end, not a fully independent quote source for those transfers; worth separating in any future connector scoping.

## /exchange-rates page — WebFetch summary
- **No live rate table or FJD figure shown on the page itself.** The page is descriptive only: explains buy/sell rate concepts, and states "Rates displayed are indicative only and subject to change... updated every 30 minutes" — implying a rate table exists somewhere (in-store display, or the "Lotus FX Online" app) but **not on this public web page** as fetched.
- Directs users to three channels for an actual rate: physical store, the Lotus FX Online app, or contacting customer service by phone/email (`aucustomercare@lotusfx.com`).
- No fee schedule document found.
- No calculator found on this page.

## Tier assessment
**Tier 3 — no public FX table or calculator on the public web page**, despite the site *talking about* rates. The "Lotus FX Online" app was not evaluated (out of scope for a web-triage round; also apps are a different collection surface with their own considerations). If the app turns out to expose something public-facing and observable, that would be a reason to revisit — but the public website itself does not qualify.

## Confidence flags
- Did not check whether au.lotusfx.com has a New Zealand-equivalent domain/page (the WebSearch snippet mentioned NZ branches under a general "lotusfx.com" umbrella) — only the AU page was fetched here, per this batch's provider scope. If Lotus FX Pacific coverage matters for NZ origin too, that needs its own check.
- Did not evaluate the "Lotus FX Online" app; flagged above as an open question rather than assumed either way.
- The MoneyGram-agent relationship is stated by Lotus FX's own site, not independently verified against MoneyGram's own material in this session.
