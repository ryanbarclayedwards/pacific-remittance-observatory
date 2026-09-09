# Westpac Australia (westpac.com.au) — evidence, checked 2026-09-09

## robots.txt
URL: https://www.westpac.com.au/robots.txt (WebFetch)
```
# Allow all crawlers
User-agent: *
Allow: /

# Keep these tool endpoints crawlable all crawlers
Allow: /content/public/wbc/en/_services/serialiser/calculator/
Allow: /content/public/wbc/en/_services/calcs-forms-tools/

# Restricted areas for all crawlers
Disallow: /search/
Disallow: /branch-locator/
Disallow: /_services/
Disallow: /_services/serialiser/
Disallow: /content/public/wbc/en/_services/serialiser/
Disallow: /content/dam/public/wbc/introducernet/
Disallow: /content/public/wbc/en/deeplink-web-redirect.html
Disallow: /locateus-ios*
Disallow: /locateus-android*
Disallow: /disclaimer/
Disallow: /footer-cta/
Disallow: /test-aem-1817/
Disallow: /test/
Disallow: /*.doc
Disallow: /*.docx

# Global sitemap declarations
Sitemap: https://www.westpac.com.au/sitemap.xml
Sitemap: https://www.westpac.com.au/sitemap-65.xml
Sitemap: https://www.westpac.com.au/news/sitemap.xml
Sitemap: https://www.westpac.com.au/content/dam/public/wbc/seo/sitemap-locator.xml
```
Notably, this robots.txt **explicitly carves out an Allow for calculator/tool endpoints** even inside an otherwise-disallowed `_services/serialiser/` path — a clear signal Westpac wants calculator tools crawlable. Worth confirming which page(s) actually use that path.

## International money transfer page
URL: https://www.westpac.com.au/international-travel/international-transfers/
- Fee schedule confirmed exact: Online/App foreign currency $0, Online/App AUD $20, in-branch $32; receiving $12 AUD (waived ≤$100 equivalent).
- Currency converter referenced: "Use the currency converter to get indicative foreign exchange rates," linking to /personal-banking/services/currency-converter/ — not embedded on this page, not independently fetched this round.
- Pacific currencies/destinations confirmed named on this page: Fiji (FJD), Samoa (WST), Solomon Islands (SBD), Tonga (TOP), Vanuatu (VUV), Papua New Guinea (PGK) — all six.

## FX rates page
URL: https://www.westpac.com.au/personal-banking/services/foreign-exchange-rates/
- WebFetch: no live rate table; the six Pacific currencies appear only in a FAQ list of "other acceptable currencies," no rates/timestamps. Page instructs customers to sign in to the App/Online Banking for actual rates, or phone 1800 221 815 for an indicative rate on request (not automatable).

## Currency converter redirect — resolved
`https://www.westpac.com.au/personal-banking/services/currency-converter/` was fetched directly with `curl` (honest UA, following redirects): it 301-redirects to the same FX-rates URL above. The resulting page (211,332 bytes, HTTP 200) **does contain all six Pacific currencies server-side**, but only as a static reference list with flag icons and currency names/codes (e.g. `<td>Tongan Pa'anga - <b>TOP</b></td>`) — there is no numeric rate, buy/sell price, or timestamp anywhere near these entries. This confirms, rather than resolves, the earlier WebFetch finding: the page tells a visitor which currencies Westpac deals in, not what today's rate is. Actual rates require sign-in or a phone call, per the page's own instructions.

## Tier assignment
**Tier 3 (unobservable this round).** All six Pacific currencies are named, and a fee schedule is public with exact figures, but no path to an actual numeric rate without logging in or phoning was found — the "currency converter" link is not a calculator, it is a static supported-currency list. This is a firmer finding than most other Tier 3 calls in this batch: both the FAQ text and the raw byte-level page content agree.

## Confidence flags
- Not confirmed whether the Westpac App or Online Banking (both requiring login) expose a machine-reachable rate endpoint once authenticated — irrelevant to this project regardless, per CLAUDE.md §1.4 (no credentials).
- No browser available this session; only static/redirect-following HTTP checks were possible.
