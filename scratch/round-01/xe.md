# Xe Money Transfer — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://www.xe.com/robots.txt (fetched via `curl`)

Verbatim (abridged — the "bad bot" block is the same standard boilerplate list seen on Wise):

```
User-Agent: *
Disallow: /fxwidgets/
Disallow: /migration/
Disallow: /currencytransfers/
Disallow: /logout
Disallow: /logout/*

User-Agent: Rogerbot
[... ~75 more legacy download-manager/offline-browser user-agents, including
     "User-Agent: WebFetch" ...]
Disallow: /

Host: https://www.xe.com/
Sitemap: https://www.xe.com/sitemap.xml
```

Same coincidental `WebFetch`-named entry in the same widely-copy-pasted legacy bad-bot list as
Wise's robots.txt — see the note in `scratch/round-01/wise.md`; not treated as a targeted
block. The general `User-Agent: *` rule permits public content; `/fxwidgets/`,
`/currencytransfers/`, and `/migration/` are excluded, which likely covers Xe's own rate-widget
and send-money transaction paths.

## Content — AU send-money page

`https://www.xe.com/en-au/send-money/` (WebFetch): page text referenced *"Get a live,
bank-beating money transfer rate for your chosen currency"* but the actual quote appeared to
require registration/login at `account.xe.com`. No Pacific destination (Fiji, Tonga, Samoa,
Vanuatu, Solomon Islands, PNG) was mentioned on this page. Two follow-up path guesses —
`/en-au/send-money/to-fiji/` and (implicitly) a currency-pair page — both returned **404**;
these are unconfirmed wrong-path guesses, not evidence that Xe doesn't serve Fiji.

No published FX rate table or fee schedule was found linked from this page (Xe is well known
externally for its currency-converter reference tool, but that path — `/currencytransfers/` —
is explicitly disallowed by robots.txt in any case, and the separate `xe.com` currency
converter is a distinct product from Xe Money Transfer).

## Tier assignment

**Tier 3 (provisional) — no login-free quote surface found; Pacific destination coverage
unconfirmed.**

Justification: the send-money landing page pushes toward login before showing a rate, and no
Pacific destination was confirmed served at all. This is a weaker basis than the other MTOs
checked in this batch — genuinely unconfirmed rather than cleanly established as blocked.

## Confidence flags

- **This is the least-confirmed finding in this batch.** Only one page was fetched; the actual
  send-money flow, the AU country-destination list, and whether Xe serves any Pacific corridor
  at all remain open. Recommend a follow-up pass before publishing this as a firm Tier 3.
- The `/currencytransfers/` and `/fxwidgets/` robots.txt disallows were not tested against —
  correctly avoided in this pass, but they also block the paths most likely to hold the rate
  table, which structurally limits how far a robots-compliant automated check can go on Xe.
