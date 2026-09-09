# Suncorp Bank (suncorpbank.com.au) — evidence, checked 2026-09-09

## Domain note
The banking site is **suncorpbank.com.au**, not suncorp.com.au (the latter is Suncorp Group's general/insurance site). Both robots.txt files were checked; the banking-relevant one is suncorpbank.com.au.

## robots.txt
URL: https://www.suncorpbank.com.au/robots.txt
Fetched via curl with honest UA. Verbatim:
```
User-agent: *
Allow: /
Sitemap: https://www.suncorpbank.com.au/sitemap.xml
```
(For reference, https://www.suncorp.com.au/robots.txt — the group site — is identical in form: `Allow: /` plus a sitemap. Not the operative domain for banking, included only because it was checked first before the domain distinction was noticed.)

## International transfer pages
URL: https://www.suncorpbank.com.au/bank-and-save/international/paying-overseas-bank-accounts.html
- Fee schedule: Internet Banking — "No Suncorp Bank fee" (overseas/intermediary banks may still charge); branch — $30.00.
- Two tools linked without login apparently required: a "Foreign Exchange Calculator" and an exchange-rates page ("Check today's exchange rates") — neither independently tested/fetched this round.
- No Pacific Island destination or currency named on this specific page.

URL: https://www.suncorpbank.com.au/help-support/faqs/international.html
- Confirms the currency list for "global payments": AUD, CAD, CHF, DKK, EUR, FJD, GBP, HKD, INR, JPY, NOK, NZD, PGK, PHP, SEK, SGD, THB, USD, ZAR. **Only FJD and PGK** are Pacific currencies here — TOP, WST, VUV, SBD are absent, meaning Tonga, Samoa, Vanuatu and Solomon Islands appear to be unreachable in local currency through this product even if the connector were built.
- References "Suncorp Bank's Foreign Currency Rates page" by name but the actual link/URL was not captured in this fetch.

## Tier assignment
**Tier 3 for the full six-currency Pacific set; a narrower Tier 1/2 candidate exists only for FJD/PGK.** Even if the FX calculator and rates page prove to be fully public (untested this round), Suncorp's own currency list excludes four of the six target Pacific currencies. Given CLAUDE.md's Tier definitions apply per-provider rather than per-currency, and the project's stated destinations span all Pacific corridors, recommend recording Suncorp as a **partial/limited-coverage provider** rather than a clean Tier 1/2/3 — flagged as a decision for the maintainer in the report rather than resolved here.

## Confidence flags
- The FX calculator and dedicated rates page (both referenced, neither fetched) are the main open items — could move this to Tier 1 or 2 for FJD/PGK specifically.
- Did not determine whether Suncorp Bank is still operationally independent or has been absorbed into another banking group; the site presents as a standalone bank brand as of the check date, but this project has not independently verified current ownership/structure and none of the pages checked stated it either way. Flagged as UNCHECKED rather than asserted.
