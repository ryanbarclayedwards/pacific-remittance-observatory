# Western Union — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://www.westernunion.com/robots.txt (fetched via `curl`)

Verbatim:

```
User-agent: *
Disallow: /web-inf/
Disallow: /pdf/
Disallow: /*interstitialPage*
Disallow: /*kycVerification*
Disallow: /*session-expired*
Disallow: /*site-restriction*
Disallow: /*temporary-outage.html*

Sitemap: https://www.westernunion.com/sitemap-index.xml
[... 17 more sitemap entries, mostly locale/section indexes ...]
```

No AI-crawler-specific or blanket disallow. General content paths (currency converter,
country pages) are permitted; only internal/technical paths (KYC verification, session-expired
pages, PDFs) are excluded.

## Content — currency converter

`https://www.westernunion.com/au/en/currency-converter.html` (WebFetch): a public currency
converter, reachable without login, covers all six Pacific currencies checked — FJD, TOP, WST,
VUV, SBD, PGK. Page text: *"Convert popular currencies at effective exchange rates with our
currency converter calculator"* and *"Exchange Rates and Fees shown are estimates, vary by a
number of factors including payment and payout methods, and are subject to change."* A "Send
money" link leads to the actual quote/send flow — not fetched separately in this pass, so
whether *that* flow requires login before showing a real quote is unconfirmed.

No standalone fee-schedule document was found linked from this page.

## Account required? / bot wall

Not established either way for the actual send-money quote flow (only the standalone
converter was checked). No CAPTCHA or block encountered on the converter page itself.

## Tier assignment

**Tier 2 (provisional) — public currency converter confirmed; actual quote flow (fees,
delivery options) not yet verified as account-free.**

Justification: a public FX converter without login covering all six Pacific currencies is
confirmed. CLAUDE.md's Tier 2 bar is "a public page returns a quote for fixed inputs without
an account" — the converter gives a rate but the page's own wording flags rates/fees as
"estimates" pending the actual send flow, which was not tested. Recommend confirming the
`/send-money` flow before treating this as settled.

## Confidence flags

- The `Send money` quote flow (real fees, delivery method-specific) was not independently
  fetched — only the standalone converter page. This is the main gap.
- No fee-schedule document (as distinct from the converter) was located.
