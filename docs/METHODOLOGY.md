# METHODOLOGY v0.3 (draft — E1 decided; collection methods extended; other OPEN items remain)

**Do not treat this as settled.** Sections marked OPEN are research decisions for the
maintainer, not implementation details for an agent.

**Version history:**
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

**OPEN (E2):** where a provider deducts the fee from the sent amount rather than adding it,
the formula changes. Record `amount_sent_includes_fee` per observation. Never assume.

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

**Secondary: best observed provider rate, retained from the first collection run.** Store both
`benchmark_fx_rate` (central bank) and, where available, the best provider rate observed on the
same day, as a dependency-free robustness check. This does not change which rate the primary
cost figures are computed against — it is stored alongside so a referee who dislikes the
primary choice can recompute with the other, per the original framing this decision confirms.

Whatever the choice, the benchmark series is archived daily alongside the quotes and is part of
the release. A cost figure whose benchmark cannot be reproduced is not reproducible.

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
