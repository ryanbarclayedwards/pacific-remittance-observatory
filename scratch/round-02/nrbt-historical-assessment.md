# NRBT historical exchange-rate file — assessment (not imported)

**Date checked:** 2026-09-09
**File:** `average_daily_exchange_rates.xlsx`, fetched from
`https://www.reservebank.to/data/docs/fmarkets/exrates/average_daily_exchange_rates.xlsx`
(815,225 bytes), saved alongside this note as `nrbt-historical-rates.xlsx`.
**Read with:** `openpyxl` via `pandas.ExcelFile` — installed only in the local venv for this
one-off inspection, not added to `requirements.txt`, since no committed connector uses it this
round. It will need adding if/when this file is actually imported.

## Structure

Five sheets, one per two-year period: `2017 to 2018`, `2019 to 2020`, `2021 to 2022`,
`2023 to 2024`, `2025 to 2026`. Each sheet has the same layout: a title block in the first six
rows, then one data row per business day, with three side-by-side blocks of nine currencies
each (AUD, EUR, FJD, GBP, JPY, NZD, USD, WST, CHF) — BUY (columns 1–9), MID (columns 14–22),
SELL (columns 27–35) — sharing one date column (column 0). This is not a tidy long-format
table; a real import would need to reshape it (one row per date × currency × BUY/MID/SELL,
or one row per date × currency with buy/mid/sell as three fields, matching this project's
existing observation shape) rather than load the sheet as-is.

## Coverage

| Sheet | In-range rows | In-range date span | Out-of-range rows found |
|---|---|---|---|
| 2017 to 2018 | 514 | 2017-01-02 → 2018-12-31 | 1 (`2003-07-17`) |
| 2019 to 2020 | 521 | 2019-01-01 → 2020-12-31 | 1 (`2009-03-22`) |
| 2021 to 2022 | 493 | 2021-01-01 → 2022-12-30 | 0 |
| 2023 to 2024 | 522 | 2023-01-02 → 2024-12-31 | 0 |
| 2025 to 2026 | 423 | 2025-01-01 → 2026-09-09 | 1 (`2028-05-28`) |

Total: 2,473 in-range rows, 3 stray out-of-range dates (one per three of the five sheets) —
almost certainly single-cell data-entry errors in the source workbook, not a structural
problem. A real import would need to detect and either exclude or flag these, not trust
`min()`/`max()` on the date column blindly. This is the file's only real data-quality flag
found in this pass; it was not investigated further (row-level manual correction of someone
else's spreadsheet is out of scope for an assessment).

**Confirms the historical claim from Round 1** (`scratch/round-01/benchmarks/
national-reserve-bank-of-tonga.md`): a single file, in-range coverage 2017-01-02 through
2026-09-09 (today), no per-date-page scraping required.

## Does it cover the 2023 manual-audit period (Jul–Aug 2023)?

Yes. The `2023 to 2024` sheet has clean, in-range rows for the full period, e.g.:

| Date | AUD BUY | NZD BUY | AUD MID | NZD MID | AUD SELL | NZD SELL |
|---|---|---|---|---|---|---|
| 2023-07-25 | 0.6467 | 0.7108 | 0.6335 | 0.6943 | 0.6203 | 0.6778 |
| 2023-08-01 | 0.6486 | 0.7096 | 0.6354 | 0.6931 | 0.6223 | 0.6766 |
| 2023-08-04 | 0.6592 | 0.7147 | 0.6460 | 0.6982 | 0.6328 | 0.6817 |

As a loose sanity check only (not a verification of CLAIMS.md C2, which is the maintainer's
own job against their own files, per CLAUDE.md §4): C2 records 25 Jul 2023 NZ→Tonga via
'Ave Pa'anga Pau, NZ$200 → TOP 284.10, implying a rate of 1.4205 TOP/NZD. NRBT's published MID
rate for that date, inverted per METHODOLOGY §2.4's convention (1/0.6943), gives 1.4403
TOP/NZD — about 1.4% higher than the bank's actual transacted rate, which is the direction and
rough size you'd expect from a bank's own margin sitting under the central bank's reference
rate. This is a plausibility check, not independent confirmation of C2.

## Recommendation (not acted on this round)

The file is a strong backfill candidate — single source, wide date range, includes NZD
throughout. Importing it would need: (1) a reshape step from the three-block layout to this
project's tidy per-currency-pair rows, (2) a rule for the ~3 stray out-of-range dates, and (3)
per CLAUDE.md §1.3, treatment as a genuine **backfill** — new rows with their own
`collection_run_id`, dated as of this import, never presented as if collected daily in real
time on the historical dates themselves. Not done this round, per the brief's "report; do not
import it yet."
