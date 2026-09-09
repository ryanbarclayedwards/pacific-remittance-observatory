# OFX — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://www.ofx.com/robots.txt (fetched via `curl`)

Verbatim:

```
User-agent: *
Disallow: /sitecore/
Disallow: */aggregate/$
Disallow: */aggregate$
Sitemap: https://www.ofx.com/en-au/sitemap.xml
Sitemap: https://www.ofx.com/en-us/sitemap.xml
Sitemap: https://www.ofx.com/en-ca/sitemap.xml
Sitemap: https://www.ofx.com/en-gb/sitemap.xml
Sitemap: https://www.ofx.com/en-nz/sitemap.xml
Sitemap: https://www.ofx.com/en-hk/sitemap.xml
Sitemap: https://www.ofx.com/en-sg/sitemap.xml
Sitemap: https://www.ofx.com/en-ie/sitemap.xml
[... matching news-sitemap entries ...]
```

No AI-crawler-specific or blanket disallow; only CMS-internal (`/sitecore/`) and an
`/aggregate` endpoint excluded. Both `en-au` and `en-nz` sitemaps confirm AU and NZ locales
exist.

## Content — AU page

`https://www.ofx.com/en-au/` (WebFetch): a public currency converter tool exists, reachable
without login ("Currency converter" under Tools and Resources). Page states OFX supports "30+
currencies" but does not enumerate them on this page — a "full list of our supported
currencies" link exists but its target content wasn't fetched in this pass. None of the six
Pacific currencies (FJD, TOP, WST, VUV, SBD, PGK) were directly named on the page fetched.

Page also references "Exchange rates," "Historical exchange rates," and "Daily currency
update" resources — consistent with a published daily FX rate table existing, though the
specific rate-table URL wasn't confirmed. No fee-schedule link was found (OFX is known to
charge via FX margin rather than a flat fee schedule, but this wasn't confirmed on-page).

A follow-up guess at a specific currency-pair page,
`https://www.ofx.com/en-au/currency-pairs/aud-fjd/`, returned **404** — an unconfirmed wrong
URL pattern, not evidence Fiji is unsupported.

## Tier assignment

**Unconfirmed — insufficient evidence to assign a tier with confidence.**

Justification: OFX plausibly has published daily rates (Tier 1-like) or a login-free converter
(Tier 2-like), but this pass did not confirm Pacific-currency coverage at all. Recommend not
publishing a tier call for OFX from this evidence; needs a follow-up pass that finds the actual
supported-currencies list and the real rate-table URL.

## Confidence flags

- **No tier is asserted with confidence for OFX** — flagged explicitly rather than guessed.
- Whether OFX serves any of the six Pacific currencies is unconfirmed both ways.
- The "full list of supported currencies" page (linked but not fetched) is the obvious next
  step and was not reached in this pass.
