"""Golden tests for the benchmark carry-forward resolver (Round 6, reports/06-live.md, Task C).

Synthetic weekend/holiday gaps, not real store data -- fast, offline, and lets each edge case
be constructed precisely rather than hoping the real store happens to contain one.
"""
from __future__ import annotations

import csv
from datetime import date, timedelta

import pytest

from collect.benchmark_lookup import (
    MAX_CARRY_FORWARD_DAYS,
    resolve_benchmark_rate,
    load_published_rates_from_store,
)

# A small synthetic week: Friday 2026-09-04 published, Sat/Sun not, Monday 2026-09-07 published.
RATES = {
    (date(2026, 9, 4), "NZD"): (1.40, "obs-fri-nzd"),
    (date(2026, 9, 4), "AUD"): (1.65, "obs-fri-aud"),
    (date(2026, 9, 7), "NZD"): (1.41, "obs-mon-nzd"),
}


def test_returns_the_direct_rate_when_published_that_day():
    r = resolve_benchmark_rate(date(2026, 9, 4), "NZD", RATES)
    assert r is not None
    assert r.rate == 1.40
    assert r.is_carried_forward is False
    assert r.age_days == 0
    assert r.source_observation_id == "obs-fri-nzd"
    assert r.source_date == date(2026, 9, 4)


def test_carries_forward_across_a_single_weekend_day():
    r = resolve_benchmark_rate(date(2026, 9, 5), "NZD", RATES)  # Saturday
    assert r is not None
    assert r.rate == 1.40
    assert r.is_carried_forward is True
    assert r.age_days == 1
    assert r.source_observation_id == "obs-fri-nzd"
    assert r.source_date == date(2026, 9, 4)


def test_carries_forward_across_a_full_weekend():
    r = resolve_benchmark_rate(date(2026, 9, 6), "NZD", RATES)  # Sunday
    assert r is not None
    assert r.rate == 1.40  # still Friday's rate
    assert r.is_carried_forward is True
    assert r.age_days == 2
    assert r.source_date == date(2026, 9, 4)


def test_currencies_are_resolved_independently():
    # AUD has no Monday rate in this fixture -- only NZD does. Confirms the resolver doesn't
    # cross-contaminate currencies when walking backward.
    r_nzd = resolve_benchmark_rate(date(2026, 9, 7), "NZD", RATES)
    r_aud = resolve_benchmark_rate(date(2026, 9, 7), "AUD", RATES)
    assert r_nzd.is_carried_forward is False  # Monday NZD is directly published
    assert r_aud.is_carried_forward is True  # Monday AUD carries Friday forward
    assert r_aud.age_days == 3
    assert r_aud.source_observation_id == "obs-fri-aud"


def test_returns_none_when_nothing_within_the_lookback_window():
    target = date(2026, 9, 4) + timedelta(days=MAX_CARRY_FORWARD_DAYS + 5)
    r = resolve_benchmark_rate(target, "NZD", RATES)
    assert r is None


def test_never_carries_forward_from_a_carry_forward_two_gaps_in_a_row():
    # Two separate one-day gaps, each with its own real publication before it -- the resolver
    # must always land on a genuinely published rate, never chain through a hypothetical
    # carried-forward one (there's no such thing stored, by design).
    rates = {
        (date(2026, 1, 1), "NZD"): (1.30, "obs-a"),
        (date(2026, 1, 3), "NZD"): (1.35, "obs-b"),
    }
    r = resolve_benchmark_rate(date(2026, 1, 2), "NZD", rates)  # gap day, between a and b
    assert r.source_observation_id == "obs-a"  # the nearest *prior* real publication
    assert r.age_days == 1

    r2 = resolve_benchmark_rate(date(2026, 1, 3), "NZD", rates)  # directly published
    assert r2.is_carried_forward is False
    assert r2.source_observation_id == "obs-b"


def _write_store_csv(path, rows, columns):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for row in rows:
            writer.writerow([row.get(c, "") for c in columns])


def test_load_published_rates_from_store_prefers_provider_quote_timestamp(tmp_path):
    columns = [
        "observation_id", "provider_id", "availability_status", "origin_currency",
        "provider_fx_rate", "provider_quote_timestamp", "collected_at",
    ]
    _write_store_csv(
        tmp_path / "2026-09.csv",
        [
            {
                "observation_id": "backfill-row",
                "provider_id": "nrbt",
                "availability_status": "observed",
                "origin_currency": "NZD",
                "provider_fx_rate": "1.39",
                "provider_quote_timestamp": "2026-09-04T00:00:00+00:00",
                "collected_at": "2026-09-09T11:30:00+00:00",  # the backfill's real fetch date
            },
            {
                "observation_id": "live-row",
                "provider_id": "nrbt",
                "availability_status": "observed",
                "origin_currency": "NZD",
                "provider_fx_rate": "1.42",
                "provider_quote_timestamp": "",
                "collected_at": "2026-09-10T11:00:00+00:00",  # live connector: same-day
            },
            {
                "observation_id": "orbitremit-row",  # a non-NRBT row -- must be ignored
                "provider_id": "orbitremit",
                "availability_status": "observed",
                "origin_currency": "AUD",
                "provider_fx_rate": "1.73",
                "provider_quote_timestamp": "",
                "collected_at": "2026-09-10T11:00:00+00:00",
            },
            {
                "observation_id": "error-row",  # not "observed" -- must be ignored
                "provider_id": "nrbt",
                "availability_status": "error",
                "origin_currency": "NZD",
                "provider_fx_rate": "",
                "provider_quote_timestamp": "",
                "collected_at": "2026-09-11T11:00:00+00:00",
            },
        ],
        columns,
    )

    rates = load_published_rates_from_store(store_dir=tmp_path)

    # Backfill row: dated by its own historical date (2026-09-04), not its fetch date.
    assert rates[(date(2026, 9, 4), "NZD")] == (1.39, "backfill-row")
    # Live row: no provider_quote_timestamp, falls back to collected_at (2026-09-10).
    assert rates[(date(2026, 9, 10), "NZD")] == (1.42, "live-row")
    # Non-NRBT and non-observed rows excluded.
    assert (date(2026, 9, 10), "AUD") not in rates
    assert len(rates) == 2
