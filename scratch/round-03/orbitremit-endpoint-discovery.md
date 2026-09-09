# OrbitRemit — endpoint discovery, from raw page source only

**Date:** 2026-09-09
**Method:** inspect already-fetched raw page source
(`scratch/round-02/verify/orbitremit-aud-top.body.html`, Round 2's sweep) for the client-side
widget's data source — no execution, no browser, no new fetch beyond what Round 2 already did.

## What was checked

- Absolute-URL scan of the page and its Next.js streaming payload (`self.__next_f.push([...])`
  chunks — part of the raw server-delivered HTML, not executed JS) for anything under `/api/`
  or containing `api`, `rate`, `quote`, `convert`, `fx`: only CDN image asset URLs
  (`cdn.orbitremit.com/images/...`), social links, and other `/currency-converter/<pair>` page
  URLs. No API endpoint found.
- Relative-path scan of the same decoded payload for `/api/...` or rate/quote/convert/fx paths:
  four more `/currency-converter/<pair>` links (`aud-to-fjd`, `aud-to-nzd`, `aud-to-vuv`,
  `aud-to-wst`) — confirms, again, no `nzd-to-top` page exists — and nothing else.

**Hard stop for a true API endpoint: could not identify one from page source in a reasonable
effort.** No further iteration attempted, per Round 3's explicit condition.

## What was found instead — genuinely server-rendered, not an endpoint

While searching, the streaming payload turned out to already contain a full server-rendered
AUD→TOP comparison table (the page's own "compare at a glance" widget), not gated behind any
client-side fetch:

| AUD sent | TOP received | Implied rate |
|---|---|---|
| 5 | 8.67 | 1.734000 |
| 10 | 17.34 | 1.734000 |
| 25 | 43.34 | 1.733600 |
| 50 | 86.68 | 1.733600 |
| 100 | 173.36 | 1.733600 |
| 500 | 866.82 | 1.733640 |
| 1,000 | 1,692.37 | 1.692370 |
| 5,000 | 8,296.73 | 1.659346 |
| 10,000 | 16,552.18 | 1.655218 |

This is not one clean rate. Fitting a two-tier model (a flat rate up to some threshold, a
different flat rate beyond it) against these figures: a promotional rate of ~1.73364 TOP/AUD
applies to the first 500 AUD, and a standard rate of ~1.6511 TOP/AUD applies beyond that —
matches every row to within rounding. This lines up exactly with OrbitRemit's own marketing
copy already on record (`scratch/round-01/orbitremit.md`): "Free transfer + exclusive promo
rate for new customers, with the promotional rate capped at the first $500."

Separately, the page's own `<meta name="description">` states a third figure — "$1 AUD =
1.69237 TOP" — which matches neither the promotional nor the standard rate implied by the
table. All three figures are genuine and server-rendered; none is reconciled into one "the
rate" here. The connector built against this (`collect/orbitremit/connector.py`) uses the 500
AUD table row specifically — the last one still at the promotional rate — and discloses the
meta-description discrepancy in every observation's `status_detail`, per CLAUDE.md §1.1: never
present one number as "the" rate when the source itself shows more than one.

No separate fee amount was found anywhere in raw bytes on this page — the table's implied rate
already blends whatever margin/fee OrbitRemit applies; `fee` is stored `null`, not decomposed
or assumed.
