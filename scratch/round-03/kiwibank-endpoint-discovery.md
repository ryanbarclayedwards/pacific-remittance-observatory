# Kiwibank — endpoint discovery, from raw page source only

**Date:** 2026-09-09
**Method:** inspect already-fetched raw page source (`scratch/round-02/verify/kiwibank.body.html`,
Round 2's sweep) plus one further honest fetch of the one linked JS asset found, for its text
content only — no execution, no browser.

## What's on the page

The rate widget markup is a `<a class="richtext-rate" data-rate="240" data-nosnippet>FX Rate
TOP Buy TT (active)</a>` pattern, one per currency, with a small integer `data-rate` id (TOP=240,
FJD=130, PGK=185, SBD=205, VUV=255, WST=265, AUD=94, confirmed stable across the Round 1 and
Round 2 fetches for TOP specifically). The numeric rate itself is not in the raw HTML — it's
injected client-side, keyed by that id.

## What was checked

- Every `<script>` tag on the page (`scratch/round-02/verify/kiwibank.body.html`): two external
  scripts (`https://media.kiwibank.co.nz/static/js/index.js`, an Optimizely A/B-testing snippet)
  and a handful of inline `<script type="application/json">` blocks carrying navigation menu
  data only — nothing rate-related.
- Fetched `index.js` directly (one honest request, 595,795 bytes, saved as
  `scratch/round-03/kiwibank-index.js`) and searched its text for `richtext-rate`, `data-rate`,
  and any `/rate`, `/fx` path strings. Zero hits for `richtext-rate` at all — this bundle does
  not contain the widget's logic. `data-rate-*` hits found (`data-rate-comparison`,
  `data-rate-product`, etc.) belong to unrelated loan/mortgage rate-comparison components, not
  the FX widget.
- Checked immediately around the widget markup in the raw HTML for a wrapping element carrying
  a `data-endpoint`/`data-api`-style attribute. None found.

## Conclusion

**Hard stop: could not identify the endpoint from page source in a reasonable effort.** The
widget's actual rendering logic lives in a JS bundle not referenced anywhere in the static page
source checked — likely a route-specific or lazily-loaded chunk with no direct link visible
without executing the page. Per Round 3's explicit condition, this stops here; no further
iteration (guessing bundle filenames, searching a CDN listing, etc.) was attempted.
