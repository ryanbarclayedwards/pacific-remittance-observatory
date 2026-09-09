# NRBT fixtures

`exchange-rates-2026-09-09.html` — raw HTML bytes from a fresh `curl` fetch of
`https://www.reservebank.to/index.php/financial-system/financial-markets/exchange-rates`,
2026-09-09, with an honest, identifying user agent. Used by `tests/test_nrbt.py` so the parser
runs offline against committed bytes, never a live re-fetch.

At time of fetch, the page's own "Last Updated" marker read "09 September 2026", and the New
Zealand Dollar row read BUY 0.7367 / MID 0.7210 / SELL 0.7052 (NZD per 1 TOP).
