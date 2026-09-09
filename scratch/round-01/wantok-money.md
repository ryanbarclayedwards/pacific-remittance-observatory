# WanTok Money — evidence

Date checked: 2026-09-09

## URLs fetched
- https://wantokmoney.com/robots.txt — FAILED (DNS)
- https://www.wantokmoney.com/robots.txt — FAILED (DNS)
- https://wantok.vu/robots.txt — OK (marketing subsite, Vanuatu)
- https://wantok.to/robots.txt — OK (marketing subsite, Tonga)
- https://wantok.vu/wantok-money/ — OK
- https://wantok.to/wantok-money/ — OK

## Anomaly (verbatim tool errors)
```
getaddrinfo ENOTFOUND wantokmoney.com
```
```
getaddrinfo ENOTFOUND www.wantokmoney.com
```
The domain that both marketing subsites (`wantok.vu`, `wantok.to`) point users to as the actual transactional platform — "Simply visit www.wantokmoney.com and start using your digital wallet" — does not resolve in DNS at all, from either the apex or `www` hostname. This is not a bot wall or block; the domain appears to not exist / not be configured, as of the check date. Could not confirm via web.archive.org — that tool was unavailable this session ("Claude Code is unable to fetch from web.archive.org").

## wantok.vu/robots.txt (verbatim)
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

Sitemap: https://wantok.vu/sitemap_index.xml
```

## wantok.to/robots.txt (verbatim)
```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

Sitemap: https://wantok.to/sitemap_index.xml
```
Both permit crawling outside wp-admin.

## Findings (from the marketing pages, since the platform itself is unreachable)
- Both marketing pages describe a mobile-wallet transfer service "across the Pacific" but neither states specific origin countries (no explicit mention of Australia or New Zealand on either page checked) or a specific destination country beyond the implied Vanuatu/Tonga split by domain.
- No fee schedule or FX rate table on either marketing page.
- No quote calculator on either marketing page — both simply link out to the (unreachable) wantokmoney.com.
- Login/account: unclear from marketing copy alone ("start using your digital wallet") whether a quote can be seen pre-login; irrelevant here since the platform itself couldn't be reached.

## Tier assessment
Tier 3 — the actual transactional domain does not resolve. Cannot check its robots.txt, FX table, fee schedule, or calculator because the site is unreachable. The two marketing subsites are informational only and expose no quote surface themselves.
