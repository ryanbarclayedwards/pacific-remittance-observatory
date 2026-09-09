# Samoa Money Transfer — evidence

Date checked: 2026-09-09
Domain: samoamoneytransfer.co.nz

## URLs fetched
- https://samoamoneytransfer.co.nz/robots.txt
- https://samoamoneytransfer.co.nz/ (fetched twice, second time targeting fee/rate text specifically)

## robots.txt (verbatim)
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

Sitemap: https://samoamoneytransfer.co.nz/wp-sitemap.xml
```
Blocks only `/wp-admin/`; everything else permitted.

## Findings
- Address given is Otara, Auckland, NZ; phone +64 9 273 6330 — NZ-based, origin NZ. No mention of Australia as an origin found.
- Destination: Samoa (implied by name and content; not independently cross-checked against a destinations list).
- Fee and rate figures ARE published directly on the homepage: "Transfers / Bank Transfers $10 / 12 Per Transfer" and a rate figure "1.56" shown in the header navigation area. Presented as static text, not a table, and not obviously dated — no visible "as at" timestamp was found in the fetched content.
- No dedicated rates/fees URL found; the figures live on the homepage itself. Nav menu items seen: Home, About Us, Services, Food Shopping, AML/CFT, Agent Locations, Contact — no "Rates" or "Fees" page.
- No quote calculator found.
- No explicit statement on account requirements; site offers a "Get a Call Back" contact form rather than a self-service flow.

## Tier assessment
Tier 2 (borderline) — leaning toward: this looks closer to a static, undated fee/rate footer than a genuinely daily-published tariff, and it's NZ-only (no AU origin found, so out of scope for AU corridors; relevant only if NZ→Samoa is in scope). Flagged for the report's "decisions not made" section: the rate/fee text is unsourced as to update frequency, so calling it `published_tariff` (Tier 1) would be presenting an undated figure as current — recommend NOT reconstructing a quote from this without confirming the "1.56" rate is refreshed regularly, e.g. by re-checking on a different date and seeing if it moves.

## Confidence flag
Did not confirm whether "1.56" refers to NZD/WST or some other pair — currency and direction of that rate were not stated in the fetched content excerpt.
