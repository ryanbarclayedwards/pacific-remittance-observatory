# Round 6 — the repository goes public, and the collector runs unattended for the first time

**Date:** 2026-09-11
**Scope:** relocate `hm-ds/` out of the repository tree (already `.gitignore`'d, never in git
history — confirmed again this round); decide and record the `archive/` redistribution policy;
create the GitHub remote and push; watch the first Actions run and fix what breaks; build the
benchmark carry-forward resolver (Task C) as a point-of-use lookup, not a backfill; start Task
B's three-consecutive-unattended-scheduled-runs clock the moment the push succeeded.

**Explicitly out of scope:** no new connector, no new corridor, no change to the 2023 audit
data. This report follows `docs/REPORTING.md` and assumes no memory of this session.

**Outcome in one line:** the repository is public at
`https://github.com/ryanbarclayedwards/pacific-remittance-observatory`. A pre-push review found
one real problem — a file naming a real individual alongside internal negotiating strategy —
which was removed and rewritten out of history before anything was pushed. The push itself took
several failed attempts across two different authentication paths before succeeding. Once live,
the workflow's **scheduled** trigger fired and completed a full, successful, unattended run
before either of us could manually dispatch one — real evidence the two things most expected to
break (the Python 3.8-local vs 3.12-CI gap, and whether `GITHUB_TOKEN` can actually push) do not
break. **Task B's clock started at 2026-09-10 21:26:49 UTC. As at the time of writing, one
consecutive unattended scheduled run has completed** — see §5.1, which is this report's required
answer to that question.

---

## 2. What I did

1. **Pre-publication safety review**, before touching the remote. Read every tracked file
   outside `archive/`/`store/`/`scratch/` (the working set that could plausibly contain
   something written by a person rather than fetched from a provider). Found one real problem:
   `docs/outreach-emails.md` named a real individual and contained internal negotiating strategy
   about approaching him for historical data access — the maintainer confirmed this was correct
   to flag and directed removal, including from history, since nothing had been pushed yet.
   Everything else checked out: no `hm-ds/` reference anywhere, no real credentials or tokens (a
   few keyword hits in raw-fetched third-party pages — a CORS header listing `authorization` as
   an allowed header name, a bank's own public client-side analytics key, "password" inside
   login-form UI copy — none of them ours), and one low-severity absolute-local-path leak.
2. **Removed the file and rewrote it out of history**, since nothing had been pushed yet and
   this was still cheap to do correctly:
   - Copied the file's full content to two locations outside the repository tree first (a
     durable copy at `~/Desktop/pacific-remittance-observatory-private/outreach-emails.md`, plus
     a session-scratch backup), and verified both byte-identical before removing anything.
   - Removed it from the working tree and committed the removal.
   - Installed `git-filter-repo` locally via `pip3` (not available via Homebrew in this
     environment; this is a one-time local tool for the history rewrite, not a project
     dependency) and ran it to strip the file from every commit.
   - Verified clean by exit code, not by eyeballing output: `git log --all --oneline --
     docs/outreach-emails.md` (exit 0, no output) and `git rev-list --objects --all | grep -i
     outreach` (exit 1, no match).
   - Added `docs/outreach-emails.md` and `docs/private/` to `.gitignore` so the same class of
     file can't be re-added by accident.
3. **Scanned the rest of the tree for the same class of problem** (named individuals outside a
   published citation; internal-strategy language). Found nothing else — the only other mention
   of the same company name is `CLAIMS.md`'s existing A14 entry, which cites a public review's
   own footnote for who ran a programme, not the individual or any strategy content.
4. **Fixed the absolute-local-path finding**: `collect/ingest_2023_audit.py`'s `HM_DS_DATA` no
   longer hardcodes `/Users/ryanbedwards/...`. It now defaults to `~/Desktop/hm-ds/Data` via
   `Path.home()` (no username baked into the source) and can be overridden with
   `HM_DS_DATA_PATH`. `reports/04-historical.md` was left untouched, per the maintainer's own
   instruction — a report is a historical record of what actually ran, not something rewritten
   to look tidier in hindsight.
5. **Wrote `docs/PRE-PUBLICATION-CHECK.md`**, turning the review just performed into a
   repeatable checklist (named individuals, internal strategy content, credentials/tokens,
   absolute paths, unrelated data, a documented history-rewrite procedure, push-target
   verification), and referenced it from a new `CLAUDE.md` §1.8. Re-ran every check clean before
   proceeding.
6. **Added the remote and attempted the first push.** This took substantially more than one
   attempt, split across two different authentication paths — full detail in §3.2, since the
   specific failures and their fixes are themselves a finding worth recording accurately, not
   just summarising as "eventually worked."
7. **The maintainer completed the push independently**, after switching from a token-based
   attempt in this session to their own terminal (installing Homebrew, then `gh` directly from
   GitHub's release `.pkg` after `brew install gh` failed to build, then `gh auth login`'s
   browser flow). They also found a second, independent cause behind some of the earlier
   failures: they had been typing the local macOS account name (`ryanbedwards`) where their
   GitHub username (`ryanbarclayedwards`) was needed. To get past the token's missing `workflow`
   scope, they held `.github/workflows/collect.yml` back from the first push (`git rm --cached`,
   committed as "temp: hold workflow back from initial push") and pushed everything else.
8. **Verified the resulting repository state** was exactly what the maintainer described:
   working tree and index clean, `origin/main` at the "temp: hold workflow back" commit, local
   `main` matching it exactly. Restored `collect/ingest_2023_audit.py`'s path fix onto that base
   (it had been part of local work not yet reflected upstream) and re-added
   `.github/workflows/collect.yml` to tracking in its own commit, without pushing — the same
   token would reject it for the same reason.
9. **Printed the workflow file's contents once, then stopped doing that.** The maintainer
   reported their terminal was corrupting long output mid-line — on that printed file, and
   separately on a later long status summary that wasn't a file print at all. Going forward,
   anything long and verbatim goes to a file with a path given, not into the terminal directly.
10. **The maintainer created `.github/workflows/collect.yml` directly via GitHub's web UI**,
    copying from the local file via `pbcopy` rather than from anything printed to the terminal —
    sidestepping the token's scope restriction entirely. Verified afterwards: exactly one copy
    at the correct path, byte-identical to the local file, nothing stray from GitHub reporting
    the file "already existed" on a retried creation attempt.
11. **`git pull` merged cleanly** — both branches had added the same file with identical
    content, so git resolved it automatically with no conflict.
12. **Found the workflow had already run, unprompted, via its scheduled trigger**, before either
    of us could manually dispatch one. Checked the run via GitHub's public Actions API: event
    `schedule`, conclusion `success`, every step succeeded, a real (non-heartbeat) collection
    landed. Full detail in §3.3. The maintainer agreed this satisfied Task A more strongly than a
    manual dispatch would have, since the scheduled path is the one that has to work unattended.
    Task B's clock was set from this run's completion time.
13. **Pushed the three commits that had accumulated locally** (the merge, the workflow-tracking
    restoration, and a `CLAIMS.md` entry recording the machine-default git identity on the
    commits made before one was configured) — succeeded on the first attempt, confirming the
    earlier failures were specifically about the `workflow`-scoped file, not push access in
    general.
14. **Recorded the cron-drift finding**: the scheduled run's actual start time against its
    configured target, as a `CLAIMS.md` entry and a `docs/METHODOLOGY.md` v0.6→v0.7 freshness
    note, with the accompanying `CHANGELOG.md` migration entry `CLAUDE.md` §1.6 requires.
15. **Ran the full local test suite** (Python 3.8; `pytest` and the rest of `requirements.txt`
    were not yet installed in this local environment and needed installing first) — 50/50 pass.
16. Wrote this report.

---

## 3. Findings

### 3.1 Pre-publication review — one real finding, otherwise clean

| Check | Result |
|---|---|
| Named individuals / internal strategy content | **One finding**: `docs/outreach-emails.md` named a real individual and contained internal negotiating strategy about him. Removed and rewritten out of history (§2.2–2.3). Nothing else found outside a legitimate published citation |
| `hm-ds/` in git history | No — confirmed again this round, unchanged from Round 5 |
| Credentials/tokens in tracked files | No real ones. A handful of keyword matches in raw-fetched third-party page content (a CORS header naming `authorization` as an allowed header, a bank's own public client-side analytics key, "password" inside login-form UI copy) — all third-party, all benign |
| Absolute local paths | One: `collect/ingest_2023_audit.py`. Fixed (§2.4). `reports/04-historical.md` also has one, left as-is deliberately |
| Push target | `https://github.com/ryanbarclayedwards/pacific-remittance-observatory.git` — confirmed to match exactly before every push attempt |

### 3.2 The push — what actually failed, in order

Two separate authentication paths were tried; both eventually hit real, distinct problems, not
the same problem twice.

**This session's attempt (personal access token):**

| Attempt | Result |
|---|---|
| `git push` with no credentials configured | `fatal: could not read Username for 'https://github.com': Device not configured` — no stored GitHub credentials in the configured `osxkeychain` helper, no SSH key present |
| PAT via a one-off inline credential helper (token never written to `.git/config`) | `error: RPC failed; HTTP 400 curl 22` / `fatal: the remote end hung up unexpectedly`, repeated |
| Confirmed the token itself was valid and the repo existed (`GET /user`, `GET /repos/...` both `200`) | Ruled out an invalid token or wrong repo name |
| Forced `http.version=HTTP/1.1`; forced `protocol.version=1` | Same HTTP 400, unchanged |
| Raised `http.postBuffer` to `524288000` and pushed with `--no-thin` | **The RPC/400 problem went away.** Root cause not conclusively isolated (the repository is only 3.3MB, so this wasn't a payload-size problem in the usual sense; likely an interaction between this machine's old bundled git (2.24.3) and GitHub's HTTP transport) |
| With that fixed, the push reached a real, different rejection: `refusing to allow a Personal Access Token to create or update workflow .github/workflows/collect.yml without workflow scope` | The token lacked the `workflow` scope GitHub requires for any push touching a file under `.github/workflows/`. This is the trouble spot the brief predicted, just surfaced after clearing an unrelated transport problem first |

At this point the maintainer chose to authenticate independently rather than regenerate the
token in this session.

**The maintainer's own terminal, completed independently:**

- `brew install gh` failed — the local Command Line Tools are too old to build Go from source.
- Installed `gh` from GitHub's release `.pkg` directly instead, then `gh auth login` (browser
  flow).
- Found a second, unrelated cause behind some earlier failures: entering the local macOS account
  name (`ryanbedwards`) instead of the actual GitHub username (`ryanbarclayedwards`) when a
  prompt asked for one.
- Pushed successfully, holding `.github/workflows/collect.yml` back from that first push (same
  `workflow`-scope limitation) via `git rm --cached` and a `.gitignore` change made ready to
  commit that removal, then recovered a subsequent staging-area mistake with `git reset`.
- **Note on the maintainer's own account of this step**: they described adding
  `.github/workflows/collect.yml` to `.gitignore` as part of the hold-back commit. The commit
  actually pushed (`022893a`, "temp: hold workflow back from initial push") contains only the
  file's removal — no `.gitignore` change. Recorded as a minor discrepancy between the intended
  and actual state, not something requiring correction (the practical result — the file untracked
  and off the remote — was the same either way, and `.gitignore` was addressed separately for
  the privacy removal in §2.2).

**A live credential was pasted directly into this session's chat** (a personal access token) so
that this session could attempt the push on the maintainer's behalf. That attempt failed for the
reasons above rather than succeeding, but the token was live and valid for a period regardless.
Recommended to the maintainer at the time: revoke it once no longer needed, now that
authentication runs through `gh auth login` instead.

### 3.3 The scheduled run that beat us to it

The workflow's first execution was not the manually-dispatched run either of us was about to
trigger — it was the scheduled `cron` trigger, firing on its own before we got there.

| Field | Value |
|---|---|
| Run ID | `34532136518` |
| Trigger | `schedule` (not `workflow_dispatch`) |
| Cron target | `0 19 * * *` (19:00 UTC) |
| Actual start | 2026-09-10 21:25:49 UTC — **2h26m late** |
| Completed | 2026-09-10 21:26:49 UTC (about 1 minute of actual runtime) |
| Conclusion | `success` |

Every step in the job succeeded: checkout, Python 3.12 setup, `pip install -r requirements.txt`,
Collect, `normalise.validate --strict`, Commit (the `GITHUB_TOKEN` push), Report failures (no
issue opened — nothing to report). It was a **real collection**, not the heartbeat fallback: two
new archive artefacts (`archive/nrbt/2026/09/10/735c0ffd...json.gz`, 11,238 bytes;
`archive/orbitremit/2026/09/10/c8e3eda2...json.gz`, 31,902 bytes) and real rows appended to
`store/observations/2026-09.csv` (43,567 → 54,315 bytes), committed by the identity the
workflow's own Commit step sets: `pro-collector <noreply@devpolicy.org>`.

This is the first direct evidence against the two problems the brief specifically expected:
Python 3.8-local vs 3.12-CI produced no divergence (confirmed independently in §3.4 too), and
`GITHUB_TOKEN`'s default `contents: write` permission was sufficient for the Commit step's push
— for files outside `.github/workflows/`, which is a separate, narrower restriction (§3.2), not
the general push-permission question the brief was worried about.

### 3.4 Local test suite

Run this round, on the local Python 3.8 environment (after installing `pytest` and the rest of
`requirements.txt`, none of which had been installed locally before now): **50/50 tests pass.**
Combined with §3.3's clean Python 3.12 CI run, this is now two independent confirmations that
the Python 3.8/3.12 gap flagged since Round 2 has produced no actual divergence — still not a
guarantee against a future one, but no longer a completely untested risk.

### 3.5 The carry-forward resolver (Task C)

`collect/benchmark_lookup.py`: `resolve_benchmark_rate(target_date, currency, published_rates)`
is a pure function (no I/O) that walks backward up to 10 calendar days to find the most recent
published NRBT rate for a given date/currency, returning a `BenchmarkResolution` (`rate`,
`is_carried_forward`, `age_days`, `source_observation_id`, `source_date`) or `None` if nothing
resolves within the window. `load_published_rates_from_store()` builds its input from the real
store CSVs. **Carry-forward is derived at the point of use only — nothing is written back to
`store/`.** This settles Round 5 §5.2's open backfill-vs-forward-only question, not just defers
it again: the store holds only what NRBT actually published, permanently; carry-forward is a
lookup-time convenience, never a stored fact. 7 new tests cover a direct match, a single-day and
a full-weekend carry-forward, independent resolution per currency, the lookback window being
exhausted, never chaining through an already-carried-forward value, and the store-loader's
date-field preference. Not yet wired into the live NRBT connector's own output — the module and
its tests exist as shared plumbing any future caller (the connector, or a `cost_pct` analysis
joining provider quotes to a benchmark) can use; the maintainer accepted this as Task C
delivered without requiring that wiring this round.

---

## 4. Decisions I made

1. **Preserved `docs/outreach-emails.md`'s content outside the repository before removing it,
   rather than just deleting it.** *Reversible* — the maintainer said the content has ongoing
   value; deleting it outright would have destroyed something with no clear need to.
2. **Used `git-filter-repo`, installed locally via `pip3`, rather than `git filter-branch`.**
   *Not reversible after the fact in the sense that matters* — a history rewrite is exactly the
   kind of thing to get right the first time. `filter-repo` is what upstream git itself now
   points people toward; `filter-branch` is slower and easier to get subtly wrong.
3. **Verified the history rewrite by exit code, not by reading output.** *N/A — a verification
   method, not a change.* `git log --all -- <path>` printing nothing looks identical whether the
   command succeeded with no matches or failed outright; only the exit code distinguishes them,
   and only the exit code was actually checked.
4. **Did not touch the commits already public with the machine-default author identity.**
   *Reversible in principle, deliberately not exercised* — this was the maintainer's own explicit
   call (§5 below), not something decided unilaterally.
5. **Set git identity repo-locally, not globally.** *Reversible.* Scopes the fix to this project
   without touching the maintainer's configuration for any other repository, which nothing in
   the brief asked for.
6. **Treated the already-completed scheduled run as satisfying Task A**, rather than insisting on
   also triggering `workflow_dispatch` once `gh` wasn't available in this session's own shell.
   *Not my call to make unilaterally, and wasn't made unilaterally* — put to the maintainer as a
   recommendation with the reasoning (a scheduled success is stronger evidence than a manual one,
   since scheduled is the path that has to work unattended); they agreed explicitly before Task
   B's clock was started.
7. **Started Task B's clock at the scheduled run's completion time (2026-09-10 21:26:49 UTC),
   not at whatever moment this report happens to be written.** *Reversible if wrong, but
   shouldn't be* — that timestamp is the actual, verifiable moment the workflow first ran
   unattended and succeeded; using it (rather than "now") keeps the three-day count honest
   against a real event instead of a conversational one.

---

## 5. Decisions I did not make

### 5.1 How many consecutive unattended scheduled runs have completed, and what is the longest unbroken run of daily observations in the store?

**One consecutive unattended scheduled run has completed as at the time of writing** — run
`34532136518`, 2026-09-10, described fully in §3.3. This report is being written only hours
after that run, so this number is expected to still be low; it is not yet the three consecutive
runs Task B is watching for, and won't be reachable inside this session regardless of anything
done from here — the remaining wait is genuinely wall-clock, one scheduled run per day, and this
round's work on it stops here by design (see §10).

**Longest unbroken run of daily observations in the store: 2 consecutive calendar days**
(2026-09-09, 2026-09-10) — numerically unchanged from Round 5's finding, but no longer built
entirely from manual runs: 2026-09-10 now includes one unattended, scheduled collection among
its several `collection_run_id`s for that date. The streak length itself won't extend until a
scheduled run lands on a *new* calendar day (2026-09-11 UTC or later) with no manual run already
covering it.

### 5.2 Whether to regenerate the token used this session with `workflow` scope, or continue on the maintainer's `gh` authentication going forward

Not decided this round, and not this session's call — the maintainer chose to stop attempting the
token route for tonight and authenticate independently instead, which they completed. Whether to
go back and add `workflow` scope to the original token (making it fully capable, including for
future workflow-file changes pushed from this session) or to rely on `gh auth login` exclusively
going forward is an open, low-stakes housekeeping question, not blocking anything — the workflow
file is now on the remote either way (§2.10). **Recommendation**: rely on `gh` going forward, and
revoke the original token (raised already at the time it was pasted into this session, §3.2) —
one fewer live credential to track, and `gh`'s browser-based auth doesn't have the scope-omission
failure mode that caused most of this round's push friction.

---

## 6. Errors and anomalies

**The RPC/400 push failure**, verbatim, before the `http.postBuffer` fix:
```
error: RPC failed; HTTP 400 curl 22 The requested URL returned error: 400
fatal: the remote end hung up unexpectedly
fatal: the remote end hung up unexpectedly
Everything up-to-date
```
The trailing "Everything up-to-date" alongside two "remote end hung up" failures on the same
invocation was not fully explained — plausibly an artefact of git retrying part of the push
negotiation internally. Not investigated further once the fix (`http.postBuffer` +
`--no-thin`) made the problem go away; flagged here rather than asserted as understood.

**The workflow-scope rejection**, verbatim:
```
! [remote rejected] main -> main (refusing to allow a Personal Access Token to create or update workflow `.github/workflows/collect.yml` without `workflow` scope)
```

**`brew install gh` failure**, as the maintainer reported it: the local Command Line Tools are
too old to build Go from source. Exact error text not captured in this session, since it ran in
the maintainer's own terminal — reported here as a fact relayed, not independently verified.

**Terminal output corruption**, reported by the maintainer twice this round: once on a long file
print (a YAML workflow file, arriving with fragments like "pip install -r r" and "git config
user.ema"), once on a long prose status summary with no file content at all (fragments like "I
can't trigger workflow_disp"). Confirmed by the maintainer to be a rendering issue on their end,
not a content problem — the same file, read back from disk, was correct. No longer relevant to
future rounds' correctness, but relevant to *how* future rounds should deliver anything long:
write it to a file, give the path, keep terminal replies short.

---

## 7. Repository changes

| File | Change | Why |
|---|---|---|
| `docs/outreach-emails.md` | Removed; rewritten out of git history | Named a real individual alongside internal negotiating strategy — §2.2–2.3 |
| `.gitignore` | Edited | Adds `docs/outreach-emails.md`, `docs/private/` |
| `collect/ingest_2023_audit.py` | Edited (twice: `hm-ds/` relocation path, then the absolute-path fix) | `HM_DS_DATA` now defaults to `~/Desktop/hm-ds/Data` via `Path.home()`, overridable via `HM_DS_DATA_PATH` — no hardcoded username |
| `docs/PRE-PUBLICATION-CHECK.md` | Created | Turns this round's pre-push review into a repeatable checklist |
| `CLAUDE.md` | Edited | New §1.8 references the checklist |
| `docs/METHODOLOGY.md` | Edited (v0.5→v0.6→v0.7) | v0.6: archive publication decision (new §8). v0.7: §4 freshness gains the cron-drift finding |
| `README.md` | Edited | New "What's in `archive/`" section, public-facing statement of the publication decision |
| `CLAIMS.md` | Edited (G5, G6, G7 added) | Full Disk Access constraint; machine-default git identity on pre-`23e4627` commits; cron-drift measurement |
| `CHANGELOG.md` | Edited | Migration notes for every schema/methodology/policy change this round |
| `collect/benchmark_lookup.py` | Created | `resolve_benchmark_rate()` and `load_published_rates_from_store()` — Task C |
| `tests/test_benchmark_lookup.py` | Created | 7 tests for the resolver |
| `scratch/round-06/demonstrate_carry_forward.py` | Created | Standalone demonstration script for the resolver, evidence-only |
| `.github/workflows/collect.yml` | Removed from tracking, then restored | Held back from the first push (missing token scope), then re-added; created independently on the remote via GitHub's web UI; reconciled by `git pull`'s automatic merge |

No file under `archive/` or `store/` was modified after being written — the only changes there
this round were the scheduled run's own append (`archive/nrbt/...`, `archive/orbitremit/...`,
`store/observations/2026-09.csv`).

---

## 8. Claims register delta

| Claim | Before | After |
|---|---|---|
| G5 | (new) | REFUTED — Full Disk Access blocks reads under `~/Desktop` despite `stat`/`ls` succeeding |
| G6 | (new) | PARTIALLY TRUE — pre-`23e4627` commits on `origin/main` carry a machine-default author; left as-is by maintainer decision |
| G7 | (new) | REFUTED — GitHub's scheduled trigger fired 2h26m after its configured target on its first run |
| G1, G2 | Unchanged | Still genuinely undocumented from GitHub's own docs; G1/G2 themselves untouched this round |

---

## 9. Confidence flags

- **The RPC/400 fix's root cause is not conclusively identified** (§6) — raising
  `http.postBuffer` and using `--no-thin` made the symptom disappear, but why this machine's git
  2.24.3 needed that against a 3.3MB repository wasn't traced further.
- **The `brew install gh` failure and its exact error text come from the maintainer's own
  report**, not from anything run or observed in this session — relayed, not independently
  verified.
- **`docs/outreach-emails.md`'s hold-back-commit discrepancy** (§3.2): the maintainer described a
  `.gitignore` change as part of that commit; the commit itself shows only the file removal. Low
  stakes (practical outcome was identical either way) but worth flagging since it's a case of the
  maintainer's own account not matching the verified git history exactly.
- **`resolve_benchmark_rate()` is tested but not yet exercised against the live NRBT connector's
  actual output** — its 7 tests use constructed and store-loaded lookups, not a run through the
  connector's own current code path.
- **One scheduled run is a single data point.** §3.3's clean result (no Python-version issue, no
  push-permission issue) is real evidence, but one run is not yet enough to rule out an
  intermittent problem that a second or third run could still surface — which is exactly what
  the remaining wall-clock wait in §5.1 is for.
- **The cron-drift measurement (G7) is a single data point too** — 2h26m late on this one run.
  Framed in `METHODOLOGY.md` as "expect drift, don't assume a fixed time," not as "expect
  approximately 2h26m of drift every day," since nothing yet shows the delay is consistent.

---

## 10. Recommended next round

**For the remainder of Task B's wall-clock wait**: watch, don't build. Check whether the
schedule fires again on 2026-09-11 UTC and 2026-09-12 UTC, whether each run lands a real
`collect:` commit (or an honest heartbeat if there's nothing to commit), and whether anything in
the Actions environment produces output that differs from local in a way that matters — none of
which can be compressed faster than the days actually passing.

**Once three consecutive unattended runs are confirmed**: decide whether `resolve_benchmark_rate()`
should be wired into the live NRBT connector's own output (so a benchmark-dependent field the
connector writes is carry-forward-aware automatically) or stays a library any future analysis
calls directly — not decided this round, and not urgent while Task B is still the priority.

**Housekeeping, low priority**: the `workflow`-scope-vs-`gh`-auth question (§5.2); whether to
revoke the personal access token pasted into this session, if not already done.

**Deliberately left undone this round, per the brief:**
- No new connector.
- No new corridor.
- The 2023 audit data was not touched.
- `resolve_benchmark_rate()` was not wired into the live connector — built as shared plumbing
  only, accepted as such.
- The historical 2017–2026 benchmark series was not regenerated with carry-forward rows — by
  design, permanently, not just this round (§3.5).
