# PROVIDERS.md — collection triage

One row per provider. Filled in Sprint 1, Session 3. **Not** a coverage target: a map of what
is and isn't observable, published as a finding in its own right.

Candidate list drawn from the operators publicly listed as serving AU/NZ → Pacific corridors as
at 2026-09-09. That is market-structure information, not another platform's data.

## Tiers

- **1 — published tariff.** Public daily FX table + public fee schedule. Quote reconstructed
  arithmetically. Stable, cheap, low-brittleness. Flag `collection_method = published_tariff`.
- **2 — public quote calculator.** Public page returns a quote for fixed inputs, no account.
  Flag `collection_method = public_quote`.
- **3 — unobservable.** No public surface, credentials required, or automated access blocked.
  Flag `availability_status = unobservable`. Re-check quarterly. Do not work around.

## Columns

`provider` · `type` (bank / global MTO / corridor specialist / fintech) · `AU origin` ·
`NZ origin` · `Pacific destinations served` · `public FX table?` · `public fee schedule?` ·
`public calculator?` · `account required?` · `CAPTCHA / bot wall?` · `robots.txt permits?` ·
`tier` · `priority` · `date checked` · `notes`

## Candidates

### Banks — check Tier 1 first
ANZ · ASB · BNZ · Commonwealth Bank · HSBC · Kiwibank · National Australia Bank ·
St. George · Suncorp · Westpac

Banks are the expensive tail in the 2023 data, so having them cleanly matters. They usually
publish a daily FX table and a fee schedule, which together reconstruct a quote without any
transactional flow. Start here.

### Global MTOs — likely Tier 2, likely brittle
MoneyGram · Ria Money Transfer · Western Union · WorldRemit · Wise · Xe Money Transfer ·
Remitly · Revolut · OFX

Public calculators are common; bot walls are also common. Expect several to fail from a cloud
runner while working locally.

### Pacific corridor specialists — expect Tier 3, and record it honestly
'Ave Pa'anga Pau · IMEX · Island Flexi Transfer · KlickEx · KlickEx Pacific ·
Lotus Foreign Exchange · OrbitRemit · Pacific Ezy · Pacific Way · Rocket Remit ·
Samoa Money Transfer · The Ink Patch · TransCrypt · WanTok Money

**These matter most and are hardest to reach.** In the 2023 audit the corridor specialists
were repeatedly the cheapest options. Several have no automatable public quote surface at all.

Do not paper over this. A panel that silently omits the cheapest providers will systematically
overstate the cost of remitting, which is the exact error the project exists to avoid. The
coverage map must be published alongside every release, and any headline statistic must state
which providers it does and does not include.

## Benchmark sources

Same triage, under `collect/benchmarks/`. Receiving-country central banks publishing daily
indicative rates: Reserve Bank of Fiji · National Reserve Bank of Tonga ·
Central Bank of Samoa · Reserve Bank of Vanuatu · Central Bank of Solomon Islands ·
Bank of Papua New Guinea.

## Known corridor exceptions

**Niue.** Shares a banking system with New Zealand; ordinary bank transfers are free. A
cheapest-provider ranking for NZ → Niue is misleading without annotation. The same may apply
to Cook Islands and Tokelau. Decide the exclusion or annotation rule before publication, not
after someone notices.
