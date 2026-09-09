# TransCrypt — evidence

Date checked: 2026-09-09

## URLs fetched
- https://saverasia.com/compare/transcrypt/ (used only to locate TransCrypt's own domain; SaverAsia/SaverAmericas/SaverAfrica list it, but it is NOT listed on saverpacific.com/transfer-operators/)
- https://transcryptglobal.com/robots.txt — 301 redirect
- https://www.triple-a.io/robots.txt
- https://www.triple-a.io/

## Redirect (verbatim tool output)
```
REDIRECT DETECTED: The URL redirects to a location that was not fetched automatically.
Original URL: https://transcryptglobal.com/robots.txt
Redirect URL (from the server's Location header — server-supplied, not verified): https://www.triple-a.io/robots.txt
Status: 301 Moved Permanently
```
transcryptglobal.com permanently redirects (whole-domain) to triple-a.io.

## triple-a.io robots.txt (verbatim)
```
User-agent: * Allow: /
User-agent: GPTBot Allow: /
User-agent: ClaudeBot Allow: /
User-agent: PerplexityBot Allow: /
User-agent: Google-Extended Allow: /
Sitemap: https://www.triple-a.io/sitemap.xml
```
(also references a machine-readable `triple-a.io/llms.txt`)

## Findings
- triple-a.io describes itself as B2B payment infrastructure ("Pay and get paid globally in stablecoins and local currencies") — not a consumer remittance service.
- The fetched homepage content does not mention any Pacific Island country (Fiji, Samoa, Tonga, Vanuatu, Solomon Islands, PNG) or AUD/NZD as supported currencies. It claims "30+ local currencies" and "70+ countries" generically, without a published list in the content retrieved.
- No evidence TransCrypt, under either its old brand or as Triple-A, currently serves an AU/NZ→Pacific consumer remittance corridor at all.

## Tier assessment
Tier 3 — effectively discontinued as a Pacific-facing consumer remittance brand. TransCrypt appears to have been absorbed into Triple-A, a B2B stablecoin payments company with no found Pacific consumer offering. Not that it's "blocked" — it's that the thing PROVIDERS.md meant by "TransCrypt" doesn't appear to exist in that form any more.

## Confidence flag
Did not confirm Triple-A's full currency/country list (only checked the homepage) — possible a Pacific corridor exists somewhere in their coverage docs, but nothing on the surface suggests a consumer-facing AU/NZ→Pacific remittance product, which is the thing PROVIDERS.md is asking about.
