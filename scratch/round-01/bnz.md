# Bank of New Zealand (bnz.co.nz) — evidence, checked 2026-09-09

## robots.txt
URL: https://www.bnz.co.nz/robots.txt (WebFetch)
```
User-agent: *
Disallow: /api/ #Siverstripe APIs
Disallow: /content/ #Silverstripe api for cards
Disallow: /XMLFeed/ #Rates feeds
Disallow: /static/www/html/
Disallow: /search/
Disallow: /search/api/search/
Disallow: /client/

Sitemap: https://www.bnz.co.nz/sitemap.xml
```
Notable: `/XMLFeed/` is explicitly commented "#Rates feeds" and disallowed — the machine-readable rates feed is off-limits, but this does not disallow the general HTML rates page.

## Fee schedule
URL: https://www.bnz.co.nz/support/rates-and-fees/essentials/service-fees
Confirmed via WebFetch, exact figures:
- Self-service online, sending foreign currency: no charge
- Self-service online, sending NZD: $5 per payment
- Staff-assisted: $25 per payment
- Received, credited to BNZ account: $10 per payment
- Received, credited to another bank: $15 per payment
- Trace/amendment/cancellation: $25 per payment
No Pacific Island country named on this specific page (only Japan, as a correspondent-fee example).

## FX rate table
URL: https://www.bnz.co.nz/personal-banking/international/exchange-rates
WebFetch could not extract the actual rate table — the returned text describes the page ("indicative foreign exchange rates in the table below... updated on business days only") but the table itself was not present in the fetched/converted content, most likely because it renders client-side (JavaScript) rather than being present in server-delivered HTML. **No Pacific currency rates confirmed from this page.**

## Tier assignment
**Unresolved this round — provisionally Tier 3, not Tier 1.** A public fee schedule exists, and robots.txt does not block the HTML rates page (only the machine-readable feed), but no rate table content was actually observed. Per the brief's instruction not to stretch a classification, I am not calling this Tier 1 on the strength of a page description alone. Note for the maintainer: CLAUDE.md §4 ("prefer boring... requests over Playwright") means a real collector will hit this page with a plain HTTP client, same as this fetch did — if the rate table genuinely requires JavaScript to render and there is no discoverable underlying JSON/XML endpoint (the disallowed `/XMLFeed/` may or may not be that endpoint — its content was not inspected, out of respect for the Disallow), a "boring" collector may not be able to reach it either, independent of robots.txt permission.

## Confidence flags
- Did not fetch `/XMLFeed/` despite curiosity about whether it is the underlying data source, because robots.txt disallows it — deliberate, per CLAUDE.md §1.5 ("respect robots.txt").
- No browser-rendering check was possible this session (Chrome extension not connected) to confirm whether the table is genuinely JS-only or whether WebFetch's HTML→markdown conversion simply dropped it. This is the single biggest gap in the BNZ evidence and should be resolved with a real browser or a raw `curl` + view-source check before any tier finalisation.
