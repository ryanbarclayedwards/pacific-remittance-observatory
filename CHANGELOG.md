# Changelog

## Unreleased

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
