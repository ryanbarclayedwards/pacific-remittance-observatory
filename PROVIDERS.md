# PROVIDERS.md — collection triage

One row per provider. Filled in Sprint 1, Session 3 (Round 1, 2026-09-09). **Not** a coverage
target: a map of what is and isn't observable, published as a finding in its own right.

Candidate list drawn from the operators publicly listed as serving AU/NZ → Pacific corridors as
at 2026-09-09. That is market-structure information, not another platform's data.

**Evidence.** Every claim below is backed by a fetch saved under `scratch/round-01/`, one file
per provider (kebab-case slug of the name). Round 1 method, scope and confidence caveats are in
`reports/01-triage.md` — read that alongside this table, not this table alone.

## Tiers

- **1 — published tariff.** Public daily FX table + public fee schedule. Quote reconstructed
  arithmetically. Stable, cheap, low-brittleness. Flag `collection_method = published_tariff`.
- **2 — public quote calculator.** Public page returns a quote for fixed inputs, no account.
  Flag `collection_method = public_quote`.
- **3 — unobservable.** No public surface, credentials required, or automated access blocked.
  Flag `availability_status = unobservable`. Re-check quarterly. Do not work around.

A tier suffixed **(provisional)** means Round 1 found supporting evidence but did not fully
exercise the surface (e.g. a calculator confirmed to exist by page text, not by submitting a
real quote and reading back a number). Treat these as the tier the evidence points to, not as
settled — see `reports/01-triage.md` §9 for what would upgrade them to firm.

Two entries carry a status outside 1/2/3, recorded 2026-09-09 on maintainer decisions against
`reports/01-triage.md` §5.2: **UNRESOLVED** (MoneyGram — a robots.txt signal conflict is not
reconciled; no collection either way until it is) and **PENDING_PERMISSION** (Central Bank of
Solomon Islands, Bank of Papua New Guinea — the maintainer is asking the banks directly; not
treated as Tier 3 while that's pending).

## Columns

`provider` · `type` (bank / global MTO / corridor specialist / fintech) · `AU origin` ·
`NZ origin` · `Pacific destinations served` · `public FX table?` · `public fee schedule?` ·
`public calculator?` · `account required?` · `CAPTCHA / bot wall?` · `robots.txt permits?` ·
`tier` · `priority` · `date checked` · `notes`

`priority` is a Round 1 judgement about which candidates are worth Session 4/7 attention first,
given Tier and the corridor sequencing in CLAIMS.md §F (Tonga first, AU–Fiji second). It is not
a coverage target — see the caveat in `reports/01-triage.md` §5 about what it does and doesn't
mean for AU→Tonga specifically.

---

## Banks

| Provider | Type | AU origin | NZ origin | Pacific destinations served | Public FX table? | Public fee schedule? | Public calculator? | Account required? | CAPTCHA/bot wall? | robots.txt permits? | Tier | Priority | Date checked | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ANZ (New Zealand) | Bank | – | Y | Fiji, Solomon Is, Samoa, Tonga, Vanuatu, Cook Is, PNG, Kiribati, New Caledonia, Timor-Leste | **BLOCKED** — see below | Y, exact figures, confirmed via fresh fetch 2026-09-09 | n/a | N (fee schedule) / N/A (rate table blocked before an account question arises) | **Y — Incapsula bot-challenge, confirmed 2026-09-09** | Y (allow all; no robots.txt on tools subdomain) | **Split: fee schedule Tier 1-observable; FX rate table BLOCKED** | **High (fee schedule); blocked (rate table)** | 2026-09-09 (Round 1 tier), 2026-09-09 (Round 2 correction) | **Corrected 2026-09-09** (`reports/02-connectors.md` §5/§6): Round 1's "confirmed via WebFetch" finding does not survive a fresh, honest `curl` fetch. `tools.anz.co.nz/foreign-exchange/fx-rates/` — the only URL ANZ's own site links to for rates, confirmed by following their own navigation and redirect chain — returns an Incapsula bot-challenge page to a plain HTTP client. The fee schedule page is genuinely open and was independently re-confirmed. No workaround was attempted. |
| Kiwibank | Bank | – | Y | Currencies listed; destinations not itemised on the page checked | Probable — server-rendered currency rows confirmed; numeric rate value is JS-injected, not captured | Y, exact figures | Not found | N | N | Y | **1 (probable)** | **High** | 2026-09-09 | Second-strongest NZ candidate. Needs one more pass to confirm the actual rate-serving endpoint before treating Tier 1 as settled. |
| ANZ (Australia) | Bank | Y | – | Fiji, Tonga, Samoa, Vanuatu, Solomon Is, PNG, Kiribati, Cook Is | Referenced, not independently confirmed this round | Y, exact figures | Linked, not confirmed | N (for fee/calculator pages checked) | N | Y (allow all) | **2 (probable)** | **Medium** | 2026-09-09 | Fee schedule solid. No AU-origin bank reached Tier-1 confidence in Round 1 — see report §5 on what that means for the Session 4 AU→Tonga target. |
| Commonwealth Bank | Bank | Y | – | None named in the fee PDF | Page exists; no currency data found in raw HTML | **Y** — confirmed via dated (23 Jul 2026) static, machine-fetchable PDF | Linked, not tested | N (for PDF/fee info) | N | Y | **2** | **Medium** | 2026-09-09 | Fee PDF is genuine but silent on Pacific currencies specifically (only EUR/GBP/NZD/USD get an explicit same-currency fee table) — a methodology gap if built. |
| St. George | Bank | Y | – | FJD only, named | Y, exact figures | Y, exact figures | Linked, untested | Unclear | N | Y (but `/bt-calc/` specifically disallowed — relevance to the FX calculator unclear) | **2 (probable)** | **Low–Medium** | 2026-09-09 | Only FJD confirmed as a destination currency; converter tool exists but untested. |
| BNZ | Bank | – | Y | Not named on the fee page checked | Page exists; table not confirmed (client-rendered, not in raw HTML) | Y, exact figures | Not found | Unclear | N | Y (only blocks `/XMLFeed/` rates feed, not the HTML page) | **3 (provisional)** | Low | 2026-09-09 | Softest Tier 3 in the batch — a browser render (not available this round) could move this to Tier 1 or 2. |
| NAB | Bank | Y | – | Widest list of any bank checked: 21 Pacific/Micronesian entities named | Not confirmed (no currency codes in raw HTML) | Prose only, 2 figures, not a table | Not found for anonymous users (rates behind login) | Y (for rates) | N | Y | **3** | n/a | 2026-09-09 | Notable finding: broadest *stated* destination coverage of any bank, but no table, no calculator, incomplete public fee info — coverage claims and observability diverge sharply here. |
| Suncorp Bank | Bank | Y | – | Currency list confirms only FJD, PGK of the six target currencies | Referenced, not fetched | Y ($0 online / $30 branch) | Referenced, not fetched | N | N | Y (allow all) | **3** (full set) / possible 2 for FJD+PGK only | n/a | 2026-09-09 | Even best case, TOP/WST/VUV/SBD are outside Suncorp's product scope entirely — a currency-scope limit, not an access limit. |
| ASB | Bank | – | Y | Not established | Not confirmed | Ambiguous (may be a receiving-bank fee, not ASB's own) | Not found | Unknown | **Y** — honest-UA connection reset on robots.txt itself | Blocked at connection level before readable | **3** | n/a | 2026-09-09 | Automated access refused outright for an honestly-identified client. |
| HSBC (Australia) | Bank | Y | – | None named | Not confirmed | Partial (correspondent fee only) | Not found (app-only) | Y (app required to transact) | N | Y | **3** | n/a | 2026-09-09 | Site states HSBC is closing its Australian retail banking business over the next 18 months — moot as a build target regardless of tier. |
| Westpac (Australia) | Bank | Y | – | All 6 named | Byte-verified: the "currency converter" is a static supported-currency list, **not a live rate table** | Y, exact figures | The "converter" link redirects to the same static list — not a working calculator | Y (real rates require app/online banking or a phone call) | N | Y (explicitly allows calculator paths) | **3** | n/a | 2026-09-09 | Byte-level check specifically ruled out treating the "converter" as Tier 2 — it returns no rate. |
| Westpac (New Zealand) | Bank | – | Y | Not established | Blocked | Blocked | Blocked | Unknown | **Y** — Akamai WAF 403 on robots.txt itself | Blocked before robots.txt was readable | **3** | n/a | 2026-09-09 | Outright automated-access block for an honestly-identified client. |

**Confidence note (whole batch):** no browser session was available this round (Chrome
extension not connected), so every "client-rendered, not confirmed" or "requires login" finding
above rests on static HTTP fetches only. A real browser render is the single highest-value next
check for BNZ, ANZ (Australia), Commonwealth Bank, NAB and St. George before any tier is treated
as final or a connector is built against it.

## Global MTOs

| Provider | Type | AU origin | NZ origin | Pacific destinations served | Public FX table? | Public fee schedule? | Public calculator? | Account required? | CAPTCHA/bot wall? | robots.txt permits? | Tier | Priority | Date checked | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Remitly | Global MTO | Y | Unconfirmed | Fiji, Tonga, Samoa, Vanuatu, Solomon Is, PNG — all six listed | N | Not located directly | **Y**, login-free | N | N | Y | **2** | **High** | 2026-09-09 | Strongest Tier 2 finding of Round 1: login-free calculator plus all six Pacific destinations explicitly listed. |
| Wise | Global MTO | Y | Unconfirmed | Fiji confirmed via a live worked example; Tonga/Samoa/Vanuatu/Solomon Is/PNG not found on the page checked | N | N | **Y**, login-free, directly observed for Fiji | N (for the Fiji example) | N | Y | **2 for Fiji; unconfirmed for the rest** | Medium | 2026-09-09 | Only Pacific destination directly confirmed is Fiji. robots.txt disallows a literal `User-agent: WebFetch` in an old, widely copy-pasted bad-bot list — judged coincidental (no AI-crawler-named entries present), not a deliberate block of this project, but flagged for a second opinion. |
| Western Union | Global MTO | Y | Unconfirmed | FJD/TOP/WST/VUV/SBD/PGK all present on the currency converter | N | N | **Y**, login-free converter confirmed for all six currencies | Unconfirmed for the actual send/quote flow | N | Y | **2 (provisional)** | Medium | 2026-09-09 | Converter confirmed; whether the full send flow stays account-free through to a quote was not independently verified. |
| WorldRemit | Global MTO | Y | Y (sitemap locale only, page not fetched) | Fiji, Samoa confirmed on the AU page; Tonga/Vanuatu/Solomon Is/PNG not found there | N | N | No calculator on the landing page checked; only a worked example | Quote step not reached | N | Y | **2/3 boundary (provisional)** | Low | 2026-09-09 | Only 2 of 6 target destinations confirmed present; genuinely on the tier boundary. |
| Ria Money Transfer | Global MTO | Y | Inferred only (sitemap locale) | Currency pages exist for all six; actual transfer service to each unconfirmed | N | N | Homepage widget exists but untested; rate pages explicitly state "login to see actual send rates" | Y (for real quotes) | N | Y | **3 (provisional)** | Low | 2026-09-09 | Only unauthenticated figures found are labelled mid-market reference rates, not real send quotes. |
| Xe Money Transfer | Global MTO | Unconfirmed | Unconfirmed | Not confirmed for any of the six | N | N | Push toward login before a rate is shown | Appears Y | N | Y (same old bad-bot list naming `WebFetch` as Wise's) | **3 (provisional, weakly evidenced)** | n/a — needs follow-up before trusting | 2026-09-09 | Weakest finding of the batch: one page fetched, two follow-up URLs 404'd. Not a settled Tier 3. |
| MoneyGram | Global MTO | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | 403 on the one AU page fetched, independent of robots | **N** — `User-agent: ClaudeBot` / `Disallow: /`, site-wide | **UNRESOLVED** | n/a | 2026-09-09 | **Changed 2026-09-09** (maintainer decision, `reports/01-triage.md` §5.2): not settled Tier 3. MoneyGram's general `User-agent: *` rule carries `Content-Signal: ai-train=no, use=reference` — a first-party statement that reference use is permitted — alongside the ClaudeBot-specific `Disallow: /`. These two signals conflict and are not reconciled here. No collection either way until decided. |
| Revolut | Global MTO / fintech | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Y (banking app, by design) | Y — 403 on the one page fetched | Y (the path checked wasn't in the locale-disallow list) | **3 (provisional)** | n/a | 2026-09-09 | Independently Tier 3 by design (account-based banking app) regardless of the 403's cause, which wasn't investigated further. |
| OFX | Global MTO | Y (locale exists) | Y (locale exists) | Not confirmed for any of the six | Plausible (a "daily currency update" is referenced) but URL unconfirmed | Not located | Login-free converter exists | Unconfirmed | N | Y | **Unconfirmed — no tier asserted** | n/a — needs follow-up | 2026-09-09 | Evidence genuinely too thin to call a tier; declined to guess. |
| OrbitRemit | Global MTO | Y | Y | Fiji, Samoa, Tonga, Vanuatu (+50 countries worldwide) | N (a rate figure is exposed in page metadata) | Partial — flat-fee claims found via search, not a formal schedule page | **Likely Y (provisional)** — a rate is served even to a static fetch, and the vendor's own text describes a login-free calculator | Only to actually send, not to get a quote | Not observed on the main site (a support subdomain 403'd, separate infra) | Y (`Allow: /`, a few promo paths disallowed) | **2 (provisional)** | **Medium** | 2026-09-09 | **Recategorised 2026-09-09** (maintainer decision, `reports/01-triage.md` §5.3) from "Pacific corridor specialist" to Global MTO — reads as a general remittance service reaching ~50 countries, of which four are Pacific destinations, not a Pacific specialist. |

## Pacific corridor specialists

These matter most and are hardest to reach. In the 2023 audit the corridor specialists were
repeatedly the cheapest options — a panel that silently omits them overstates the cost of
remitting. Most of Round 1's Tier 3 findings sit here, which is the honest result, not a
shortfall in the triage.

| Provider | Type | AU origin | NZ origin | Pacific destinations served | Public FX table? | Public fee schedule? | Public calculator? | Account required? | CAPTCHA/bot wall? | robots.txt permits? | Tier | Priority | Date checked | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Samoa Money Transfer | Corridor specialist | N | Y | Samoa (implied) | No dedicated table; a rate figure appears on the homepage itself | A static fee figure appears on the homepage itself ($10/$12) | N | Unclear | N | Y (blocks only `/wp-admin/`) | **2 (borderline)** | Low–Medium | 2026-09-09 | The figures are undated with no visible refresh mechanism — closer to a stale placeholder than a genuine daily tariff. Needs a re-check on a different date before this tier is trusted. |
| IMEX Money Transfer | Corridor specialist | Unconfirmed (found only via a third-party page) | Y | Samoa, Tonga | N (homepage rate widget unresolved — static-fetch limitation) | Partial — flat $8 NZD fee disclosed in prose/T&Cs, no tiered schedule | Not confirmed (JS-rendered rate widget, could not evaluate) | Y (ID + proof of address to send) | Not observed | Y (empty Disallow) | **3 (provisional — boundary)** | Low | 2026-09-09 | The unresolved rate widget is the one thing that could move this to Tier 2 — worth a browser-based re-check. |
| Rocket Remit | Corridor specialist | Y | Y (per other sources, not re-verified) | Cook Is, Fiji, Samoa, Tonga, Vanuatu, PNG (Solomon Is per an unverified press release) | N | N (PNG page gives only a vague "$0–5" range) | N — quote appears gated behind signup/login per FAQ text | Y (per FAQ text) | Not observed | Y (empty Disallow) | **3** | Low | 2026-09-09 | The homepage's "Get Rate" button's actual behaviour is unconfirmed — no browser session was available to click it. Worth a follow-up before treating Tier 3 as final. |
| 'Ave Pa'anga Pau | Corridor specialist (a TDB bank product) | Y | Y | Tonga | N (only a prose "~4.5% typical margin" claim) | N (only a prose "no fees" claim) | N — the site's own "how it works" copy states live quotes require account creation | Y | Not observed | AU: no robots.txt (404). NZ: fetch inconclusive, unconfirmed — needs re-check | **3** | n/a | 2026-09-09 | Own copy states live quotes are gated behind account creation. |
| Lotus Foreign Exchange | Corridor specialist / FX bureau | Y | Not checked this round | Fiji (eWire); also a MoneyGram agent for wider Pacific reach | N — the exchange-rates page is descriptive only, no live table | N | N | Unclear (login links present, not confirmed mandatory for a quote) | Not observed | No robots.txt (404) | **3** | n/a | 2026-09-09 | Talks about rates but shows none; no calculator. |
| Island Flexi Transfer | Corridor specialist | Y | – | Tonga (third-party corroborated, not first-party confirmed) | N | N | N — intake is a Google Form, not a quote mechanism | De facto (manual, via form + bank deposit) | Not observed | No robots.txt (404) | **3** | n/a | 2026-09-09 | No quote surface of any kind exists to observe. |
| Pacific Ezy | Corridor specialist | N | Y | Samoa (per the page checked) | N | N | N | Unclear — "members"-based model, not tested | Not observed | Y (empty Disallow) | **3** | n/a | 2026-09-09 | No public quote/tariff surface found on the pages checked. |
| KlickEx | Corridor specialist / fintech | Y (per third-party sources) | Y (per third-party sources) | Tonga, Samoa, Fiji, Vanuatu, PNG, Cook Is, Solomon Is (per third-party sources, not first-party confirmed) | Unknown — homepage blocked | Unknown — homepage blocked | Unknown — homepage blocked | Unknown | **Y** — homepage returned HTTP 403 to automated fetch | robots.txt names ClaudeBot and other AI crawlers as disallowed; otherwise permits with a 10s crawl-delay | **3** | n/a | 2026-09-09 | Active bot wall plus explicit AI-crawler exclusion in robots.txt. |
| KlickEx Pacific | Same entity as KlickEx | – | – | – | – | – | – | – | – | – | **3** | n/a | 2026-09-09 | klickex.com is run by KlickEx Pacific Limited — this is not a separate provider on the evidence found. Kept as its own row to match the original candidate list. |
| The Ink Patch Money Transfer | Corridor specialist | Unknown | Presumed (Auckland-registered) | Samoa (inferred from name/context, not confirmed) | N | N | N | n/a — no crawlable site | n/a | n/a — no crawlable site found | **3** | n/a | 2026-09-09 | No discoverable website at all; only a Facebook page and regulator/registry listings. |
| TransCrypt | Corridor specialist (per original candidate list) | n/a | n/a | None found | N | N | N | n/a | Not observed | Y | **3** | n/a | 2026-09-09 | Brand appears discontinued/absorbed into Triple-A, a B2B stablecoin infrastructure company — whole-domain 301 redirect, no Pacific consumer offering found. |
| WanTok Money | Corridor specialist | Not stated on marketing pages | Not stated on marketing pages | Vanuatu, Tonga (by domain split) | N | N | N | Unknown | n/a | n/a for wantokmoney.com (does not resolve); marketing subsites permit crawling | **3** | n/a | 2026-09-09 | The actual transactional domain (wantokmoney.com) does not resolve in DNS at all — this reads as a real outage or abandonment, not a temporary blip, but was only checked once. |
| Pacific Way Money Transfer | Corridor specialist | Unverified (search snippets only) | Unverified (search snippets only) | Unverified | Unknown | Unknown | Unknown | Unknown | n/a | Could not fetch | **3** | n/a | 2026-09-09 | A hard unknown, not a normal Tier 3: the server's TLS certificate doesn't cover its own hostname, so it's unreachable to any certificate-validating client. No attempt was made to bypass certificate validation. |

## Benchmark sources

Same triage, under `collect/benchmarks/`. Receiving-country central banks publishing daily
indicative rates. This scoping feeds the benchmark-choice options memo in
`reports/01-triage.md` §5 — the choice itself (CLAIMS.md E1) is the maintainer's, not made here.

| Bank | AUD rate published? | NZD rate published? | Format | Update frequency | History available? | Page stability | robots.txt | Date checked |
|---|---|---|---|---|---|---|---|---|
| Reserve Bank of Fiji | Y — homepage widget + downloadable `.xlsx` | Y — same | HTML widget (today only) + downloadable `.xlsx` | Daily (inferred from one day's date stamp) | `.xlsx` exists; depth unconfirmed (not opened) | Data file lives in a dated `/wp-content/uploads/2026/09/...` path — likely shifts monthly (inferred, not observed across months) | Open (WordPress/Yoast default) | 2026-09-09 |
| National Reserve Bank of Tonga | Y | Y | HTML table (buy/mid/sell) + downloadable `.xlsx`, 2017–current | Daily (inferred: page dated same-day, sibling weekly/monthly pages carry visibly older stamps) | **Best of six** — single multi-year file, 2017–present | Joomla component route, not date-keyed; no change observed | Open (Joomla defaults, no AI-crawler rules) | 2026-09-09 |
| Central Bank of Samoa | Y | Y | HTML table + downloadable, date-stamped-filename `.xlsx` | Daily (inferred: filename date matches page date, single observation) | Exists; depth unconfirmed (not opened) | Historical-file filename appears to re-date each publication — a collector would need to discover the current filename each run, not assume a fixed URL | **No robots.txt file (404)** — unrestricted by omission | 2026-09-09 |
| Reserve Bank of Vanuatu | Y | Y | HTML table, one row per business day on the page itself | **Best-evidenced daily cadence** — ~10 distinct weekday-only dated rows directly observed in one fetch | Built into the same paginated page; depth beyond ~10 days not probed | Joomla component route, not date-keyed. **TLS certificate chain is broken** — standard clients refuse the connection; this is a bigger stability risk than the URLs | robots.txt redirects into a 404 (no file actually served) — reads as unrestricted but delivery is unusual | 2026-09-09 |
| Central Bank of Solomon Islands | Y | Y | HTML table only, no download found on the page checked | **Ambiguous** — page claims ~9am daily but its own "previous rate" column is dated a full week earlier, not one day earlier | None found on this page (a general "download centre" exists elsewhere, unconfirmed) | Clean CMS route, no date-keying observed | **PENDING_PERMISSION** — maintainer emailing the bank directly to ask (2026-09-09); not Tier 3. robots.txt as observed explicitly disallows `ClaudeBot` by name (Cloudflare AI-crawler blocklist) | 2026-09-09 |
| Bank of Papua New Guinea | **Not established** | **Not established** | **Not established** | **Not established** | **Not established** | **Not established** | **PENDING_PERMISSION** — maintainer emailing the bank directly to ask (2026-09-09); not Tier 3. Same Cloudflare blocklist as CBSI, explicitly disallows `ClaudeBot` | 2026-09-09 |

## Known corridor exceptions

**Niue.** Shares a banking system with New Zealand; ordinary bank transfers are free. A
cheapest-provider ranking for NZ → Niue is misleading without annotation. The same may apply
to Cook Islands and Tokelau. Decide the exclusion or annotation rule before publication, not
after someone notices.
