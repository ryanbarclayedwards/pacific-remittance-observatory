# ANZ New Zealand FX rate table — confirmed blocked to an honest HTTP client

**Date checked:** 2026-09-09
**Method:** `curl` with an honest, identifying user agent (`PacificRemittanceObservatory/0.1
(+https://github.com/devpolicy/pacific-remittance-observatory; research@devpolicy.org)`), no
header spoofing, no retries beyond following ANZ's own site navigation and redirect chain.

## What was tried

1. Direct fetch of `https://tools.anz.co.nz/foreign-exchange/fx-rates/` (the URL Round 1
   recorded as the confirmed FX table source) — see `anz-nz-fx-rates-incapsula-blocked.html`.
   926 bytes. Body is an Incapsula challenge page: `Request unsuccessful. Incapsula incident ID:
   136000310247516698-163488754764875720`.
2. ANZ's own fee-schedule page (`www.anz.co.nz/personal/fx-international/international-money-transfers/`,
   genuinely fetched, see `tests/fixtures/anz-nz/fees.raw.html`) links to
   `www.anz.co.nz/personal/fx-international/foreign-exchange-rates/` for rates.
3. That URL 301-redirects to `tools.anz.co.nz/foreign-exchange/fx-rates/` — the same blocked
   resource. See `anz-nz-fx-rates-redirect-target-blocked.html` (identical Incapsula challenge,
   different incident ID).
4. ANZ's exchange-rate-graphs page (`www.anz.co.nz/personal/fx-international/exchange-rate-graphs/`,
   genuinely fetched, 240,757 bytes, no Incapsula challenge — see
   `anz-nz-exchange-rate-graphs.html`) itself only links out to `tools.anz.co.nz/foreign-exchange/
   fx-rates?currencyPair=...` for the actual rate data behind its charts, for major pairs
   (NZD/AUD, NZD/EUR, NZD/GBP, NZD/JPY, NZD/USD) — not TOP, and the same blocked subdomain.

## Conclusion

Every path from ANZ New Zealand's own site to its live FX rate data funnels through
`tools.anz.co.nz`, which returns an Incapsula bot-challenge page to a plain HTTP client
regardless of entry point. This is not a wrong-URL-guess problem; it is a real, consistent
block, confirmed via ANZ's own navigation rather than a single request. No attempt was made to
solve the JS challenge, spoof a browser fingerprint, or otherwise get past it — that would be
exactly the kind of workaround CLAUDE.md §1.5 rules out.

**This contradicts Round 1's finding** (`scratch/round-01/anz-new-zealand.md`, `PROVIDERS.md`),
which recorded this page as Tier 1, "confirmed via WebFetch." Round 1's own confidence flags
already noted this rested on `WebFetch`'s fetch, not a raw byte-for-byte check — this is exactly
that gap surfacing. The most likely explanation is that Anthropic's `WebFetch` tool uses fetching
infrastructure capable of clearing a JS challenge (a full browser render, a different IP
reputation, or both) that a plain, honestly-identified `httpx`/`curl`-based production collector
cannot replicate without itself becoming a bot-wall workaround. `WebFetch` is not a reliable
stand-in for what a production Python collector can actually observe — this is the concrete
case that proves the point Round 2's brief raised in the abstract.

## What remains genuinely open

- ANZ New Zealand's **fee schedule** (`tests/fixtures/anz-nz/fees.raw.html`) is genuine,
  unblocked, real content — confirms the "OUR Fee" finding from Round 1 (undisclosed amount,
  standard goMoney/Internet Banking channel fee is $0).
- ANZ New Zealand's **FX rate table** is not observable by an honest automated client. For
  PROVIDERS.md purposes this downgrades the FX-table half of ANZ NZ's tier from "confirmed" to
  **blocked** — see the maintainer decision needed in `reports/02-connectors.md`.
