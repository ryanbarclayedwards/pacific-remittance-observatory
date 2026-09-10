# Pacific Remittance Observatory

An open, append-only database of remittance prices for Australia and New Zealand → Pacific
corridors. Collected automatically from public sources, archived permanently, published free.

**Status:** pre-alpha. Nothing here is a data release yet.

**Maintained by:** Ryan Edwards

---

## What this is

Comparison sites answer "what does it cost today?". Nobody holds a public record of what it
cost *yesterday*, at provider level, with an honest timestamp. That record is what this
project builds.

Three properties define it:

1. **Append-only.** Every observation is kept forever. Corrections supersede, never overwrite.
2. **Traceable.** Every number resolves to an archived raw response.
3. **Honest about freshness.** Every observation carries when it was collected and, where the
   source reveals it, when the price was set.

## What this is not

- Not a remittance service. It executes no transfers.
- Not comprehensive. Several Pacific corridor specialists have no automatable public quote
  surface. Their absence is recorded as a coverage gap, never filled with a guess.
- Not dependent on any commercial party, agreement, credential or funding line. If it needs a
  contract or a login, it is out of scope by design.

## Design constraints

One maintainer. No budget. No credentials. No commercial agreements.

Everything follows from that:

| Constraint | Consequence |
|---|---|
| No budget | Git is the database. GitHub Actions is the scheduler. Devpolicy's existing site is the front end. |
| No credentials | Public web surfaces only. No API keys, no accounts, no partner programmes. |
| One maintainer | Connector count is minimised. Agentic repair is load-bearing, not a nice-to-have. |
| Research use | Stata is the analysis layer. Reproducibility beats coverage. |

## Layout

```
collect/     fetch → hash → archive → emit raw record   (Python, deterministic)
normalise/   parse → canonicalise → validate → append   (Python, pure functions)
store/       append-only observation store               (committed to git)
archive/     raw payloads, content-addressed            (committed to git)
release/     immutable tagged releases: csv, parquet, dta
stata/       analysis layer — indicators, tables, paper output
schema/      observation.schema.json — the single contract
docs/        methodology, data dictionary, coverage map
```

## What's in `archive/`

`archive/` holds the raw, unmodified bytes of every page, table and document this project has
ever fetched to produce an observation — every daily FX table, every fee schedule, every
provider comparison table, content-addressed by a SHA-256 hash of the exact bytes received. It
is published in full, alongside `store/` and every release, not excerpted or gated behind a
request. Reasoning: this is factual rate and fee data published by the provider or platform
itself, not anything personal or sensitive; reproducing an observation requires the exact bytes
it was parsed from, not a description of them (`docs/METHODOLOGY.md` §8); and full publication
is standard practice for a research web archive. If you believe a specific archived file
shouldn't be published — a technical error on your platform's end swept up in a fetch, say, not
a request to suppress an unfavourable price — contact **[CONTACT]** with the file path and the
reason.

## Start here

- `CLAUDE.md` — how the coding agent must behave. Read before touching anything.
- `CLAIMS.md` — what is actually known, versus what was assumed. Check before asserting.
- `SPRINT-01.md` — the current plan.
- `PROVIDERS.md` — the collection triage.
- `docs/METHODOLOGY.md` — cost definitions. Versioned.
