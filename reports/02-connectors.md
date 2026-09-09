# Round 2 — two connectors

**Date:** 2026-09-09
**Scope:** build exactly two connectors — ANZ New Zealand (Tier 1, published tariff, NZ→Tonga
NZ$200) and the National Reserve Bank of Tonga benchmark (Tier 1, published tariff) — full
lifecycle (fetch → hash → archive → parse → normalise → validate → append), against fresh raw
fetches, with golden tests reproducible offline from committed fixtures. Also: assess NRBT's
2017–present historical file without importing it.

**Explicitly out of scope:** a third connector, any other provider, any browser-based fetch, any
workaround for a block. This report follows the structure in `docs/REPORTING.md` (numbering
fixed after Round 1 — see that file's changelog) and assumes no memory of this session.

**Outcome in one line:** Task B (NRBT) is built, tested, run live, and validated end to end.
Task A (ANZ NZ) is blocked; a maintainer-directed raw-fetch verification sweep of every other
Tier 1/2 candidate then found the real problem is broader than one provider — most bank rate
pages are client-rendered, not bot-walled, which makes true Tier 1 rarer than `PROVIDERS.md`
assumed. Nothing survives the sweep that fits the current NZ→Tonga Tier 1 corridor, so Task A
did not run this round — reported, not substituted for.

---

## 2. What I did

1. Read `reports/01-triage.md`, `CLAUDE.md`, `CLAIMS.md`, `SPRINT-01.md`, `docs/METHODOLOGY.md`
   in full, then recorded the four maintainer decisions from Round 1 §5 before touching any
   build code: Session 4's corridor changed to NZ→Tonga via ANZ NZ (SPRINT-01.md, CLAIMS.md
   §F); the benchmark rate (E1) decided — central bank primary, best-observed-provider-rate
   secondary, NRBT first (`CLAIMS.md` E1, `docs/METHODOLOGY.md` v0.1→v0.2, `CHANGELOG.md`);
   OrbitRemit recategorised as a global MTO (`PROVIDERS.md`); MoneyGram set to `UNRESOLVED` and
   Central Bank of Solomon Islands/Bank of Papua New Guinea set to `PENDING_PERMISSION`
   (`PROVIDERS.md`); and `docs/REPORTING.md`'s subsection-numbering convention fixed.
2. Planned Round 2 (shared plumbing, Task A, Task B, evidence discipline, method constraints)
   and got explicit approval before writing any connector code.
3. Set up a local Python 3.8 venv (`.venv/`, gitignored) since no newer interpreter was
   available locally; installed `requirements.txt` plus `pytest`, all importing cleanly. CI
   (`.github/workflows/collect.yml`) targets Python 3.12 — nothing written this round uses a
   3.9+-only feature at runtime (`from __future__ import annotations` covers the lowercase
   generic type hints), so this shouldn't matter, but it's untested against 3.12 directly.
4. Fresh, honest-UA `curl` fetches (not `WebFetch`) of all three planned sources: ANZ NZ's FX
   rate table, ANZ NZ's fee schedule, NRBT's daily rate table. **The ANZ NZ FX rate table came
   back as an Incapsula bot-challenge page**, not the rate table Round 1 recorded. I did one
   round of light, honest diligence — checking whether ANZ's own site links to the rates
   another way (it doesn't; every path, including a 301 redirect and a linked
   exchange-rate-graphs page, funnels to the same blocked resource) — then stopped rather than
   pursue a workaround. Full account in `scratch/round-02/anz-nz-fx-table-blocked.md`.
5. Committed the evidence (including the block) as its own checkpoint, corrected `PROVIDERS.md`
   accordingly, then proceeded with Task B while flagging Task A for the maintainer (this
   report's §5.1) rather than picking a replacement provider or corridor myself.
6. Built the shared plumbing (`collect/archive.py`, `collect/store.py`, `collect/run.py`,
   `collect/report_failures.py`, `normalise/validate.py`) — the entrypoints
   `.github/workflows/collect.yml` already calls.
7. Built `collect/benchmarks/nrbt/connector.py` against the real table structure (inspected the
   raw HTML directly, targeted `table.table-custom-4c` specifically), documented and applied
   the quote-orientation inversion METHODOLOGY §2.4 had flagged as undecided, wrote a golden
   test (`tests/test_nrbt.py`, 6 cases) that runs entirely offline against a committed fixture,
   and confirmed it passes.
8. Ran the real pipeline once (`python -m collect.run --all`): one live NRBT fetch, archived,
   parsed, normalised, appended to `store/observations/2026-09.csv`. Ran
   `python -m normalise.validate --strict` against it — found and fixed a real bug in my own
   validator (a manual "required field" pre-check that didn't understand required-but-nullable
   schema fields), then confirmed a clean pass.
9. Fetched and assessed NRBT's 2017–present historical file (structure, coverage, a
   data-quality flag on three stray out-of-range dates, and a spot-check against the 2023
   Jul–Aug audit period) — reported, not imported, per the brief.
10. Committed after each checkpoint (evidence → connector+tests → live run+validator fix →
    historical assessment → this report), so the round has usable, working output at every
    point, not just at the end.
11. Published this report and asked the maintainer how to proceed on the blocked Task A, with
    four options, no recommendation pressed.
12. On the maintainer's direction: ran a raw-fetch verification sweep of every other Round 1
    Tier 1/2 bank/MTO candidate (ten sites, one honest fetch each, no retries, no browser),
    saved to `scratch/round-02/verify/`, checking specifically for bot-management infrastructure
    and whether target rate figures are present in raw bytes or only after JavaScript.
13. Added a permanent `verification_method` column (`raw_fetch` / `webfetch_summary`) to every
    row in `PROVIDERS.md`, corrected several rows the sweep directly contradicted (Wise's
    "confirmed for Fiji" claim didn't survive re-reading Round 1's own evidence; OrbitRemit
    upgraded on genuine raw-byte evidence), and committed the sweep as its own checkpoint.
14. Rewrote this report's §5.1 with the sweep's findings and their implication for the Tier 1
    premise generally, per the maintainer's explicit instruction — see below.

---

## 3. Findings

### 3.1 Task A — ANZ New Zealand: blocked

| Source | Status | Detail |
|---|---|---|
| Fee schedule (`www.anz.co.nz/personal/fx-international/international-money-transfers/`) | **Open, genuinely fetched** | 310,618 bytes, real content, confirms Round 1's "OUR Fee" finding: standard goMoney/Internet Banking channel fee is $0; an undisclosed additional "OUR Fee" may apply, shown only at the point of payment. |
| FX rate table (`tools.anz.co.nz/foreign-exchange/fx-rates/`) | **Blocked** | 926-byte Incapsula bot-challenge page (`Request unsuccessful. Incapsula incident ID: 136000310247516698-163488754764875720`) to a plain, honestly-identified `curl` client. Confirmed via ANZ's own navigation, not a wrong URL guess: the fee page's own link, a 301 redirect, and a linked exchange-rate-graphs page (240,757 bytes, genuinely open) all funnel to the same blocked endpoint. |

No connector was built for ANZ NZ this round. See §5.1.

### 3.2 Task B — National Reserve Bank of Tonga: built, tested, run, validated

| Check | Result |
|---|---|
| Fresh fetch of the daily rate page | 52,703 bytes, genuine content, no block |
| Table located by parser | `table.table-custom-4c`, 12 currency rows, BUY/MID/SELL columns |
| NZD row (2026-09-09) | BUY 0.7367 / MID 0.7210 / SELL 0.7052 (NZD per 1 TOP, as published) |
| Golden tests (`tests/test_nrbt.py`) | 6/6 passing, offline, against the committed fixture |
| Live run (`python -m collect.run --all`) | 1 observation, `availability_status = observed` |
| Archived artefact | `archive/nrbt/2026/09/09/ae44686cff21f14b90cb36d5281210bb2ba8f6c4750566771fb3c65e197701f6.json.gz` |
| Store row | `store/observations/2026-09.csv`, `collection_run_id = run-20260909T111117Z-22d0f577` |
| `python -m normalise.validate --strict` | 1 row checked, 0 errors |
| `provider_fx_rate` / `amount_received` (TOP per 1 NZD, inverted from the published MID rate) | 1.3869625520110958 |

### 3.3 NRBT historical file assessment

| Sheet | In-range rows | In-range span | Out-of-range rows |
|---|---|---|---|
| 2017 to 2018 | 514 | 2017-01-02 → 2018-12-31 | 1 (`2003-07-17`) |
| 2019 to 2020 | 521 | 2019-01-01 → 2020-12-31 | 1 (`2009-03-22`) |
| 2021 to 2022 | 493 | 2021-01-01 → 2022-12-30 | 0 |
| 2023 to 2024 | 522 | 2023-01-02 → 2024-12-31 | 0 |
| 2025 to 2026 | 423 | 2025-01-01 → 2026-09-09 | 1 (`2028-05-28`) |

2,473 clean in-range rows total; 3 stray out-of-range dates (single-cell errors, not a
structural problem). The file is not a tidy table — three side-by-side BUY/MID/SELL blocks per
sheet sharing one date column — a real import would need to reshape it. Full detail, including
the Jul–Aug 2023 spot-check against `CLAIMS.md` C2, is in
`scratch/round-02/nrbt-historical-assessment.md`. Not imported this round, per the brief.

---

## 4. Decisions I made

1. **Stopped pursuing the ANZ NZ FX rate table after one round of light, honest diligence**
   (checking ANZ's own linked alternatives, not retrying the blocked URL itself or spoofing
   headers). *Not reversible without a genuinely new approach* — but see §5.1; I did not
   unilaterally substitute a different provider or corridor to keep Round 2 moving, since that
   would have been touching a provider beyond what was approved.
2. **Corrected `PROVIDERS.md`'s ANZ NZ row immediately** rather than leaving a stale "Tier 1,
   confirmed" claim standing while waiting for direction on what to build instead. *Reversible*
   — it's a factual correction with evidence, not a coverage decision.
3. **Built the shared plumbing (`collect/archive.py`, `run.py`, `store.py`,
   `report_failures.py`, `normalise/validate.py`) even though the brief said "two connectors and
   nothing else."** *Reversible in structure, not in spirit* — treated as necessary scaffolding
   a connector needs to be more than a standalone script, not a third thing. `report_failures.py`
   is a deliberately minimal stub (no GitHub issue creation) to keep this reading as plumbing,
   not a new feature.
4. **Added `pytest` to `requirements.txt`.** *Reversible.* No test runner was previously
   specified; `pytest` is the standard choice and CLAUDE.md §5 requires golden-file tests to
   exist and run somewhere.
5. **Did not add `openpyxl` to `requirements.txt`** for the historical-file assessment —
   installed it only in the local venv for one-off inspection, since no committed connector code
   uses it. *Reversible; trivial to add when the file is actually imported.*
6. **Quote-orientation convention for `*_fx_rate` fields: destination currency per 1 origin
   currency unit** (documented in `collect/benchmarks/nrbt/connector.py` and applied by
   inverting NRBT's published NZD-per-TOP rate). METHODOLOGY §2.4 flagged this as needing
   standardisation and had not yet decided it. *Reversible, but has real consequences if
   changed* — every stored `*_fx_rate` value inherits this convention; changing it later means
   either a documented reinterpretation of existing rows or a new methodology version, never a
   silent flip.
7. **Benchmark-row conventions**: `amount_sent = 1.0`, `fee = null` (not `0`), for a row that
   represents a published rate rather than a transfer quote. *Reversible* — no other connector
   depends on these values being any particular number yet.

---

## 5. Decisions I did not make

### 5.1 What to do about Task A now that ANZ NZ's FX table is confirmed blocked

The maintainer decided, minutes before this round started, to build Session 4 as NZ→Tonga via
ANZ NZ specifically because Round 1 recorded it as the one confirmed Tier 1 bank. That finding
does not survive a fresh, honest fetch — see §3.1 and
`scratch/round-02/anz-nz-fx-table-blocked.md`. This is a genuine reopening of a decision made on
the basis of evidence that turned out not to hold, not a minor implementation snag.

**What broke, specifically:** `tools.anz.co.nz/foreign-exchange/fx-rates/` — the only URL ANZ's
own site links to for FX rates, confirmed via their own navigation and redirect chain — returns
an Incapsula bot-challenge page (`Request unsuccessful. Incapsula incident ID: ...`) to a plain,
honestly-identified HTTP client. The most likely explanation is that Anthropic's `WebFetch` tool
(used throughout Round 1) has fetching infrastructure capable of clearing that challenge — a
full browser render, different IP reputation, or both — that a production Python collector
cannot replicate without itself becoming exactly the kind of bot-wall workaround CLAUDE.md §1.5
rules out. `WebFetch` is not a reliable proxy for what an honest automated collector can
actually observe. This is the concrete case Round 2's evidence-discipline change was written to
catch, and it caught it.

**The maintainer's response to this finding, in full**, was not to pick a replacement provider —
it was to question whether the triage *method* itself is sound, on the observed pattern that
ANZ NZ (Incapsula), ASB (connection reset) and Westpac NZ (Akamai 403) are three commercial
banks with three different bot walls against three different Round 1 checks. The instruction:
run a raw-fetch verification sweep — one honest fetch each, no retries, no browser, no crawling
— across every remaining Tier 1/2 candidate before building anything, add a permanent
`verification_method` column to `PROVIDERS.md` distinguishing `raw_fetch` from
`webfetch_summary`, and only build Task A this round if something survives the sweep with real
numbers in the raw bytes.

**The sweep.** Ten candidates, one fetch each, saved to `scratch/round-02/verify/`: Kiwibank,
BNZ, ANZ (Australia), Commonwealth Bank, NAB, St. George, Remitly, Wise, Western Union,
OrbitRemit. (ANZ NZ's fee schedule was excluded — already confirmed open earlier this round, no
need to re-fetch it.)

| Candidate | HTTP | Bot-management infra detected | Real content or challenge? | Target numbers in raw bytes? |
|---|---|---|---|---|
| Kiwibank | 200 | None | Real | **No** — `data-rate="240"` is a widget-row ID, not a rate (same finding as Round 1, now raw-fetch confirmed) |
| BNZ | 200 | Akamai (`akamai-grn`) | Real | **No** — `window.__PRELOADED_STATE__` inspected directly; contains nav/feature-flags only, no rate table |
| ANZ (Australia) | 200 | Incapsula (`visid_incap_`, `x-cdn: Imperva`) — present but did not challenge | Real | **No** — no currency codes anywhere in raw HTML |
| Commonwealth Bank | 200 | Cloudflare (`__cf_bm`) | Real | **No** — matches Round 1's own direct `curl` finding |
| NAB | 200 | Akamai Bot Manager (`_abck`, `bm_sz`, `akacd_`) — present but did not challenge | Real | **No** |
| St. George | 200 | None | Real | **No** — Round 1's "TOP" sighting was a false positive (HTML comment `SBGRP TOPNavigation`) |
| Remitly | 200 | None (istio-envoy) | Real | **No** — expected; a Tier 2 calculator needs interactive input |
| Wise | 200 | Cloudflare (`__cf_bm`) | Real | **No** — TOP/FJD appear only in a currency-catalogue metadata blob, not a computed rate. **Corrects Round 1**: its "confirmed for Fiji" claim traces to a worked example that was actually AUD→PHP, not Fiji |
| Western Union | 200 | Akamai Bot Manager (`_abck`, `bm_sz`) — present but did not challenge | Real | **No** — FJD appears only as a currency-picker dropdown label |
| OrbitRemit | 200 | Cloudflare | Real | **Yes** — meta description on `/currency-converter/aud-to-fjd` and `/currency-converter/aud-to-top` states a real figure server-side (`$1 AUD = 1.57014 FJD`, `$1 AUD = 1.69237 TOP`), no JS required |

**What this actually shows — the implication for the Tier 1 premise, made explicit.** It is
*not* that commercial banks are systematically bot-walled shut. Nine of ten candidates returned
real, unblocked content — several through Incapsula, Akamai Bot Manager or Cloudflare Bot
Management infrastructure that is demonstrably present (visible in cookies and headers) but
simply didn't challenge a plain, honestly-identified GET. Only ANZ NZ's specific rate-table
endpoint issued an actual, unpassable challenge to this project's traffic. **The real, more
common failure mode is a different one entirely: modern bank websites are overwhelmingly
client-rendered.** The rate table itself is fetched by client-side JavaScript after the page
loads, not embedded in the server-delivered HTML. A "boring" collector (`requests`/`httpx`,
no browser — CLAUDE.md §4's explicit preference) receives a real page and no rate, every time,
for every bank checked except Kiwibank's near-miss (a widget with the right shape but a
placeholder value) and OrbitRemit (which embeds a real number precisely because it's rendered
into a `<meta>` tag server-side, seemingly for SEO purposes, not for a collector's benefit).

**This does change the architecture, not just the provider list — the maintainer's own framing
is correct.** `PROVIDERS.md`'s Tier 1 definition ("public daily FX table... reconstructed
arithmetically") assumed a table exists in the page a collector fetches. For every bank checked
this round except Kiwibank's structural near-miss, that assumption is false: the table exists
only after JavaScript runs. Tier 1 is not blocked shut by adversarial bot walls — it is much
rarer than `PROVIDERS.md` assumed, because most banks' *architecture*, not their *policy*,
keeps the rate out of a plain client's reach. Reaching an actual Tier 1 bank rate going forward
likely means one of: (i) finding a bank whose rate table is still server-rendered (untested and
possibly rare among the ten checked), (ii) discovering the underlying JSON/XHR endpoint the
client-side widget itself calls (still "boring" — a static API request, not a browser — but
real engineering work, and untested this round whether such endpoints are even reachable
without their own bot-management challenge), or (iii) revising what "Tier 1" means for a bank
in practice. None of these were pursued this round — per the maintainer's explicit instruction,
the sweep recorded and did not fix.

**Does anything survive with real numbers in raw bytes? One partial case, and it doesn't fit
the current corridor.** OrbitRemit's `/currency-converter/aud-to-top` page states a genuine,
server-rendered rate (`$1 AUD = 1.69237 TOP`) with no JS needed — this is a real survivor by the
letter of the maintainer's bar. But: it's AUD-origin, not NZD — checking OrbitRemit's own linked
converter pages found `aud-to-top` but no `nzd-to-top` (the NZD pairs listed are
`nzd-to-aud/inr/lkr/npr/php/vnd` — no Pacific currencies among them), so it does not serve the
NZ→Tonga corridor Session 4 currently targets. And the rate is only half a published tariff —
no fee *amount* was found in raw bytes anywhere on the page (only generic "fixed transfer fees"
text), so even for AU→Tonga this doesn't fully close a `published_tariff` reconstruction from
raw bytes alone; it would need to be built as Tier 2 (`public_quote`), which is what
`PROVIDERS.md` already calls it.

**Conclusion: nothing survives the sweep that satisfies the current Task A scope (NZ→Tonga,
Tier 1, via a bank tariff).** Per the maintainer's own instruction, this is reported rather than
substituted for. Task A did not run this round. `PROVIDERS.md` is updated (verification_method
column, corrected Wise/OrbitRemit/ANZ AU/Kiwibank/BNZ/Commonwealth Bank/NAB/St. George rows) so
this finding is structural, not confined to this report.

**What I had to assume, given Task A didn't happen:** nothing about ANZ NZ itself — no fee
figures, no rate figures, no service-option enumeration were assumed or fabricated in place of
the blocked data. The only real assumption made this round was the quote-orientation inversion
for NRBT (§4.6), which is documented, not silent.

**Does the cost measure close end to end for NZ→Tonga NZ$200 via ANZ NZ, from archived bytes
alone? No — not yet, and this is the direct, honest answer to that question.** The benchmark
leg closes completely: `store/observations/2026-09.csv`'s one row traces to
`archive/nrbt/2026/09/09/ae44686cff21f14b90cb36d5281210bb2ba8f6c4750566771fb3c65e197701f6.json.gz`,
passes schema validation, and its `provider_fx_rate` (1.3869625520110958 TOP per NZD) is a real,
reproducible, archived figure. But `cost_pct` per METHODOLOGY §2.2
(`benchmark_receive_value = amount_sent × benchmark_rate; implicit_cost_value =
benchmark_receive_value − amount_received; cost_pct = implicit_cost_value / benchmark_receive_value
× 100`) needs an `amount_received` figure from an actual ANZ NZ quote observation, and no such
observation exists — Task A did not run. There is nothing to compute `cost_pct` from on the
provider side; asserting one now would mean inventing the missing half, which CLAUDE.md §1.1
rules out categorically. The honest state of Round 2 is: one full, working, validated leg of the
measure (the benchmark), and zero legs of the other (the provider quote), not a partial or
approximate `cost_pct`.

### 5.2 The `MoneyGram Content-Signal` vs `robots.txt ClaudeBot disallow` conflict

Unchanged from Round 1 — recorded as `UNRESOLVED` in `PROVIDERS.md`, not touched this round
since Round 2 didn't involve MoneyGram. Flagging only that it's still open.

---

## 6. Errors and anomalies

**ANZ NZ FX rate table** (`curl` with an honest UA, no header spoofing):
```
HTTP/2 200
content-length: 926
```
Body (in full):
```html
<html style="height:100%"><head><META NAME="ROBOTS" CONTENT="NOINDEX, NOFOLLOW">...<iframe id="main-iframe" src="/_Incapsula_Resource?SWUDNSAI=31&xinfo=8-25365969-0 pNNN RT(1788951571170 16) q(0 -1 -1 10) r(0 -1) B12(14,0,0) U18&incident_id=136000310247516698-163488754764875720&edet=12&cinfo=0e0000008edc&rpinfo=1032&cts=...&cip=60.241.75.120&mth=GET" frameborder=0 width="100%" height="100%">Request unsuccessful. Incapsula incident ID: 136000310247516698-163488754764875720</iframe></body></html>
```

**ANZ NZ FX rates page, redirect chain** (following the fee page's own link):
```
https://www.anz.co.nz/personal/fx-international/foreign-exchange-rates/
-> HTTP 301 -> https://tools.anz.co.nz/foreign-exchange/fx-rates/ -> HTTP 200, same Incapsula challenge, incident ID 136000310247516698-163488754764875720 (different session, same block)
```

**My own validator bug**, first run of `normalise.validate --strict` against the real NRBT row:
```
normalise.validate: checked 1 row(s) across store/observations/
1 error(s):
  - 2026-09.csv:2: missing required field(s): ['amount_sent_includes_fee']
```
Cause: a manual pre-check (`missing = [f for f in required if obs.get(f) in (None, "")]`)
treated a required-but-nullable field's legitimate `None` as "missing." `jsonschema.validate`
already handles required-but-nullable fields correctly (required means key-present, not
non-null); the manual check was redundant and wrong, and was removed rather than patched around.
Re-run after the fix: `all rows valid`, exit 0.

**Local environment**: only Python 3.8.3 was available locally (`/Library/Frameworks/
Python.framework/Versions/3.8/bin/python3`); CI targets 3.12. A local venv was created
specifically for this round (`.venv/`, already gitignored) rather than assuming system Python
matches CI. Not run against 3.12 directly this round.

---

## 7. Repository changes

| File | Change | Why |
|---|---|---|
| `SPRINT-01.md`, `CLAIMS.md` | Edited | Recorded the Session 4 corridor decision (`reports/01-triage.md` §5.1: NZ→Tonga via ANZ NZ) and closed E1 (`reports/01-triage.md` §5.4: central bank primary, best-observed-provider-rate secondary). |
| `docs/METHODOLOGY.md`, `CHANGELOG.md` | Edited | METHODOLOGY v0.1→v0.2: §2.3 rewritten, decided, documents what a central-bank indicative rate actually is. Version-bump note in CHANGELOG per CLAUDE.md §1.6. |
| `PROVIDERS.md` | Edited (three times) | OrbitRemit recategorised, MoneyGram set UNRESOLVED, CBSI/BPNG set PENDING_PERMISSION (maintainer decisions); ANZ NZ's FX-table row corrected to BLOCKED; then a `verification_method` column added to every row, with Wise/OrbitRemit/ANZ AU/Kiwibank/BNZ/Commonwealth Bank/NAB/St. George rows corrected or strengthened per the raw-fetch sweep. |
| `docs/REPORTING.md` | Edited | Subsection-numbering convention fixed (maintainer instruction). |
| `scratch/round-02/*.md`, `scratch/round-02/nrbt-historical-rates.xlsx` | Created | Evidence: the ANZ NZ block (raw challenge-page bytes + write-up), the historical-file assessment + the file itself. |
| `scratch/round-02/verify/*` | Created | The ten-candidate raw-fetch verification sweep: response headers and bodies, one honest fetch each. |
| `tests/fixtures/anz-nz/fees.raw.html`, `tests/fixtures/nrbt/*` | Created | Fresh raw fetches, per Round 2's evidence-discipline change. The NRBT one is a golden-test fixture; the ANZ NZ fee page is evidence only (no connector built against it yet). |
| `collect/archive.py`, `collect/store.py`, `collect/run.py`, `collect/report_failures.py` | Created | Shared plumbing: fetch, hash, archive, append-only store writer, connector registry/CLI, minimal failure-reporting stub. |
| `collect/benchmarks/nrbt/connector.py` | Created | The NRBT benchmark connector (Task B). |
| `normalise/validate.py` | Created | The CI validation gate: schema, archive resolution, arithmetic sanity. |
| `tests/test_nrbt.py` | Created | 6 golden tests, offline, against the committed NRBT fixture. |
| `requirements.txt` | Edited | Added `pytest`. |
| `archive/nrbt/2026/09/09/<sha256>.json.gz` | Created | The first real archived artefact — output of the live pipeline run, not a fixture. |
| `store/observations/2026-09.csv` | Created | The first real observation row — same live run. |
| `.venv/` | Created, not committed | Local Python 3.8 environment for running tests and the pipeline; already covered by `.gitignore`. |

No connector or provider outside ANZ NZ and NRBT was touched. No file under `archive/` or
`store/` was modified after being written — only appended to, once.

---

## 8. Claims register delta

No `CLAIMS.md` entries changed status this round — Round 1's decisions were recorded in the
prior commit series, before this round's build work started, not re-touched here.
`PROVIDERS.md`'s ANZ NZ row changed (see §7, Repository changes) — that register lives in
`PROVIDERS.md` directly, per `CLAIMS.md` §D's own note that the full table is maintained there,
not duplicated in `CLAIMS.md`.

---

## 9. Confidence flags

- **The ANZ NZ block's root cause (WebFetch clearing an Incapsula challenge a plain client
  cannot) is a strong inference from the evidence, not independently confirmed.** I did not test
  whether `WebFetch` itself would still succeed against the same URL today — doing so wasn't
  necessary to establish that a production collector is blocked, which is the fact that matters,
  but it means the *explanation* for the Round 1/Round 2 discrepancy is my best read, not a
  proven mechanism.
- **The quote-orientation convention (§4.6)** is a real methodological choice made to unblock
  Task B, not a neutral default — METHODOLOGY §2.4 explicitly left it open. It's documented in
  the connector's docstring and in `status_detail` on every row it produces, but it is a
  decision, and a different one is defensible.
- **Local testing used Python 3.8, not the 3.12 CI targets.** Nothing written this round is
  known to need 3.9+ syntax at runtime, but this was not verified by actually running under
  3.12.
- **The historical file's 3 stray out-of-range dates were found by a coarse per-sheet year-range
  filter**, not a full data-quality audit of all 2,473 rows — there could be other, less obvious
  errors (a plausible-looking but wrong date, a currency column misaligned on some row) that a
  coarse filter wouldn't catch. Worth a closer pass before any future import.
- **The Jul–Aug 2023 cross-check against `CLAIMS.md` C2** used one date (25 Jul 2023) and one
  provider (`'Ave Pa'anga Pau`) as a plausibility check on the historical file, not a
  verification of C2 itself. The ~1.4% gap between NRBT's mid rate and the bank's actual
  transacted rate is consistent with an ordinary bank margin, but that's an interpretation, not
  a proven explanation.
- **`report_failures.py` is untested against a real failure** — this round's one live run
  succeeded, so the "no failures" path is exercised; the failure-reporting path itself has not
  been observed against a genuine `availability_status = error` row from a live run.
- **The sweep's "bot-management infrastructure present but did not challenge" reading is based
  on headers and cookies (Incapsula/Akamai/Cloudflare fingerprints), not on knowing those
  vendors' actual decision logic.** It's possible some of these requests were one lucky roll
  each — a bot-management product can decide per-request, per-session, or per-IP-reputation, and
  none of that is visible from one fetch. Treat "didn't challenge this time" as exactly that, not
  as "never challenges."
- **The sweep checked one URL per candidate, not the whole site.** A candidate marked "no target
  numbers in raw bytes" on the specific page checked could still have a server-rendered rate
  somewhere else not looked at — this happened once already this round (ANZ NZ's fee page is
  open even though its rate page isn't), so it's a real, not hypothetical, risk.
- **OrbitRemit's AUD→TOP/AUD→FJD rate-in-meta-description pattern was checked on two pages; it
  was not confirmed whether this holds for its other currency pairs or whether the specific
  meta-description mechanism is stable over time** (it reads like an SEO artefact of whatever
  templating framework renders the page, which could change without notice).
- **The `verification_method` classification for the 25 `PROVIDERS.md` rows not touched this
  round is a judgement call, not a fresh check.** Rows kept as `raw_fetch` from Round 1 evidence
  (MoneyGram, KlickEx, Pacific Way, WanTok Money, TransCrypt) earned that label because their
  determining fact was a protocol-level observation (a robots.txt disallow, a TLS mismatch, a
  DNS failure, an HTTP status) rather than WebFetch's content parsing — this is a real
  distinction, but it was applied by re-reading Round 1's evidence files this round, not by
  re-fetching them.

---

## 10. Recommended next round

**The open question is now architectural, not a provider pick.** §5.1's sweep found the real
constraint on Tier 1 is that most bank rate tables are client-rendered, not that banks block
honest collectors — Kiwibank's widget and OrbitRemit's meta-description rate are the only two
of eleven checked (across both rounds) with any structural path to a server-rendered number.
Before Task A resumes, this needs a decision, not another candidate swap:

- **Option 1 — chase the client-side data endpoint.** Kiwibank's `data-rate="240"` reads like a
  lookup key into a small API; discovering and calling that endpoint directly is still "boring"
  (a static request, no browser) but is real engineering, not triage, and it's untested whether
  the endpoint itself sits behind its own access control. Worth a scoped, time-boxed attempt
  before ruling it out.
- **Option 2 — accept Tier 1 is rarer than assumed and lower the bar for Session 4.** Build
  against OrbitRemit's genuinely server-rendered rate as a Tier 2 (`public_quote`) connector
  instead of a Tier 1 tariff reconstruction — but note it only reaches AU→Tonga, not NZ→Tonga,
  reopening the origin-country question from Round 1 §5.1 a second time, and changes Session 4's
  own "Tier 1 first, because tariffs are stable" rationale.
- **Option 3 — re-scope what "published tariff" means for a bank in practice.** If most banks'
  rate tables genuinely require an endpoint call rather than a page read, `PROVIDERS.md`'s Tier
  1 definition (or the collection-method taxonomy in `docs/METHODOLOGY.md` §3) may need a
  documented middle category — a rate reconstructed from a discovered API rather than a rendered
  page — rather than treating that as either Tier 1 or Tier 2 by fiat.

No recommendation pressed among these — this is exactly the kind of design call the maintainer's
own instruction this round said belongs to them.

**Whatever is decided, before it's built:** fetch it fresh and honestly first, in writing,
before committing to it anywhere else — this round's whole premise (don't trust a claim about
what's fetchable without a raw check) applies to every future candidate, not just the ones that
already failed.

**Deliberately left undone this round:**
- No third connector, no other provider touched, per the brief.
- The MoneyGram/robots.txt conflict (§5.2) — unchanged, not this round's concern.
- The historical file was assessed, not imported — a real import needs the reshape work and the
  stray-date handling noted in §3.3, and should be its own dated backfill with its own
  `collection_run_id`, never presented as same-day collection.
- `report_failures.py`'s GitHub-issue-opening half of the repair loop (CLAUDE.md §4.1) — still a
  stub, deliberately, until there's a real failure to design it against.
- Running the test suite and pipeline under Python 3.12 to match CI exactly.
