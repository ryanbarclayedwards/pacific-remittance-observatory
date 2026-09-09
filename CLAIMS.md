# CLAIMS.md — verification register

**v2.** Every factual assertion the project relies on. Nothing enters code, docs or a paper
without appearing here first.

**Status:** `VERIFIED` · `REFUTED` · `UNCONFIRMED` (checked, inconclusive) · `UNCHECKED`

**Provenance.** The originating handover and recon workbook came from a ChatGPT session.
Several confident assertions did not survive checking. Treat every `UNCHECKED` inherited claim
as a hypothesis.

**Framing change in v2.** The project no longer depends on any comparison platform, agreement
or third party. Sections A and B are therefore **background and comparator context**, not
dependencies. They matter for the paper and for validation, not for whether the collector runs.

---

## 0. Blocking items

| # | Item | Why blocking |
|---|---|---|
| E1 | No benchmark FX rate has been chosen. Every cost figure depends on one. | Cannot compute cost. Decide before Session 4. |
| P1 | robots.txt and terms not yet checked for any provider. | Cannot write collection code. Session 3. |
| C2/C3 | 2023 audit figures not yet verified against the maintainer's own files. | Cannot regression-test. Session 2. |

---

## A. SaverPacific / Saver Global — comparator, not dependency

| # | Claim | Status | Checked |
|---|---|---|---|
| A1 | saverpacific.com live; footer "© SaverPacific 2026" | VERIFIED | 2026-09-09 |
| A2 | Operated by Saver Global Pty Ltd | VERIFIED | 2026-09-09 |
| A3 | WordPress (`wp-content/themes/saverpacific/`) | VERIFIED | 2026-09-09 |
| A4 | 33 transfer operators listed | VERIFIED | 2026-09-09 |
| A5 | Comparison widget at `/compare/` | **REFUTED** — `/compare/` is the provider-profile namespace; widget is on `/send-money-from-australia/` | 2026-09-09 |
| A6 | Recon workbook provider slugs | **REFUTED (partial)** — ≥4 wrong; actual: `ave-paanga-pau`, `klickex-low-priority`, `national-australia-bank`, `wise` | 2026-09-09 |
| A7 | PNG an available destination | **REFUTED for the AU page** — 10 listed, PNG absent | 2026-09-09 |
| A8 | Part of a six-region Saver family | VERIFIED | 2026-09-09 |
| A14 | Run by DMA Global and 360 South Pty Ltd, the operator of the first EMPR iteration | VERIFIED as at 2023 (EMPR review, fn 23) | 2026-09-09 |
| A15 | Uses a mix of real-time and weekly-updated rates | VERIFIED as at 2023 (EMPR review) | 2026-09-09 |
| A16 | At least one Saver regional site partly DFAT-funded via the ILO ASEAN Triangle programme | VERIFIED as at 2023 | 2026-09-09 |

**Use:** external comparator for validation and for the paper's measurement argument. Not a
data source. No collection from it, and no dependency on any agreement with its operator.

## B. Send Money Pacific — historical context

Source for B5–B14: *EMPR Independent Mid-term Review*, Cummings & Corvisy, June 2023, DFAT.
https://www.dfat.gov.au/sites/default/files/empr-mid-term-review.pdf — read in full 2026-09-09.

| # | Claim | Status | Checked |
|---|---|---|---|
| B1 | SMP has closed; homepage shows a closure notice | **REFUTED as stated** — homepage serves the normal service description. EMPR funding ran 2021–2025 so wind-down is plausible; verify directly | 2026-09-09 |
| B2 | AU, NZ and USA origins (USA → Fiji, Samoa, Tonga only) | VERIFIED, current homepage | 2026-09-09 |
| B3 | Destinations: Fiji, Kiribati, PNG, Samoa, Solomon Is, Tonga, Tuvalu, Vanuatu — **eight**, not eleven | VERIFIED, current homepage | 2026-09-09 |
| B4 | Originally managed by Developing Markets Associates from 2009 | VERIFIED | 2026-09-09 |
| B5 | CulturalPulse managing contractor from April 2021; revamped site live August 2021 | VERIFIED | 2026-09-09 |
| B6 | AU/NZ origin, $200/$500 amounts, cost/speed sorting, three initial results | VERIFIED | 2026-09-09 |
| B7 | Weekly price updates, up to six days stale; previous iteration monthly; real-time deliberately excluded for all providers on cost grounds | VERIFIED — stronger than the handover claimed | 2026-09-09 |
| B9 | 25 MTOs listed; end-of-programme target 28 | VERIFIED as at 2023 | 2026-09-09 |
| B10 | EMPR 2021–2025, AU$3m, DFAT + MFAT | VERIFIED | 2026-09-09 |
| B11 | An SMP reporting dashboard existed and was scraped for the review | VERIFIED | 2026-09-09 |
| B12 | Review found the programme unsustainable; no local partner, no exit strategy; IP could be gifted or sold | VERIFIED | 2026-09-09 |
| B13 | Most-used corridors Aug 2021–May 2023: AU–Fiji 21%, NZ–Samoa 13%, AU–Samoa 11%, AU–Vanuatu 10%, NZ–Tonga 7% | VERIFIED | 2026-09-09 |
| B14 | Niue shares a banking system with NZ; free transfers made cheapest-provider results misleading until corrected | VERIFIED | 2026-09-09 |
| B8 | Central Bank of Samoa March 2026 report cites SMP monthly averages | UNCHECKED | — |

**Use:** B7 is the single most useful finding in the project. Weekly refresh, up to six days
stale, monthly before that, real-time deliberately excluded — that is the measurement problem
this project exists to fix, stated by the programme's own reviewers.

## C. Existing Devpolicy research

| # | Claim | Status |
|---|---|---|
| C1 | July–Aug 2023 daily audit data held in tidy form | VERIFIED (maintainer) |
| C2 | 25 Jul 2023 NZ→Tonga 'Ave Pa'anga Pau NZ$200 → TOP 284.10, fee 0, rate 1.42 | UNCHECKED — verify against C1, not the published paper |
| C3 | 3 Aug 2023 AU–Tonga showed 21 options from 15 RSPs | UNCHECKED — verify against C1 |
| C4 | SMP and SaverPacific are independent sources | **REFUTED** — common lineage (A14). The 2023 audit compared two related platforms. Belongs in the paper |

## D. Provider observability — the live register

Populated in Sprint 1 Session 3. One row per provider, per `PROVIDERS.md`. Every entry needs a
date checked and a robots.txt determination. Re-check Tier 3 quarterly.

`UNCHECKED` for all candidates as at 2026-09-09.

## E. Open methodological decisions

| # | Issue | Status |
|---|---|---|
| E1 | Benchmark FX rate unspecified; no deep market for TOP, WST, VUV, SBD, PGK, FJD | **OPEN — BLOCKING.** See METHODOLOGY §2.3 |
| E2 | Fee-inclusion convention varies by provider and changes the formula | OPEN — record per observation |
| E3 | Provider identity harmonisation across vintages | OPEN — provider master with `active_from`/`active_to` |
| E4 | Comparability of 2023 manual and 2026 automated vintages | OPEN — vintage flags mandatory |
| E5 | Corridors where domestic-style banking makes comparison meaningless (Niue/NZ per B14; possibly Cook Islands, Tokelau) | OPEN — decide before publication |
| E6 | Balanced panel of consistently observable providers versus all observed providers | OPEN — probably publish both |

## F. Corridor selection

B13 says the most-used corridors were AU–Fiji, NZ–Samoa, AU–Samoa, AU–Vanuatu, with NZ–Tonga
fifth. The 2023 audit covers Tonga.

Resolution: **Tonga first**, because regression-testing against data you already hold matters
more than reach in Sprint 1. **AU–Fiji second**, as the first coverage-driven corridor. Record
the reasoning in METHODOLOGY so corridor choice is never mistaken for a sampling frame.

## G. Infrastructure assumptions to verify

| # | Assumption | Status |
|---|---|---|
| G1 | GitHub Actions is free for public repositories | UNCHECKED — verify current terms |
| G2 | Scheduled workflows are disabled after repository inactivity; unclear whether the workflow's own commits reset the clock | UNCHECKED — **test before relying on it**; add a heartbeat if needed |
| G3 | Provider sites may block cloud runner IP ranges | UNCHECKED — test each connector from Actions, not just locally |
| G4 | Git remains adequate as the store at projected volume | VERIFIED by arithmetic — a few KB per quote, single-digit thousands of files per year |
