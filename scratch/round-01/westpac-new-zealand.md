# Westpac New Zealand (westpac.co.nz) — evidence, checked 2026-09-09

## robots.txt and content page — both blocked
URL: https://www.westpac.co.nz/robots.txt
URL: https://www.westpac.co.nz/foreign-exchange/send-money-to-or-from-overseas/

Both tried via WebFetch (two separate attempts each) and via direct `curl` with an honestly-identified UA (`PacificRemittanceObservatory-recon/0.1`, contact URL included). **All four requests returned HTTP 403.** The `curl` response body (identical for both URLs) is a branded Akamai/Adobe-instrumented error page:
```html
<meta name="ak-status-code" content="403">
...
var digitalData = {
  page: {
    pageInfo: {
      pageName: "wbcnz:www:sitedownerror",
      pageType: "OutagePage"
    }
  }
};
```
This is a bot-wall/WAF response (Akamai), not a normal 403-with-reason or a robots.txt-level instruction — it fires even for `robots.txt` itself, before any crawling directive could be read. There is no robots.txt to consult because the block happens earlier in the request pipeline.

## Tier assignment
**Tier 3 (blocked).** Automated access is refused outright, including to robots.txt, for an honestly-identified client. Per CLAUDE.md §1.5, this is recorded as blocked and not worked around — no user-agent spoofing or other bypass was attempted.

## Confidence flags
- Not established whether this WAF blocks all non-browser clients uniformly, or specifically flagged this collector's IP/UA/request pattern — the distinction doesn't change the classification (either way, the honestly-identified collector cannot reach the site) but would matter if the maintainer ever wanted to understand *why*.
- Westpac AU (a related but operationally separate entity/domain, westpac.com.au) was freely accessible throughout this session — the block is specific to the .co.nz domain/infrastructure, not a general Westpac-brand policy.
