# Ria Money Transfer — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://www.riamoneytransfer.com/robots.txt (fetched via `curl`)

Verbatim (relevant lines):

```
User-agent: *
Allow: /
Disallow: /*?_rsc=

User-agent: meta-externalagent
Disallow: /

Sitemap: https://www.riamoneytransfer.com/sitemap.xml
```

No AI-crawler-specific disallow (no ClaudeBot rule). General crawling is permitted; the only
site-wide disallow targets Meta's AI-training crawler. `?_rsc=` query strings (Next.js React
Server Component prefetch artefacts) are excluded as non-canonical duplicates — irrelevant to
this project.

## Origin coverage

- `https://www.riamoneytransfer.com/` served the en-au locale by default (AUD currency shown)
  when fetched without a locale path. **Australia confirmed as a send-from origin.**
- New Zealand is not mentioned on the AU homepage, but a `sitemap-rates/en-nz.xml` sub-sitemap
  exists (see below), implying an NZ-locale site exists even though it wasn't linked from the
  page fetched. `https://www.riamoneytransfer.com/en-au` and `/en-nz` path variants were not
  independently confirmed to resolve — inferred from the sitemap locale naming only.
- Direct fetch of `https://www.riamoneytransfer.com/au` and `/nz` (no `en-` prefix) both
  returned **HTTP 500** — wrong path guesses, not a block (the working locale prefix appears to
  be `en-au`, per the sitemap).

## Pacific destination coverage — currency pages exist, transfer service unconfirmed

Sitemap `https://www.riamoneytransfer.com/sitemap.xml` lists 36 regional
`sitemap-rates/<locale>.xml` sub-sitemaps. Within `sitemap-rates/en-au.xml` and
`sitemap-rates/en-nz.xml`, found `rates-conversion` URLs for FJD (Fiji), TOP (Tonga), WST
(Samoa), VUV (Vanuatu), SBD (Solomon Islands), and PGK (PNG). No matches for Kiribati (AUD is
the currency there — not distinguishable) or Tuvalu (also AUD) via currency-code search.

**These are currency-conversion reference pages, not confirmed transfer-service pages.**
Fetched `https://www.riamoneytransfer.com/en-au/rates-conversion/?From=AUD&To=FJD&Amount=200`
directly: it shows a mid-market reference rate (1.00 AUD = 1.58576111 FJD) with the text *"We
use the mid-market rate for reference only. Login to see actual send rates."* No fee, no
delivery method, no send flow — just a converter widget with a login prompt for real rates.

Tried `https://www.riamoneytransfer.com/en-au/send-money/fiji` as a guess at an actual
country-service landing page: **HTTP 404**. This specific URL guess was wrong, not proof that
no such page exists under a different path — flagged below.

## Quote calculator

Homepage (`/`) shows a prominent quote widget with a worked example (100 AUD → 4,622.10 PHP,
0 AUD fee "for first transfer") for a Philippines-destination transfer. **Whether this widget
accepts Fiji/Tonga/Samoa/Vanuatu/Solomon Islands/PNG as destination options, and whether
selecting one returns a real quote without login, was not tested interactively** — this fork
prioritised throughput over an interactive per-destination browser test given the batch size.
This is the single largest gap in the Ria findings.

## Account required?

The only rate figures actually reachable without logging in are mid-market reference rates
explicitly labelled as not the real send rate. "Login to see actual send rates" is stated
directly on the rates-conversion page.

## CAPTCHA / bot wall

None encountered in the fetches made (WebFetch requests all succeeded except for the two wrong
path guesses, which 500'd/404'd rather than being blocked).

## Tier assignment

**Tier 3 — unobservable as currently understood, with a flagged gap.**

Justification: the only unauthenticated numbers on the site are explicitly-labelled mid-market
reference rates ("login to see actual send rates"), not real quotes — this fails the Tier 2
bar of "a public page returns a quote for fixed inputs without an account." No public FX table
or fee schedule was found. However, this is provisional: the homepage quote widget was not
tested interactively for Pacific destinations, and it is plausible — Ria does market itself as
covering "190+ countries" — that entering Fiji/Tonga/etc. into that widget returns a real quote
pre-login the way the PHP example did. **Recommend a follow-up interactive check before this
Tier 3 call is treated as final.**

## Confidence flags

- NZ origin support is inferred from sitemap locale naming (`en-nz`), not from a loaded NZ
  page — not directly observed.
- Whether Ria actually delivers to Fiji/Tonga/Samoa/Vanuatu/Solomon Islands/PNG (versus just
  publishing SEO currency-converter pages for those currencies) is **not confirmed either way**.
  Currency-code presence in the rates sitemap is weak evidence of an actual transfer corridor.
- The homepage quote widget's behaviour for Pacific destinations specifically was not tested —
  this is the main reason the Tier 3 call above is flagged provisional rather than settled.
- Kiribati and Tuvalu both use AUD, so a currency-code sitemap search cannot distinguish
  "serves Kiribati/Tuvalu" from "doesn't" — would need a destination-country page test instead.
