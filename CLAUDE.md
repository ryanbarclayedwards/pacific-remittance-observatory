# CLAUDE.md — Pacific Remittance Observatory

**v2 — 9 September 2026.** Read in full before any task. This overrides general helpfulness.

**Project:** an open, append-only database of remittance prices for Australia and New Zealand →
Pacific corridors, collected automatically from public sources.

**Institutional home:** Development Policy Centre, ANU.

**Reality:** one part-time maintainer, no budget, no credentials, no commercial agreements. The
maintainer writes Stata, not Python. Optimise for something that survives unattended, not for
something impressive.

**Language:** Australian English (normalise, harmonise, organisation, licence as noun).

---

## 1. Hard constraints

Not preferences. A change violating one of these is wrong even if it passes tests.

### 1.1 Never invent an observation

Never write a number into the data path that did not come from an archived response.

- Missing value → `null` plus a status code. Never a default, never an interpolation, never a
  value carried forward from a previous run, never a figure recalled from training data.
- **Exception, maintainer decision 2026-09-10 (`reports/05-live.md`):** a *benchmark* rate may
  be carried forward from the last published business day when the source publishes none for a
  given date (a weekend or public holiday) — never silently: the carrying row must set
  `benchmark_is_carried_forward = true` and `benchmark_age_days` to how stale it is. This
  applies only to a benchmark (METHODOLOGY.md §2.3), never to a provider's own quote — a
  provider observation is either genuinely observed that day or `null`, always. The exception
  exists because losing benchmark coverage to a central bank's publication calendar was judged
  a worse trade than a flagged approximation; the flag is what keeps it from becoming a silent
  default.
- If you are reasoning about what a price *probably* was, stop and open an issue.
- **No LLM runs inside the collection or normalisation path.** You write and repair the code;
  deterministic code produces the data.

### 1.2 Every observation traces to an archived artefact

Every row carries `raw_payload_sha256`. Normalisation is a pure function of an archived file.
If the artefact is absent, the observation is invalid and must not be released.

### 1.3 Append-only

- Never modify or delete anything under `archive/`, `store/` or `release/`.
- Corrections are new rows with `supersedes` and `correction_reason`.
- Never re-run a past date to "fix" it. Backfills are new rows with a new `collection_run_id`.

### 1.4 No dependencies that can be withdrawn

This project deliberately depends on nothing that requires permission, payment, credentials or
goodwill. **Do not introduce:**

- API keys, accounts, OAuth, partner programmes, affiliate schemes
- paid services of any kind, including "free tier" services that require a card
- any data source obtained under an agreement rather than from a public page
- any dependency on a comparison site's back end

If a provider cannot be observed from a public surface without credentials, it is
`unobservable`. That is a recorded finding, not a problem to solve creatively.

### 1.5 Collect only what is permitted

Never bypass authentication, CAPTCHA, rate limits, paywalls or robots directives. Never
impersonate a customer, create accounts, or submit real transactions. Respect robots.txt and a
courteous request rate. Identify the collector honestly in the user agent, with a contact URL.

Where collection is blocked, write `availability_status = blocked` with the reason and stop. A
recorded gap is a research finding; a circumvented control is a liability for the University.

**What is and is not a workaround.** Bypassing an access control means defeating
something built to stop you: clearing a bot challenge, solving a CAPTCHA, spoofing a
user agent to evade a directive, or using credentials you were not given. All
forbidden.

Calling a public page's own unauthenticated JSON or XHR endpoint is not a workaround.
That endpoint is as public as the page whose script calls it, and a single honest
request to it is less intrusive than rendering the whole page. It is permitted, and it
is preferred where available, because a JSON endpoint is more stable to parse and less
likely to break on a cosmetic redesign.

Two conditions. Stop if robots.txt disallows the endpoint path. Stop if the endpoint
requires a key, token or session extracted from page source — that is credential use,
and it is a different thing.

### 1.6 Versioned contracts

Do not change `schema/observation.schema.json` or `docs/METHODOLOGY.md` without bumping the
version and writing a migration note in `CHANGELOG.md`. Silent schema drift destroys the panel.

### 1.7 Claims need sources

Any assertion about the external world in code, docs or commit messages needs an entry in
`CLAIMS.md` with a URL and a check date. Do not restate inherited claims as fact.

### 1.8 Pre-publication check before any first push to a new remote

Run `docs/PRE-PUBLICATION-CHECK.md` in full before the first push to any new public remote,
and again after any git-history rewrite. Origin: `docs/outreach-emails.md` named a real
individual alongside internal negotiating strategy and had to be removed from history before
this repository's own first push (`reports/06-live.md`).

---

## 2. Architecture

### 2.1 Git is the database

There is no server, no hosted database, no object store. The repository *is* the archive.

- Raw payloads go to `archive/<provider>/<YYYY>/<MM>/<DD>/<sha256>.json.gz`
- Observations append to `store/observations/<YYYY-MM>.csv`
- Releases are git tags with built artefacts under `release/`

Git already provides append-only history, content hashing, diffs, distribution and free
hosting. Do not add infrastructure that duplicates what git does. Do not propose a database
until the store exceeds roughly a million rows, which at the planned collection rate is years
away.

### 2.2 Layer boundary

```
COLLECT (Python)      fetch → hash → archive → emit raw record
NORMALISE (Python)    parse → canonicalise → validate → append to store
── frozen release boundary ──
ANALYSE (Stata)       .dta + .do → indicators, ranks, tables, paper output
PUBLISH               static JSON built from the store, read by the Devpolicy site
```

The maintainer writes Stata. Therefore:

- Everything above the boundary is Python and is yours to maintain.
- Everything below is Stata, reviewed line by line by a human. Draft it, comment it heavily,
  never restructure it unasked.
- Releases export `.dta` (Stata 14 format) alongside CSV and Parquet, with variable and value
  labels populated from the data dictionary.
- **Stata cannot run in CI.** Any indicator CI must verify needs a Python reference
  implementation in `normalise/reference/`, with the `.do` tested against it on a committed
  fixture. Flag divergence loudly; never adjust either side to make them agree.

### 2.3 Front end

Devpolicy's existing website hosts the public interface. Do not build a new web platform, an
API server, or an auth system. The deliverable to the site is a static JSON file built from
the store on each run.

---

## 3. Collection tiers

Every provider is classified and the classification is published.

**Tier 1 — reachable without defeating anything.** Defined by reachability, not by markup
shape (revised 2026-09-09; Round 2 found most bank rate tables are client-rendered, which
made the original markup-based definition rarer than intended without actually being any
less publicly reachable). A quote is reconstructed arithmetically from a daily FX rate and a
fee schedule, both retrievable by a plain, honestly-identified HTTP client — no account, no
browser, no control defeated. Two forms, each its own `collection_method`:

- `published_tariff` — the number is in the page's own server-rendered HTML.
- `client_api` — the number comes from a public JSON/XHR endpoint the page's own client-side
  script calls. Discovering and calling that endpoint directly is not a workaround (see
  §1.5's "what is and is not a workaround") and is preferred over `published_tariff` where
  both exist, since an API is more stable to parse and less likely to break on a cosmetic
  redesign. Carries its own brittleness profile — flag it distinctly, never fold it into
  `published_tariff`.

Most banks fall here, in one form or the other. Cheapest to collect, most stable, least
brittle. Never present a reconstructed quote as a live one.

**Tier 2 — public quote calculator.** A public page returns a quote for fixed inputs without
an account. Flag as `collection_method = public_quote`.

**Tier 3 — unobservable.** No public surface, one requiring credentials, one that blocks
automated access, or a `client_api` endpoint that fails either of §1.5's two conditions
(robots.txt disallow, or a key/token/session required). Flag as `availability_status =
unobservable` with the reason and the date checked. Re-check quarterly. **Do not attempt to
work around this.**

Build Tier 1 before Tier 2. Bank tariffs are stable for months; calculators break weekly.

Benchmark rates are collected by the same mechanism under `collect/benchmarks/`, with the same
contract, from receiving-country central bank pages.

---

## 4. Working method

- **Plan first.** Any task beyond a one-line fix: write a plan, stop, wait for approval.
- **One concern per pull request.** Even solo. The diff is the audit trail and becomes part of
  the replication package.
- **Stay in your lane.** A connector task touches `collect/` only. A QA task touches `tests/`.
  If a task seems to require crossing, say so and stop.
- **Small over broad.** One connector working end to end beats ten half-built ones. Do not
  expand corridor, amount or provider coverage while anything existing is red.
- **Prefer boring.** Requests over Playwright. A parsed table over a headless browser. Fewer
  moving parts survive unattended; clever ones do not.

### 4.1 The repair loop — this is the load-bearing part

A solo unfunded scraper project dies of connector rot. Reducing that is your main job.

When a connector fails you receive: the failing test, the last successful payload, the current
payload, the diff, and the connector source. Nothing else. You must:

1. Diagnose what changed upstream.
2. Propose the minimal patch.
3. Show golden tests still pass against *historical* fixtures.
4. Open a PR. Do not merge.

If an upstream change means a field is gone, the correct patch emits `null` with a status code.
It is never to source that field from somewhere else, and never to infer it.

If a connector fails on three consecutive runs and you cannot repair it, reclassify the
provider to Tier 3 and open an issue. A quiet, honest gap beats a noisy, wrong number.

---

## 5. CI gates

A commit fails if any of these fail:

- JSON schema validation of every new observation
- golden-file tests for every connector
- arithmetic sanity: `amount_received > 0`; fees non-negative; implied rate coherent with
  `amount_sent`, `fee` and `amount_received`; cost within documented bounds
- **no row without a `raw_payload_sha256` resolving to a file in `archive/`**
- no modification to files under `archive/`, `store/` or `release/` in a code PR
- schema or methodology change without a version bump

The fourth gate mechanically enforces §1.1. Do not weaken it.

---

## 6. Wrong even though it looks helpful

1. Filling a gap so a chart looks complete.
2. Averaging a provider's multiple service options into one "provider price".
3. Treating a zero advertised fee as a low cost.
4. Concatenating vintages or collection methods without flags.
5. Substituting a different benchmark when the primary one is unavailable.
6. Re-running a past date to fix it.
7. Adding providers or corridors to look comprehensive.
8. Rewriting the Stata to be more idiomatic.
9. Reporting a stale quote without its freshness metadata.
10. Presenting a reconstructed tariff quote as a live quote.
11. Adding a service, key or account to make something easier.
12. Working around a block rather than recording it.
