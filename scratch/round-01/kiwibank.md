# Kiwibank (kiwibank.co.nz) — evidence, checked 2026-09-09

## robots.txt
URL: https://www.kiwibank.co.nz/robots.txt (WebFetch)
```
User-agent: *
Disallow: /go-fly-promotion/
Disallow: /forms/staff/
Disallow: /statementsconfirmation/
Disallow: /home-loan-renewal/
Disallow: /nzpost-kiosk/
Disallow: /opt-in-confirmation/
Disallow: /branch-landing/
Disallow: /branch-wifi/
Disallow: /offer/
Disallow: /application-form-scheduled-maintenance/
Disallow: /forms/pieapp/download.asp

Sitemap: https://www.kiwibank.co.nz/sitemap.xml
```
None of the disallowed paths touch the FX/fees page.

## FX rates & fees page
URL: https://www.kiwibank.co.nz/personal-banking/accounts/international/foreign-exchange-rates-and-fees/
Fetched directly with `curl` (honest UA), 468,235 bytes, HTTP 200. The raw server-delivered HTML (not client-rendered — confirmed by direct byte search, no JavaScript execution) contains a structured table with all six Pacific currencies:
```
FJD – Fiji Dollars      → <a class="richtext-rate" data-rate="130" data-nosnippet>FX Rate FJD Buy TT(active)</a>
PGK – Papua New Guinea Kina → data-rate="185", "FX Rate PGK Buy TT (active)"
SBD – Solomon Islands Dollars → data-rate="205", "FX Rate SBD Buy TT (active)"
TOP – Tongan Pa'anga     → data-rate="240", "FX Rate TOP Buy TT (active)"
VUV – Vanuatu Vatu        → data-rate="255", "FX Rate VUV Buy TT (active)"
WST – Samoan Tala         → data-rate="265", "FX Rate WST Buy TT (active)"
```
The currency rows and labels are server-rendered (present in the raw HTML with no JS execution). The `data-rate` values (130, 185, 205, 240, 255, 265) are small sequential-looking integers, not plausible FX rate magnitudes — these read as internal reference/row IDs for a client-side rate widget that injects the live numeric rate at render time, not the rate itself. **The live numeric rate was not captured this round** — confirming it requires either a rendered browser (unavailable this session) or locating the widget's data endpoint, which was not pursued, being out of scope for triage (would cross into connector engineering, per the round-1 brief).

## Fee schedule
Confirmed via WebFetch on the same page, exact NZD figures:
- Internet banking (SHA — shared cost): $10 equivalent
- Internet banking (OUR — sender pays all): $20 equivalent
- Branch/email (SHA): $25 equivalent
- Branch/email (OUR): $35 equivalent
- Inbound: $12, both foreign-currency and NZD accounts

## Tier assignment
**Tier 1 (probable), pending live-rate confirmation.** All structural elements of a published tariff are present and server-rendered without login: currency rows for all six target currencies and a full fee schedule. The one missing piece is confirming the actual numeric rate is retrievable without a browser/JS runtime — likely via a discoverable JSON/data endpoint the page's own widget calls, not yet located. Recommend this as a strong Session-4 connector candidate, with endpoint discovery as the first engineering step.

## Confidence flags
- Did not attempt to locate or call the widget's underlying data endpoint — deliberately, to stay inside triage scope.
- The Tier 1 call rests on structural evidence (page renders currency labels server-side) rather than a directly observed numeric rate. If the underlying endpoint turns out to be unreachable/authenticated, this should be revised to Tier 2 or 3.
