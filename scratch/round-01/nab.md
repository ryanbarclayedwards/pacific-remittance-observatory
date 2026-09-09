# National Australia Bank (nab.com.au) — evidence, checked 2026-09-09

## robots.txt
URL: https://www.nab.com.au/robots.txt (WebFetch)
```
User-agent: *

Disallow: /cgi-bin/
Disallow: /mobile
Disallow: /vgnmedia
Disallow: /search
Disallow: /common
Disallow: /static
Disallow: /content/experience-fragments
Disallow: /Internet_Banking
Disallow: /automation
Disallow: /content/dam/nab/documents/assets
Disallow: /maintenance
Allow: /common/privacy-policy
Allow: /common/website-disclaimer

Sitemap: https://www.nab.com.au/sitemap.xml
```
Does not block the international-banking pages examined.

## International transfer page
URL: https://www.nab.com.au/personal/international-banking/transfer-money-overseas/additional-information
- Fee prose only, not a structured table: "no fee for international money transfers sent by NAB Internet Banking when made in foreign currency. If you are transferring Australian dollars the fee is $30." Branch: $30.
- No public calculator link found for non-customers; page describes real-time rates for logged-in users only.
- Extensive Pacific destination list confirmed: American Samoa, Cook Islands, Fiji, French Polynesia, Guam, Kiribati, Marshall Islands, Micronesia, Nauru, New Caledonia, Niue, Northern Mariana Islands, Palau, Pitcairn, Samoa, Solomon Islands, Tokelau, Tonga, Tuvalu, Vanuatu, Wallis and Futuna — the broadest destination list found across all ten banks in this batch.

## FX rates page
URL: https://www.nab.com.au/personal/international-banking/foreign-exchange-rates
- WebFetch: page titled "Foreign exchange calculator and rates," directs to "our foreign exchange calculator," but no actual rate table or working calculator rendered in the fetched content. An "Important Information" section reportedly failed to render ("Apologies but the Important Information section you are trying to view is not displaying properly at the moment") — this may be a genuine site fault at check time, not necessarily representative.
- Direct `curl` (honest UA), 468,276 bytes, HTTP 200: **no occurrence of TOP, WST, VUV, SBD, PGK or FJD anywhere in the raw server-delivered HTML.** Rate data (if any) is client-rendered.

## Tier assignment
**Tier 3 (unobservable this round).** No fee table (prose only, two figures), no rate table reachable by a plain HTTP client, no public calculator confirmed for non-logged-in use. The destination list is the widest of any bank checked, which makes NAB worth re-checking once/if a data endpoint is found — but nothing here supports a public reconstruction today.

## Confidence flags
- The "Important Information section... not displaying properly" message could indicate either a genuine transient fault (worth re-checking) or a component that never renders without JS/login — not distinguished this round.
- Did not test the calculator interactively (no browser available). If it turns out to work for anonymous users, NAB should be reconsidered for Tier 2.
