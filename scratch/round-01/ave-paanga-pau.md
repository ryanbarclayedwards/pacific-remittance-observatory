# 'Ave Pa'anga Pau — evidence

Date checked: 2026-09-09

## Sites
- AU origin: https://www.avepaanga.com.au/
- NZ origin: https://www.avepaanga.co.nz/
- AU secure portal: https://secure.avepaanga.com.au/
- Operated by Tonga Development Bank (TDB), built with IFC/World Bank support (per prior WebSearch of public sources — background, not re-verified here).

## robots.txt
- `https://www.avepaanga.com.au/robots.txt` → HTTP 404 Not Found (no robots.txt file present at that path).
- `https://www.avepaanga.co.nz/robots.txt` → fetch returned no usable body (tool could not retrieve content; distinct from a clean 404). Treated as **unconfirmed**, not as "permits everything." Needs a direct re-check with a plain HTTP client before relying on it.

## AU homepage (avepaanga.com.au) — WebFetch summary
- Confirms AU→Tonga transfers.
- No dedicated FX rate table found. Site states: "The foreign exchange cost can vary but is generally close to 4.5%." — a disclosed *typical margin*, not a live rate or a rate table.
- No formal fee schedule page. Site states: "There are no fees for using 'Ave Pa'anga Pau TDB Ltd."
- A "You Send / Recipient Gets" converter widget appears on the homepage, but whether it functions without an account could not be confirmed from static fetch (likely JS-driven).
- "Get Started" routes to sign-up: `https://secure.avepaanga.com.au/select-account-and-country`. Login at `https://secure.avepaanga.com.au/users/sign_in`.
- No CAPTCHA/bot-wall mentioned in fetched content.

## NZ homepage (avepaanga.co.nz) — WebFetch summary
- Confirms NZ→Tonga transfers ("Fast and Reliable Money Transfers to Tonga").
- Same "no dedicated FX table, ~4.5% typical margin" pattern.
- "No fees" claimed.
- Registration required via portal at `secure.avepaanga.co.nz` to see a live quote.

## /how-it-works (avepaanga.com.au)
- Step 1 "Create an Account", Step 2 "Add a Beneficiary", Step 3 "Get live quotes and arrange a transfer in minutes."
- **This is the key finding**: live quotes are explicitly gated behind account creation. There is no public quote surface.

## Tier assessment
**Tier 3 — unobservable without an account.** No public FX table, no public fee schedule document (only a prose claim of "no fees" and a prose claim of "~4.5% margin"), and the site's own "how it works" copy states live quotes require account creation. CLAUDE.md §1.4/§1.5 rule out creating an account to get past this.

## Confidence flags
- avepaanga.co.nz robots.txt result was inconclusive (tool returned no body, not a clean 404/200) — needs a direct re-check, don't treat as "no robots.txt" on this evidence alone.
- Whether the homepage "You Send/Recipient Gets" widget returns a real quote without login was not confirmed either way — inferred Tier 3 primarily from the explicit "how it works" account-gating, which is solid, not from the widget.
- IFC/TDB backstory not re-verified in this session; carried from general knowledge of the sector via WebSearch snippets, not independently confirmed against a primary source page today.
