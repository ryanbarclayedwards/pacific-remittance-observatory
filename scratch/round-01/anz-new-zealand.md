# ANZ New Zealand (anz.co.nz + tools.anz.co.nz) — evidence, checked 2026-09-09

## robots.txt — anz.co.nz
URL: https://www.anz.co.nz/robots.txt (WebFetch; not independently curled)
```
User-agent: *

Sitemap: https://www.anz.co.nz/sitemap.xml
```
No Disallow lines.

## robots.txt — tools.anz.co.nz
URL: https://tools.anz.co.nz/robots.txt
Fetched via curl with honest UA. Result: HTTP 200 body is a generic Dynatrace-instrumented 404 error page ("404 - File or directory not found"), i.e. **no robots.txt file exists on this subdomain**. By the robots convention, absence of robots.txt means no crawling restriction is declared — not a block.

## FX rate table
URL: https://tools.anz.co.nz/foreign-exchange/fx-rates/
Confirmed via WebFetch: a daily buy/sell FX rate table for NZD, covering all six Pacific currencies of interest:
- TOP (Tonga Pa'anga) — example quoted: buy 1.2999, sell 1.4537
- WST (Samoa Tala)
- VUV (Vanuatu Vatu)
- SBD (Solomon Islands Dollar)
- PGK (Papua New Guinea Kina)
- FJD (Fiji Dollar)

Timestamp shown on page: "ANZ indicative rates for IMT rates as of 21:20 NZT, 09 Sep 2026". Rates explicitly labelled "indicative only" — "they do not represent exchange rates which are available under any product or service provided by ANZ."

## Fee schedule
URL: https://www.anz.co.nz/personal/fx-international/international-money-transfers/
Public fee table, no login required:
- ANZ goMoney: $0
- ANZ Internet Banking: $0
- By calling: $15
- At branch: $15
- ANZ Direct Online (business): $5
- Page notes an "OUR Fee may apply", shown to the customer before confirming payment — not disclosed as a fixed public figure.

Pacific destinations named: Fiji, Solomon Islands, Samoa, Tonga, Vanuatu, Cook Islands, Papua New Guinea, Kiribati, New Caledonia, Timor-Leste.

## Tier assignment
**Tier 1 (published_tariff).** A daily indicative FX rate table (with timestamp) for all six Pacific currencies of interest, plus a public fee schedule, both without login. Strongest single candidate found in this batch. A quote could be reconstructed arithmetically from the two pages.

## Confidence flags
- The FX rate table content was read via WebFetch's summarization, not verified byte-for-byte; the exact table structure (all rows/columns) has not been captured — needed before writing a parser.
- "OUR Fee" (a correspondent-fee-covering option) is mentioned but not quantified publicly; if used by some transfers, the reconstructed quote could be incomplete for those cases. Record as a known gap in the cost formula, not a reason to downgrade the tier.
- fx-rates table's actual timestamp cadence (how often during the day it updates) not established — only a single snapshot observed.
