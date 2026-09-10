# Round 4 — corrections, and the 2023 audit ingested

**Date:** 2026-09-10
**Scope:** four maintainer corrections against Rounds 2–3 recorded first (what is/isn't a
workaround, already-recorded in Round 3; a promotional-rate schema gap; an NRBT benchmark
limitation; a "closes structurally vs substantively" vocabulary fix); a placeholder-URL
housekeeping pass; then the round's real work — ingest the 2023 manual audit (Task A), backfill
the NRBT historical benchmark (Task B), and compare the two (Task C).

**Explicitly out of scope:** a third connector. No new connector was built this round — Task A
and Task B are one-off imports, deliberately not registered in `collect.run.CONNECTORS`. This
report follows `docs/REPORTING.md` and assumes no memory of this session.

**Outcome in one line:** the 2023 audit (1,188 observations, two waves) and the NRBT historical
benchmark (4,757 observations, 2017–2026) are both ingested and validate clean against the
current schema with no distortion. Computed cost_pct for 780 matched audit rows against the
backfilled benchmark: correlation 0.988 with the audit's own reported costs, 100% agreement on
which provider was cheapest across 110 date×corridor groups — a strong, unforced validation. Two
real bugs were found and fixed along the way (silent binary-content corruption in the archive
layer, a silent-NaN-as-real-rate bug in the backfill parser), and CLAIMS.md C2/C3 are now
checked directly against primary data for the first time.

---

## 2. What I did

1. Read `reports/03-endpoints.md` in full, then recorded four maintainer rulings before
   touching any pipeline code:
   - **CLAUDE.md §1.5**: the previous round's "what is and is not a workaround" clause stays;
     this round added nothing new there.
   - **`schema/observation.schema.json` v0.1→v0.2**: `rate_is_promotional` (boolean) and
     `promotion_detail` (string) added — the schema had `fee_is_promotional` but nothing for a
     promotional *rate*, which is exactly where Round 3's OrbitRemit distortion lived.
   - **`docs/METHODOLOGY.md` v0.3→v0.4**: §2.3 documents NRBT's published MID as the midpoint
     of the bank's own dealing spread (BUY/SELL), not an interbank mid-market rate — a known
     limitation, and the reason the secondary benchmark stays load-bearing.
   - **`docs/REPORTING.md`**: added "closes structurally" vs "closes substantively" as a
     defined distinction, after Round 3's §5.1 (report 02) claimed the cost measure "closes end
     to end" when a `fee = null` gap meant it had only closed structurally.
2. Housekeeping: found every `github.com/devpolicy/...` reference across the repository (4
   files). Fixed the one that mattered functionally — `collect/archive.py`'s live `USER_AGENT`,
   sent to every external site this project fetches from — to a non-committal placeholder
   rather than an unverified claim. Left historical evidence files that accurately quote what
   was actually sent at the time untouched, and left `reports/03-endpoints.md` alone since it
   already correctly flagged the issue itself.
3. Rebuilt `collect/orbitremit/connector.py` (Corrections 1+2): emits one observation per
   comparison-table row (all nine amounts: 5, 10, 25, 50, 100, 500, 1000, 5000, 10000 AUD) with
   `rate_is_promotional`/`promotion_detail` populated per row, instead of Round 3's single
   500-AUD row presented as if representative. Found and fixed a real parsing gap in the
   process: the table's ninth row (10,000 AUD) isn't inlined in the page's streaming payload
   like the other eight — it's referenced by id and needed a second, explicit resolution step.
4. Found and fixed a real bug while rebuilding the connector: appending the new, wider schema to
   the existing `store/observations/2026-09.csv` (written under the old, narrower schema)
   produced a ragged CSV `normalise.validate` couldn't even parse. `collect/store.py` now
   migrates a month-file's header when it's a clean prefix extension (backfilling old rows' new
   cells as empty, never touching an existing value; refuses anything else as a human decision).
   Root cause: the two new schema fields were inserted mid-list instead of at the end — fixed,
   and the convention is now documented directly in the schema file.
5. Found and fixed a second real bug while preparing Task B: `archive_bytes()` decoded every
   response body as UTF-8 with `errors="replace"`, which would have silently corrupted any
   binary payload (the `.xlsx` Task B needed to archive) the first time one was actually used.
   Now tries UTF-8 first, falls back to base64 for anything that isn't, byte-for-byte
   recoverable either way.
6. Searched for the 2023 manual audit dataset CLAIMS.md C1 references — not in the repository,
   not in an initial `~/Downloads` search. Asked the maintainer directly rather than guess or
   proceed without it. The maintainer located it: `hm-ds/Data/audit1.csv` and `audit2.csv`,
   inside a folder of their own broader research data (household survey microdata, unrelated
   Stata files, draft paper output). Added `hm-ds/` to `.gitignore` immediately — only the two
   audit CSVs are this project's concern, and survey microdata has no established basis for
   redistribution under this project's public archive.
7. Read the maintainer's own `.do` file (`hm-ds/Remittance in the Pacific (JDE)_20260509.do`) in
   full to understand the raw CSVs' actual structure and conventions before writing an importer
   — not guessed at. Verified every field mapping arithmetically against the raw data before
   committing to it (see §3.1).
8. Built and tested `collect/backfill_nrbt_historical.py` (Task B) and
   `collect/ingest_2023_audit.py` (Task A) — both dry-run first, checked carefully, then run for
   real. `normalise.validate --strict` passes clean at every stage: 2,489 rows (before this
   round) → 4,773 (after Task B) → 5,961 (after Task A).
9. Ran Task C: joined every 2023 audit row to the backfilled NRBT benchmark by date and origin
   currency, computed `cost_pct`, and compared to the audit's own precomputed `Cost_PP` (kept
   verbatim in each row's `notes` during ingestion for exactly this purpose). Investigated the
   408 audit rows that didn't match a benchmark rate before reporting the comparison, rather than
   silently excluding them — confirmed every one falls on a weekend or an AU/NZ public holiday.
10. Verified CLAIMS.md C2 and C3 directly against the ingested primary data (not the published
    paper, per C2's own instruction) — C2 verified exactly, C3 refuted with the real figures.
11. Committed after each checkpoint throughout (rulings → housekeeping → connector rebuild + bug
    fix → archive bug fix → backfill script → backfill run → ingestion script → ingestion run →
    claims → Task C analysis → this report).

---

## 3. Findings

### 3.1 The 2023 audit's actual structure (verified, not assumed)

| Fact | Verified as |
|---|---|
| Two waves, not one | `audit1.csv`: 2023-03-28 to 2023-04-25 (29 dates), corridors AUSTON/AUSVAN/NZTON/NZVAN. `audit2.csv`: 2023-07-25 to 2023-08-07 (14 dates), AUSTON/NZTON only |
| Send amount | Fixed 200 units of the origin currency for every row — confirmed by the benchmark column's own naming (`200AUD_NZD`) and by back-solving `amount_received` against `fee`/`fxrate` for 684+504 rows, not assumed from one example |
| Fee convention | Denominated in the origin currency. Whether it's deducted from the 200 before conversion or charged on top **varies by row and isn't stated in the source** — one row (Western Union Cash, NZTON, 2023-07-26) fits "on top" far better than "deducted" (a 5.94-unit gap vs ~1-unit tolerance everywhere else), proving both conventions are genuinely present. `amount_sent_includes_fee` is left `null` throughout rather than inferred from whichever formula fits — CLAUDE.md §1.1 |
| Website codes | `1` = Send Money Pacific, `2` = Saver Pacific (confirmed in the maintainer's own `.do` file) |
| Blank rows | 12 rows in `audit1.csv` (Saver Pacific, AUSTON, 2023-04-03) have every provider field empty but `Rank` and the benchmark columns still filled — read as "no options recorded that day," not a parsing gap, and excluded distinctly from genuinely-unrecognised-provider rows |

### 3.2 Import results

| | Task A (2023 audit) | Task B (NRBT historical) |
|---|---|---|
| Observations imported | 1,188 (684 + 504) | 4,757 |
| Rows excluded, and why | 696 Vanuatu-corridor rows (out of scope this round — no Vanuatu benchmark), 12 blank placeholder rows | 3 stray out-of-range dates (single-cell errors in NRBT's own workbook, e.g. a row dated 2028 inside the "2025 to 2026" sheet), 189 currency-rows with a blank/non-numeric cell (mostly one origin currency missing on a holiday specific to its home market — NRBT's own AUD cell literally reads "Public Holiday: New Year's Day" on 2017-01-02 while NZD has a real rate that day) |
| `normalise.validate --strict` | Clean | Clean |
| `collected_at` convention | The real historical date, per row (this genuinely is when each quote was observed) | Fixed at 2026-09-09 (the one real file-fetch date) for every row; `provider_quote_timestamp` carries the historical date instead |

Total store size after this round: 5,961 rows (was 5 before Round 4).

### 3.3 CLAIMS.md C1–C3, checked against primary data

| Claim | Before | After |
|---|---|---|
| C1 | VERIFIED (maintainer, unelaborated) | VERIFIED and expanded: two waves, not one, now located and ingested |
| C2 | UNCHECKED | **VERIFIED exactly** — 25 Jul 2023, NZTON, Ave Pa'anga Pau, Saver Pacific: amountreceived 284.1, fee 0, rate 1.42, matching the claim precisely |
| C3 | UNCHECKED | **REFUTED** — 3 Aug 2023, AUSTON shows 18 option-level rows (9 per platform × 2 platforms), 11 distinct raw MTO/mode options, 9 distinct base providers (7 per individual platform) — not 21 options from 15 RSPs under any grouping checked |

---

## 4. Decisions I made

1. **Left `amount_sent_includes_fee` null for every 2023 audit row**, rather than inferring it
   per-row or per-provider from which fee-arithmetic formula fits best. *Reversible, but should
   stay this way* — the one clear counter-example (§3.1) proves the source genuinely mixes both
   conventions; guessing per row would be exactly the "reasoning about what a price probably
   was" CLAUDE.md §1.1 rules out.
2. **Preserved the audit's own `Cost_PP` and embedded benchmark figures as text in `notes`**,
   not as this project's own `benchmark_fx_rate`. *Reversible.* `benchmark_fx_rate` is reserved
   for this project's own NRBT-sourced figure; populating it from a different, undocumented
   benchmark would misrepresent what the field means, even though keeping the original figure
   for traceability (and for Task C) is valuable.
3. **Left `speed_hours_min`/`speed_hours_max` null throughout**, storing only `speed_text`.
   *Reversible.* Converting "Next day" or "1-3 days" into a numeric hour range would invent
   precision the source doesn't state — the same reasoning as decision 1.
4. **Slugged providers to match `PROVIDERS.md`'s existing Round 1 naming where the same entity
   was already triaged there** (`ave-paanga-pau`, `klickex`, `western-union`, etc.), and split
   ANZ and Westpac by corridor into `anz-australia`/`anz-new-zealand` and
   `westpac-australia`/`westpac-new-zealand` rather than one shared slug. *Reversible, and
   directly addresses CLAIMS.md E3* (provider identity harmonisation across vintages) —
   deliberately, since this is the first real test of that open item.
5. **Did not ingest the Vanuatu rows in `audit1.csv`** even though they're real data in the
   source file. *Reversible, straightforward to add later* — this project has no Vanuatu
   benchmark (RBV's broken TLS chain stays un-worked-around), so a Vanuatu observation would sit
   with `benchmark_fx_rate` permanently null; keeping this round's scope to what Task A/B/C
   actually asked for (Tonga) rather than expanding coverage unasked.
6. **Added `hm-ds/` to `.gitignore` immediately on finding it**, before doing anything else with
   it. *Not reversible in the sense that matters* — this was the right default regardless of
   what turned out to be inside; only `audit1.csv`/`audit2.csv`'s content (via the archived
   envelope) becomes part of this project's public data.
7. **Fixed the ragged-CSV and binary-corruption bugs in the shared plumbing** rather than working
   around them narrowly for this round's specific needs. *Reversible in implementation, not in
   spirit* — both were latent bugs that would have bitten a future round regardless of what
   triggered discovering them this time.

---

## 5. Decisions I did not make

### 5.1 Did the 2023 data fit the schema without distortion, and what did Task C's comparison show?

**Yes, cleanly, with three deliberate exceptions already covered above.** Every field in both
audit CSVs has a home: either a schema column (most fields), a documented exclusion already
built into the schema's own policy (`Rank` — an explicitly excluded derived field, same as
`cost_pct`; `Date2`/`Thu`/`Weekend` — trivially derivable from `collected_at`, not new
information), or explanatory prose in `notes`/`status_detail` for facts that don't fit a
structured field without misrepresenting what that field means (the audit's own `Cost_PP` and
embedded benchmark figures — §4 decision 2). Nothing was dropped silently, and nothing was
invented to fill a gap the schema couldn't otherwise carry. The schema did not need to change to
accommodate this data — the one schema change this round (`rate_is_promotional`,
`promotion_detail`) was for the *OrbitRemit correction*, unrelated to the audit import.

**Task C's comparison, in full** (`scratch/round-04/task_c_comparison.py`,
`task_c_full_comparison.csv`):

- 780 of 1,188 audit rows matched a backfilled NRBT benchmark rate for the same date and origin
  currency. The 408 that didn't are **every weekend and AU/NZ public holiday in both audit
  windows** (Good Friday, Easter Monday, ANZAC Day, and every Saturday/Sunday) — verified by
  checking the actual weekday of each unmatched date, not assumed. NRBT doesn't publish a rate
  on non-business days; the audit recorded live MTO quotes daily regardless. A real,
  understood structural gap between a business-day benchmark series and a daily audit, not a
  join bug.
- **Pearson correlation between my `cost_pct` (NRBT benchmark) and the audit's own `Cost_PP`:
  0.988**, across all 780 matched rows.
- **97.7%** of matched rows agree on sign (both positive — a real cost either way).
- **100%** of the 110 date×corridor groups with 2+ providers identify the **same cheapest
  provider** under both benchmarks.
- **Mean within-day Spearman rank correlation: 0.998** — the relative ordering of providers on
  any given day is almost never disturbed by which benchmark is used.
- **Mean difference: my figure runs about 0.44 percentage points below the audit's own**,
  consistently (median −0.47, std 0.85). Not adjusted to close this gap — it's a small, expected
  difference given a different benchmark source, and per §2.3's own correction this round (NRBT's
  MID is a dealing-spread midpoint, not a neutral market mid), there's no reason to expect exact
  agreement in the first place.

**Direction, ordering and rough magnitude all hold**, per the brief's own framing — this is a
strong, unforced validation of the pipeline against real historical data collected by a
different method entirely (manual audit vs. this project's own benchmark backfill), computed
independently and only then compared, not tuned to agree.

### 5.2 Task C's held-out cases are worth a closer look, not acted on this round

The 408 unmatched rows are understood (§5.1) but not resolved — this project's benchmark
coverage is Tonga business-day rates only. Whether that's acceptable for the eventual published
observatory (i.e., whether weekend/holiday observations should carry a `benchmark_fx_rate` at
all, or whether `cost_pct` for those rows should simply stay uncomputable) is a METHODOLOGY
question, not decided here — flagged for a future round or the maintainer's own judgement.

---

## 6. Errors and anomalies

**Ragged CSV, first `normalise.validate --strict` after the schema grew:**
```
pandas.errors.ParserError: Error tokenizing data. C error: Expected 44 fields in line 7, saw 46
```

**`RuntimeError` from the store migration's own safety check**, when the two new schema fields
were still mid-list (before being moved to the end):
```
RuntimeError: /Users/ryanbedwards/pacific-remittance-observatory/store/observations/2026-09.csv has a header that is not a prefix of the current schema columns -- this needs a human decision, not an automatic migration. existing=[...43 columns...] target=[...45 columns, 'rate_is_promotional' and 'promotion_detail' inserted after 'fee_is_promotional' rather than at the end...]
```
This was the safety check working correctly, not a failure — it refused to guess, exactly as
designed.

**The Western Union Cash fee-convention outlier**, verbatim source row (`audit2.csv`,
2023-07-26):
```
{'date': '26/07/2023', 'website': '2', 'corridor': 'NZTON', 'mtos': 'Western Union (Cash)', 'modeoftransaction': 'Account - Cash', 'speed': 'Less than one hour', 'amountreceived': '270.54', 'FXrate': '1.35', 'Fee ': '4', 'Cost_PP': '7.08', '200AUD_NZD': '291.14'}
```
`(200 − 4) × 1.35 = 264.6` (5.94 off `270.54`); `200 × 1.35 = 270.0` (0.54 off, within the
usual rounding tolerance). This single row is why `amount_sent_includes_fee` was left null for
the whole import rather than assumed.

**The 12 blank placeholder rows**, verbatim (`audit1.csv`, first instance):
```
{'Date': '3/4/2023', 'Website': '2', 'Corridor': 'AUSTON', 'MTOs': '', 'modeoftransaction': '', 'Speed': '', 'amountreceived ': '', 'fxrate': '', 'Fee ': '', 'Cost_PP': '', 'Date2': 'Mon', 'Thu': '0', 'Weekend': '0', 'Rank': '1', 'AUD_Paanga': '314.44', 'NZD_Paanga': '294.2', 'AUD_Vatu': '15915', 'NZD_Vatu': '14891.2'}
```

**NRBT's own "blank cell" convention**, verbatim (`nrbt-historical-rates.xlsx`, 2017-01-02, AUD
column):
```
"Public Holiday: New Year's Day"
```
while the NZD column for the same row and date is a genuine empty cell (`nan`), not text —
two different ways the same source represents "no rate today," both correctly excluded by the
Round 4 fix to the backfill parser (which previously accepted `float(nan)` as a valid rate,
since `nan` is a valid float and doesn't raise).

---

## 7. Repository changes

| File | Change | Why |
|---|---|---|
| `CLAUDE.md` | Unchanged this round | Round 3's "what is/isn't a workaround" clause stands; nothing new added |
| `schema/observation.schema.json` | Edited (v0.1→v0.2) | `rate_is_promotional`, `promotion_detail` added at the end of `properties` (with the ordering convention now documented in the file itself) |
| `docs/METHODOLOGY.md` | Edited (v0.3→v0.4) | §2.3: NRBT's MID documented as a dealing-spread midpoint, not an interbank mid |
| `docs/REPORTING.md` | Edited | "Closes structurally" vs "closes substantively" defined |
| `CHANGELOG.md` | Edited | Entries for both version bumps |
| `.gitignore` | Edited | `hm-ds/` excluded — see §4 decision 6 |
| `collect/archive.py` | Edited (twice) | Placeholder URL removed from `USER_AGENT`; binary-content corruption fixed (`archive_bytes`/`read_archived_bytes`/`read_archived_body`) |
| `collect/orbitremit/connector.py` | Rewritten | Emits all nine table rows, not one; ninth-row reference resolution added |
| `collect/store.py` | Edited | Schema-growth migration (`_migrate_header_if_needed`) |
| `collect/backfill_nrbt_historical.py` | Created | Task B: NRBT historical import, not a connector |
| `collect/ingest_2023_audit.py` | Created | Task A: 2023 audit import, not a connector |
| `normalise/validate.py` | Edited | `rate_is_promotional` added to the boolean-field list |
| `requirements.txt` | Edited | `openpyxl` added (now actually used by committed code, not just exploratory analysis) |
| `tests/test_archive.py`, `test_orbitremit.py`, `test_store.py` (new), `test_backfill_nrbt_historical.py` (new), `test_ingest_2023_audit.py` (new) | Edited/created | 41 tests total this round, all offline |
| `archive/nrbt/...`, `archive/orbitremit/...`, `archive/manual-audit-2023/...` | Created | Real archived artefacts: the NRBT historical `.xlsx`, the audit CSVs, live OrbitRemit/NRBT fetches |
| `store/observations/2017-*.csv` through `2026-*.csv` (117 new files) | Created | Task B's backfill |
| `store/observations/2023-03/04/07/08.csv` | Appended | Task A's import |
| `scratch/round-03/*` | (Round 3, referenced not changed) | — |
| `scratch/round-04/*` | Created | Task C's comparison script and full row-level output |
| `hm-ds/` | **Not committed** | Maintainer's own broader research data; gitignored, see §4 decision 6 |

No file under `archive/` or `store/` was modified after being written — the header-migration
exception widens a file's structure without changing any existing cell's *value*, per
`collect/store.py`'s own documented policy.

---

## 8. Claims register delta

| Claim | Before | After |
|---|---|---|
| C1 | VERIFIED (maintainer) | VERIFIED and expanded — two waves located and ingested |
| C2 | UNCHECKED | VERIFIED exactly against `audit2.csv` |
| C3 | UNCHECKED | REFUTED — 18 options / 9 base providers, not 21 / 15 |
| C2/C3 (blocking item, §0) | Blocking | Resolved |

---

## 9. Confidence flags

- **The fee-convention finding (one row fits "on top," most fit "deducted") is based on
  arithmetic tolerance, not a documented rule.** It's possible a handful of other rows are
  similarly ambiguous and happened to fall within the 1–2 unit tolerance used for classification
  by coincidence rather than genuinely fitting the "deducted" convention. `amount_sent_includes_fee`
  being null throughout means this ambiguity can't silently produce a wrong number, but it also
  means it's not resolved, just correctly not-guessed-at.
- **Provider type classification** (`bank`/`global_mto`/`corridor_specialist`) for the audit's
  MTOs was assigned from this project's own Round 1 `PROVIDERS.md` categorisation where the
  entity was already triaged there — reasonable, but not independently re-verified this round.
- **The Task C comparison's 0.44-percentage-point mean gap direction (mine consistently lower)**
  is reported as observed, not explained beyond "different benchmark source" — a real
  investigation of exactly why NRBT's MID runs where it does relative to whatever benchmark the
  original audit used would need to know that original benchmark's methodology, which isn't
  documented in the source files checked this round.
- **The 12 blank placeholder rows' actual meaning is inferred** (a day with no recorded options
  on Saver Pacific/AUSTON), not confirmed from the maintainer or any documentation — a
  reasonable reading of the pattern (Rank and benchmark columns present, everything else empty),
  not a certainty.
- **`hm-ds/`'s exclusion from git is a judgement call about sensitivity**, not a confirmed
  restriction — the maintainer hasn't stated the household survey data can't be shared, only
  that it wasn't what this project asked for. Erring toward not committing it seemed clearly
  right regardless, but it's worth the maintainer's own explicit confirmation if that folder's
  fate matters going forward (delete it, move it elsewhere, or something else).
- **Task C's script lives in `scratch/round-04/`, not `normalise/reference/`** as CLAUDE.md §2.2
  anticipates for indicator logic that needs a Python reference implementation Stata can be
  tested against. This round's comparison was a one-off validation, not a committed indicator —
  worth revisiting if `cost_pct` becomes something Stata actually needs to reproduce from this
  project's own reference implementation.

---

## 10. Recommended next round

**Decide E5 (Niue/Cook Islands/Tokelau-style corridor exceptions) and E2 (fee-inclusion
convention) properly now that real data exists to reason about them** — this round's
`amount_sent_includes_fee` finding (§3.1, §6) is exactly the kind of concrete case METHODOLOGY §2's
OPEN items were waiting for.

**Consider whether to import the Vanuatu rows in `audit1.csv`** once/if a Vanuatu benchmark
becomes reachable (Reserve Bank of Vanuatu's TLS chain would need to actually get fixed on their
end — still not something to work around).

**Get the maintainer's read on `hm-ds/`'s fate** — confirmed excluded from git, but its
longer-term handling (delete, relocate, leave as untracked local reference) hasn't been decided.

**Deliberately left undone this round:**
- No third connector, per the brief.
- Vanuatu rows in `audit1.csv` — real data, not ingested (§4 decision 5).
- E2/E5 — informed by this round's findings but not decided.
- `report_failures.py`'s GitHub-issue-opening half of the repair loop — still a stub (Round 2/3's
  flag, unchanged).
- Python 3.12 testing / the CI-triggering push — still blocked on a git remote not existing
  (Round 3 §5.2, unchanged this round; the maintainer has said they're creating one).
