# Central Bank of Samoa (CBS) — benchmark scoping evidence

Date checked: 2026-09-09
Domain: www.cbs.gov.ws

## robots.txt

URL: https://www.cbs.gov.ws/robots.txt — **HTTP 404**. No robots.txt file exists at the
domain root. Per robots.txt convention (RFC 9309 and prior de facto practice), a 404 on the
robots.txt URL means no crawl restrictions are asserted — the site is unrestricted by omission,
not by explicit permission.

## Where rates are published

Homepage links to `/daily-exchange-rates`, which resolves to
`https://www.cbs.gov.ws/daily-exchange-rates`.

That page lists, as "Units of Foreign Currency per ST1.00":

| Currency | Rate |
|---|---|
| AUD | 0.51119 |
| NZD | 0.63004 |
| USD | 0.36911 |
| EUR | 0.31748 |
| FJD | 0.81507 |
| JPY | 56.79997 |
| GBP | 0.27253 |
| CNY (onshore) | 2.47678 |
| CNY (offshore) | 2.47551 |

Plus a separate SAT/USD buy/sell spread note. Both AUD and NZD present. Page marked "09 Sep
2026" at time of check. Disclaimer on page: "these are indicative rates only but not for
market use" — consult commercial banks for actual trading rates.

## Format

HTML table (two columns: currency, rate) on the live page. A downloadable Excel file,
"Historical Daily Rates" (filename observed as `Historical-Daily-Rates090926-1.xlsx`, i.e.
date-stamped 09-09-26 in the filename), is linked from the same page.

## Update frequency

Page dated "09 Sep 2026" at time of check; the historical-rates filename itself carries that
same date, consistent with the file being regenerated/re-dated daily — inferred from the
filename pattern on a single observation, not confirmed by checking on a second day.

## Historical data

A dedicated "Historical Daily Rates" download exists, similar in kind to NRBT's. Depth of
history (how far back the file goes) was not inspected — would require downloading and opening
the spreadsheet, out of scope for reconnaissance.

## Stability assessment

Basis: the historical-rates filename appears to be re-dated with each publication
(`...090926-1.xlsx` for 9 Sep 2026), which is a mild instability signal for anyone trying to
hot-link a permanent URL to "today's" file — the collector would need to discover the current
filename from the page each run rather than assuming a fixed URL. This is inferred from a
single filename observed once, not confirmed across multiple days.
