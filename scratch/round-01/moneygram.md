# MoneyGram — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://www.moneygram.com/robots.txt (fetched via `curl`, one request)

Verbatim (relevant lines):

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

Followed by a second `User-agent: *` block disallowing internal paths
(`/AgentConnect*`, `/Market/*`, `/MGI*/*`, `/theme/*`, `/WCM/*`, `/WCS/*`, `/wps/*`,
`/brand-center`), a 5-second crawl-delay, and a sitemap reference.

## Decision to stop

`User-agent: ClaudeBot` carries an unconditional `Disallow: /` for the entire site. This
recon session is running as Claude. Per CLAUDE.md §1.5 ("Respect robots.txt... Identify the
collector honestly in the user agent, with a contact URL"), the honest identification of an
Anthropic-model-based collector falls under this rule. No further automated requests were
made to moneygram.com beyond the robots.txt fetch itself.

One earlier WebFetch attempt at `https://www.moneygram.com/au/en/` (before the robots.txt
disallow was discovered) returned **HTTP 403 Forbidden** — consistent with active bot-wall
enforcement, independent of the robots directive.

## Tier assignment

**Tier 3 — unobservable (robots.txt disallow).**

Justification: robots.txt explicitly disallows ClaudeBot from the entire site; an honestly
self-identified automated collector for this project is exactly the kind of client the
directive targets. Combined with an independent 403 on a page-not-behind-login, this is
treated as closed rather than probed further. No FX table, fee schedule, or calculator URL
was checked as a result — checking further would have required continuing to crawl a site
that has told this class of client not to.

## Confidence flags

- FX table / fee schedule / calculator existence, AU/NZ origin, and Pacific destination
  coverage are **not established** for MoneyGram — the robots block was hit before those
  checks. This is a gap, not a "no."
- The general `User-agent: *` block is `Allow: /` with `Content-Signal: ai-train=no,
  use=reference` — i.e. non-AI crawlers (a plain `requests`-based collector with a generic
  UA) are not blocked by the general rule. Only the AI-crawler-specific rules disallow.
  Whether that means a *human-identified, non-AI-branded* Python collector would be
  robots-compliant while an AI-agent-run one is not is a real ambiguity worth the
  maintainer's attention — flagged in the round report rather than decided here.
