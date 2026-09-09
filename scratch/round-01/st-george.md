# St.George Bank (stgeorge.com.au) — evidence, checked 2026-09-09

St.George is part of Westpac Group (robots.txt below references a shared `/ocg-westpac/` path), so its infrastructure and rates likely trace back to Westpac's back end — noted, not confirmed.

## robots.txt
URL: https://www.stgeorge.com.au/robots.txt (WebFetch)
```
# /robots.txt file for http://www.stgeorge.com.au/
User-agent: *
Disallow: /goldservice
Disallow: /gold
Disallow: /personal/bank-accounts/transaction-accounts/complete-freedom-a
Disallow: /personal/bank-accounts/transaction-accounts/complete-freedom-b
Disallow: /personal/bank-accounts/transaction-accounts/complete-freedom-c
Disallow: /personal/bank-accounts/savings-accounts/maxi-saver-a
Disallow: /personal/bank-accounts/savings-accounts/maxi-saver-b
Disallow: /personal/bank-accounts/savings-accounts/maxi-saver-c
Disallow: /ocg/
Disallow: /ocg-westpac/
Disallow: /content/sbg/stg/en/_services/serialiser/
Disallow: /_services/
Disallow: /test/
Disallow: /tandt/
Disallow: /widgetConfig/
Disallow: /bt-calc/
Disallow: /locateus-ios*
Disallow: /locateus-android*
Disallow: /content/dam/stg/downloads/styleguides/
Sitemap: https://www.stgeorge.com.au/sitemap.xml
Sitemap: https://www.stgeorge.com.au/sitemap-locator.xml
```
Note `/bt-calc/` is disallowed — an internal calculator path is explicitly blocked from crawlers (unclear if this is the currency converter or an unrelated "BT" — BT Financial Group — calculator; not confirmed either way). The currency converter examined below is at `/help/calculators/currency-converter`, a different path, not disallowed.

## Send money overseas page
URL: https://www.stgeorge.com.au/personal/international-payments/send-money-overseas
- Fee schedule: foreign-currency transfer $0, AUD transfer $20 (both confirmed exact figures).
- Currency converter linked: https://www.stgeorge.com.au/help/calculators/currency-converter — described as "Convert one currency value to another with our simple to use calculator." Only FJD is confirmed named as a Pacific currency on this particular page; no Pacific destination country named explicitly.

## Currency converter page
URL: https://www.stgeorge.com.au/help/calculators/currency-converter
WebFetch could not confirm whether this is a live interactive converter or a static table, could not confirm the currency list (TOP/WST/VUV/SBD/PGK/FJD not found in the fetched content), and could not confirm whether login is required. Page mentions "all available currencies" being sent by daily email on request, without listing them.

## Tier assignment
**Tier 2 (probable), pending confirmation.** A public fee schedule with exact figures exists, and a currency-converter tool is linked and not blocked by robots.txt — but its actual behaviour (live calculator vs. static list, currency coverage, login requirement) could not be confirmed from static fetches this round.

## Confidence flags
- The `/bt-calc/` robots.txt disallow is unexplained — flagged in case it turns out to be the FX calculator's backing path (would change this from Tier 2 to Tier 3).
- Currency converter functionality entirely unconfirmed — no browser available this session to test interactively.
- Because St.George shares Westpac Group infrastructure, its findings should be read alongside the Westpac AU entry rather than treated as fully independent.
