# Remitly — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://www.remitly.com/robots.txt (fetched via `curl`)

Verbatim (abridged — most entries are promo/campaign landing pages, not relevant here):

```
User-Agent: *

Disallow: /*/transfer/
Disallow: /*/stilt
[... ~45 promo/campaign/terms-and-conditions path exclusions ...]
Disallow: /*/proof_of_work/
Disallow: /*/log_pow_metric
Disallow: /*/*/share-*-*
Disallow: /*/*/home/complaints$
Disallow: /*/*/home/key-service$
Disallow: /*/*/home/error$
Disallow: /*/*/*/*?fb_campaign=  [... and similar tracking-parameter exclusions ...]
Disallow: /fr/en/home/send_to/morocco
Disallow: /in/*/*
Allow: /in/*/receive-money
Disallow: /r/*
Disallow: /blog/?s=  [... blog search/admin paths ...]
Sitemap: https://www.remitly.com/sitemap.xml
```

No AI-crawler-specific or blanket disallow. `/*/transfer/` (the actual transaction step) is
excluded — consistent with not crawling the authenticated send flow — but country/destination
landing pages and the marketing calculator are not excluded.

## Content — AU page

`https://www.remitly.com/au/en/` (WebFetch): a public quote calculator is present and usable
without login — page showed "You send [AUD] / They receive [currency] / Fee / Total" with a
"Send money" button. **All six Pacific destinations checked were listed:** Fiji, Tonga, Samoa,
Vanuatu, Solomon Islands, Papua New Guinea ("Sending to Fiji" / "Sending to Tonga" / etc — each
as an explicit destination link).

A "Rates and Fees" navigation link exists (referencing e.g. `currency-converter/aud-to-inr-rate`
as a pattern), but a full fee-schedule document was not directly located in this pass.

## Tier assignment

**Tier 2 — public quote calculator, no account required, all six Pacific destinations present.**

Justification: this is the strongest finding in the MTO batch — an unauthenticated calculator
plus confirmed listings for every Pacific destination checked. Matches CLAUDE.md's Tier 2 bar
directly. Not Tier 1: no static published FX table/fee schedule was found (fees appear
per-quote inside the calculator, which is expected for a Tier 2 provider).

## Confidence flags

- The calculator's behaviour was read from the landing page description, not driven
  interactively (no amount/destination actually submitted) — the *existence* of a login-free
  calculator with correct-looking Pacific destinations is well evidenced, but an actual worked
  quote for a Pacific corridor was not captured in this pass.
- "Rates and Fees" page content (whether it amounts to a documented fee schedule) was not
  directly fetched.
