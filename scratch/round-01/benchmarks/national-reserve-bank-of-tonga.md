# National Reserve Bank of Tonga (NRBT) — benchmark scoping evidence

Date checked: 2026-09-09
Domain: www.reservebank.to

## robots.txt

URL: https://www.reservebank.to/robots.txt — HTTP 200, standard Joomla default file:

```
User-agent: *
Disallow: /administrator/
Disallow: /api/
Disallow: /bin/
Disallow: /cache/
Disallow: /cli/
Disallow: /components/
Disallow: /includes/
Disallow: /language/
Disallow: /layouts/
Disallow: /libraries/
Disallow: /logs/
Disallow: /modules/
Disallow: /plugins/
Disallow: /tmp/
```

None of these paths touch the public exchange-rate pages. No AI-crawler-specific rules.

## Where rates are published

Primary page: `https://www.reservebank.to/index.php/financial-system/financial-markets/exchange-rates`

Shows daily indicative BUY / MID / SELL rates for 12 currencies against TOP, including AUD and
NZD (e.g. USD 0.4307 / 0.4230 / 0.4154). Page marked "Last Updated: 09 September 2026" at time
of check.

Related pages on the same site:
- Weekly: `/index.php/financial-system/financial-markets/weekly-exchange-rates` (marked
  "last updated 04 Sep 2026" at time of check)
- Monthly: `/index.php/financial-system/financial-markets/monthly-exchange-rates` (marked
  "last updated 31 Aug 2026" at time of check)

## Format

HTML table (BUY/MID/SELL columns) on the daily page. A downloadable Excel file, "Daily
Exchange Rates: from 2017 to Current" (~678 KB), is linked from the same page — this is the
historical archive.

A separate PDF, "Fees & Charges" comparison across commercial banks/FX dealers for inward and
outward transfers, is also linked (~792 KB) — relevant to Task A provider triage, not the
benchmark itself, noted for reference.

## Update frequency

Daily page dated "09 September 2026" at time of check; the existence of separate weekly/monthly
pages with their own "last updated" stamps (04 Sep and 31 Aug respectively) is corroborating
evidence that the daily page updates on a materially faster cadence than those — consistent
with daily updates, though only observed on one day.

## Historical data

**Best of the six.** A single downloadable Excel workbook covers 2017 to date — multi-year
daily history in one file, no scraping of individual date pages required.

## Stability assessment

Basis: this is a standard Joomla component-driven page (`index.php?option=...` style URLs
implied by the `/index.php/financial-system/...` path structure) which tends to be stable
across content updates since the routing is menu-driven rather than filename/date-keyed (unlike
RBF's dated upload path). No direct evidence of the URL having changed historically — inferred
from CMS structure, not observed over time.
