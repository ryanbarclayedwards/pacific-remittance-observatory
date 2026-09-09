# Reserve Bank of Fiji (RBF) — benchmark scoping evidence

Date checked: 2026-09-09
Domain: www.rbf.gov.fj

## robots.txt

URL: https://www.rbf.gov.fj/robots.txt — HTTP 200

```
User-agent: *
Disallow: /wp-content/uploads/wpo/wpo-plugins-tables-list.json

# START YOAST BLOCK
# ---------------------------
User-agent: *
Disallow:

Sitemap: https://www.rbf.gov.fj/sitemap_index.xml
# ---------------------------
# END YOAST BLOCK
```

Effectively unrestricted (WordPress/Yoast default; the only disallow is one plugin JSON file
unrelated to exchange rate content). No AI-crawler-specific rules.

## Where rates are published

- Homepage (https://www.rbf.gov.fj/) carries a rate widget: AUD 0.6256, NZD 0.7711, plus USD,
  EUR, JPY, GBP, dated "09 September 2026" on the page.
- Dedicated page `https://www.rbf.gov.fj/reserve-bank-of-fiji-exchange-rates/` is
  **explanatory only** — describes the FJD currency-basket peg (AUD, NZD, USD, JPY, GBP, EUR)
  and states "Exchange rates published on the RBF website are for indicative purposes only,"
  directing users to a commercial bank for firm quotes. No rate table, no date stamp on this
  page itself.
- The actual machine-readable daily series is under Statistics:
  `https://www.rbf.gov.fj/statistics/economic-and-financial-statistics/` → section "8.0
  External Sector" → **direct download**
  `https://www.rbf.gov.fj/wp-content/uploads/2026/09/8.8-Exchange-Rates-Daily-3.xlsx`
  (labelled "8.8 Exchange Rates Daily"; a separate "8.7 Exchange Rates Monthly" file also
  exists on the same page).

## Format

Homepage: HTML widget (today's rate only). Statistics page: downloadable `.xlsx`, filename
dated by upload month (`2026/09/...`), suggesting the file is periodically re-uploaded rather
than served from a stable permanent URL — **not independently confirmed**, inferred from the
filename path containing the year/month.

## Update frequency

Homepage widget dated "09 September 2026" at time of check — consistent with a daily update,
but only one day's observation was made; not confirmed across multiple days.

## Historical data

The "8.8 Exchange Rates Daily" xlsx is a distinct download from "8.7 Exchange Rates Monthly,"
implying the daily file itself may hold more than one day's data, but its contents were not
opened/inspected in this pass (would require downloading and parsing the spreadsheet, out of
scope for reconnaissance). Not confirmed how far back it goes.

## Stability assessment

Basis: the actual data lives in an uploads path keyed by year/month
(`/wp-content/uploads/2026/09/...`), which is standard WordPress media-library behaviour and
suggests the URL for "today's" file could change filename/path monthly even if the page
linking to it stays constant. This is an inference from the URL pattern, not confirmed by
comparing two months' filenames.
