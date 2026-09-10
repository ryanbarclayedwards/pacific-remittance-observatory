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
| P1 | robots.txt and terms not yet checked for any provider. | **Resolved 2026-09-09** — robots.txt checked for all 33 PROVIDERS.md candidates plus 6 benchmark sources in Round 1; see PROVIDERS.md. |
| C2/C3 | 2023 audit figures not yet verified against the maintainer's own files. | **Resolved 2026-09-10** — C2 VERIFIED, C3 REFUTED, both directly against `audit1.csv`/`audit2.csv`. See section C and `reports/04-historical.md` Task A. |

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
| A9 | SaverPacific / Saver Global operates a US-origin page | **REFUTED** — no US-origin page in `saverpacific.com`'s own sitemap (`wp-sitemap-posts-page-1.xml` lists only AU-from, AU-to and NZ-from pages); every plausible URL slug (`send-money-from-usa`, `-united-states`, `-us`) returns 404. Whether a separate Saver Global US domain exists elsewhere is not established — this refutes a `saverpacific.com` US page specifically, not any Saver Global US service anywhere | 2026-09-09 |
| A10 | SaverPacific operates a NZ-origin page | VERIFIED — `saverpacific.com/send-money-from-new-zealand/` live, comparison widget present (same pattern as the AU page), 10 Pacific destinations listed: Cook Islands, Fiji, Kiribati, Niue, Samoa, Solomon Islands, Timor Leste, Tonga, Tuvalu, Vanuatu (PNG absent, as on the AU page) | 2026-09-09 |
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
| B1 | SMP has closed; homepage shows a closure notice | **VERIFIED** — direct fetch (2026-09-09) serves a static closure notice (`Last-Modified: Wed, 03 Jun 2026`, `cf-cache-status: DYNAMIC`, i.e. not a stale cache hit), corroborated independently by Wayback Machine history: a 33,909-byte page consistent with a full operating site on 11 Jan 2026 shrinks to a 1,716-byte closure notice, matching in size and date, by 6 Jun 2026. This supersedes an earlier same-day entry in this register that read "REFUTED as stated"; that entry could not be reconciled against this evidence and is flagged, not silently overwritten — see `reports/01-triage.md` §6 | 2026-09-09 |
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
| C1 | July–Aug 2023 daily audit data held in tidy form | **VERIFIED and expanded, 2026-09-10.** Located and ingested (Round 4, `reports/04-historical.md` Task A): two audit waves, not one — `audit1.csv` (2023-03-28 to 2023-04-25, 29 dates) and `audit2.csv` (2023-07-25 to 2023-08-07, 14 dates), both against Send Money Pacific and Saver Pacific. 1,188 Tonga-corridor observations imported; Vanuatu rows in `audit1.csv` exist but weren't ingested this round (no Vanuatu benchmark — see `PROVIDERS.md`) |
| C2 | 25 Jul 2023 NZ→Tonga 'Ave Pa'anga Pau NZ$200 → TOP 284.10, fee 0, rate 1.42 | **VERIFIED, 2026-09-10** — confirmed directly against the underlying `audit2.csv` row (Saver Pacific, NZTON, 'Ave Pa'anga Pau, 25/07/2023): amountreceived 284.1, Fee 0, FXrate 1.42. Exact match, checked against the primary data as instructed, not the published paper |
| C3 | 3 Aug 2023 AU–Tonga showed 21 options from 15 RSPs | **REFUTED, 2026-09-10** — the underlying data (`audit2.csv`, 2023-08-03, AUSTON) shows 18 option-level rows (9 per platform × 2 platforms: Send Money Pacific, Saver Pacific), 11 distinct raw MTO/mode options, 9 distinct base providers (7 per individual platform). Not 21 options or 15 RSPs by any grouping checked. This claim originated in the pre-project ChatGPT handover (see Provenance, above) — the maintainer's count, as of this entry: the third refuted claim traced to that handover |
| C4 | SMP and SaverPacific are independent sources | **REFUTED** — common lineage (A14). The 2023 audit compared two related platforms. Belongs in the paper |

## D. Provider observability — the live register

Populated in Sprint 1 Session 3 (Round 1, 2026-09-09). One row per provider, per `PROVIDERS.md`
— the full table lives there, not duplicated here, so it is never at risk of drifting from the
one place it's actually maintained. Every entry has a date checked and a robots.txt
determination. Re-check Tier 3 quarterly.

## E. Open methodological decisions

| # | Issue | Status |
|---|---|---|
| E1 | Benchmark FX rate unspecified; no deep market for TOP, WST, VUV, SBD, PGK, FJD | **DECIDED 2026-09-09.** Receiving-country central bank primary, best-observed-provider-rate retained as secondary from the first collection run. National Reserve Bank of Tonga is the first benchmark source built (Round 2). See METHODOLOGY §2.3 v0.2 and `reports/01-triage.md` §5.4 for the scoping this decision was made against |
| E2 | Fee-inclusion convention varies by provider and changes the formula | **RESOLVED 2026-09-10.** Per-observation, never inferred, `null` when the source doesn't state it — proven necessary, not just cautious, by a real mixed-convention case within one provider in the 2023 audit (Western Union Cash, NZTON, 2023-07-26 fits "fee on top," every other row that round fits "fee deducted"). See `docs/METHODOLOGY.md` §2.2 v0.5 and `reports/05-live.md` |
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

**Amended 2026-09-09.** The Session 4 *origin country* changes from Australia to **New
Zealand** (SPRINT-01.md, Session 4) — Round 1 triage (`reports/01-triage.md` §5.1) found no
AU-origin bank at confirmed Tier 1, while ANZ New Zealand is confirmed Tier 1 and reaches
Tonga. Maintainer decision: option (b), proceed now rather than wait on a browser re-check of
the AU-origin candidates — Session 4 proves the pipeline, not market coverage. Tonga stays the
first destination; AU–Fiji stays the second target, unchanged.

## G. Infrastructure assumptions to verify

| # | Assumption | Status |
|---|---|---|
| G1 | GitHub Actions is free for public repositories | **VERIFIED** — GitHub's current docs (`docs.github.com/en/actions/reference/usage-limits-billing-and-administration`, checked 2026-09-09) state Actions usage on standard GitHub-hosted runners is free for public repositories. No explicit numeric ceiling found in the fetched page; full ToS/Acceptable Use Policy not read, so this is "free per current billing docs," not an audited guarantee against abuse-throttling |
| G2 | Scheduled workflows are disabled after repository inactivity; unclear whether the workflow's own commits reset the clock | **Threshold VERIFIED** — GitHub's current docs (`docs.github.com/en/actions/using-workflows/events-that-trigger-workflows`, checked 2026-09-09) state public-repo scheduled workflows are disabled after 60 days with no repository activity. **Whether the workflow's own commit counts as "activity" remains UNCHECKED** — not settled by GitHub's documentation (the page doesn't define "repository activity"); only circumstantial evidence exists (widely-used community "keepalive" Marketplace actions, no GitHub-staff confirmation found). A concrete empirical test (65+ days, no other repo activity) is specified in `reports/01-triage.md` §5 — a Session 6 concern, not resolved here |
| G3 | Provider sites may block cloud runner IP ranges | UNCHECKED — test each connector from Actions, not just locally |
| G4 | Git remains adequate as the store at projected volume | VERIFIED by arithmetic — a few KB per quote, single-digit thousands of files per year |
| G5 | Local dev environment can read arbitrary files under `~/Desktop` | **REFUTED, 2026-09-10, known environment constraint.** On this maintainer's machine, the coding-agent process can `stat`/`ls` an exact file path under `~/Desktop` (confirming the file exists, its size, its modified date) but cannot actually read its contents — every read attempt (`head`, `cat`, Python `open()`) fails with "Operation not permitted." This is macOS's Full Disk Access privacy control, not a wrong path or a missing file — `hm-ds/`'s relocation there (Round 6, `reports/06-live.md`) hit this directly. Fix is a macOS Privacy & Security setting (Full Disk Access, or Files and Folders → Desktop), not a code change; recorded here so the next person who hits "path exists but every read fails" doesn't spend an hour on it before checking this |
| G6 | Every commit's author identity reflects the maintainer's real name/email | **PARTIALLY TRUE, known provenance gap, recorded 2026-09-11.** No `user.name`/`user.email` was configured (local or global) before this repository's first push, so git fell back to a machine default: commits up to and including `022893a` ("temp: hold workflow back from initial push") on `origin/main` carry `Ryan Edwards <ryanbedwards@MacBookPro.nbn>` — the local macOS account and hostname, not a chosen identity. From `23e4627` onward, `user.name`/`user.email` are set (repo-local) to the maintainer's actual name and `ryanbarclayedwards@gmail.com`. The maintainer's explicit decision (`reports/06-live.md`): leave the earlier commits as they are rather than rewrite already-public history for an author-field correction — the machine-default address reveals nothing sensitive, and rewriting live history is a materially bigger cost than the field it would fix |
| G7 | GitHub's scheduled (`cron`) trigger fires at (approximately) its configured time | **REFUTED, 2026-09-10/11, best-effort confirmed with a data point.** `collect.yml`'s cron is `0 19 * * *` (19:00 UTC). The workflow's first scheduled run (`34532136518`) started at 21:25:49 UTC — about 2h26m late. GitHub's own docs already say scheduled workflows are "best-effort," but gave no expected magnitude; this is the first concrete measurement against this repository's own workflow, not a general GitHub benchmark, and drift may vary run to run. Consequence for analysis, recorded in `docs/METHODOLOGY.md` under freshness: `collected_at` is the ground truth for *when* an observation happened, never the cron target time — nothing downstream should assume a fixed daily collection time, only a fixed daily collection attempt. See `reports/06-live.md` |
