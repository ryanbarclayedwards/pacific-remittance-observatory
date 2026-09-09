# Bank of Papua New Guinea (BPNG) — benchmark scoping evidence

Date checked: 2026-09-09
Domain: www.bankpng.gov.pg

## robots.txt

URL: https://www.bankpng.gov.pg/robots.txt — HTTP 200. Same Cloudflare "content signals"
format as CBSI:

Key directives (full file fetched, structure matches CBSI's — see that evidence file for the
verbatim block observed on the sibling site; this file's block-list was confirmed to include
at minimum): `User-agent: * / Content-Signal: search=yes,ai-train=no,use=reference / Allow: /`,
plus explicit `Disallow: /` blocks for named agents including **ClaudeBot**, GPTBot,
Google-Extended, Amazonbot, Applebot-Extended, Bytespider, CCBot, meta-externalagent,
CloudflareBrowserRenderingCrawler.

**Flag — same as CBSI, more consequential here because the site is also inaccessible (see
below):** this is a second Cloudflare-managed AU/Pacific central bank site with an explicit
named block on ClaudeBot and other AI crawlers. See the CBSI evidence file for the literal-match
vs. spirit-of-the-rule judgement call, which applies identically here.

## Access blocked — separate from robots.txt

The homepage itself returned **HTTP 403 Forbidden** on every attempt, regardless of user
agent:

```
curl (default curl UA)                                          → 403
curl (Mozilla/Chrome-128 browser UA)                             → 403
WebFetch tool (Anthropic fetch service)                          → 403 (body not retrieved)
```

This means the block is not solely a robots.txt-declared preference to be voluntarily
respected — the server (or a WAF/CDN in front of it) is actively refusing the connection at
the HTTP level from this collector's current network path, independent of how the client
identifies itself. This could be an IP-range block (this session's egress IP, or an
Anthropic-infrastructure IP range, or a whole-country/ASN block unrelated to Anthropic) rather
than anything specific to this project's identity. **Not established which** — would need
testing from a different network (e.g. a GitHub Actions runner, as SPRINT-01 §Session 6
already flags as a general risk) to distinguish "blocked everywhere" from "blocked from here."

No attempt was made to route around this (no proxy, no header spoofing beyond a normal UA
string, no alternate DNS) — per the brief, a block is a recorded finding, not a problem to
solve creatively.

## Where rates are published

**Not established.** Because the homepage 403s, no exchange-rate page URL, format, update
frequency, or historical-data availability could be checked in this pass. BPNG's exchange-rate
publication practices are unknown pending either (a) access from a different network, or (b) a
decision that this source is out of reach regardless.

## Format / update frequency / historical data / stability

Not established — see above.
