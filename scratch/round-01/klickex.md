# KlickEx / KlickEx Pacific — evidence

Date checked: 2026-09-09

**Note on the two PROVIDERS.md candidate rows:** "KlickEx" and "KlickEx Pacific" appear to be **the same entity and the same site**, not two distinct providers. klickex.com's own title tag reads "KlickEx Pacific Limited – Send Money Transfers Across The Pacific", and a WebSearch snippet on a NomuPay/TerraPay partnership describes "KlickEx Pacific Limited" as the operating company behind klickex.com (a NomuPay subsidiary). CLAIMS.md A6 separately notes that SaverPacific's own listing lists both "klickex-low-priority" and "klickex-pacific" as distinct provider slugs — that looks like a SaverPacific cataloguing quirk, not evidence of two real, separately-observable services. Recommend PROVIDERS.md carry one row for this entity, cross-referencing the alternate name, unless you have separate evidence they're genuinely distinct.

## Site
https://klickex.com/ — Auckland-based, NZ FSP-registered (FSP585928 per WebSearch snippet), serving NZ/AU → Tonga, Samoa, Fiji, Vanuatu, PNG, Cook Islands, Solomon Islands (plus non-Pacific corridors) per third-party/search-snippet description.

## robots.txt
`https://klickex.com/robots.txt` → HTTP 200. Cloudflare-managed, notably includes an explicit AI-bot content-use signal and named disallows for AI crawlers:
- Content-signal style directive: `search=yes,ai-train=no,use=reference` (applies broadly per the fetch summary)
- Named user-agents blocked: **ClaudeBot**, GPTBot, Google-Extended, CCBot, Bytespider, meta-externalagent, Applebot-Extended, Amazonbot
- `Disallow: /wp-admin/` with `Allow: /wp-admin/admin-ajax.php` (standard WordPress pattern)
- `Crawl-delay: 10`
- `Sitemap: https://klickex.com/wp-sitemap.xml`

**This site's robots.txt names ClaudeBot specifically as a disallowed agent.** Flagging this verbatim per the brief's instruction to quote applicable directives — any future connector for this provider needs to identify itself honestly (CLAUDE.md §1.5) and would need to reckon with this directive rather than route around it.

## Homepage fetch
`https://klickex.com/` → **HTTP 403 Forbidden** to WebFetch. No body retrieved. This is consistent with active bot-management (Cloudflare) blocking automated fetch, separate from and in addition to the robots.txt AI-bot exclusion above. Not investigated further — no attempt made to retry with a different client or work around the block, per the brief.

## Tier assessment
**Tier 3 — bot wall.** Independent of whatever a public quote page might contain, the site returns 403 to an honestly-identified automated fetch and its robots.txt explicitly names AI crawlers as disallowed. Re-check quarterly per CLAUDE.md §3 in case the posture changes.

## Confidence flags
- Did not see the homepage content itself (403), so FX table / fee schedule / calculator / account-required questions are **unanswered from first-party evidence** — everything about KlickEx's actual offering here comes from WebSearch snippets of third-party pages (Wikipedia, TerraPay press release, SaverPacific), not from klickex.com directly. Treat the destination list above as background, not verified.
- Did not attempt the Chrome browser tool for this one (browser extension was not connected during this session — see anomalies in the final report). A rendered-browser view might behave differently than the raw fetch (e.g. pass a JS challenge) but that was not tested; if it were tested, using a normal browser view to *read* the page is not the same as bypassing the CAPTCHA/bot-wall the brief prohibits, but this needs a judgment call, not an assumption — flagging for the parent rather than deciding it.
