# Commonwealth Bank (commbank.com.au) — evidence, checked 2026-09-09

## robots.txt
URL: https://www.commbank.com.au/robots.txt (WebFetch paraphrase, not independently curled this round)
Summary: explicitly permits AI/LLM crawlers (named Claude variants, GPTBot, others) via `Allow: /`; for general user-agents disallows system paths (`/bin/`, `/etc/`), APIs, test areas, personal/sensitive documents, and netbank/digital-banking paths; refund pages disallowed except for one named bot. Four sitemaps declared (main, articles, support, tools/calculators). Not in obvious conflict with fetching the public FX/fee pages.

## FX rates page
URL: https://www.commbank.com.au/international/foreign-exchange-rates.html
- WebFetch: page titled "Foreign exchange rates," states "Find the latest exchange rates for buying, selling, sending or receiving foreign currency," but no rate table content was present in the fetched/converted output.
- Direct `curl` (honest UA), 45,430 bytes, HTTP 200: **no occurrence of TOP, WST, VUV, SBD, PGK or FJD anywhere in the raw server-delivered HTML.** The page is client-rendered; a plain HTTP client (the kind CLAUDE.md prefers — "requests over Playwright") gets no rate data from this URL as served.
- Page links a fee PDF: https://www.commbank.com.au/content/dam/commbank/personal/apply-online/download-printed-forms/ADB1784.pdf ("Standard fees and charges for international payments and travel funds") — **not fetched/parsed this round**; PDFs are usually static and this is a promising lead for Session 4, but confirming it was out of scope for this pass.

## Calculator
URL: https://www.commbank.com.au/international/foreign-exchange-calculator.html — linked from the rates page, not independently tested (would need interactive input; no browser available this session).

## Fee schedule PDF (opened and read in full)
URL: https://www.commbank.com.au/content/dam/commbank/personal/apply-online/download-printed-forms/ADB1784.pdf
Downloaded via `curl` (honest UA), HTTP 200, 150,920 bytes, genuine PDF (not an HTML error page). Titled "Standard fees and charges for international payments and travel funds," **dated 23 July 2026**, document code 006-505 240726. This is a real, static, machine-readable, dated fee schedule reachable by a plain HTTP client — no JavaScript required. Key figures (AUD, GST inclusive where applicable):
- IMT via branch/manual instruction: $30.00 per transfer
- IMT via Digital channels (NetBank/CommBank app/CommBiz), AUD→foreign currency: fee waived
- IMT via NetBank/CommBank app, AUD→AUD (no FX conversion): $30.00
- IMT via CommBiz, AUD→AUD (no FX conversion): fee waived
- Cancellation/return request: $25.00 + overseas banks' costs
- Amendment: $25.00 + overseas banks' costs
- Trace/investigation: $25.00
- IMT received, credited to CBA AUD or FX account: up to $11.00 per transfer
- Foreign cash buy/sell: 1% of transaction (min $10.00)
- The Bank covers correspondent/payment-agent fees for cross-currency IMTs in most cases; explicit "Additional Overseas Banks' Fee" schedule given for EUR/GBP/NZD/USD same-currency transfers ($33/$17/$17/$37) — **no Pacific currency appears in this specific table**, so it is silent on whether Pacific-currency same-currency transfers carry an equivalent fee.
- Document states: "A full list of the Commonwealth Bank's Foreign Exchange rates is available at commbank.com.au" — confirms a rate list exists publicly, but does not itself contain rate figures, and the HTML page it points to did not deliver rate data to a plain client (see above).
- No Pacific Island country or Pacific currency (TOP/WST/VUV/SBD/PGK/FJD) is named anywhere in this seven-page document.

## Tier assignment
**Tier 2 (public_quote), pending — leaning toward Tier 1 if the FX rate page's data source can be found.** A genuine, dated, statically-fetchable fee schedule now confirmed (the PDF). The missing piece for Tier 1 is a machine-reachable daily FX rate table: the HTML rates page renders no currency data to a plain HTTP client, and the fee PDF does not include rates. The calculator (Tier 2 candidate) exists but was not tested interactively. Recommend as a secondary Session-4 candidate behind ANZ NZ and (pending endpoint discovery) Kiwibank.

## Confidence flags
- FX rate page's underlying data source (if any) not located — same open question as BNZ. This is the deciding factor between Tier 1 and Tier 2/3 for CBA.
- Calculator functionality (a Tier 2 path independent of the rates page) untested — no interactive/browser tooling available in this session.
- The fee PDF's silence on Pacific currencies specifically (only EUR/GBP/NZD/USD get an explicit same-currency correspondent-fee table) is a gap for the cost formula, not just for tiering — worth carrying into METHODOLOGY §2.5 discussion if CBA is built.
