"""Shared benchmark-rate resolver (Round 6, reports/06-live.md, Task C).

Round 4's ingestion of the 2023 audit found 408 of 1,188 provider observations (34%) had no
same-day NRBT benchmark to compare against -- every one on a weekend or an AU/NZ public
holiday, not a data gap (Round 4, reports/04-historical.md). Round 5 recorded the fix as
policy (CLAUDE.md section 1.1's narrow, explicit carry-forward exception; schema.json v0.3's
`benchmark_is_carried_forward` / `benchmark_age_days`) but deliberately deferred building it.

**Carry-forward happens at the point of use, not the point of storage** (maintainer decision,
this round). `store/` holds only what NRBT actually published -- this resolver derives a
carried-forward answer on demand from that real data and flags it every time. No synthetic row
is ever written back to `store/`; regenerating the 2017-2026 historical series with ~2,000
carried-forward rows baked in would confuse an observation (what NRBT published) with an
inference (what we assume applied on a day it published nothing), which is exactly the
distinction CLAUDE.md section 1.1 exists to protect.

Usage: build a `published_rates` lookup once (via `load_published_rates_from_store()` for real
use, or a small dict literal for a test), then call `resolve_benchmark_rate()` per date/currency
pair as needed -- by the live connector deciding what to write for benchmark_fx_rate-adjacent
fields, or by any future cost_pct analysis joining provider quotes to a benchmark.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
STORE_DIR = REPO_ROOT / "store" / "observations"

# A genuine multi-day source outage should surface as "unresolvable", not be silently bridged
# forever -- this bounds how far back a carry-forward search reaches. Wide enough to cross a
# long weekend plus an adjacent public holiday (the longest gap actually observed in Round 4's
# ingestion was 3 calendar days: Good Friday through Easter Monday), narrow enough that a real
# outage doesn't get quietly papered over.
MAX_CARRY_FORWARD_DAYS = 10


@dataclass(frozen=True)
class BenchmarkResolution:
    rate: float
    is_carried_forward: bool
    age_days: int
    source_observation_id: str
    source_date: date


def resolve_benchmark_rate(
    target_date: date,
    currency: str,
    published_rates: dict[tuple[date, str], tuple[float, str]],
) -> BenchmarkResolution | None:
    """published_rates: {(date, currency): (rate, observation_id)} -- genuinely published rates
    only; never itself contains a carried-forward entry (there is nothing to carry forward
    from a carry-forward -- always resolve back to a real publication).

    Returns None if no published rate exists for target_date or any of the
    MAX_CARRY_FORWARD_DAYS days before it -- a real gap, not bridged indefinitely.
    """
    key = (target_date, currency)
    if key in published_rates:
        rate, obs_id = published_rates[key]
        return BenchmarkResolution(
            rate=rate,
            is_carried_forward=False,
            age_days=0,
            source_observation_id=obs_id,
            source_date=target_date,
        )

    for offset in range(1, MAX_CARRY_FORWARD_DAYS + 1):
        candidate_date = target_date - timedelta(days=offset)
        key = (candidate_date, currency)
        if key in published_rates:
            rate, obs_id = published_rates[key]
            return BenchmarkResolution(
                rate=rate,
                is_carried_forward=True,
                age_days=offset,
                source_observation_id=obs_id,
                source_date=candidate_date,
            )

    return None


def load_published_rates_from_store(
    *, provider_id: str = "nrbt", store_dir: Path = STORE_DIR
) -> dict[tuple[date, str], tuple[float, str]]:
    """Build the {(date, currency): (rate, observation_id)} lookup from the real store.

    A row counts as "genuinely published" if it's a provider_id="nrbt" observation with
    availability_status="observed" -- both the live daily connector's rows and the historical
    backfill's rows qualify equally; both represent NRBT actually publishing a rate for that
    date, just fetched at different times (collect/benchmarks/nrbt/connector.py's run() vs
    collect/backfill_nrbt_historical.py). The date used is provider_quote_timestamp if present
    (the backfill's convention -- the historical date the rate applied to), falling back to
    collected_at (the live connector's convention -- collected same-day, so collected_at *is*
    the rate's date).
    """
    rates: dict[tuple[date, str], tuple[float, str]] = {}
    if not store_dir.is_dir():
        return rates

    for csv_path in sorted(store_dir.glob("*.csv")):
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("provider_id") != provider_id:
                    continue
                if row.get("availability_status") != "observed":
                    continue
                rate_s = row.get("provider_fx_rate", "")
                if not rate_s:
                    continue
                currency = row.get("origin_currency", "")
                date_s = row.get("provider_quote_timestamp") or row.get("collected_at")
                if not date_s:
                    continue
                obs_date = datetime.fromisoformat(date_s).date()
                rates[(obs_date, currency)] = (float(rate_s), row.get("observation_id", ""))

    return rates
