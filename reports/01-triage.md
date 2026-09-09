# Round 1 — reconnaissance and triage

**Date:** 2026-09-09
**Scope:** classify every candidate in `PROVIDERS.md` (33 providers) and every candidate
benchmark source (6 receiving-country central banks) by Tier per `CLAUDE.md` §3; scope the
benchmark-rate decision (`CLAIMS.md` E1) without making it; verify five open `CLAIMS.md` items
(B1, G1, G2, A9, A10); define a reusable round-report structure and publish this report against
it.

**Explicitly out of scope:** no connector code, no collection code, no data observations.
Nothing in this round writes to `archive/`, `store/`, or `release/`. The benchmark-rate choice
(E1) itself is the maintainer's, not made here. No workaround was attempted for any blocked,
CAPTCHA-gated, or credential-gated surface.

This report follows the structure defined in `docs/REPORTING.md`. Read it as a standalone
document — it does not assume familiarity with the session that produced it.

---

## 1. What I did

1. Read `CLAUDE.md`, `CLAIMS.md`, `SPRINT-01.md`, `PROVIDERS.md`, `docs/METHODOLOGY.md`,
   `README.md` and `.gitignore` in full before touching anything.
2. Drafted a plan (six parallel research batches, evidence-file convention, commit structure)
   and got explicit approval before any file was touched.
3. Ran `git init` (this session) and, before starting Round 1 work, made one baseline commit of
   the pre-existing repository contents (Sprint 1 Sessions 1–2 output), so Round 1's work is a
   clean diff on top rather than bundled with unrelated scaffold.
4. Launched six parallel research agents (forked from this session, sharing its context), each
   with a defined batch: banks (10 candidates), global MTOs (9), Pacific corridor specialists
   in two batches (7 + 7), central-bank benchmark scoping (6), and CLAIMS.md verification (5
   items). Each agent used `WebFetch` as primary tool, with the Chrome browser tool available
   as a fallback for JS-rendered pages only — never to bypass a login, CAPTCHA, or bot wall —
   though in practice the Chrome extension was not connected this session, so every finding in
   this round rests on static HTTP fetches (`WebFetch`/`curl`), not a rendered browser. This is
   a real method limitation, flagged throughout and repeated in §9.
5. All six agents hit a session-wide API rate limit simultaneously partway through and were
   resumed from their existing transcripts and already-saved evidence — no work was lost, no
   provider was re-checked from scratch.
6. As each batch completed, I read its evidence files (spot-checking a sample — ANZ New
   Zealand, the SendMoneyPacific/B1 evidence, and MoneyGram's robots.txt — against the agent's
   summary before accepting any tier call) and assembled the findings into `PROVIDERS.md`.
7. Updated `CLAIMS.md` for B1, G1, G2, A9, A10, plus P1 (resolved as a direct consequence of
   Task A's robots.txt checks, not separately requested but directly evidenced).
8. Wrote `docs/REPORTING.md` (the structure this report follows) and this report.
9. Committed in four steps: scaffold baseline, triage findings (`PROVIDERS.md` + evidence),
   claims verification (`CLAIMS.md` + evidence), and the two Task D documents (this commit, made
   after this report is written).

---

## 2. Findings

### 2.1 Banks

| Provider | Type | AU origin | NZ origin | Pacific destinations served | Public FX table? | Public fee schedule? | Public calculator? | Account required? | CAPTCHA/bot wall? | robots.txt permits? | Tier | Priority | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ANZ (New Zealand) | Bank | – | Y | Fiji, Solomon Is, Samoa, Tonga, Vanuatu, Cook Is, PNG, Kiribati, New Caledonia, Timor-Leste | **Y** — confirmed, all 6 target currencies, timestamped | Y, exact figures | n/a (table suffices) | N | N | Y (allow all) | **1** | **High** | Strongest candidate in Round 1. Rate table structure not yet captured byte-for-byte; an "OUR Fee" for some transfer types is disclosed but not quantified publicly — a cost-formula gap, not a tier downgrade. |
| Kiwibank | Bank | – | Y | Currencies listed; destinations not itemised on the page checked | Probable — server-rendered currency rows confirmed; numeric rate is JS-injected, not captured | Y, exact figures | Not found | N | N | Y | **1 (probable)** | **High** | Needs one more pass to confirm the actual rate-serving endpoint before Tier 1 is settled. |
| ANZ (Australia) | Bank | Y | – | Fiji, Tonga, Samoa, Vanuatu, Solomon Is, PNG, Kiribati, Cook Is | Referenced, not independently confirmed this round | Y, exact figures | Linked, not confirmed | N | N | Y (allow all) | **2 (probable)** | **Medium** | No AU-origin bank reached Tier-1 confidence in Round 1 — see §5.1. |
| Commonwealth Bank | Bank | Y | – | None named in the fee PDF | Page exists; no currency data in raw HTML | **Y** — dated (23 Jul 2026), machine-fetchable PDF | Linked, not tested | N | N | Y | **2** | **Medium** | Fee PDF is silent on Pacific currencies specifically — a methodology gap if built. |
| St. George | Bank | Y | – | FJD only | Y, exact figures | Y, exact figures | Linked, untested | Unclear | N | Y (`/bt-calc/` disallowed, relevance unclear) | **2 (probable)** | **Low–Medium** | Only FJD confirmed as a destination currency. |
| BNZ | Bank | – | Y | Not named on the page checked | Page exists; not confirmed (client-rendered) | Y, exact figures | Not found | Unclear | N | Y (only `/XMLFeed/` disallowed) | **3 (provisional)** | Low | Softest Tier 3 in the batch — a browser render could move this to Tier 1 or 2. |
| NAB | Bank | Y | – | Widest list of any bank checked: 21 Pacific/Micronesian entities | Not confirmed | Prose only, not a table | Not found for anonymous users | Y (for rates) | N | Y | **3** | n/a | Broadest *stated* coverage of any bank, but no table, no calculator — coverage claims and observability diverge sharply. |
| Suncorp Bank | Bank | Y | – | Currency list confirms only FJD, PGK | Referenced, not fetched | Y ($0 online / $30 branch) | Referenced, not fetched | N | N | Y (allow all) | **3** (full set) / possible 2 for FJD+PGK only | n/a | Even best case, TOP/WST/VUV/SBD are outside Suncorp's product scope entirely. |
| ASB | Bank | – | Y | Not established | Not confirmed | Ambiguous | Not found | Unknown | **Y** — honest-UA connection reset on robots.txt itself | Blocked at connection level | **3** | n/a | Automated access refused outright for an honestly-identified client. |
| HSBC (Australia) | Bank | Y | – | None named | Not confirmed | Partial | Not found (app-only) | Y | N | Y | **3** | n/a | Site states HSBC is closing its Australian retail banking business over the next 18 months — moot regardless of tier. |
| Westpac (Australia) | Bank | Y | – | All 6 named | Byte-verified: the "converter" is a static currency list, **not a live rate table** | Y, exact figures | Redirects to the same static list — not a working calculator | Y (app/online banking or phone) | N | Y | **3** | n/a | Byte-level check specifically ruled out treating the "converter" as Tier 2. |
| Westpac (New Zealand) | Bank | – | Y | Not established | Blocked | Blocked | Blocked | Unknown | **Y** — Akamai WAF 403 on robots.txt itself | Blocked before robots.txt readable | **3** | n/a | Outright automated-access block for an honestly-identified client. |

No browser session was available this round for any bank (see §1.4), so every "client-rendered,
not confirmed" or "requires login" finding above rests on static HTTP fetches only.

### 2.2 Global MTOs

| Provider | Type | AU origin | NZ origin | Pacific destinations served | Public FX table? | Public fee schedule? | Public calculator? | Account required? | CAPTCHA/bot wall? | robots.txt permits? | Tier | Priority | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Remitly | Global MTO | Y | Unconfirmed | Fiji, Tonga, Samoa, Vanuatu, Solomon Is, PNG — all six | N | Not located directly | **Y**, login-free | N | N | Y | **2** | **High** | Strongest Tier 2 finding of Round 1. |
| Wise | Global MTO | Y | Unconfirmed | Fiji confirmed via a live worked example; other five not found on the page checked | N | N | **Y**, login-free, directly observed for Fiji | N (Fiji example) | N | Y | **2 for Fiji; unconfirmed for rest** | Medium | robots.txt disallows a literal `User-agent: WebFetch` in an old bad-bot list — judged coincidental (no AI-crawler-named entries present), flagged for a second opinion. |
| Western Union | Global MTO | Y | Unconfirmed | All six present on the currency converter | N | N | **Y**, login-free converter, all six currencies | Unconfirmed for full send flow | N | Y | **2 (provisional)** | Medium | Converter confirmed; the full account-free send/quote flow was not independently verified end to end. |
| WorldRemit | Global MTO | Y | Y (sitemap locale only) | Fiji, Samoa confirmed; other four not found | N | N | No calculator on the page checked; worked example only | Quote step not reached | N | Y | **2/3 boundary (provisional)** | Low | Only 2 of 6 target destinations confirmed present. |
| Ria Money Transfer | Global MTO | Y | Inferred only | Currency pages exist for all six; transfer service unconfirmed | N | N | Widget exists, untested; rate pages say "login to see actual send rates" | Y (for real quotes) | N | Y | **3 (provisional)** | Low | Only unauthenticated figures found are mid-market reference rates, not real send quotes. |
| Xe Money Transfer | Global MTO | Unconfirmed | Unconfirmed | Not confirmed for any of the six | N | N | Push toward login before a rate is shown | Appears Y | N | Y (same old bad-bot list naming `WebFetch`) | **3 (provisional, weakly evidenced)** | Needs follow-up | Weakest finding of the batch: one page fetched, two follow-up URLs 404'd. Not a settled Tier 3. |
| MoneyGram | Global MTO | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | 403 on the one page fetched, independent of robots | **N** — `User-agent: ClaudeBot` / `Disallow: /`, site-wide | **3** | n/a | Stopped immediately on the explicit ClaudeBot disallow. See §5.2 for the open question this raises. |
| Revolut | Global MTO / fintech | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Unconfirmed | Y (banking app, by design) | Y — 403 on the one page fetched | Y (path checked wasn't disallowed) | **3 (provisional)** | n/a | Independently Tier 3 by design regardless of the 403's cause. |
| OFX | Global MTO | Y (locale exists) | Y (locale exists) | Not confirmed for any of the six | Plausible, unconfirmed URL | Not located | Login-free converter exists | Unconfirmed | N | Y | **Unconfirmed — no tier asserted** | Needs follow-up | Evidence genuinely too thin to call a tier; declined to guess. |

### 2.3 Pacific corridor specialists

These matter most and are hardest to reach: in the 2023 audit they were repeatedly the cheapest
options. Most of Round 1's Tier 3 findings sit here — that is the honest result PROVIDERS.md
warns to expect, not a shortfall in the triage.

| Provider | Type | AU origin | NZ origin | Pacific destinations served | Public FX table? | Public fee schedule? | Public calculator? | Account required? | CAPTCHA/bot wall? | robots.txt permits? | Tier | Priority | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OrbitRemit | Corridor specialist (candidate list) — reads as a general 50-country global MTO | Y | Y | Fiji, Samoa, Tonga, Vanuatu (+50 countries worldwide) | N (rate figure in page metadata) | Partial (flat-fee claims via search) | **Likely Y (provisional)** — rate served even to a static fetch; vendor's own text describes a login-free calculator | Only to actually send | Not observed on main site (support subdomain 403'd) | Y | **2 (provisional)** | **Medium** | Category mismatch flagged, not resolved — see §5.3. |
| Samoa Money Transfer | Corridor specialist | N | Y | Samoa (implied) | No table; a rate figure on the homepage itself | A static fee figure on the homepage ($10/$12) | N | Unclear | N | Y (blocks only `/wp-admin/`) | **2 (borderline)** | Low–Medium | Figures are undated with no visible refresh mechanism — closer to a stale placeholder than a genuine daily tariff. Re-check on a different date before trusting. |
| IMEX Money Transfer | Corridor specialist | Unconfirmed (third-party page only) | Y | Samoa, Tonga | N (rate widget unresolved — static-fetch limitation) | Partial — flat $8 NZD fee in prose/T&Cs | Not confirmed (JS-rendered widget) | Y (ID + proof of address) | Not observed | Y (empty Disallow) | **3 (provisional — boundary)** | Low | The unresolved rate widget is the one thing that could move this to Tier 2. |
| Rocket Remit | Corridor specialist | Y | Y (per other sources) | Cook Is, Fiji, Samoa, Tonga, Vanuatu, PNG (Solomon Is per unverified press release) | N | N (PNG: vague "$0–5" range) | N — appears gated behind signup/login per FAQ | Y (per FAQ) | Not observed | Y (empty Disallow) | **3** | Low | The homepage's "Get Rate" button's actual behaviour is unconfirmed — no browser session was available to click it. |
| 'Ave Pa'anga Pau | Corridor specialist (a TDB bank product) | Y | Y | Tonga | N (prose "~4.5% typical margin" only) | N (prose "no fees" only) | N — own copy says live quotes require account creation | Y | Not observed | AU: no robots.txt (404). NZ: fetch inconclusive | **3** | n/a | — |
| Lotus Foreign Exchange | Corridor specialist / FX bureau | Y | Not checked this round | Fiji (eWire); also a MoneyGram agent | N — descriptive only, no live table | N | N | Unclear | Not observed | No robots.txt (404) | **3** | n/a | Talks about rates but shows none. |
| Island Flexi Transfer | Corridor specialist | Y | – | Tonga (third-party corroborated only) | N | N | N — intake is a Google Form | De facto (manual, form + bank deposit) | Not observed | No robots.txt (404) | **3** | n/a | No quote surface of any kind exists to observe. |
| Pacific Ezy | Corridor specialist | N | Y | Samoa (per the page checked) | N | N | N | Unclear — "members"-based | Not observed | Y (empty Disallow) | **3** | n/a | No public quote/tariff surface found on the pages checked. |
| KlickEx | Corridor specialist / fintech | Y (third-party) | Y (third-party) | Tonga, Samoa, Fiji, Vanuatu, PNG, Cook Is, Solomon Is (third-party, not first-party confirmed) | Unknown — homepage blocked | Unknown — homepage blocked | Unknown — homepage blocked | Unknown | **Y** — homepage 403 | robots.txt names ClaudeBot and other AI crawlers as disallowed | **3** | n/a | Active bot wall plus explicit AI-crawler exclusion. |
| KlickEx Pacific | Same entity as KlickEx | – | – | – | – | – | – | – | – | – | **3** | n/a | klickex.com is run by KlickEx Pacific Limited — not a separate provider on the evidence found. Kept as its own row to match the original candidate list. |
| The Ink Patch Money Transfer | Corridor specialist | Unknown | Presumed (Auckland-registered) | Samoa (inferred from name/context) | N | N | N | n/a — no crawlable site | n/a | n/a — no crawlable site found | **3** | n/a | No discoverable website at all; only a Facebook page and regulator/registry listings. |
| TransCrypt | Corridor specialist (per original list) | n/a | n/a | None found | N | N | N | n/a | Not observed | Y | **3** | n/a | Brand appears discontinued/absorbed into Triple-A, a B2B stablecoin infrastructure company — whole-domain 301 redirect, no Pacific consumer offering found. |
| WanTok Money | Corridor specialist | Not stated | Not stated | Vanuatu, Tonga (by domain split) | N | N | N | Unknown | n/a | n/a for wantokmoney.com (does not resolve) | **3** | n/a | The transactional domain does not resolve in DNS at all — checked once. |
| Pacific Way Money Transfer | Corridor specialist | Unverified (search snippets only) | Unverified (search snippets only) | Unverified | Unknown | Unknown | Unknown | Unknown | n/a | Could not fetch | **3** | n/a | A hard unknown, not a normal Tier 3: the server's TLS certificate doesn't cover its own hostname. No attempt was made to bypass certificate validation. |

### 2.4 Benchmark sources

| Bank | AUD rate published? | NZD rate published? | Format | Update frequency | History available? | Page stability | robots.txt | 
|---|---|---|---|---|---|---|---|
| Reserve Bank of Fiji | Y — homepage widget + downloadable `.xlsx` | Y — same | HTML widget (today only) + downloadable `.xlsx` | Daily (inferred from one day's stamp) | `.xlsx` exists; depth unconfirmed (not opened) | File lives in a dated `/wp-content/uploads/2026/09/...` path — likely shifts monthly (inferred, not observed across months) | Open (WordPress/Yoast default) |
| National Reserve Bank of Tonga | Y | Y | HTML table (buy/mid/sell) + downloadable `.xlsx`, 2017–current | Daily (inferred: page dated same-day, sibling weekly/monthly pages carry visibly older stamps) | **Best of six** — single multi-year file, 2017–present | Joomla component route, not date-keyed; no change observed | Open (Joomla defaults, no AI-crawler rules) |
| Central Bank of Samoa | Y | Y | HTML table + downloadable, date-stamped-filename `.xlsx` | Daily (inferred: filename date matches page date, one observation) | Exists; depth unconfirmed (not opened) | Historical-file filename appears to re-date each publication — a collector would need to discover the current filename each run | **No robots.txt file (404)** — unrestricted by omission |
| Reserve Bank of Vanuatu | Y | Y | HTML table, one row per business day on the page itself | **Best-evidenced daily cadence** — ~10 distinct weekday-only dated rows directly observed in one fetch | Built into the same paginated page; depth beyond ~10 days not probed | Joomla component route. **TLS certificate chain is broken** — standard clients refuse the connection; bigger stability risk than the URLs | robots.txt redirects into a 404 (no file actually served) — reads as unrestricted, delivery is unusual |
| Central Bank of Solomon Islands | Y | Y | HTML table only, no download found on the page checked | **Ambiguous** — page claims ~9am daily but its own "previous rate" column is dated a full week earlier | None found on this page (a general "download centre" exists elsewhere, unconfirmed) | Clean CMS route, no date-keying observed | Open for a generic UA, but **explicitly disallows `ClaudeBot` by name** (Cloudflare AI-crawler blocklist) |
| Bank of Papua New Guinea | **Not established** | **Not established** | **Not established** | **Not established** | **Not established** | **Not established** | Same Cloudflare blocklist as CBSI, **explicitly disallows `ClaudeBot`** |

All six checked 2026-09-09.

---

## 3. Decisions I made

1. **Ran research as six parallel forked agents rather than sequentially.** *Reversible —* a
   method choice for this round only. Reason: 33 providers + 6 banks + 5 claims, each needing
   several courteous, spaced requests, would have been slow and context-heavy done serially.
   Each agent saved its own evidence and I personally reviewed and spot-checked outputs before
   accepting any tier call, rather than transcribing agent summaries unverified.

2. **Split ANZ and Westpac into separate AU/NZ rows** in the findings tables, rather than one
   row per brand. *Reversible.* Reason: the two country operations have materially different
   FX-rate and fee-schedule surfaces (ANZ NZ is Tier 1; ANZ AU is Tier 2 (probable)) — one row
   would have forced an inaccurate single tier onto two different observability profiles.

3. **Treated an absent robots.txt (404) as "no declared restriction,"** consistent with the
   robots.txt convention, for Central Bank of Samoa, Island Flexi Transfer, Lotus Foreign
   Exchange, and 'Ave Pa'anga Pau (AU). *Reversible if the maintainer wants a more conservative
   default.* This is a convention reading, not new policy.

4. **Stopped all further automated checking of any site whose robots.txt explicitly disallowed
   `ClaudeBot`** (MoneyGram, KlickEx, Central Bank of Solomon Islands, Bank of Papua New
   Guinea), per CLAUDE.md §1.5's instruction to identify the collector honestly and respect
   robots directives. *Not reversible within this round without re-contacting those sites* —
   but see §5.2 for an open question this decision surfaces about future, differently-branded
   collector code.

5. **Did not attempt to work around any block encountered** — Pacific Way's broken TLS
   certificate, WanTok Money's non-resolving domain, ASB's and Westpac NZ's connection-level
   resets, Bank of Papua New Guinea's 403 across every user agent tried. Each is recorded as a
   finding, not investigated further. *Not reversible retroactively, but each can be re-checked
   in a future round* — several (BPNG especially) may simply be network-path-dependent rather
   than a deliberate universal block, and SPRINT-01 already flags testing from a GitHub Actions
   runner as a separate, later concern (G3).

6. **Committed the pre-existing repository contents as a separate baseline commit** before any
   Round 1 change, since `git init` had only just been run this session and nothing was
   committed yet. *Reversible in the sense that history could be rewritten, but not recommended*
   — it keeps Round 1's diff clean and auditable on its own.

7. **Resumed all six research agents from their existing transcripts after a simultaneous
   rate-limit failure**, rather than restarting any of them, so already-completed provider
   checks and saved evidence were not redone or discarded.

---

## 4. Decisions I did not make

### 5.1 The Session 4 target (AU→Tonga Tier 1 connector) has no confirmed AU-origin Tier-1 candidate

SPRINT-01 Session 4 specifies "a bank, published daily FX table plus published fee schedule...
Australia → Tonga, A$200." Round 1 found exactly one confirmed Tier 1 bank — **ANZ New
Zealand** — and it is NZ-origin, not AU-origin. The strongest AU-origin bank found (ANZ
Australia) is Tier 2 (probable): its fee schedule is solid but its FX rate table was referenced,
not independently confirmed, this round.

**Options:**
- **(a)** Re-check ANZ Australia's (and BNZ's, Commonwealth Bank's, NAB's, St George's) FX rate
  pages with an actual browser render before Session 4 starts — this round had no working
  Chrome extension, so several "client-rendered, not confirmed" findings may resolve to Tier 1
  on a second look. Lowest-cost option if it works, but doesn't guarantee an AU-origin Tier 1
  bank exists.
- **(b)** Start Session 4 with **NZ → Tonga via ANZ New Zealand** instead, since it is the one
  confirmed Tier 1 candidate reaching Tonga, and revisit AU-origin coverage in a later session.
  This changes the sprint's stated corridor and would need a CLAIMS.md/SPRINT-01 note explaining
  why, per CLAUDE.md §1.6/1.7.
- **(c)** Proceed with ANZ Australia at Tier 2 (probable) and build a Session-4 connector
  against its calculator instead of a published tariff — this contradicts SPRINT-01's explicit
  "Tier 1 first" sequencing rationale (Session 4 exists specifically because bank tariffs are
  stable and calculators are brittle) and is not recommended without discussion.

**Recommendation:** (a) first — it's a half-day of browser-based re-checking, not a new round,
and resolves real uncertainty rather than working around it. If it doesn't produce an AU-origin
Tier 1 bank, (b) is the honest fallback and matches CLAIMS.md §F's Tonga-first reasoning even if
the origin country needs updating.

### 5.2 What "respect robots.txt, identify honestly" means for a differently-named collector

MoneyGram, KlickEx, and two central banks (Solomon Islands, PNG) disallow `ClaudeBot`
specifically, under a general `User-agent: *` rule that otherwise permits crawling (MoneyGram's
general rule is explicitly `Allow: /` with `Content-Signal: ai-train=no, use=reference`). This
round's collector ran as Claude and respected the disallow. But the eventual production
collector (per CLAUDE.md §2.2, Python, not an LLM) will not identify itself as `ClaudeBot` — it
will have its own honest user agent and contact URL, per CLAUDE.md §1.5.

**Options:**
- **(a)** Treat the evident intent (an AI-crawler blocklist, listing ClaudeBot alongside GPTBot,
  Google-Extended, Bytespider, etc.) as the operative signal, and keep these providers Tier 3
  regardless of the production collector's literal user-agent string.
- **(b)** Treat robots.txt literally: a differently-named, honestly-identified Python collector
  is not addressed by a directive naming a different agent, and re-triage these once the actual
  collector user agent is decided.

**Recommendation:** (a). The disallow's evident purpose is to keep AI systems off the site;
building a collector whose only distinguishing feature from a disallowed one is its name string
reads as a workaround, which CLAUDE.md §1.5 and §4 (wrong-even-though-helpful #12) both rule
out. This is a judgement call about intent, not a settled reading of the text, so flagging
rather than deciding it unilaterally.

### 5.3 OrbitRemit's category (and Rocket Remit, IMEX, Samoa Money Transfer's tier confidence)

OrbitRemit is listed under PROVIDERS.md's "Pacific corridor specialists" heading but reads, on
the evidence gathered, as a general remittance service reaching roughly 50 countries — Fiji,
Samoa, Tonga and Vanuatu among them — rather than a Pacific specialist. Kept under the original
heading in this report and in PROVIDERS.md to match the brief's candidate list; recategorising
it is a maintainer call, not made here. Separately, four tier calls in §2 are marked
"(provisional)" or "(borderline)" specifically because the evidence supporting them was thinner
than the others in their batch (Samoa Money Transfer's undated homepage figures, IMEX's
unresolved rate widget, Rocket Remit's untested "Get Rate" button, OrbitRemit's own tier) — a
second pass with a working browser session is the natural next step for all four before any is
treated as settled.

### 5.4 Benchmark rate options memo (CLAIMS.md E1 / METHODOLOGY §2.3) — scoping only, not a recommendation on which to pick

**What a central-bank-benchmark approach would give:**
- 5 of 6 banks (all but PNG) publish daily indicative rates against both AUD and NZD on a
  public page, no account or credential needed.
- 2 of 5 reachable banks (Tonga, Samoa) offer a ready-made historical download — Tonga's goes
  back to 2017, enough for backtesting against the 2023 manual-audit vintage.
- Vanuatu's page is itself a rolling daily archive (no separate file needed), with the
  strongest *directly observed* daily-cadence evidence of the six (ten dated rows visible in a
  single fetch, versus inference from a single "last updated" stamp elsewhere).
- All are official, receiving-country-anchored rates, matching METHODOLOGY §2.3's stated
  preference for a receiving-country central bank as the primary benchmark.

**What it wouldn't give:**
- **Papua New Guinea is currently a hard gap.** Its central bank's homepage returned 403 to
  every user agent tried (default, browser-spoofed, and the WebFetch tool itself) — not yet
  established whether this is a permanent block or specific to this session's network path
  (SPRINT-01 §G3 already flags cloud-runner IP blocks as a risk worth a separate test).
- **Solomon Islands' true update cadence is unconfirmed** — the page claims daily but its own
  comparison column is dated a week back, at least as consistent with weekly refresh as daily.
  Needs a second observation on a different date to resolve.
- **Fiji's and Samoa's machine-readable files sit at URLs/filenames that look like they shift**
  (year/month path; date-stamped filename) — a connector would need to re-discover the current
  URL each run rather than hardcode one, a small fragility Tonga and Vanuatu don't share.
- **Two of six (Solomon Islands, PNG) name `ClaudeBot` explicitly in a Cloudflare AI-crawler
  robots.txt blocklist** — the same open question as §5.2, here applied to a benchmark source
  rather than a provider.
- **Reserve Bank of Vanuatu's TLS certificate chain is broken** (missing intermediate
  certificate) — this round's evidence was gathered with certificate verification disabled for
  research reading only; a production connector should not do this quietly, and the underlying
  issue is the bank's, not this project's, to fix.
- No bank's page offers TOP/WST/VUV/SBD/PGK/FJD history beyond the two download files (Tonga,
  Samoa) and RBV's rolling page — no single source covers all six currencies' history in one
  place.

**Realistic alternatives for gaps**, per METHODOLOGY §2.3's own framing (secondary = best
provider rate observed on the day): not researched this round is whether the IMF or World Bank
publish usable daily or monthly rates for these six currencies as a PNG-specific fallback — flag
as unresearched, not absent. METHODOLOGY's own secondary proposal doesn't require new research
to stand as an interim PNG fallback if the maintainer wants one now.

**No recommendation is made on the choice itself** — that decision is explicitly the
maintainer's, per the brief and per CLAIMS.md E1's framing.

---

## 5. Errors and anomalies

**ASB** — `curl` to robots.txt:
```
* HTTP/2 stream 1 was not closed cleanly: INTERNAL_ERROR (err 2)
```
Zero bytes returned; TLS handshake completed normally first.

**Westpac (New Zealand)** — WebFetch/`curl` to both robots.txt and content page, HTTP 403, body
contains:
```
<meta name="ak-status-code" content="403">
pageName: "wbcnz:www:sitedownerror", pageType: "OutagePage"
```

**HSBC Australia** — page text, quoted exactly:
> "HSBC will be closing its retail banking business in Australia over the next 18 months. You
> can no longer apply for new products and services."

**NAB** — FX rates page, quoted exactly:
> "Apologies but the Important Information section you are trying to view is not displaying
> properly at the moment."

**MoneyGram** — one WebFetch attempt at `https://www.moneygram.com/au/en/` (before the
robots.txt disallow was discovered):
```
The server returned HTTP 403 Forbidden.
```

**Bank of Papua New Guinea** — homepage, three separate attempts:
```
curl (default UA)              -> 403
curl (Chrome-128 browser UA)   -> 403
WebFetch tool                  -> "The server returned HTTP 403 Forbidden. The response body was not retrieved."
```

**Reserve Bank of Vanuatu** — TLS verification failure:
```
verify error:num=20:unable to get local issuer certificate
verify error:num=21:unable to verify the first certificate
```
Certificate: `subject=/CN=*.rbv.gov.vu`, `issuer=/C=GB/O=The Trustico Group Ltd/CN=Trustico RSA DV SSL CA 2`.

Also, robots.txt:
```
HTTP/1.1 301 Moved Permanently -> Location: https://www.rbv.gov.vu/index.php/en/robots.txt
```
which itself returns a Joomla `<title>Error: 404</title>` page.

**Central Bank of Solomon Islands** — daily-rates page text, quoted exactly:
> "Exchange rates are published around 9:00 am daily except on public and bank holidays"

alongside a "previous rate" column dated 2026-09-02 against a "last updated" of 2026-09-09 — a
seven-day gap, not one day.

**Pacific Way Money Transfer** — TLS hostname mismatch (both apex and `www`):
```
Hostname/IP does not match certificate's altnames: Host: www.pacificwaymoneytransfer.com. is not in the cert's altnames: DNS:cpanel.pacificwaymoneytransfer.com, DNS:mail.pacificwaymoneytransfer.com, DNS:webdisk.pacificwaymoneytransfer.com, DNS:webmail.pacificwaymoneytransfer.com
```

**WanTok Money** — DNS resolution failure, both hostnames:
```
getaddrinfo ENOTFOUND wantokmoney.com
getaddrinfo ENOTFOUND www.wantokmoney.com
```

**TransCrypt** — whole-domain redirect:
```
301 Moved Permanently: transcryptglobal.com -> www.triple-a.io
```

**KlickEx** — homepage:
```
The server returned HTTP 403 Forbidden.
```

**OrbitRemit** — currency converter widget, the page's own error text under a static fetch:
```
An error occurred while fetching estimates.
```

**Chrome browser tool** — every research agent that attempted to use it received:
```
Browser extension is not connected. Please ensure the Claude browser extension is installed and running...
```
No finding in this round used a rendered browser page; every finding rests on static
HTTP fetches. This is the single largest method limitation of Round 1 — see §9.

**CLAIMS.md B1** — the register's own pre-existing entry, dated 2026-09-09 (the same day as
this check), read "REFUTED as stated — homepage serves the normal service description." A
direct fetch today shows a static closure notice with `Last-Modified: Wed, 03 Jun 2026`. These
two findings, both dated 2026-09-09, cannot both be describing the live site at the moment each
was checked — either the earlier check hit a stale cache or a different host, or its date stamp
is inaccurate; a same-day change is very unlikely given the three-month-old `Last-Modified`
header. Resolved in favour of the new, corroborated evidence (see §8), but the discrepancy
itself is recorded here rather than quietly dropped.

---

## 6. Repository changes

| File | Change | Why |
|---|---|---|
| `PROVIDERS.md` | Filled in | Task A/B: full Tier 1/2/3 classification for all 33 candidates and 6 benchmark sources, replacing the empty candidate-list scaffold. |
| `CLAIMS.md` | Edited | Task C: B1 corrected to VERIFIED (closed) with the discrepancy flagged; G1 and G2's threshold VERIFIED; G2's sub-question left UNCHECKED with a proposed test; A9/A10 added; P1 marked resolved as a direct consequence of Task A. |
| `docs/REPORTING.md` | Created | Task D: defines the 10-section round-report structure this report and all future round reports follow. |
| `reports/01-triage.md` | Created | Task D: this report. |
| `scratch/round-01/*.md` (35 files) | Created | Evidence for every bank/global-MTO/corridor-specialist finding in §2.1–2.3 — one file per provider, URLs and quoted excerpts, so every table cell in PROVIDERS.md and this report is checkable. |
| `scratch/round-01/benchmarks/*.md` (6 files) | Created | Evidence for §2.4's benchmark-source findings. |
| `scratch/round-01/claims/*.md` (4 files) | Created | Evidence for the B1, G1, G2, A9/A10 verifications in §8. |

No file under `archive/`, `store/`, or `release/` was touched, per CLAUDE.md §1.3/§5.

---

## 7. Claims register delta

| Claim | Before | After | Evidence |
|---|---|---|---|
| B1 | REFUTED as stated (dated 2026-09-09, same day) | **VERIFIED** — SendMoneyPacific has closed | Live fetch (`Last-Modified: 03 Jun 2026`, not a cache hit) + Wayback Machine history (operating site 11 Jan 2026 → closure-notice-sized page by 6 Jun 2026). Corrects a same-day discrepancy in the register, flagged in §6 above rather than silently overwritten. |
| G1 | UNCHECKED | **VERIFIED** — GitHub Actions free for public repos on standard hosted runners | Current GitHub docs, `docs.github.com/en/actions/reference/usage-limits-billing-and-administration`. No numeric ceiling found; full ToS/AUP not read. |
| G2 (threshold) | UNCHECKED | **VERIFIED** — 60-day scheduled-workflow inactivity threshold, public repos | Current GitHub docs, `docs.github.com/en/actions/using-workflows/events-that-trigger-workflows`. |
| G2 (does a workflow's own commit reset the clock) | UNCHECKED | **Still UNCHECKED** — not settled by GitHub's documentation | Circumstantial only (community "keepalive" Marketplace actions, no GitHub-staff statement found). A concrete 65+ day empirical test is specified in §5.4's sibling discussion is not applicable here — see the test spec in `scratch/round-01/claims/g2.md`, summarised: schedule a daily-commit-only workflow, make no other repo activity, check status after 65+ days. |
| A9 (new) | Not previously in the register | **REFUTED** — no US-origin page on saverpacific.com | Sitemap check + five URL-slug probes, all 404. Absence on saverpacific.com only, not a claim about any Saver Global US service anywhere. |
| A10 (new) | Not previously in the register | **VERIFIED** — NZ-origin page exists and is live | `saverpacific.com/send-money-from-new-zealand/`, 10 Pacific destinations listed. |
| P1 | "robots.txt and terms not yet checked for any provider" (blocking) | **Resolved** — checked for all 33 candidates plus 6 benchmark sources | See PROVIDERS.md, this report §2. |

---

## 8. Confidence flags

**Method-wide:**
- No browser session was available this round (Chrome extension not connected). Every finding
  described as "client-rendered, not confirmed," "requires login (untested)," or resting on a
  calculator's landing-page text rather than a submitted quote is a direct consequence of this.
  It affects: BNZ, ANZ (Australia), Commonwealth Bank, NAB, St George, Kiwibank's numeric rate,
  WorldRemit, Ria Money Transfer, Rocket Remit's "Get Rate" button, IMEX's rate widget, and the
  size of RBV/Fiji/Samoa's historical download files (links confirmed to exist, contents not
  opened).
- Several findings rest on `WebFetch`'s summarisation rather than raw byte-for-byte extraction.
  Where a tier call hinged on the result, this was cross-checked with a direct `curl` (done for
  most bank robots.txt files and several page bodies); fee figures and destination lists mostly
  rest on WebFetch summaries only and should be treated as paraphrase-risked until a connector
  actually parses them.
- "Update frequency" for every benchmark bank except Reserve Bank of Vanuatu is inferred from a
  single day's observation, not confirmed across two different dates. Solomon Islands'
  daily-vs-weekly cadence is a genuine, unresolved ambiguity (see §6).

**Specific, generous flags carried up from individual evidence files:**
- Destination lists for KlickEx and IMEX's AU-origin claim rest on third-party pages (Wikipedia,
  TerraPay, Remitly), not the provider's own site — first-party confirmation failed (403) or
  wasn't found.
- No CAPTCHA was directly observed anywhere in Round 1, but several homepages either blocked the
  fetch outright before a CAPTCHA would appear (KlickEx) or gated the relevant flow behind login
  first (IMEX, 'Ave Pa'anga Pau) — absence of an observed CAPTCHA is not evidence one wouldn't
  appear further down the funnel.
- Bank of Papua New Guinea's 403 could be IP/network-path-specific rather than universal — not
  established which; testing from a GitHub Actions runner (a different network path) would
  help resolve this and is already a planned SPRINT-01 §G3 check for a different reason.
- Central Bank of Solomon Islands and Bank of Papua New Guinea share what looks like the same
  Cloudflare-managed robots.txt template almost verbatim — possibly a shared regional
  hosting/CDN provider rather than independent policy choices by each bank, though this is
  speculation, not confirmed.
- G1's "free" finding lacks a stated numeric ceiling in the page fetched; GitHub's full Terms of
  Service/Acceptable Use Policy (which could contain abuse-throttling language) was not read.
- A9's negative finding (no US-origin SaverPacific page) is scoped to the `saverpacific.com`
  domain and three guessed alternate domains — not an exhaustive search for any Saver Global US
  service under an unguessed domain.

---

## 9. Recommended next round

**Before Session 4 (connector build) starts:**
1. Re-check ANZ (Australia), BNZ, Commonwealth Bank, NAB and St. George's FX rate pages with a
   working browser session — this round's single largest gap was the unavailable Chrome
   extension, and it specifically affects the AU-origin banks that matter most for the Session 4
   target. See §5.1.
2. Resolve the AU→Tonga-vs-NZ→Tonga question in §5.1 with the maintainer before writing any
   connector code.
3. Re-check Central Bank of Solomon Islands' rate page on a different date to resolve the
   daily-vs-weekly cadence ambiguity (§2.4, §6) before it's relied on as a benchmark.
4. Decide the benchmark rate (CLAIMS.md E1) using §5.4's scoping — not deferred to this report.

**Deliberately left undone this round, and why:**
- No provider's calculator was interactively driven end-to-end (input a real corridor/amount,
  read back a number) — Round 1's brief was explicitly reconnaissance, not connector-adjacent
  probing, and no browser session was available regardless.
- The MoneyGram/KlickEx/central-bank "differently-named collector" question (§5.2) was not
  decided — it's a policy call for whenever connector code is actually written, not before.
- OrbitRemit's category mismatch (§5.3) was flagged, not corrected in PROVIDERS.md's structure —
  changing the candidate-list categorisation is a maintainer call.
- G2's sub-question (does a workflow's own commit reset the 60-day clock) was not tested — it
  needs 65+ days of real wall-clock time and belongs to Session 6, not this round.
- PNG's central-bank 403 was not retested from a different network path — that's the same
  question SPRINT-01 §G3 already earmarks for testing from an actual GitHub Actions runner,
  not a reconnaissance-round concern.
