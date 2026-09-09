# ASB Bank (asb.co.nz) — evidence, checked 2026-09-09

## robots.txt
URL: https://www.asb.co.nz/robots.txt

Two conflicting results:
1. **WebFetch** (uses Anthropic's own fetcher/UA) returned content and paraphrased it as disallowing: `/ASBWeb/Javascript/`, `/iFrames/` (investment/pricing pages), `/markets/historicgraphs.asp`, `/content/dam/asb/documents/`, `/content/asb/forms/`, `/content/asb/constant-collection/`, `/content/asb/creatives/`, and — significantly — **`/content/asb/ratesboard/`**. Also reported an extensive blocklist (400+ specific bot user-agents: HTTrack, Wget, WebZIP, ia_archiver, Yandex, MJ12bot, DotBot, etc.), each disallowed entirely, while Google Image Bot is explicitly permitted.
2. **curl**, using an honestly-identified UA string (`PacificRemittanceObservatory-recon/0.1`, contact URL included, per CLAUDE.md §1.5), got: `HTTP/2 stream 1 was not closed cleanly: INTERNAL_ERROR (err 2)` — the connection was reset with zero bytes returned, on `robots.txt` itself. Retried with `-v`; TLS handshake completed normally (valid ASB Bank Limited cert), request was sent, and the server terminated the stream before returning any response.

This is a live discrepancy: a generic/undisclosed fetcher gets a 200, an honestly-identified courteous client gets reset. Per CLAUDE.md, the collector must identify itself honestly — so the operative fact for this project is the **second** result: blocked.

## FX rates & fees page
URL: https://www.asb.co.nz/foreign-exchange/foreign-exchange-rates.html — via WebFetch: lists Pacific currency codes (TOP, WST, FJD confirmed present in an "all ASB currencies" list) but the live rate table itself did not render in the fetched content (likely client-side rendered) — no numeric rates captured.

URL: https://www.asb.co.nz/foreign-exchange/rates-and-fees.html — via WebFetch: a fee table headed "Other Bank Fees" lists: USD $5.00; AUD→CBA account $7.50; AED/CAD/CNY/FJD/INR/NOK/PHP/SEK/TOP/WST/ZAR $10.00; AUD→non-CBA/CHF/DKK/EUR/GBP/PGK/THB $20.00; HKD/JPY/NZD/SGD/VUV/XPF $25.00. **Not confirmed whether this is ASB's own outbound send fee or a fee charged by receiving/correspondent banks** — the heading "Other Bank Fees" suggests the latter, which would make it the wrong figure for reconstructing ASB's own quote. No public calculator link found on this page.

## Tier assignment
**Tier 3 (unobservable/blocked).** Automated access from an honestly-identified client is blocked (connection reset on robots.txt itself), and robots.txt (as read by a different fetcher) explicitly disallows a "ratesboard" path plus maintains a large scraper blocklist. Per CLAUDE.md §1.5 and §3, this is recorded as blocked, not worked around.

## Confidence flags
- The robots.txt discrepancy (WebFetch success vs. honest-UA reset) is the single most important anomaly in this batch — it directly demonstrates that ASB's block is UA-sensitive, which is exactly the situation CLAUDE.md says to record honestly rather than route around (e.g. by mimicking a browser UA).
- Did not attempt further UA variations, retries, or a real-browser check (Chrome extension unavailable this session) — deliberately, to avoid probing for a bypass.
- Fee-table interpretation ("Other Bank Fees" — whose fee?) is unresolved; even if ASB were reclassified, this ambiguity would need resolving first.
