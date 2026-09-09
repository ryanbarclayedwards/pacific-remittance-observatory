"""Backfill: National Reserve Bank of Tonga's 2017-present historical rate file.

Not a connector -- deliberately not registered in collect.run.CONNECTORS. This is a one-off,
manually-run import of a file already fetched and assessed (Round 2,
scratch/round-02/nrbt-historical-assessment.md; Round 4, reports/04-historical.md, Task B).
Run it once with `python -m collect.backfill_nrbt_historical`.

Source file: scratch/round-02/nrbt-historical-rates.xlsx, fetched 2026-09-09 (Round 2). Five
sheets, one per two-year period, each with three side-by-side BUY/MID/SELL blocks (9 currencies
each) sharing one date column. Only NZD and AUD are imported -- the same two origin currencies
the live NRBT connector (collect/benchmarks/nrbt/connector.py) already covers; extending to the
other seven currencies the file happens to contain would be speculative coverage, not something
this project currently needs (see that connector's own ORIGIN_CURRENCIES comment).

Freshness fields (METHODOLOGY.md section 4): `collected_at` is fixed at the file's actual fetch
time, 2026-09-09 -- that is genuinely when this project fetched the underlying bytes, once, in
a single request. `provider_quote_timestamp` carries each row's own historical date -- the date
NRBT's own table says the rate applied to. These are never collapsed into each other: this
backfill is not "presented as same-day collection" for any of its ~2,470-per-currency historical
dates (CLAUDE.md section 1.3), because collected_at correctly stays fixed at the one real fetch
date throughout.

Known data-quality exclusion (Round 2): three rows across the five sheets carry a date outside
their own sheet's nominal two-year range (e.g. a row dated 2028 inside the "2025 to 2026"
sheet) -- single-cell errors in NRBT's own workbook. These are excluded from import and logged
explicitly by this script, never silently dropped and never imported as if genuine.
"""
from __future__ import annotations

import argparse
import math
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from collect.archive import ARCHIVE_ROOT, archive_bytes
from collect.store import append_observations

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILE = REPO_ROOT / "scratch" / "round-02" / "nrbt-historical-rates.xlsx"
SOURCE_URL = "https://www.reservebank.to/data/docs/fmarkets/exrates/average_daily_exchange_rates.xlsx"
PROVIDER_ID = "nrbt"
PROVIDER_NAME_RAW = "National Reserve Bank of Tonga"
CONNECTOR_ID = "benchmarks.nrbt.historical_backfill"
CONNECTOR_VERSION = "0.1.0"
METHODOLOGY_VERSION = "0.4"

# The file's actual, single fetch time (Round 2). Not "now" -- see module docstring.
FETCHED_AT = datetime(2026, 9, 9, 11, 30, 0, tzinfo=timezone.utc)

# Column layout, 0-indexed from column 0 (the shared date column). Confirmed against the raw
# file in Round 2 (scratch/round-02/nrbt-historical-assessment.md) and re-verified here.
CURRENCY_OFFSETS = {"AUD": 0, "EUR": 1, "FJD": 2, "GBP": 3, "JPY": 4, "NZD": 5, "USD": 6, "WST": 7, "CHF": 8}
BUY_BLOCK_START = 1
MID_BLOCK_START = 14
SELL_BLOCK_START = 27

# Origin currencies this backfill imports -- deliberately narrow, see module docstring.
ORIGIN_CURRENCIES = {"NZD": "NZL", "AUD": "AUS"}


def parse_sheet(df: pd.DataFrame, sheet_name: str) -> tuple[list[dict], list[dict]]:
    """Returns (valid_rows, excluded_rows). Each row dict: {date, rates: {CCY: {buy,mid,sell}}}."""
    lo_s, hi_s = sheet_name.split(" to ")
    lo_year, hi_year = int(lo_s), int(hi_s)

    raw_dates = pd.to_datetime(df.iloc[6:, 0], errors="coerce")
    valid_rows: list[dict] = []
    excluded_rows: list[dict] = []

    for idx, date in raw_dates.items():
        if pd.isna(date):
            continue
        row = df.iloc[idx]
        rates = {}
        for ccy, offset in CURRENCY_OFFSETS.items():
            if ccy not in ORIGIN_CURRENCIES:
                continue
            try:
                buy = float(row[BUY_BLOCK_START + offset])
                mid = float(row[MID_BLOCK_START + offset])
                sell = float(row[SELL_BLOCK_START + offset])
            except (TypeError, ValueError):
                continue
            # float(nan) succeeds silently (nan is a valid float) -- a blank or non-numeric
            # cell (e.g. "Public Holiday: New Year's Day", or a genuinely empty cell) must be
            # excluded explicitly, not accidentally stored as a NaN rate.
            if math.isnan(buy) or math.isnan(mid) or math.isnan(sell):
                continue
            rates[ccy] = {"buy": buy, "mid": mid, "sell": sell}

        record = {"date": date.date(), "sheet": sheet_name, "rates": rates}
        if lo_year <= date.year <= hi_year:
            valid_rows.append(record)
        else:
            excluded_rows.append(record)

    return valid_rows, excluded_rows


def build_observation(
    *,
    date,
    origin_currency: str,
    rates: dict,
    sha256: str,
    archive_path: Path,
    collection_run_id: str,
) -> dict:
    row = rates[origin_currency]
    top_per_origin = 1 / row["mid"]
    quote_ts = datetime(date.year, date.month, date.day, tzinfo=timezone.utc)

    return {
        "observation_id": str(uuid.uuid4()),
        "collection_run_id": collection_run_id,
        "supersedes": None,
        "correction_reason": None,
        "collected_at": FETCHED_AT.isoformat(),
        "provider_quote_timestamp": quote_ts.isoformat(),
        "source_last_updated": None,
        "quote_validity_text": None,
        "collection_method": "published_tariff",
        "source_system": "collector",
        "source_url": SOURCE_URL,
        "connector_id": CONNECTOR_ID,
        "connector_version": CONNECTOR_VERSION,
        "methodology_version": METHODOLOGY_VERSION,
        "origin_country_iso3": ORIGIN_CURRENCIES[origin_currency],
        "origin_currency": origin_currency,
        "destination_country_iso3": "TON",
        "destination_currency": "TOP",
        "amount_sent": 1.0,
        "amount_sent_includes_fee": None,
        "provider_id": PROVIDER_ID,
        "provider_name_raw": PROVIDER_NAME_RAW,
        "provider_name_canonical": PROVIDER_NAME_RAW,
        "provider_type": "other",
        "option_id": None,
        "option_name_raw": None,
        "funding_method": None,
        "delivery_method": None,
        "amount_received": top_per_origin,
        "fee": None,
        "fee_currency": None,
        "fee_is_promotional": None,
        "rate_is_promotional": False,
        "promotion_detail": None,
        "provider_fx_rate": top_per_origin,
        "benchmark_fx_rate": None,
        "benchmark_source": None,
        "benchmark_observation_id": None,
        "speed_text": None,
        "speed_hours_min": None,
        "speed_hours_max": None,
        "availability_status": "observed",
        "status_detail": (
            f"Backfilled {date.isoformat()} from NRBT's historical rates file (Round 4 "
            f"backfill, reports/04-historical.md Task B). BUY {row['buy']} / MID {row['mid']} "
            f"/ SELL {row['sell']} {origin_currency} per 1 TOP; provider_fx_rate and "
            f"amount_received are the MID rate inverted to TOP per 1 {origin_currency} "
            f"({top_per_origin:.6f}), per METHODOLOGY.md section 2.4. collected_at reflects "
            f"when this project actually fetched the underlying file (2026-09-09, once); "
            f"provider_quote_timestamp carries the historical date this specific rate applied "
            f"to -- these are deliberately not collapsed into each other."
        ),
        "raw_payload_sha256": sha256,
        "raw_payload_path": str(archive_path.relative_to(ARCHIVE_ROOT.parent)),
        "notes": None,
    }


def run(*, dry_run: bool = False) -> None:
    if not SOURCE_FILE.exists():
        print(f"backfill_nrbt_historical: source file not found: {SOURCE_FILE}", file=sys.stderr)
        sys.exit(1)

    raw_bytes = SOURCE_FILE.read_bytes()
    sha256, archive_path = archive_bytes(
        PROVIDER_ID, SOURCE_URL, 200, {}, raw_bytes, fetched_at=FETCHED_AT
    )
    print(f"backfill_nrbt_historical: archived source file as {sha256} -> {archive_path}")

    xl = pd.ExcelFile(SOURCE_FILE)
    all_valid: list[dict] = []
    all_excluded: list[dict] = []
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name, header=None)
        valid, excluded = parse_sheet(df, sheet_name)
        all_valid.extend(valid)
        all_excluded.extend(excluded)

    print(f"backfill_nrbt_historical: {len(all_valid)} in-range dates, {len(all_excluded)} excluded")
    for rec in all_excluded:
        print(f"  excluded (out of range for sheet {rec['sheet']!r}): {rec['date'].isoformat()}")

    collection_run_id = f"backfill-nrbt-historical-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"

    by_month: dict[str, list[dict]] = {}
    skipped_missing_currency = 0
    for rec in all_valid:
        for origin_currency in ORIGIN_CURRENCIES:
            if origin_currency not in rec["rates"]:
                skipped_missing_currency += 1
                continue
            obs = build_observation(
                date=rec["date"],
                origin_currency=origin_currency,
                rates=rec["rates"],
                sha256=sha256,
                archive_path=archive_path,
                collection_run_id=collection_run_id,
            )
            month = rec["date"].strftime("%Y-%m")
            by_month.setdefault(month, []).append(obs)

    total = sum(len(v) for v in by_month.values())
    print(
        f"backfill_nrbt_historical: {total} observations across {len(by_month)} month-files "
        f"({skipped_missing_currency} currency-rows skipped: unparseable rate cell)"
    )

    if dry_run:
        print("backfill_nrbt_historical: --dry-run, not writing")
        return

    for month in sorted(by_month):
        append_observations(by_month[month], month=month)

    print("backfill_nrbt_historical: done")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    run(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
