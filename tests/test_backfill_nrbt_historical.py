"""Golden tests for the NRBT historical backfill's parsing logic (Round 4,
reports/04-historical.md, Task B). Uses a small synthetic DataFrame shaped like the real
workbook, not the full file -- fast, offline, and exercises the specific edge cases the real
file actually contains: a "Public Holiday" text cell, a genuine NaN cell, and an out-of-range
stray date.
"""
from __future__ import annotations

import math

import pandas as pd
import pytest

from collect.archive import ARCHIVE_ROOT
from collect.backfill_nrbt_historical import (
    BUY_BLOCK_START,
    CURRENCY_OFFSETS,
    MID_BLOCK_START,
    SELL_BLOCK_START,
    build_observation,
    parse_sheet,
)


def _make_sheet_df(rows: list[dict]) -> pd.DataFrame:
    """rows: list of {"date": <str or None>, "AUD": (buy,mid,sell) or None, "NZD": (...)}.
    Builds a 6-header-row + N-data-row frame matching the real file's column layout (39 cols,
    9 currencies x 3 blocks + date column)."""
    ncols = SELL_BLOCK_START + 9  # matches the real file's 39-column layout
    header_rows = [[None] * ncols for _ in range(6)]
    data_rows = []
    for r in rows:
        row = [None] * ncols
        row[0] = r.get("date")
        for ccy, offset in CURRENCY_OFFSETS.items():
            triple = r.get(ccy)
            if triple is None:
                continue
            row[BUY_BLOCK_START + offset] = triple[0]
            row[MID_BLOCK_START + offset] = triple[1]
            row[SELL_BLOCK_START + offset] = triple[2]
        data_rows.append(row)
    return pd.DataFrame(header_rows + data_rows)


def test_parses_a_clean_row_for_both_currencies():
    df = _make_sheet_df([{"date": "2023-07-25", "AUD": (0.65, 0.63, 0.62), "NZD": (0.71, 0.69, 0.68)}])
    valid, excluded = parse_sheet(df, "2023 to 2024")
    assert len(valid) == 1
    assert excluded == []
    assert valid[0]["rates"]["AUD"] == {"buy": 0.65, "mid": 0.63, "sell": 0.62}
    assert valid[0]["rates"]["NZD"] == {"buy": 0.71, "mid": 0.69, "sell": 0.68}


def test_excludes_a_public_holiday_text_cell_not_a_fabricated_rate():
    df = _make_sheet_df(
        [{"date": "2017-01-02", "AUD": ("Public Holiday: New Year's Day",) * 3, "NZD": (0.71, 0.69, 0.68)}]
    )
    valid, excluded = parse_sheet(df, "2017 to 2018")
    assert len(valid) == 1
    assert "AUD" not in valid[0]["rates"]
    assert valid[0]["rates"]["NZD"] == {"buy": 0.71, "mid": 0.69, "sell": 0.68}


def test_excludes_a_genuine_nan_cell_not_stored_as_a_nan_rate():
    # The real bug this test guards against: float(nan) succeeds silently, so an early version
    # of this parser stored NaN as if it were a real rate.
    df = _make_sheet_df([{"date": "2017-01-02", "NZD": (float("nan"), float("nan"), float("nan"))}])
    valid, excluded = parse_sheet(df, "2017 to 2018")
    assert len(valid) == 1
    assert "NZD" not in valid[0]["rates"]
    for ccy_rates in valid[0]["rates"].values():
        assert not any(math.isnan(v) for v in ccy_rates.values())


def test_excludes_an_out_of_range_stray_date():
    df = _make_sheet_df(
        [
            {"date": "2003-07-17", "AUD": (0.6, 0.59, 0.58), "NZD": (0.7, 0.69, 0.68)},
            {"date": "2017-06-01", "AUD": (0.6, 0.59, 0.58), "NZD": (0.7, 0.69, 0.68)},
        ]
    )
    valid, excluded = parse_sheet(df, "2017 to 2018")
    assert len(valid) == 1
    assert len(excluded) == 1
    assert excluded[0]["date"].isoformat() == "2003-07-17"


def test_build_observation_sets_collected_at_and_provider_quote_timestamp_correctly():
    df = _make_sheet_df([{"date": "2023-07-25", "NZD": (0.7108, 0.6943, 0.6778)}])
    valid, _ = parse_sheet(df, "2023 to 2024")

    obs = build_observation(
        date=valid[0]["date"],
        origin_currency="NZD",
        rates=valid[0]["rates"],
        sha256="f" * 64,
        archive_path=ARCHIVE_ROOT / "nrbt" / "2026" / "09" / "09" / ("f" * 64 + ".json.gz"),
        collection_run_id="backfill-test",
    )

    assert obs["collected_at"].startswith("2026-09-09")  # the real, single fetch date
    assert obs["provider_quote_timestamp"].startswith("2023-07-25")  # the historical date
    assert obs["origin_currency"] == "NZD"
    assert obs["origin_country_iso3"] == "NZL"
    assert obs["collection_method"] == "published_tariff"
    assert obs["rate_is_promotional"] is False
    assert obs["provider_fx_rate"] == pytest.approx(1 / 0.6943, rel=1e-9)
