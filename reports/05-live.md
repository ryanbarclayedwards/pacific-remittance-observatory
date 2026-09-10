# Round 5 — safety audit, three decisions, and getting ready to run live

**Date:** 2026-09-10
**Scope:** a safety audit of `hm-ds/` before the repository goes public; three maintainer
decisions on Round 4's open questions (benchmark carry-forward, E2, the benchmark-sensitivity
finding); then Round 5 proper — safety audit and remote readiness (Task A), CI verification
(Task B), three consecutive scheduled runs (Task C), and exercising the failure path once
(Task D).

**Explicitly out of scope:** a third connector. No remote was added and nothing was pushed —
the maintainer explicitly held that until the `hm-ds/` question was settled, and it still is:
the maintainer is moving the folder; the remote URL hasn't arrived yet. This report follows
`docs/REPORTING.md` and assumes no memory of this session.

**Outcome in one line:** the safety audit is clean — `hm-ds/` never entered git history, nothing
to rewrite — and only two specific files under it (`audit1.csv`, `audit2.csv`) are read by any
code in this repository. Three decisions recorded and implemented (benchmark carry-forward
policy + schema, E2 closed, the benchmark-sensitivity finding documented as a quantified
property). Task D found and fixed a real, previously-invisible failure mode: a total connection
failure produced zero rows, not an error row — fixed, tested, exercised live, reverted cleanly.
**Tasks B and C are blocked on the remote and could not run this round** — see §5.1, which
answers this report's required question directly: the collector is not yet running unattended on
any schedule.

---

## 2. What I did

1. Read `reports/04-historical.md` in full, then ran the safety audit before anything else, per
   the brief's explicit ordering:
   - `git log --all --oneline -- hm-ds/` — empty.
   - `git rev-list --objects --all | grep -i hm-ds` — empty.
   - Also checked for any `.dta` file or a bare `audit1.csv`/`audit2.csv` ever entering git
     history outside the archived envelope — none found. `hm-ds/` never touched git history at
     any point, not even transiently. **No history rewrite is needed.**
   - Searched all of `collect/` and `tests/` for any reference to `hm-ds` — found exactly one:
     `collect/ingest_2023_audit.py`'s `HM_DS_DATA = REPO_ROOT / "hm-ds" / "Data"`, narrowed by
     the script's own `WAVES` dict to precisely `audit1.csv` and `audit2.csv`. Nothing else
     under `hm-ds/` (the `.dta` files, the `.do` files, `Result/`, `Simulation.xlsx`,
     `Myfile.doc`) is read by any code in this repository.
2. Recorded three maintainer decisions before touching pipeline code:
   - **Benchmark carry-forward**: `schema/observation.schema.json` v0.2→v0.3 adds
     `benchmark_is_carried_forward` and `benchmark_age_days`. `CLAUDE.md` §1.1 gained a narrow,
     explicit exception to its own "never carry a value forward" rule — benchmark only, never a
     provider's own quote, never silent.
   - **E2 closed**: `docs/METHODOLOGY.md` §2.2 now states the resolved rule (per-observation,
     never inferred, null when unstated) with the Western Union Cash counter-example as the
     proof it's necessary, not just cautious. `CLAIMS.md` E2 marked resolved.
   - **Benchmark-sensitivity finding recorded**: `docs/METHODOLOGY.md` §2.3 (v0.4→v0.5) now
     documents, with Round 4's actual numbers, that benchmark choice moves cost *levels* by
     ~0.44pp on average while leaving *rankings* 99.8% undisturbed.
   - `CLAIMS.md` C3 also got the provenance note the maintainer asked for.
3. Round 5 Task D, done first among the round's own tasks since it needed no remote: tested
   what a genuine connection failure (DNS lookup failure) actually does. Found it propagated as
   a raw, uncaught exception all the way to `collect/run.py`'s outer `try/except`, which kept
   the overall run alive but silently produced **zero observations** for that connector — not
   an `availability_status = "error"` row, contradicting `.github/workflows/collect.yml`'s own
   stated design. Fixed it properly (see §3.3), then ran the actual live test the brief asked
   for: pointed OrbitRemit at a deliberately nonexistent domain, ran the real pipeline, watched
   it produce a proper error row and a visible failure report, then reverted the URL and
   re-ran to confirm normal operation resumed. Nothing broken was committed; only the fix and
   the two confirming (real, clean) runs were.
4. Added a heartbeat fallback to `.github/workflows/collect.yml` (Task C's G2 sub-question):
   G1/G2 remain genuinely undocumented from GitHub's own docs (Round 1's finding, unchanged),
   so this doesn't resolve the open question — it removes the one failure mode that would have
   made the question worse (a day with nothing to commit is also a day with no activity to test
   the 60-day clock against). Verified the bash logic in an isolated throwaway repo and that the
   YAML parses.
5. Attempted Round 5 Tasks A(remote)/B(push)/C(scheduled runs) — all explicitly held per the
   maintainer's own instruction ("do not add a remote or push until this is settled"). Confirmed
   there is still no remote configured (`git remote -v` empty) and did not add one.
6. Committed after each checkpoint: decisions → connection-error fix → live failure-path test
   (fix commit) → confirmation run → heartbeat → this report.

---

## 3. Findings

### 3.1 Safety audit — clean

| Check | Result |
|---|---|
| `hm-ds/` ever in git history | No — `git log --all -- hm-ds/` and `git rev-list --objects --all \| grep -i hm-ds` both empty |
| Any `.dta` file ever committed | No |
| `audit1.csv`/`audit2.csv` ever committed as bare files (outside the archived envelope) | No |
| Files under `hm-ds/` actually read by any code in this repo | Exactly two: `hm-ds/Data/audit1.csv`, `hm-ds/Data/audit2.csv`, referenced only from `collect/ingest_2023_audit.py` |
| Everything else under `hm-ds/` (`.dta` files, `.do` files, `Result/`, `Simulation.xlsx`, `Myfile.doc`) | Not read by any code here — safe to relocate freely |

**One practical note for the relocation:** the 2023 audit's actual *data* is already safely
inside this project's own `archive/manual-audit-2023/` (the CSV content, archived and
committed in Round 4) and `store/observations/2023-*.csv` (the 1,188 ingested observations).
`collect/ingest_2023_audit.py` only needs to find `audit1.csv`/`audit2.csv` again if it's
re-run in the future (to reproduce the import, or if the script needs a fix). Nothing about the
pipeline's current, already-committed state depends on `hm-ds/` continuing to exist where it is.

### 3.2 Decisions implemented

| Decision | Where | Status |
|---|---|---|
| Benchmark carry-forward | `schema/observation.schema.json` v0.3, `CLAUDE.md` §1.1 | Schema and policy recorded. **Implementation (actually carrying rates forward) deliberately deferred** — see §5.2 |
| E2 closed | `docs/METHODOLOGY.md` §2.2 v0.5, `CLAIMS.md` | Done — matches what every connector/importer already does |
| Benchmark-sensitivity finding | `docs/METHODOLOGY.md` §2.3 v0.5 | Done, with Round 4's actual numbers cited |

### 3.3 The connection-failure bug (Task D)

| Before | After |
|---|---|
| A DNS failure / connection refused / timeout raised out of `fetch_and_archive()` uncaught | `fetch_and_archive()` catches it, returns a `FetchResult` with `.connection_error` set |
| `collect/run.py`'s outer `except` caught the propagated exception, run continued, **connector produced 0 rows** | Both connectors check `.connection_error` first and emit a proper `availability_status = "error"` row |
| No archived artefact existed for the failure (nothing was ever received) | `archive_failure()` archives a record of the attempt itself (URL, timestamp, exception type/message) — a real artefact that resolves under `archive/`, satisfying CLAUDE.md §1.2 even though there was no response to archive |

**Live test, verbatim console output** (OrbitRemit pointed at
`https://this-domain-deliberately-does-not-exist.pro-test.invalid/rates`):
```
collect.run: 3 observation(s), 1 not 'observed'
  - orbitremit: error: connection failed fetching https://this-domain-deliberately-does-not-exist.pro-test.invalid/rates: ConnectError: [Errno 8] nodename nor servname provided, or not known
```
```
collect.report_failures: run run-20260910T004226Z-b701c340 -- 1 failure(s):
  - orbitremit: error: connection failed fetching https://this-domain-deliberately-does-not-exist.pro-test.invalid/rates: ConnectError: [Errno 8] nodename nor servname provided, or not known
```
`normalise.validate --strict` passed clean against the error row (its archived failure-record
artefact resolves correctly). Reverted the URL, re-ran: 11 observations, 0 errors — normal
operation resumed with no trace of the deliberate break left in the codebase.

---

## 4. Decisions I made

1. **Implemented carry-forward's schema and CLAUDE.md policy but not its actual logic this
   round.** *Reversible, deliberate scope discipline* — the brief's own Round 5 priority
   ("get the collector actually running... do not build another connector this round") argued
   against spending time extending connector behaviour when the round's real job was getting
   the *existing* connectors running unattended. See §5.2.
2. **Fixed the connection-failure bug as shared plumbing** (`fetch_and_archive`/
   `archive_failure` in `collect/archive.py`), not as a patch inside each connector
   individually. *Reversible in implementation, not in spirit* — every current and future
   connector gets this for free rather than needing to remember it.
3. **Archived a record of the failed attempt itself, not a placeholder hash, for a connection
   error with no response body.** *Reversible.* CLAUDE.md §1.2's "every observation traces to
   an archived artefact" doesn't have an obvious exception for "there was nothing to archive" —
   archiving the *failure* (URL, timestamp, exception) is a real, honest artefact that
   satisfies the letter and spirit of the rule rather than working around it with a fake hash.
4. **Added the heartbeat as a fallback inside the existing Commit step, not a separate always-
   run step.** *Reversible.* Keeps the common case (there's real data to commit) exactly as
   simple as before; the heartbeat only ever fires on the day it's actually needed.
5. **Did not attempt to add a remote or push**, per explicit instruction, even though Task B/C
   were the round's stated priority. *Correct, not a shortfall* — the instruction was
   unambiguous and the safety concern it was protecting against is real.

---

## 5. Decisions I did not make

### 5.1 Is the collector running unattended on a schedule, and what is the longest unbroken run of daily observations in the store?

**No, not yet.** No git remote exists for this repository (confirmed again this round:
`git remote -v` returns nothing) — the daily `collect` workflow has never executed on GitHub
Actions, scheduled or otherwise, because there is nowhere for it to run. This is unchanged from
Round 3's finding and remains blocked on the maintainer relocating `hm-ds/` and supplying the
remote URL, per this round's own explicit instruction not to proceed without that.

**Longest unbroken run of daily observations in the store: 2 consecutive calendar days**
(2026-09-09, 2026-09-10), both from **manual** runs of `python -m collect.run --all` during
this and the previous round's work — 5 distinct `collection_run_id`s across those two days, none
of them scheduled or unattended. This is real, validated data (every row passes
`normalise.validate --strict`), but it is not evidence of an unattended schedule working — it's
evidence the pipeline works when a human runs it.

**What's actually ready, so the remote/push step (once cleared) should be quick:** the workflow
YAML is syntactically valid and its bash logic is tested in isolation (§2 step 4); both
connectors handle every failure mode found so far (challenge pages, non-200 responses, total
connection failure) without crashing the run; `normalise.validate --strict` runs clean against
the full 5,972-row store. What's *not* tested is anything specific to GitHub Actions' own
environment (the Python 3.8-local vs 3.12-CI gap Round 2 flagged remains genuinely unverified,
and whether `GITHUB_TOKEN`'s default permissions actually allow the `git push` step to succeed
is untested — this repository has never pushed anywhere).

### 5.2 Benchmark carry-forward: schema is ready, the actual logic isn't built

The maintainer's decision (Round 4 §5.2) was clear that carry-forward should happen; this round
recorded the schema and the CLAUDE.md exception but did not implement the lookup logic (in
either the live NRBT connector or as a backfill pass over the existing 2017–2026 historical
data). Two things would be needed: (a) a `resolve_benchmark_rate(date, currency)` -style
function the live connector and future analysis can share, tested against synthetic weekend/
holiday gaps; (b) a decision on whether to regenerate the existing historical backfill with
carry-forward rows filled in (~2,000+ additional rows across 2017–2026) or only apply
carry-forward going forward from here. Neither was attempted this round — flagged for the next
one, once the collector itself is confirmed running.

---

## 6. Errors and anomalies

**The connection-error propagation, before the fix** — an unhandled exception surfacing all
the way to a bare Python traceback when tested directly against `fetch_and_archive()`:
```
EXCEPTION: ConnectError [Errno 8] nodename nor servname provided, or not known
```
(Caught one level up by `collect/run.py`'s own `try/except`, so the *process* never crashed —
but the *connector* produced nothing, which is the actual problem this round found and fixed.)

**The live Task D test's full failure output** (already quoted in §3.3, repeated here per
`docs/REPORTING.md`'s "quote error messages verbatim" convention):
```
collect.run: 3 observation(s), 1 not 'observed'
  - orbitremit: error: connection failed fetching https://this-domain-deliberately-does-not-exist.pro-test.invalid/rates: ConnectError: [Errno 8] nodename nor servname provided, or not known
```

**`git rev-list --objects --all | grep -i hm-ds`** — exit code 1, no output. Confirmed clean by
absence, not by a reassuring message; worth stating plainly since "no output" and "the command
failed" can look identical without checking the exit code, which was done.

---

## 7. Repository changes

| File | Change | Why |
|---|---|---|
| `schema/observation.schema.json` | Edited (v0.2→v0.3) | `benchmark_is_carried_forward`, `benchmark_age_days` added at the end of `properties` |
| `CLAUDE.md` | Edited | §1.1 gains the narrow, flagged carry-forward exception |
| `docs/METHODOLOGY.md` | Edited (v0.4→v0.5) | §2.2 E2 resolved; §2.3 carry-forward policy + benchmark-sensitivity finding, both with real numbers |
| `CHANGELOG.md` | Edited | Entry for the v0.3 schema bump and v0.5 methodology bump |
| `CLAIMS.md` | Edited | E2 marked resolved; C3 gains the ChatGPT-handover provenance note |
| `normalise/validate.py` | Edited | `benchmark_is_carried_forward` added to boolean fields; `benchmark_age_days` needs `int()`, not `float()`, for JSON Schema's `"integer"` type |
| `collect/archive.py` | Edited | `archive_failure()`, `FetchResult.connection_error`, `fetch_and_archive()` now catches connection-level exceptions instead of raising |
| `collect/benchmarks/nrbt/connector.py`, `collect/orbitremit/connector.py` | Edited | Both check `result.connection_error` first, before the existing challenge/status-code checks |
| `.github/workflows/collect.yml` | Edited | Heartbeat fallback in the Commit step; top comment updated to reflect the current, still-unresolved G2 state |
| `tests/test_archive.py` | Edited | 4 new tests: `archive_failure`'s real artefact, `fetch_and_archive`'s connection-error catch |
| `store/observations/2026-09.csv`, `archive/nrbt/...`, `archive/orbitremit/...` | Appended | Two real confirming live runs (the schema-migration append, and the post-revert normal-operation confirmation) |

No file under `archive/` or `store/` was modified after being written. The deliberately-broken
test state (the bad `SOURCE_URL`, and the observation/archive rows it produced) was never
committed — reverted and cleaned up locally before anything else touched git.

---

## 8. Claims register delta

| Claim | Before | After |
|---|---|---|
| E2 | OPEN | RESOLVED |
| C3 | REFUTED (Round 4) | Unchanged in status; gains the ChatGPT-handover provenance note |
| G1, G2 | VERIFIED (threshold) / UNCHECKED (sub-question) | Unchanged — still genuinely undocumented; the heartbeat mitigates the consequence, doesn't resolve the question |

---

## 9. Confidence flags

- **The connection-error fix was tested against exactly one failure mode** (DNS resolution
  failure, via a genuinely nonexistent domain). Other network-level failures (connection reset,
  TLS handshake failure, a timeout under load) should hit the same broad `except Exception`
  catch in `fetch_and_archive()`, but only the DNS case was actually exercised live.
- **The heartbeat's actual necessity is now lower than when Round 1 first flagged it**, since
  every connector guarantees at least one row (success or error) after this round's fix — but
  "lower" isn't "zero" (an unhandled exception inside `collect/run.py` itself, or a
  `store.append_observations` failure, could still produce a day with nothing committed), so
  the fallback stays as real, not theoretical, insurance.
- **Whether GitHub Actions' default `GITHUB_TOKEN` permissions actually allow this workflow's
  `git push` step to succeed is untested** — `permissions: contents: write` is set, which
  should be sufficient per GitHub's own documented model, but this has never been exercised
  against a real Actions run.
- **The Python 3.8-local vs 3.12-CI gap (Round 2's flag) is still completely unverified** —
  nothing written since has been checked to need a 3.9+-only feature, but that's an absence of
  known problems, not a confirmed absence of any.
- **`hm-ds/`'s safety audit checked git history and the working tree's tracked files** — it did
  not check whether any *fork*, *clone*, or other copy of this repository exists elsewhere that
  might have captured a snapshot before `.gitignore` was added. Given this repository has never
  had a remote and hasn't been pushed anywhere, this risk should be zero, but it wasn't
  independently confirmed beyond "no remote has ever existed" (§5.1).

---

## 10. Recommended next round

**Once the maintainer has relocated `hm-ds/` and supplied the remote URL:** add the remote,
push, watch the workflow's first real run on GitHub Actions, and fix whatever breaks (Round 5
Task B, not completed this round). Then let the schedule run unattended for several days to
actually answer "three consecutive unattended runs" (Round 5 Task C) — this cannot be
compressed into one session regardless of how quickly the remote arrives; it needs real
wall-clock days to pass with the cron actually firing.

**Once there's a working schedule:** implement benchmark carry-forward's actual logic (§5.2),
and decide whether to backfill it historically or only apply it going forward.

**Deliberately left undone this round:**
- No third connector, per the brief.
- Carry-forward logic itself (schema/policy only) — §5.2.
- Round 5 Tasks B and C — blocked on the remote, per explicit instruction, not a shortfall.
- Testing the connection-error fix against failure modes other than DNS resolution.
