# REPORTING.md — round-report structure

Every working round (a session or cluster of sessions against one brief) produces one report
under `reports/`, named `NN-short-slug.md` (e.g. `01-triage.md`). This document defines the
structure every round report follows. Do not deviate from it without a reason worth writing
down here.

## Why a fixed structure

**Critical constraint: a report must be fully legible to someone who cannot see this repository
and has no memory of the session that produced it.** It will be read by a separate reviewer
working only from the file. Do not write "as discussed above" or reference file contents
without restating them. Assume nothing the reader hasn't been told in the report itself.

This matters more than it looks like it should. The maintainer is one part-time person; a
report is often read weeks after the round that produced it, by someone (the maintainer, a
future agent, a co-author) with zero working memory of the session. A report that only makes
sense to someone who was there is not a report — it's a note to self, and it fails the moment
anyone else needs it.

## Structure

1. **Header** — round number, date, scope in one sentence, what was explicitly out of scope.

2. **What I did** — chronological, concise, factual.

3. **Findings** — tables where the data is tabular. Every provider row and every benchmark
   source row, in full, in the report itself — not "see PROVIDERS.md" as a substitute for
   showing the data. Cross-reference the living file for anything that will change after this
   round (re-checks, corrections); the report is a frozen snapshot of what this round found.

4. **Decisions I made** — each with the reasoning, and flagged as reversible or not.

5. **Decisions I did not make** — numbered, each with the options, the trade-offs and a
   recommendation. This is the section the maintainer acts on.

6. **Errors and anomalies** — verbatim. Do not summarise an error message.

7. **Repository changes** — every file created or modified, one line each on why.

8. **Claims register delta** — what moved status in CLAIMS.md, and on what evidence.

9. **Confidence flags** — anything inferred rather than observed, anything unsure, anything
   tempting to guess at. Be generous here; an over-flagged report is far more useful than a
   confident wrong one.

10. **Recommended next round** — and what was deliberately left undone.

**Subsection numbering.** A section's subsections inherit that section's own number — §5's
subsections are §5.1, §5.2, and so on, never §4.x under a "## 5." heading or vice versa. Round
1's report (`reports/01-triage.md`) shipped with exactly that mismatch (a "## 4." heading with
"### 5.x" subsections) and was not corrected after the fact, per the append-only rule below —
this note exists so the same slip doesn't recur in a later round.

## Conventions

- Use Australian English throughout (per CLAUDE.md).
- Quote error messages and page text verbatim, in code fences, not paraphrased.
- Every factual claim about the external world needs a source the reader can check — a URL, an
  evidence file path under `scratch/`, or a CLAIMS.md reference. If it isn't checkable from the
  report, it doesn't belong in the report.
- Never resolve a decision that CLAUDE.md or the maintainer's brief reserves for the maintainer
  (e.g. the benchmark rate choice, corridor/provider prioritisation as a coverage target). Put
  the options and a recommendation in §5 instead.
- A report is never edited after the round it describes closes. A later correction is a new
  entry in a later round's report, with a note pointing back to what it corrects — the same
  append-only instinct as the data store, applied to the audit trail.
- **"Closes structurally" vs "closes substantively"** (added 2026-09-10, after Round 3
  overclaimed the latter while only having earned the former — see `reports/04-historical.md`
  §8's correction). A measure **closes structurally** when every leg is archived, traceable to
  a real file, and schema-valid — the pipeline works end to end. A measure **closes
  substantively** when it additionally produces a cost figure with no unfilled required
  component (no `fee = null` standing in for an unknown fee, no assumed value anywhere in the
  chain). A structural close is real progress and worth reporting as such; it is never "the
  measure closes end to end" on its own — say which one you mean, every time.
