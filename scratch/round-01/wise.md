# Wise — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://wise.com/robots.txt (fetched via `curl`)

Verbatim (abridged — the "bad bot" block is a long standard boilerplate list):

```
User-agent: *
Disallow: /attribution
Disallow: /migrate-cookies
Disallow: /visit/
Disallow: /*/*/currency-converter/
Disallow: /*/swift-bic/
Disallow: /*/help/search
Disallow: /*//publiccurrency-converter/
Disallow: /widget
Disallow: *redirectUrl=*
Disallow: *0=/public*
Disallow: */send-money/?sourceCurrency=*
Disallow: /my/send-money/send-money-to-israel
Allow: *gateway*sourceCurrency=*
Allow: *comparisons*sourceCurrency=*

User-agent: Rogerbot
User-agent: Exabot
[... ~75 more legacy download-manager/offline-browser user-agents, including
     "User-agent: WebFetch" ...]
Disallow: /

Sitemap: https://wise.com/sitemap
```

**Flag:** the long disallowed-user-agent list is a well-known, widely copy-pasted "bad bot"
block (HTTrack, Wget, Teleport Pro, GetRight, etc — circa-2000s download managers and site
rippers). It includes a literal `User-agent: WebFetch` entry, which happens to share a name
with one of this project's own tool names. This is judged to be **coincidental** — the list
predates modern AI tooling by roughly two decades and contains no AI-crawler-specific entries
(no GPTBot, ClaudeBot, CCBot, etc, unlike MoneyGram's robots.txt above). The general
`User-agent: *` block does not disallow site-wide crawling of public content. Recorded here for
the maintainer's awareness rather than treated as a targeted block.

Note: the `/*/*/currency-converter/` path is explicitly disallowed under the general rule —
any standalone currency-converter page is off-limits regardless of the bad-bot-list question.

## Content — AU send-money page

`https://wise.com/au/send-money/` (WebFetch): a public quote calculator, no login required —
page showed a live worked example (1 AUD = 45.0969 PHP) with fee and arrival-time detail.
**Fiji is listed** as a supported destination. Tonga, Samoa, Vanuatu, Solomon Islands, and PNG
were **not found** on this page — single-page finding, not confirmed absent project-wide.

No standalone published FX rate table or fee-schedule document was linked; fee figures are
shown per-transfer inside the calculator ("fees get cheaper the more you send").

## Tier assignment

**Tier 2 for Fiji (confirmed); unconfirmed for other Pacific destinations.**

Justification: a working, login-free quote calculator was directly observed producing a real
number for a sample corridor. Whether it accepts Tonga/Samoa/Vanuatu/Solomon Islands/PNG as
destinations was not tested interactively (would need to actually enter those countries into
the calculator, not just scan the landing page for mentions).

## Confidence flags

- Only Fiji confirmed present; other five Pacific destinations neither confirmed present nor
  absent — landing-page text alone is weak evidence either way.
- The robots.txt currency-converter disallow (`/*/*/currency-converter/`) means any dedicated
  rate-table page (as opposed to the send-money calculator) should not be crawled even though
  it wasn't tested here.
- The `WebFetch`-named entry in the legacy bad-bot list is worth the maintainer's own read —
  recorded as a coincidence, not asserted as one with full certainty.
