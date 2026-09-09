# Central Bank of Solomon Islands (CBSI) — benchmark scoping evidence

Date checked: 2026-09-09
Domain: www.cbsi.com.sb

## robots.txt

URL: https://www.cbsi.com.sb/robots.txt — HTTP 200. Cloudflare-managed "content signals"
format:

```
User-agent: *
Content-Signal: search=yes,ai-train=no,use=reference
Allow: /

User-agent: Amazonbot
Disallow: /
User-agent: Applebot-Extended
Disallow: /
User-agent: Bytespider
Disallow: /
User-agent: CCBot
Disallow: /
User-agent: ClaudeBot
Disallow: /
User-agent: CloudflareBrowserRenderingCrawler
Disallow: /
User-agent: Google-Extended
Disallow: /
User-agent: GPTBot
Disallow: /
User-agent: meta-externalagent
Disallow: /
```

**Flag:** this explicitly disallows the named user-agent `ClaudeBot`, and sets
`ai-train=no` for everyone under the generic `User-agent: *` block (which otherwise
`Allow: /`s general crawling). A future automated collector must identify itself honestly per
CLAUDE.md §1.5 with its own name and contact URL — it would not literally be the string
"ClaudeBot" — but the intent of this robots.txt (an AI-crawler blocklist) is unambiguous and
the ethical reading is closer to "this site does not want AI systems collecting its content"
even though a literal per-user-agent match would not catch a distinctly-named collector. This
is a judgement call the maintainer should make explicitly, not one this reconnaissance pass is
resolving. See same flag on Bank of PNG's robots.txt, which is more explicit.

## Where rates are published

`https://www.cbsi.com.sb/data-statistics/exchange-rates/todays-exchange-rates`

HTML table, 8 currency rows against SBD at time of check:

| Currency | Rate | 12-month trend |
|---|---|---|
| USD | 0.1248 | Stable |
| GBP | 0.0922 | Stable |
| EUR | 0.1074 | Stable |
| AUD | 0.1729 | Falling |
| NZD | 0.2131 | Rising |
| JPY | 19.22 | Falling |
| SDR | 0.0909 | Stable |
| CNY | 0.8372 | Stable |

Plus an "Exchange Rate Index" figure (108.9000). Page states "Exchange rates are published
around 9:00 am daily except on public and bank holidays" and shows "Last updated: September 9,
2026" alongside a "previous rate" column dated **September 2, 2026** — a full week earlier.

## Format

HTML table only. No download link for historical data found on this page; a "Download centre"
exists elsewhere under Data & Statistics (`/data-statistics/datasets-downloads/download-centre`)
but was not confirmed to contain exchange-rate history — not visited in this pass.

## Update frequency — confidence flag

The page's own text claims daily publication (~9am, except holidays), but the "previous rate"
comparison column shown is dated a week prior (2 Sep vs 9 Sep), not the prior business day.
**This is ambiguous from a single observation**: it could mean (a) the "previous" column is
deliberately a week-over-week trend reference rather than "yesterday," which is compatible
with true daily updates, or (b) the page in fact only refreshes weekly despite the "daily"
wording. Resolving this needs a second check on a different day (e.g. the following Monday) to
see whether "today's" figure and the "previous" date both roll forward by one day or by a
week. Not resolved here — flagged for a follow-up check, not guessed.

## Historical data

No historical archive or download confirmed accessible from the daily-rates page itself in this
pass (see Format, above).

## Stability assessment

Basis: page path is a clean, non-dated CMS route (`/data-statistics/exchange-rates/todays-exchange-rates`),
similar in kind to the Joomla-routed pages — no filename/date-keying observed. No history of
change was checked (single observation).
