# Round 3 — endpoint discovery and a closed corridor

**Date:** 2026-09-09
**Scope:** two rulings from the maintainer recorded first (what is/isn't a workaround; Tier 1
redefined by reachability, not markup); a corridor policy recorded (provider survives first,
corridor follows); then three tasks — time-boxed raw-page-source endpoint discovery for
Kiwibank and OrbitRemit (Task A), a fallback Tier 2 connector for OrbitRemit if Task A yields
nothing (Task B), and challenge detection built into the shared fetch path (Task C).

**Explicitly out of scope:** any browser, any retry past a hard-stop condition, any endpoint
discovery beyond Kiwibank and OrbitRemit. This report follows the structure in
`docs/REPORTING.md` and assumes no memory of this session — including no memory of Round 2,
which is summarised here only where directly relevant.

**Outcome in one line:** Task A hard-stopped for both candidates (no discoverable endpoint from
page source), but the search itself surfaced a genuinely server-rendered comparison table on
OrbitRemit's page. Task B built against it: a Tier 2 `public_quote` connector for 500 AUD →
TOP. Task C is done and wired into every connector. Combined with a generalised NRBT benchmark
connector now emitting an AUD leg, **the cost measure closes end to end for AU→Tonga, 500 AUD,
via OrbitRemit: cost_pct = −2.42%, computed entirely from archived, schema-validated bytes** —
see §5.1.

---

## 2. What I did

1. Read `reports/02-connectors.md` in full, then recorded three maintainer rulings before
   touching any code:
   - **CLAUDE.md §1.5** gained a verbatim "what is and is not a workaround" clause: calling a
     page's own public JSON/XHR endpoint is not a workaround and is preferred over rendering
     the page; clearing a challenge, spoofing identity, or using an extracted credential still
     is, always; two conditions stop it regardless (robots.txt disallow, or a required
     key/token/session).
   - **CLAUDE.md §3 and `PROVIDERS.md`'s Tier definitions** redefined: Tier 1 means "reachable
     without defeating anything," not "server-rendered markup." Two `collection_method` values
     now sit under it — `published_tariff` and the new `client_api` — added to
     `docs/METHODOLOGY.md` §3 (v0.2→v0.3, `CHANGELOG.md` entry).
   - **`SPRINT-01.md`**: the corridor stops driving provider selection. Whichever provider
     survives this round's work sets the corridor; Tonga is preferred only as a tie-breaker
     because NRBT is already built, not for any other reason. Recorded so it isn't relitigated
     a third time.
2. Built Task C first (shared plumbing, so Task A/B's connectors get it for free):
   `collect/archive.py` gained `detect_challenge()` and `fetch_and_archive()`, a combined
   fetch→hash→archive→challenge-check helper. Markers are deliberately narrow, built only from
   what Round 2's sweep actually observed (Incapsula/Cloudflare/Akamai interstitial phrases),
   specifically avoiding the false-positive-prone generic words ("captcha," "blocked," an Akamai
   *hostname*) Round 2 found in genuine pages. Golden test runs the positive case against the
   real Incapsula challenge page ANZ NZ served in Round 2, plus four negative cases built from
   Round 2's actual false positives.
3. Refactored the NRBT connector to use `fetch_and_archive()` so it gets challenge detection
   automatically. Re-ran the live pipeline to confirm nothing broke.
4. Ran Task A: inspected Kiwibank's and OrbitRemit's already-fetched Round 2 page bodies (no new
   fetch for the HTML itself) for the rate widget's data source, plus one further honest fetch
   each where a linked asset needed checking (Kiwibank's JS bundle). Both hard-stopped for a
   true API endpoint — full account in `scratch/round-03/`.
5. OrbitRemit's search surfaced a full server-rendered comparison table (AUD amounts against
   TOP received amounts) already embedded in the page's own Next.js streaming payload — not an
   endpoint, genuinely part of the raw HTML. Built Task B against it:
   `collect/orbitremit/connector.py`, Tier 2 `public_quote`, using the 500 AUD row.
6. Generalised the NRBT connector to emit one observation per configured origin currency (NZD
   and AUD, both already on the page it parses) rather than hardcoding NZD — needed once the
   corridor stopped being fixed to NZ→Tonga.
7. Ran the live pipeline: 3 new observations (NRBT/NZD, NRBT/AUD, OrbitRemit/AUD), all valid.
   Computed `cost_pct` by hand from the two same-run AUD-side rows — it closes. See §5.1.
8. Attempted the housekeeping push to trigger CI for the first time — blocked, no git remote
   exists for this repository yet. Flagged rather than worked around; see §5.2.
9. Committed after each checkpoint: rulings → Task C → Task A evidence → Task B → this report.

---

## 3. Findings

### 3.1 Task A — endpoint discovery: two hard stops, one useful byproduct

| Candidate | Endpoint found? | What was checked | Byproduct |
|---|---|---|---|
| Kiwibank | **No — hard stop** | Every `<script>` tag on the page; fetched the one linked JS bundle (`media.kiwibank.co.nz/static/js/index.js`, 595,795 bytes) and searched it for `richtext-rate`/`data-rate`/`/rate`/`/fx` path strings — zero hits for the widget's own class name. No wrapping `data-endpoint` attribute near the markup either. | Confirmed the currency→id mapping is stable across Round 1 and Round 2 fetches (TOP=240), but that's all — no path to the live number. |
| OrbitRemit | **No — hard stop, for a true endpoint** | Absolute- and relative-URL scan of the page's Next.js streaming payload (`self.__next_f.push([...])` chunks) for `/api/`, `rate`, `quote`, `convert`, `fx` — found only CDN image URLs and sibling currency-converter page links. | **A full server-rendered AUD→TOP comparison table**, already in the raw HTML, no endpoint needed — see §3.2. |

Full write-ups: `scratch/round-03/kiwibank-endpoint-discovery.md`,
`scratch/round-03/orbitremit-endpoint-discovery.md`.

### 3.2 Task B — OrbitRemit connector: built, tested, run, validated

OrbitRemit's own comparison table (server-rendered, in the streaming payload):

| AUD sent | TOP received | Implied rate |
|---|---|---|
| 5 | 8.67 | 1.734000 |
| 10 | 17.34 | 1.734000 |
| 25 | 43.34 | 1.733600 |
| 50 | 86.68 | 1.733600 |
| 100 | 173.36 | 1.733600 |
| 500 | 866.82 | 1.733640 |
| 1,000 | 1,692.37 | 1.692370 |
| 5,000 | 8,296.73 | 1.659346 |
| 10,000 | 16,552.18 | 1.655218 |

Two distinct rates fit this table almost exactly: ~1.73364 TOP/AUD for the first 500 AUD, ~1.6511
beyond it — matching OrbitRemit's own advertised "promo rate for new customers, capped at the
first $500" (`scratch/round-01/orbitremit.md`). The page's `<meta name="description">` states a
third figure, "$1 AUD = 1.69237 TOP," matching neither. The connector uses the 500 AUD row —
the last one still at the promotional rate — and discloses the meta-description discrepancy in
every observation's `status_detail` rather than silently picking one number.

| Check | Result |
|---|---|
| Golden tests (`tests/test_orbitremit.py`) | 6/6 passing, offline, against the committed fixture |
| Live run | `amount_sent=500 AUD`, `amount_received=867.41 TOP` (a fresh fetch's live figure — differs slightly from the 866.82 in the fixture/table above; the underlying market rate moves between fetches, which is expected, not a bug) |
| `collection_method` | `public_quote` (Tier 2) |
| `fee` | `null` — no fee amount found anywhere in raw bytes; not assumed |
| `python -m normalise.validate --strict` | clean |

### 3.3 Task C — challenge detection: built, wired in, tested

`collect/archive.py::detect_challenge()` and `fetch_and_archive()` — see §2 step 2. Every
connector built this round (NRBT, OrbitRemit) uses `fetch_and_archive()` and gets this for free.
5/5 tests passing: the real Incapsula challenge page from Round 2 (positive), and four negative
cases built from Round 2's actual false positives (Wise's bundled "Captcha" strings, Western
Union's Akamai *hostname*, Remitly's unrelated `this.blocked` JS variable, an ordinary page).

### 3.4 NRBT connector: generalised to emit AUD alongside NZD

Same live page, same fetch, now two observations instead of one — `origin_currency` is
configurable (`NZD`, `AUD`), both already published on the page the connector parses. See §5.1
for why this mattered this round specifically.

---

## 4. Decisions I made

1. **Used the 500 AUD row from OrbitRemit's comparison table, not the 1,000 or 10,000 row.**
   *Reversible.* 500 AUD is the last row still at the advertised promotional rate — using it
   means the observation is explicitly, honestly a promotional-rate quote (disclosed as such),
   rather than picking an arbitrary larger amount that blends promotional and standard rates in
   a way the raw bytes don't cleanly decompose.
2. **Stored the *implied* rate (`amount_received / amount_sent`) as `provider_fx_rate`, not the
   page's separate meta-description figure.** *Reversible, and the alternative is defensible* —
   chose the table-derived figure because it's tied to an actual amount/received pair that can
   be checked arithmetically from archived bytes, whereas the meta-description figure is a bare
   assertion with no worked example behind it. Both are disclosed either way.
3. **Generalised the NRBT connector to emit AUD instead of building a second, separate
   AUD-specific connector.** *Reversible.* One page, one fetch, one archive artefact already
   contains both currencies' rows — a second connector would have re-fetched and re-archived
   the same page under a different name for no reason.
4. **Did not pursue Kiwibank's endpoint further than one bundle fetch** (e.g. did not try
   guessing chunk filenames or searching for a sitemap of JS assets). *Not reversible within
   this round without more time* — this is exactly the "reasonable effort, then stop" the brief
   asked for, not a shortfall.
5. **Did not attempt the housekeeping push.** *Reversible — nothing was lost, nothing was
   attempted destructively* — no git remote exists for this repository; creating one (and
   deciding where, and whether public) is a decision for the maintainer, not something to do
   unilaterally on a "housekeeping" instruction that assumed a remote already existed. See
   §5.2.
6. **Challenge-detection markers stay narrow** (a short list of strong, specific phrases) rather
   than broad (generic words like "captcha," "blocked," "denied"). *Reversible, but the
   narrowness is deliberate* — Round 2's sweep already showed broad markers produce false
   positives in genuine pages; a missed real challenge is a research gap, a false positive is a
   connector that silently stops working on legitimate content.

---

## 5. Decisions I did not make

### 5.1 Does the cost measure close end to end for at least one corridor, from archived bytes alone?

**Yes — for AU→Tonga, 500 AUD, via OrbitRemit against the NRBT benchmark.** Both legs come from
the same collection run (`collection_run_id` shared across the NRBT and OrbitRemit rows in
`store/observations/2026-09.csv`):

| Field | NRBT (benchmark) | OrbitRemit (provider) |
|---|---|---|
| `provider_id` | `nrbt` | `orbitremit` |
| `origin_currency` | AUD | AUD |
| `destination_currency` | TOP | TOP |
| `amount_sent` | 1.0 | 500.0 |
| `amount_received` / `provider_fx_rate` | 1.6937669376693767 | 867.41 |
| `collection_method` | `published_tariff` | `public_quote` |
| `raw_payload_sha256` | `d1db87b7a40ae84e1bc9cde7a90b3cc25ebbf10c0457a81d4ba6ad37e3228531` | `4dc4450175bcee3972f21a4d6f829ff29e8a2cb42a4eb157332acd03657a4215` |

Per `docs/METHODOLOGY.md` §2.2:

```
benchmark_receive_value = amount_sent × benchmark_rate  = 500 × 1.6937669376693767 = 846.8835 TOP
implicit_cost_value     = benchmark_receive_value − amount_received = 846.8835 − 867.41 = −20.5265 TOP
cost_pct                = implicit_cost_value / benchmark_receive_value × 100 = −2.4238 %
```

**cost_pct is negative** — at OrbitRemit's promotional rate, the recipient receives *more* TOP
than NRBT's benchmark reference rate implies. This is a genuine, honest result, not an error:
it reflects a real promotional rate that undercuts the central-bank reference, not a mistake in
either figure. Both `provider_fx_rate` values above resolve to real archived files that pass
`normalise.validate --strict`; nothing here is estimated, interpolated, or assumed. `cost_pct`
itself is not stored anywhere (schema's own comment: derived fields are computed in the Stata
layer, never stored raw) — this is a by-hand sanity computation for this report, the same kind
Round 2 did for the (then-incomplete) NZ→Tonga corridor.

**Which leg would be missing for NZ→Tonga specifically, since that was the original target?**
The benchmark leg exists (NRBT publishes NZD too, `reports/02-connectors.md` §3.2) but the
provider leg does not — ANZ NZ's rate table is still blocked (Round 2 §5.1, unchanged this
round; not re-investigated, since SPRINT-01's new policy means AU→Tonga via OrbitRemit already
satisfies "one corridor proves the pipeline" and there's no standing reason to keep chasing the
blocked one). If the maintainer wants NZ→Tonga specifically closed too, the missing piece is
still the same one Round 2 identified: a genuinely reachable NZ-origin provider quote.

**Caveat that matters:** this result depends on OrbitRemit's 500 AUD promotional-tier rate
specifically. The same corridor at 1,000 AUD or above uses a different, less favourable rate
(§3.2's table) — `cost_pct` at those amounts would be a different, almost certainly less
negative or positive number. This round closes the loop for one specific amount, not for the
corridor unconditionally.

### 5.2 The housekeeping push is blocked — no remote exists

The brief asked to "push and let CI execute once" to catch a Python 3.8-vs-3.12 mismatch now
rather than in November. `git remote -v` returns nothing — this repository has never been
connected to GitHub (or anywhere else) in any session so far. Every `github.com/devpolicy/...`
URL appearing in this project's own commits and reports (including this one, and Round 1's and
Round 2's) is a placeholder inferred from CLAUDE.md's "Development Policy Centre, ANU"
institutional framing, not a verified real repository — this was not checked carefully enough
in earlier rounds and is flagged here rather than perpetuated further.

**Options, not decided here:** (a) create a new GitHub repository now (needs an account/org
name, and an explicit decision that it should be public, from the maintainer, not inferred);
(b) the maintainer already has a private remote in mind not yet shared; (c) defer the
CI-execution check to whenever the repository is actually published, treating "run once before
November" as aspirational rather than blocking this round. No git remote was added and no
account was assumed — creating a public-facing repository is exactly the kind of visible,
hard-to-reverse action that needs an explicit go-ahead, not an inference from a "push" instruction
that assumed a remote already existed.

**Consequence:** the Python 3.8-vs-3.12 risk Round 2 flagged is still unverified. `pyproject.toml`/
`requirements.txt` pin no interpreter version; nothing written across all three rounds is known
to need a 3.9+-only runtime feature, but "known to not need" is not the same as "tested under."

---

## 6. Errors and anomalies

**OrbitRemit's live fetch vs. the fixture**, verbatim comparison:
```
Fixture (Round 2 sweep, committed): 500 AUD -> 866.82 TOP
This round's live run:              500 AUD -> 867.41 TOP
```
Not a bug — the underlying rate moved between the two fetches, which is exactly what a "live
exchange rate" page is expected to do. Recorded here because the discrepancy is real and
visible in the data, not because anything malfunctioned.

**Kiwibank JS bundle search**, the two literal strings found instead of the widget's own class:
```
data-rate-comparison
data-rate-product
data-rate-rebrand
data-rate-subheading
data-rate-timestamp
```
None is `data-rate` (the widget's actual attribute) or `richtext-rate` (its class) — these
belong to unrelated components (loan/mortgage rate comparison tools) sharing a naming
convention, not the FX widget.

**Git remote check**, verbatim:
```
$ git remote -v
$ git branch -a
* master
```
Empty output for `git remote -v` — no remote configured, confirmed twice.

---

## 7. Repository changes

| File | Change | Why |
|---|---|---|
| `CLAUDE.md` | Edited | §1.5: "what is and is not a workaround" clause (verbatim, maintainer ruling). §3: Tier 1 redefined by reachability; `client_api` added alongside `published_tariff`; Tier 3 gains the two-condition failure case. |
| `docs/METHODOLOGY.md`, `CHANGELOG.md` | Edited | v0.2→v0.3: §3 collection-method taxonomy gains `client_api`. |
| `PROVIDERS.md` | Edited | Tier definitions rewritten to match CLAUDE.md §3's revision. |
| `SPRINT-01.md` | Edited | Corridor policy: provider survives first, corridor follows; Tonga preferred only as a tie-breaker. Recorded so it isn't reopened again. |
| `collect/archive.py` | Edited | `detect_challenge()`, `FetchResult`, `fetch_and_archive()` — the common fetch path every connector now uses. |
| `collect/benchmarks/nrbt/connector.py` | Edited | Uses `fetch_and_archive()`; generalised to emit one observation per configured origin currency (NZD, AUD). |
| `collect/orbitremit/connector.py`, `collect/orbitremit/__init__.py` | Created | The Task B connector: AUD→TOP, Tier 2 `public_quote`, 500 AUD row. |
| `collect/run.py` | Edited | Registers `orbitremit` alongside `benchmarks.nrbt`. |
| `tests/test_archive.py` | Created | Challenge-detection golden tests (1 positive, 4 negative). |
| `tests/fixtures/challenge-pages/incapsula-anz-nz.html` | Created | The real Incapsula challenge page from Round 2, reused as a fixture. |
| `tests/test_orbitremit.py`, `tests/fixtures/orbitremit/aud-to-top-2026-09-09.html` | Created | 6 golden tests for the OrbitRemit connector, offline. |
| `tests/test_nrbt.py` | Edited | Added the AUD-leg test. |
| `scratch/round-03/*` | Created | Kiwibank and OrbitRemit endpoint-discovery evidence, including the fetched Kiwibank JS bundle. |
| `archive/nrbt/2026/09/09/*.json.gz` (×2 more), `archive/orbitremit/2026/09/09/*.json.gz` | Created | Real archived artefacts from this round's live runs. |
| `store/observations/2026-09.csv` | Appended | 4 more real observation rows this round (2 NRBT re-runs across commits, 1 NRBT AUD, 1 OrbitRemit) — append-only throughout. |

No file under `archive/` or `store/` was modified after being written, only appended to.

---

## 8. Claims register delta

No `CLAIMS.md` entries changed status this round.

---

## 9. Confidence flags

- **The promotional/standard two-tier rate model for OrbitRemit is a fit to eight data points,
  not a confirmed mechanism.** It matches OrbitRemit's own marketing copy well and every table
  row to within rounding, but the actual tier boundary or formula was not confirmed from any
  authoritative statement beyond that copy.
- **Kiwibank's hard stop rests on checking one linked JS bundle.** It's possible the widget's
  real logic lives in a bundle not linked anywhere in the static page — genuinely undiscoverable
  from source in that case, not just unchecked — but this wasn't distinguished from "checked the
  wrong bundle."
- **The "no git remote configured" finding (§5.2) means every `github.com/devpolicy/...` URL
  cited across all three rounds' reports and commits is unverified as a real repository.** This
  should have been checked in Round 1 and wasn't; flagging it now rather than continuing to cite
  it as if verified.
- **cost_pct's sign and size (−2.42%) depend entirely on OrbitRemit's promotional rate holding
  for genuinely new customers at exactly 500 AUD** — per its own marketing language ("promo rate
  for new customers"), a repeat customer might see a different, unknown rate. This wasn't (and
  couldn't be, from raw bytes) verified.
- **Python 3.8 vs. 3.12 remains untested**, now specifically because the push meant to catch
  this is blocked (§5.2), not because it was skipped by choice.
- **`report_failures.py` is still a stub** (Round 2's flag, unchanged) — CLAUDE.md §4.1's repair
  loop is not yet real. Every connector run so far has succeeded, so this hasn't mattered in
  practice yet, but it will the first time one doesn't.
- **The challenge-detection marker list (§3.3) is necessarily incomplete** — it catches the
  specific products this project has actually encountered (Incapsula, Akamai, Cloudflare
  variants), not bot-management products not yet seen.

---

## 10. Recommended next round

**Before anything else:** resolve §5.2 with the maintainer — where does this repository actually
live, is it meant to be public, and should Round 3's or a future round's first action be
creating that remote and pushing.

**On the corridor:** confirm whether AU→Tonga, 500 AUD, via OrbitRemit (Tier 2) now counts as
satisfying SPRINT-01 Session 4's acceptance criterion, given the corridor policy this round
recorded — or whether Session 4 specifically still wants a Tier 1 (`published_tariff` or
`client_api`) source before it's considered done, in which case Kiwibank's hard stop and ANZ
NZ's block mean no Tier 1 candidate currently exists for any corridor this project has checked.

**Deliberately left undone this round:**
- No further endpoint discovery beyond Kiwibank and OrbitRemit, per the brief.
- No import of the NRBT historical file (Round 2's finding stands, untouched).
- `report_failures.py`'s GitHub-issue-opening half of the repair loop — still a stub.
- Testing under Python 3.12 — blocked on §5.2.
- Deciding whether OrbitRemit's 1,000+ AUD standard rate should also get an observation, now
  that the comparison table's full shape is known — not built this round, since the brief asked
  for one amount, not a sweep of the table.
