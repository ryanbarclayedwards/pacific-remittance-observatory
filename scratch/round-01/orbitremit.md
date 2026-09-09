# OrbitRemit — evidence

Date checked: 2026-09-09

**Scoping note:** OrbitRemit is listed under "Pacific corridor specialists" in PROVIDERS.md, but on the evidence gathered it reads more like a general global remittance company (AFSL 470646, licensed AU + NZ, "send to over 50 countries" per its own marketing) that happens to also serve some Pacific destinations, rather than a Pacific-specialist operator. Flagging the categorisation rather than silently reclassifying it — a call for the parent, not something to fix unasked.

## Site
https://www.orbitremit.com/ — AU + NZ origin, operating since 2008.

## robots.txt
`https://www.orbitremit.com/robots.txt` → HTTP 200:
```
User-agent: *
Allow: /
Disallow: /amplifier
Disallow: /30_off_first
Disallow: /20_off_first
Disallow: /15_off_first
Sitemap: https://www.orbitremit.com/sitemap.xml
```
Broadly permissive — the disallowed paths are promo/landing pages, not rate, fee, or destination content.

## Destination page — /fiji and /currency-converter/aud-to-fjd
- `https://www.orbitremit.com/fiji` — WebFetch returned only page metadata (title/description), no body; the interactive calculator did not render for a static fetch. Title/description confirm "Transfer money to Fiji from Australia or New Zealand."
- `https://www.orbitremit.com/currency-converter/aud-to-fjd` — meta description exposes a rate figure directly: **"$1 AUD = 1.56949 FJD"**. The on-page interactive converter itself returned "An error occurred while fetching estimates" under static fetch (consistent with a client-side XHR that needs a real browser context, not necessarily a bot block — not established either way). Same page lists other Oceania destinations: New Zealand, Samoa, Tonga, Vanuatu (in addition to Fiji).
- Promotional copy states "Free transfer + exclusive promo rate for new customers," with the promotional rate capped at the first $500.

## Support article on fees
`https://support.orbitremit.com/hc/en-us/articles/360003229093-How-much-does-it-cost-to-make-a-transfer` → **HTTP 403 Forbidden** (Zendesk-hosted support subdomain; separate infrastructure from the main site, which did not 403).

## WebSearch corroboration (third-party, not first-party page fetch)
- OrbitRemit's own blog (`blog.orbitremit.com`) describes the calculator flow as: go to orbitremit.com, select send/receive currencies, click "View Promo Rates," see fee and received-amount instantly — described as usable without logging in to get a quote, though an account is still needed to actually send.
- Fiji-specific fee reported elsewhere as "$1 AUD/NZD flat, free above $10,000."

## Tier assessment
**Tier 2 (public quote calculator) — provisional.** The rate-in-metadata finding (a real AUD/FJD figure served even to a non-JS fetch) plus the blog's own description of a login-free calculator flow support Tier 2. This is provisional because the interactive calculator itself could not be exercised in this session (no working browser tool — see anomalies) and the support-article confirmation attempt 403'd. Recommend a follow-up with a JS-capable browser before treating this as fully confirmed.

## Tier assessment addendum — CAPTCHA/bot wall
No CAPTCHA encountered on the main site; the only block seen was on the separate Zendesk support subdomain, which is not the collection surface a connector would use.

## Confidence flags
- Calculator functionality is inferred from (a) a rate exposed in page metadata and (b) OrbitRemit's own marketing description, not from directly operating the calculator — the Chrome browser tool was unavailable this session (extension not connected), so this could not be confirmed by direct interaction. This is the single most important thing to re-verify before this Tier 2 call is relied on.
- The categorisation question (corridor specialist vs. global MTO) is a judgment call, not a fact — noted above, not resolved.
