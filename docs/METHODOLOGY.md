# METHODOLOGY v0.5 (draft — E1 and E2 decided; collection methods extended; E5 remains open)

**Do not treat this as settled.** Sections marked OPEN are research decisions for the
maintainer, not implementation details for an agent.

**Version history:**
- v0.5 (2026-09-10) resolves E2 (§2.2: fee-inclusion is per-observation, never inferred —
  proven necessary, not just cautious, by a real mixed-convention case in the 2023 audit);
  documents benchmark carry-forward on non-business days as a flagged, CLAUDE.md §1.1-excepted
  policy (§2.3); and records the benchmark-sensitivity finding as a quantified property (§2.3:
  benchmark choice moves cost levels by ~0.44pp on average but leaves rankings 99.8%
  undisturbed). See `reports/05-live.md`.
- v0.4 (2026-09-10) documents NRBT's published MID as the midpoint of the bank's own dealing
  spread, not an interbank mid-market rate, as a known limitation (§2.3) — a Round 4 correction
  after Round 3 treated a benchmark comparison as more authoritative than the underlying rate
  actually supports. See `reports/04-historical.md`.
- v0.3 (2026-09-09) adds `client_api` to §3's collection-method taxonomy, alongside a matching
  CLAUDE.md §3 revision redefining Tier 1 by reachability rather than markup shape — see
  CHANGELOG.md for the migration note.
- v0.2 (2026-09-09) decided §2.3 (E1, the benchmark rate) and rewrote it accordingly.

All other sections are unchanged from v0.1 and remain open as marked.

## 1. Unit of observation

```
corridor × amount × provider × service option × collection timestamp
```

Provider-level figures are *derived* from option-level observations, never collected as such.
A provider offering three funding/delivery combinations produces three observations.

## 2. Cost

### 2.1 Primary consumer outcome

For a fixed amount sent, the salient outcome is **how much the recipient receives**. Rank by
`amount_received` in the consumer view; show derived cost alongside.

### 2.2 Total effective cost

```
benchmark_receive_value = amount_sent × benchmark_rate
implicit_cost_value     = benchmark_receive_value − amount_received
cost_pct                = implicit_cost_value / benchmark_receive_value × 100
```

**RESOLVED (E2), 2026-09-10.** Where a provider deducts the fee from the sent amount rather than
adding it on top, the formula changes — and the 2023 audit ingestion (Round 4,
`reports/04-historical.md`) proved this is genuinely per-observation, not a rule that holds even
within one provider. Fitting `(amount_sent − fee) × rate` against 1,188 real audit rows worked
for nearly all of them, except Western Union's cash option on NZTON, 2023-07-26 — that row fits
`amount_sent × rate` (fee charged on top) far better (0.54 units off) than the deducted formula
(5.94 units off, against a ~1-unit tolerance everywhere else). Same provider, both conventions,
in the same 14-day audit window.

The resolution: `amount_sent_includes_fee` is recorded **per observation**, **never inferred**
from which formula the numbers happen to fit, and **left `null`** whenever the source doesn't
state it outright. A connector or importer may only set it to `true`/`false` when the source
*says* so explicitly (a fee schedule stating "fee deducted from transfer amount," for instance)
— never by back-solving. This is already how every connector and the 2023 audit importer behave;
this entry just makes the rule explicit rather than leaving it as an open question.

### 2.3 Benchmark rate — DECIDED (E1), 2026-09-09

Every cost figure depends on this and there is no clean answer. TOP, WST, VUV, SBD, PGK and
FJD have no deep interbank market — that constraint doesn't go away with a decision, it just
stops blocking work.

**Primary: receiving-country central bank published daily indicative rate.** Adopted on the
scoping in `reports/01-triage.md` §5.4. **National Reserve Bank of Tonga is the first source
built** (Round 2), on the strength of its single-file history back to 2017 (covering the 2023
manual-audit vintage) and a stable, non-date-keyed URL — the strongest of the six candidates
scoped in Round 1. The same primary source is adopted for the other five central banks as
connectors are built for their corridors, subject to the per-bank caveats already on record in
`PROVIDERS.md`: Fiji's and Samoa's downloadable-file URLs/filenames appear to shift and need
re-discovery each run rather than a hardcoded link; Solomon Islands' true update cadence
(daily vs weekly) is unconfirmed; Papua New Guinea's site is currently unreachable (403 to
every user agent tried) and access is `PENDING_PERMISSION`, not attempted around; **Reserve
Bank of Vanuatu's TLS certificate chain is broken and is not worked around** — it stays Tier 3
as a benchmark source, exactly as it would as a provider, per CLAUDE.md §1.5's instruction
against circumventing a control (a broken certificate chain is not "public" access).

**What a central bank's published indicative rate actually is.** This is not a live
interbank mid-market rate, and should never be described as one. It is the rate the bank
itself publishes for its own reference purposes — typically its own buy/sell/mid quotes for
its own counter transactions, sometimes doubling as an official reference for customs or
statistical use. For currencies with no deep interbank market — every currency this project
covers — this published figure is usually the most authoritative public reference available,
but it embeds whatever margin or methodology the issuing bank itself uses to set it, and may
lag actual market conditions. Treat it as "the best available public reference for this
currency," not as a neutral wholesale rate that exists independently of any one institution's
judgement. `benchmark_source` records which bank published the rate used; `benchmark_fx_rate`
is archived exactly as raw as `provider_fx_rate` — both are observed figures, never assumed or
derived from each other.

**Known limitation, concrete case (added 2026-09-10, Round 4 correction):** NRBT's published
MID rate is not an interbank mid-market rate — it is the midpoint of the bank's own dealing
spread, i.e. `(BUY + SELL) / 2` of the rate NRBT itself would buy or sell foreign currency at
its own counter. On 2026-09-09, NZD showed BUY 0.7367 / MID 0.7210 / SELL 0.7052 — a spread of
roughly ±2.2% either side of the midpoint. A benchmark built from this MID is therefore already
carrying NRBT's own commercial margin before any provider is compared against it; it is the
best available public reference for TOP (§2.3 above), not a margin-free reference point. This
is exactly why the secondary benchmark (below) stays load-bearing rather than optional: a
provider rate that beats the MID by less than roughly the half-spread may still be within
NRBT's own normal commercial range, not necessarily cheap in any deeper sense.

**Secondary: best observed provider rate, retained from the first collection run.** Store both
`benchmark_fx_rate` (central bank) and, where available, the best provider rate observed on the
same day, as a dependency-free robustness check. This does not change which rate the primary
cost figures are computed against — it is stored alongside so a referee who dislikes the
primary choice can recompute with the other, per the original framing this decision confirms.

Whatever the choice, the benchmark series is archived daily alongside the quotes and is part of
the release. A cost figure whose benchmark cannot be reproduced is not reproducible.

**Carry-forward on non-business days, maintainer decision 2026-09-10
(`reports/05-live.md`, CLAUDE.md §1.1's exception).** NRBT (like most receiving-country central
banks here) publishes no rate on weekends or public holidays, but provider quotes exist every
day — Round 4's ingestion of the 2023 audit found 408 of 1,188 provider observations (34%) had
no same-day benchmark to compare against, and every one fell on a weekend or an AU/NZ public
holiday, not a data gap. Losing a third of observations to the benchmark's publication calendar
is a worse trade than a flagged approximation: a benchmark date with no published rate carries
the last published business day's rate forward, with `benchmark_is_carried_forward = true` and
`benchmark_age_days` set to how many days stale it is. This is never silent, never applied to a
provider's own quote (only to the benchmark side), and never applied more than however many
consecutive non-business days actually elapsed — it does not paper over a genuine multi-day
outage in the source, it only bridges the calendar gap the source itself declares (a weekend, a
holiday), and `benchmark_age_days` makes exactly how far it reached visible in the data, not
buried in a script.

**Benchmark choice materially shifts cost *levels*, not *rankings* — a quantified property, not
just an expectation.** Round 4's Task C compared `cost_pct` computed from the NRBT benchmark
against the 2023 audit's own independently-computed cost figure (a different, undocumented
benchmark), across the 780 matched rows: Pearson correlation 0.988, 97.7% agreement on sign,
**100% agreement on which provider was cheapest** across all 110 date×corridor groups with 2+
providers, mean within-day Spearman rank correlation 0.998 — but a **systematic mean gap of
about 0.44 percentage points** (NRBT-based figures running lower), consistent in direction
across the sample (median −0.47, std 0.85). In other words: which benchmark you choose barely
moves who looks cheapest on a given day, but it does move the absolute cost percentage you'd
report for any one provider by a small, consistent, non-trivial amount. Cite this finding, with
these numbers, before treating a headline cost percentage as benchmark-independent — it isn't,
even though the ranking mostly is.

### 2.4 FX margin

```
fx_margin_pct ≈ 1 − (provider_rate / benchmark_rate)
```

Sign and quote orientation must be standardised and documented per currency pair. Keep both
raw rates so others can construct their own definition.

### 2.5 Fees

Store the amount, the currency, whether it is included in the send amount, whether it is
promotional or waived, and whether a recipient-side or intermediary fee is excluded.

**A zero advertised fee is never a zero cost.**

## 3. Collection methods — never mixed silently

```
published_tariff     reconstructed from a public FX table + public fee schedule,
                      read directly from the page's own server-rendered HTML
client_api           reconstructed the same way, but the number comes from a public
                      JSON/XHR endpoint the page's own client-side script calls,
                      fetched directly rather than rendering the page — added
                      v0.3, 2026-09-09, see CLAUDE.md section 3 and section 1.5's
                      "what is and is not a workaround"
public_quote         returned by a public calculator for fixed inputs
manual_audit         hand-collected (the 2023 vintage)
```

`published_tariff` and `client_api` are both Tier 1 (CLAUDE.md §3: reachable without
defeating anything) but are never folded into one `collection_method` value — a `client_api`
observation carries a different brittleness profile (an undocumented endpoint can change
shape without any visible page redesign to warn of it) and that difference must stay visible
in the data, not just in a connector's source comments.

Every release states the method mix. Any statistic combining methods says so.

## 4. Freshness — four distinct concepts

```
collected_at              when we fetched
provider_quote_timestamp  when the provider says the price was set, if disclosed
source_last_updated       when the source page says it last changed, if disclosed
quote_validity            how long it holds, if disclosed
```

Never collapse these. Unknown is `null`, never the collection time.

## 5. Rankings

**Option-level:** the actual consumer choice.
**Provider-level:** cheapest valid option per provider under stated constraints.

Both are published. The rule is explicit and selectable, never implicit.

## 6. Coverage

Every release publishes an observability map: which providers are Tier 1, 2 and 3 on that
date, and which corridor/amount cells were successfully observed.

**OPEN:** whether headline statistics should be computed on a balanced panel of consistently
observable providers, or on all observed providers with coverage stated. The former is
comparable over time; the latter reflects the market. Probably publish both.

## 7. Corridor exceptions

**OPEN (E5):** Niue shares a banking system with New Zealand, making free bank transfers
available and cheapest-provider rankings misleading. Cook Islands and Tokelau may be similar.
Decide an exclusion or annotation rule before publication.

## 8. Versioning

This document is versioned. A change to any definition above requires a version bump, a
`CHANGELOG.md` entry, and a note in the affected releases. Historical observations are never
recomputed silently under a new definition.
