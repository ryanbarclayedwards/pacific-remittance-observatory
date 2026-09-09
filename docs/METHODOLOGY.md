# METHODOLOGY v0.1 (draft — decisions open)

**Do not treat this as settled.** Sections marked OPEN are research decisions for the
maintainer, not implementation details for an agent.

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

### 2.3 Benchmark rate — OPEN (E1), BLOCKING

Every cost figure depends on this and there is no clean answer. TOP, WST, VUV, SBD, PGK and
FJD have no deep interbank market.

Proposal, to be confirmed:

- **Primary:** receiving-country central bank published daily indicative rate.
- **Secondary:** best provider rate observed on the day, as a dependency-free robustness check.
- Store both. Parameterise the derived layer by benchmark choice so a referee who dislikes one
  can re-run with the other.

Whatever is chosen, the benchmark series is archived daily alongside the quotes and is part of
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
published_tariff     reconstructed from a public FX table + public fee schedule
public_quote         returned by a public calculator for fixed inputs
manual_audit         hand-collected (the 2023 vintage)
```

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
