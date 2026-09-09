# ANZ Australia (anz.com.au) — evidence, checked 2026-09-09

## robots.txt
URL: https://www.anz.com.au/robots.txt
Fetched via curl with honest UA (`PacificRemittanceObservatory-recon/0.1`). Verbatim:
```
# /robots.txt for http://www.anz.com/
# comments to InternetAdministration@anz.com
#
User-agent: *
Sitemap: https://www.anz.com/sitemap.xml
Sitemap: https://www.anz.com.au/plus/sitemap.xml
```
No Disallow lines. Fully permits automated access under the general robots convention.

## International transfer page
URL: https://www.anz.com.au/personal/travel-international/international-payments/
- Public fee schedule shown inline, no login required:
  - ANZ Plus app: $0 (foreign currency) / up to $15 (AUD)
  - Internet Banking: $0 (foreign currency) / $18 (AUD)
  - Phone Banking: $0 (foreign currency) / $32 (AUD)
  - Correspondent fees vary by currency/destination, listed in a table on the page.
- Public calculator linked: "Use our foreign exchange calculator to check today's foreign exchange rates, convert currencies and view any applicable fees" — https://www.anz.com.au/personal/travel-international/currency-converter/. Not confirmed to work without login (not tested interactively — no browser available in this session; Chrome extension not connected).
- Page references (but does not inline) a rates page at https://www.anz.com.au/personal/travel-international/foreign-exchange-rates/ — **not independently fetched/confirmed this round**. Flagged as a gap.
- Pacific destinations named: Fiji, Tonga, Samoa, Vanuatu, Solomon Islands, Papua New Guinea, Kiribati, Cook Islands. Tuvalu and Niue not mentioned as destinations on this page (absence noted, not confirmed unsupported).
- Note: ANZ offers reduced/cheaper fees specifically for transfers to Cook Islands, Fiji, French Polynesia, Kiribati, New Caledonia, PNG, Samoa, Solomon Islands, Timor-Leste, Tonga, Vanuatu (per page content, third-party-corroborated by search results).

## Tier assignment
**Tier 2 (public_quote), pending Tier 1 upgrade** — public calculator link exists and fee schedule is public and exact; a dedicated FX-rates page is referenced but not independently confirmed in this pass. Do not build against the referenced rates page or the calculator until both are directly verified.

## Confidence flags
- The `/personal/travel-international/foreign-exchange-rates/` page and the currency-converter calculator were not directly fetched/verified this round — found only as a link/reference within another page's content. Verify before Tier upgrade or connector work.
- WebFetch content summaries are produced by a small model, not raw HTML; fee figures above cross-checked against the robots.txt curl (verbatim) but the fee/destination text is summarized, not verbatim-quoted from the source HTML.
