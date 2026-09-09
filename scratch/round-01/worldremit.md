# WorldRemit — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://www.worldremit.com/robots.txt (fetched via `curl`)

Verbatim:

```
User-agent: *
Allow: /account/login
Allow: /account/signup
Disallow: /account/*
Disallow: /umbraco/*
Disallow: /documentverification/*
Disallow: /apple-app-site-association
Disallow: /cdn-cgi/l/email-protection
Sitemap: https://www.worldremit.com/en/sitemap_index.xml
Sitemap: https://www.worldremit.com/en-gb/sitemap_index.xml
Sitemap: https://www.worldremit.com/en-us/sitemap_index.xml
Sitemap: https://www.worldremit.com/en-my/sitemap_index.xml
Sitemap: https://www.worldremit.com/en-nz/sitemap_index.xml
Sitemap: https://www.worldremit.com/en-ca/sitemap_index.xml
Sitemap: https://www.worldremit.com/en-se/sitemap_index.xml
Sitemap: https://www.worldremit.com/en-au/sitemap_index.xml
[... other European locales ...]
Host: https://www.worldremit.com
```

No AI-crawler-specific or blanket disallow. Account/verification paths are excluded (expected
and irrelevant to public collection); general content is permitted. Locale sitemaps confirm
both `en-au` and `en-nz` sites exist.

## Content — AU page

`https://www.worldremit.com/en-au/` (WebFetch): no interactive quote calculator visible on the
page itself — it shows a worked AUD→PHP example, not a live input form, and getting an actual
quote requires proceeding to "Send Money" (unclear from this page alone whether that requires
account creation before a quote is shown, or only before sending). Text seen: *"Your receiver
does not need to have a WorldRemit account"* (about the recipient, not the sender).

Pacific destinations found listed on this page: **Fiji, Samoa**. Tonga, Vanuatu, Solomon
Islands, and Papua New Guinea were **not listed** — this is a single-page finding, not a
confirmed absence (WorldRemit may serve them via a page/flow not surfaced on the AU landing
page).

No dedicated fee schedule or FX rate table page was linked from this page.

## Tier assignment

**Tier 2/3 boundary — provisional Tier 2 for Fiji/Samoa, unconfirmed for the rest.**

Justification: a "quote without account" bar cannot be confirmed from the landing page alone —
the actual quote step wasn't reached. Recommend a follow-up check of the actual send-money
flow (does it show a real quote before requiring signup?) before finalising.

## Confidence flags

- Whether Tonga/Vanuatu/Solomon Islands/PNG are truly absent, or just not surfaced on the AU
  landing page, is unconfirmed — flagged rather than reported as a hard "no."
- Whether obtaining an actual quote (not just the example) requires account creation was not
  directly tested — this is the main gap for the tier call.
- NZ origin is confirmed to exist as a locale (`en-nz` sitemap) but the NZ page itself was not
  fetched in this pass.
