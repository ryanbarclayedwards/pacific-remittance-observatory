# HSBC Australia (hsbc.com.au) — evidence, checked 2026-09-09

## Material anomaly, checked first
URL: https://www.nab.com.au/personal/international-banking/foreign-exchange-rates (n/a — see HSBC page below)
URL: https://www.hsbc.com.au/foreign-exchange/real-time-rates/ — WebFetch confirms the page opens with: **"HSBC will be closing its retail banking business in Australia over the next 18 months. You can no longer apply for new products and services."**
This is a material, dated finding: whatever tier HSBC AU is assigned, it is a retail service in wind-down as of the check date (2026-09-09), which bears directly on whether it is worth building a connector for regardless of technical observability.

## robots.txt
URL: https://www.hsbc.com.au/robots.txt
Fetched via curl with honest UA. Verbatim:
```
User-agent: *
Disallow: /1/*
Disallow: /multiapp/*
Disallow: /webapps/*
Disallow: /messages/
Disallow: /*ep_testing
Disallow: /*ep_login
Disallow: /ep_docs/*.pdf
Disallow: /ep_internal/*.pdf
Disallow: /*hsbc-token-testing*
Disallow: /cms-dashboard*
Disallow: /cms-admin*
Disallow: /content/dam/hsbc/ar/promos*
Disallow: /content/dam/hsbc/gr/promos*
Disallow: /content/dam/hsbc/ca/promos*
Disallow: /content/dam/hsbc/om/promos*
Disallow: /content/dam/hsbc/am/promos*
Disallow: /branch-login/*
Disallow: /staff-emergency-comms/*.html
Disallow: /remote-access-instructions/*.html
Disallow: /remote-access/logon
Disallow: /remote-access/*.html
Disallow: /cgi-bin
 
sitemap: https://www.hsbc.com.au/sitemaps.xml
```
Does not block the FX/international pages examined.

## International transfers page
URL: https://www.hsbc.com.au/foreign-exchange/international-transfers/
- Correspondent Bank Cover Fee: AUD 30, disclosed. No transfer fee for "Global Money Transfers" between HSBC accounts / via app for many currencies.
- No public quote calculator usable without login found — page directs customers to the mobile app to initiate a transfer.
- No Pacific Island country or currency named on this page.
- Links a separate exchange-rates resource ("HSBC Exchange Rates") but the linked destination was 404 when guessed (`/foreign-exchange/rates/`); the actual live-rate page found via search, `/foreign-exchange/real-time-rates/`, did not render a rate table for the six Pacific currencies in the fetched content — only the retail-closure banner and a link onward to `/calculators/HSBC-exchange-rates/`, not independently tested.

## Tier assignment
**Tier 3 (unobservable this round).** No public calculator confirmed without login, no Pacific currency/destination named anywhere examined, and no rate table content confirmed. Independently of the technical tier, the retail-banking wind-down (18-month closure notice) is a strong reason not to prioritise HSBC AU regardless.

## Confidence flags
- `/calculators/HSBC-exchange-rates/` was found via search but not fetched/tested this round — small chance it is a working public calculator; low priority to chase given the closure notice.
- The retail-closure statement's exact scope (all products? all channels? a specific timeline start date?) was not further investigated — quoted verbatim above, not paraphrased, but no corroborating press release was checked. Treat as UNCONFIRMED pending a second source if it matters to any decision.
