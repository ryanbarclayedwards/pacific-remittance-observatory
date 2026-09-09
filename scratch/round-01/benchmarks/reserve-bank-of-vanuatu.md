# Reserve Bank of Vanuatu (RBV) — benchmark scoping evidence

Date checked: 2026-09-09
Domain: www.rbv.gov.vu

## TLS anomaly (flag)

`https://www.rbv.gov.vu/` and its `/robots.txt` fail standard certificate verification:

```
verify error:num=20:unable to get local issuer certificate
verify error:num=21:unable to verify the first certificate
subject=/CN=*.rbv.gov.vu
issuer=/C=GB/O=The Trustico Group Ltd/CN=Trustico RSA DV SSL CA 2
```

The leaf certificate is for the correct domain (`*.rbv.gov.vu`) but the server is not sending
a complete chain to the Trustico root, so standard TLS clients (including this session's
WebFetch tool) refuse the connection. Evidence gathered below used `curl -k` (certificate
verification disabled) as a research-only workaround to read public content; **this is not
something a production collector should do** — a connector against this site would need either
a fixed intermediate-cert bundle or would have to flag the site as currently unreachable
over verified TLS. Recorded here as a fact for the maintainer to weigh, not resolved.

## robots.txt

`https://www.rbv.gov.vu/robots.txt` → HTTP 301 redirect → `https://www.rbv.gov.vu/index.php/en/robots.txt` → **HTTP 404** ("Error: 404", Joomla error page).

Net effect: no robots.txt is actually served at any resolvable URL. Under the same
no-file-means-unrestricted convention noted for CBS, this reads as unrestricted — but the
redirect-into-404 (rather than a direct 404 at the root) is an unusual CMS routing quirk worth
noting rather than a confident "robots.txt confirms open access" claim.

## Where rates are published

Homepage (`https://www.rbv.gov.vu/index.php/en/`) carries an inline rate ticker: USD 115.86,
JPY 0.7525, NZD 67.86, GBP 156.82, **AUD 83.66**, EUR 134.69 (all against VUV, presumably —
units not stated on the ticker itself).

Dedicated page: `https://www.rbv.gov.vu/index.php/en/exchange-rates`. This is a Joomla
"Fabrik" list component showing a **row per day**, both AUD and NZD present as sortable
columns, with dated entries observed running (at time of check) 09 Sep, 08 Sep, 04 Sep, 03
Sep, 02 Sep, 01 Sep, 31 Aug, 28 Aug, 27 Aug, 26 Aug 2026 on the single page loaded — i.e. it
skips weekends (04→01 Sep has no 05/06/07; 28→27 Aug has no Sat/Sun), consistent with weekday
banking-day publication. Pagination beyond this range was not followed.

## Format

HTML table, one row per business day, both on-page (no separate download link for exchange
rates found in the fetched HTML — no `.xls`/`.pdf`/`.csv` link located).

## Update frequency

**Best-evidenced of the six for observed (not just claimed) daily cadence** — the page itself
shows one row per business day rather than a single "today" figure, so ten distinct dated
entries were directly observed in one fetch, all on weekdays, none on weekends.

## Historical data

History is built into the same page as a scrollable/paginated list rather than a separate
archive file. At least ~10 business days were visible without deliberately probing pagination
further (kept to a light touch per the courtesy instruction). How far back it goes is
unconfirmed.

## Stability assessment

Basis: URLs are Joomla component-routed (`/index.php/en/exchange-rates`), similar in kind to
NRBT's stable Joomla page — no dated/filename-keyed path was involved for the HTML table
itself. The TLS chain problem above is the more material stability concern for this site,
not the page URLs.
