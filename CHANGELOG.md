# Changelog

## Unreleased

- `schema/observation.schema.json` v0.2 → v0.3: adds `benchmark_is_carried_forward` (boolean,
  nullable) and `benchmark_age_days` (integer, nullable). Round 4's 2023-audit ingestion found
  34% of provider observations (408/1,188) had no same-day NRBT benchmark, all on weekends or
  AU/NZ public holidays. `CLAUDE.md` §1.1 gained a matching, explicitly flagged exception: a
  *benchmark* (never a provider's own quote) may carry the last published business day's rate
  forward, always marked as such. `docs/METHODOLOGY.md` v0.4 → v0.5 documents the policy and,
  separately, resolves E2 (fee-inclusion is per-observation, never inferred) and records the
  benchmark-sensitivity finding (benchmark choice moves cost levels ~0.44pp on average, leaves
  rankings 99.8% undisturbed) as a quantified property. `CLAIMS.md` E2 marked resolved. See
  `reports/05-live.md`.
- `schema/observation.schema.json` v0.1 → v0.2: adds `rate_is_promotional` (boolean, nullable)
  and `promotion_detail` (string, nullable). Round 3 built a connector against a provider rate
  that turned out to be a new-customer promotional rate with no schema field to flag it as such
  — the schema had `fee_is_promotional` but nothing for a promotional *rate*, which is where
  that specific distortion actually lived. Existing rows affected by the gap are re-emitted as
  new observations with `supersedes`, never edited in place. See `reports/04-historical.md`.
- `docs/METHODOLOGY.md` v0.3 → v0.4: §2.3 documents NRBT's published MID rate as the midpoint
  of the bank's own dealing spread (BUY/SELL), not an interbank mid-market rate — a known
  limitation, and the reason the secondary (best-observed-provider-rate) benchmark stays
  load-bearing rather than optional. Round 4 correction after Round 3 treated a benchmark
  comparison as more authoritative than the underlying rate supports. See
  `reports/04-historical.md`.
- `docs/METHODOLOGY.md` v0.2 → v0.3: §3's collection-method taxonomy gains `client_api` —
  a Tier 1 quote reconstructed from a public JSON/XHR endpoint the page's own client-side
  script calls, rather than from server-rendered HTML (`published_tariff`). Matching revision
  in `CLAUDE.md` §3: Tier 1 is now defined by reachability ("a plain HTTP client can retrieve
  the number without defeating anything"), not by markup shape — Round 2 found most bank rate
  pages are client-rendered, which made the old markup-based definition rarer than intended
  without the data being any less publicly reachable. `CLAUDE.md` §1.5 gained a matching
  "what is and is not a workaround" clarification: calling a page's own public API endpoint
  is not a workaround; clearing a challenge, spoofing identity, or using an extracted
  credential is. See `reports/02-connectors.md` §10 (Options) and the maintainer's ruling that
  opened Round 3.
- `docs/METHODOLOGY.md` v0.1 → v0.2: §2.3 (E1, the benchmark rate) decided and rewritten.
  Receiving-country central bank adopted as the primary benchmark; best-observed-provider-rate
  retained as a secondary, dependency-free check from the first collection run. National
  Reserve Bank of Tonga is the first benchmark source built. No other section changed; the
  document stays draft overall. See `CLAIMS.md` E1 and `reports/01-triage.md` §5.4 for the
  scoping this decision was made against.
- First real observation collected: National Reserve Bank of Tonga, NZD→TOP benchmark rate,
  2026-09-09 (`reports/02-connectors.md`). Repository scaffold no longer describes the current
  state accurately as of that commit.
