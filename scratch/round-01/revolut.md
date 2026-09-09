# Revolut — evidence

Date checked: 2026-09-09

## robots.txt

URL: https://www.revolut.com/robots.txt (fetched via `curl`)

Verbatim:

```
# *
User-agent: *
Allow: /sitemap-*.xml*
Disallow: /api/
Disallow: */email-verification
Disallow: */help-centre
Disallow: /*.json$
Disallow: /*_buildManifest.js$
Disallow: /*_middlewareManifest.js$
Disallow: /*_ssgManifest.js$
Disallow: /*embedded
Disallow: /*/query:*
Disallow: *?*
Allow: *?amount=
Allow: *?amount-to=
Disallow: */api/*amount*

# Localisation send money
Disallow: /en-AT/money-transfer/send-money
Disallow: /en-BE/money-transfer/send-money
[... ~20 more European-locale /money-transfer/send-money disallows;
     no en-AU or en-NZ entry present in this list ...]
Disallow: */international-transfers/

# Localisation currency converter
Disallow: /en-ES/currency-converter/convert
[... ~19 more European-locale currency-converter/convert disallows;
     no en-AU or en-NZ entry present ...]

Sitemap: https://www.revolut.com/sitemap-index.xml
Host: https://www.revolut.com
```

No AI-crawler-specific or blanket disallow. Notably, the locale-specific `/money-transfer/
send-money` and `/currency-converter/convert` disallows are enumerated per-country and do
**not** include an `en-AU` or `en-NZ` entry — those AU/NZ paths are not robots-excluded (unlike
the ~20 European locales listed). `/*/international-transfers/` is disallowed generally,
though, which may cover a relevant path regardless of locale.

## Content

`https://www.revolut.com/en-AU/money-transfer/` (WebFetch): **HTTP 403 Forbidden.** No page
content retrieved. This looks like active bot-wall enforcement (Revolut is known to run
Cloudflare-style bot management) rather than a robots.txt-based block — the path fetched isn't
listed as disallowed above. No further automated attempts were made against this domain in
this pass, consistent with not working around a block (CLAUDE.md §1.5).

## Tier assignment

**Tier 3 (provisional) — blocked from the one page checked; not otherwise established.**

Justification: single data point (one 403) isn't enough to fully characterise Revolut, but it
is consistent with a bot wall, and CLAUDE.md is explicit that a recorded block is a finding,
not something to route around. Revolut is also fundamentally an account-based banking app —
even if the marketing page loaded, actually sending money requires a Revolut account by
design, which independently caps it at Tier 3 under the "requires an account" rule regardless
of what any calculator shows.

## Confidence flags

- Only one URL was attempted; the 403 could be Cloudflare bot management, a geofence, a
  transient error, or something else — genuinely not certain which. Flagged rather than
  asserted as "bot wall confirmed."
- Whether Revolut supports any of the six Pacific currencies at all was not established either
  way.
- Because Revolut requires an account to actually transact, this provider may be Tier 3 on the
  "account required" ground alone even independent of the 403 — worth the maintainer treating
  this as a low-priority provider regardless of the exact reason.
