# Sprint 1 — first two weekends

**v2.** Rescoped for one part-time maintainer with no budget and no external dependencies.

**Goal:** one corridor, one amount, three providers, collected daily, appended to git,
validated, exported to `.dta`, charted in Stata. Nothing else.

**Sequencing principle:** build backwards from the 2023 audit data. If the pipeline cannot
losslessly carry observations you already trust, it is not ready for ones you don't.

**Nothing in this sprint depends on anyone replying to anything.** The outreach in
`docs/outreach-emails.md` is upside, not a dependency. Send it and forget it.

---

## Session 1 — schema from real data

Derive `schema/observation.schema.json` from the 2023 tidy files, not from a wishlist. Every
field in the existing data needs a home; every schema field the data cannot fill needs a
documented reason.

Then `docs/METHODOLOGY.md v0.1`. Three decisions must be settled, and they are yours, not the
agent's:

- the cost formula and its fee-inclusion convention
- the benchmark rate (see `CLAIMS.md` E1 — blocking)
- option-level versus provider-level ranking rules

Scaffold the repo: `CLAUDE.md`, CI gates, archive convention, git-as-store layout.

---

## Session 2 — ingest what you already have

```
2023 tidy files
  → ingest as source_system = devpolicy_manual_audit, vintage 2023
  → normalise against schema
  → validate (all gates green)
  → append to store/
  → tag release v0.1.0
  → export .dta with labels
  → stata/tables.do reproduces one chart from the existing paper
```

**Done when:** a published chart regenerates from `release/v0.1.0/observations.dta` via
committed Stata, and every row traces to an archived source file.

You now have a working observatory containing real data, before collecting anything new.

---

## Session 3 — triage, don't code

Fill in `PROVIDERS.md`. For each candidate: does a public FX table and fee schedule exist
(Tier 1)? A public quote calculator (Tier 2)? Neither (Tier 3)? Check robots.txt for each.

This is browsing and note-taking, not engineering. Resist starting a connector. The triage
determines which three providers are worth the next two sessions, and getting it wrong costs
far more than a session of reading.

Expect a lot of Tier 3. That is the honest finding, and publishing the observability map is
itself a contribution.

---

## Session 4 — one Tier 1 connector

A bank. Published daily FX table plus published fee schedule, reconstructed arithmetically.
**New Zealand → Tonga, NZ$200, via ANZ New Zealand.**

```
fetch → hash → archive → parse → normalise → validate → append
```

Tier 1 first because a bank's rate table survives for months while a calculator breaks
weekly, and you need one thing that works before you have anything that breaks.

**Amended 2026-09-09** (maintainer decision on `reports/01-triage.md` §5.1, option (b)). Round 1
triage found exactly one confirmed Tier 1 bank — ANZ New Zealand — and it is NZ-origin, not
AU-origin; no AU-origin bank reached confirmed Tier 1. Rather than wait on a browser-based
re-check of the AU-origin candidates, the corridor changes to NZ → Tonga so Session 4 proves the
pipeline now. This does not change CLAIMS.md §F's Tonga-first reasoning, only the origin
country; AU–Fiji remains the second target unchanged. AU-origin bank coverage is deferred to a
later session, per `reports/01-triage.md` §5.1.

---

## Session 5 — one benchmark connector

The receiving-country central bank's published daily rate. Same contract, `collect/benchmarks/`.

Without this you have amounts received but no cost. With it, the whole measure closes.

---

## Session 6 — schedule it

GitHub Actions, daily, committing to the repo.

Two things to verify rather than assume:

- **Scheduled workflows in public repos get disabled after a period of repository
  inactivity.** Whether the workflow's own commits reset that clock needs checking. If they
  don't, add a heartbeat.
- **Many sites block cloud IP ranges.** Test each connector from a runner before trusting it.
  If a provider works locally and fails on Actions, that is a Tier reclassification decision,
  not a proxy-shopping exercise.

**Done when:** three consecutive scheduled runs append without overwriting.

---

## Session 7 — one Tier 2 connector, and the repair loop

A public quote calculator. Then deliberately break its fixture and run the repair loop
end to end, so the thing that will actually keep this project alive is tested before you
need it.

---

## Session 8 — the chart

One page on the Devpolicy site. Corridor, provider lines, date axis, CSV and `.dta` links.

It renders the 2023 manual vintage and the 2026 automated vintage as **visually distinct
series with a labelled methodological break**. Getting that right now, on two vintages, is far
easier than retrofitting it later on ten.

---

## Explicitly out of scope

Additional corridors · additional amounts · additional providers · consumer UI · public API ·
World Bank RPW import · any comparison-site collection · any service requiring an account.

Coverage expands only after everything above is green and has been green, unattended, for a
fortnight.

---

## Acceptance criteria

- [ ] Benchmark decision made and documented
- [ ] 2023 audit data ingested, validated, released, exported to `.dta`
- [ ] A published-paper chart regenerated from the release via Stata
- [ ] `PROVIDERS.md` complete, with robots.txt checked for every candidate
- [ ] One Tier 1 connector collecting daily
- [ ] One benchmark connector collecting daily
- [ ] Three consecutive unattended scheduled runs, append-only
- [ ] One Tier 2 connector, with the repair loop exercised at least once
- [ ] Chart live, showing two vintages with a labelled break
- [ ] Every row in every release traces to a file in `archive/`
