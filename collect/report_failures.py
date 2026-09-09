"""python -m collect.report_failures

Minimal Round 2 stub: scans the most recent collection run for any observation whose
availability_status isn't "observed" and prints it. Does not open or update a GitHub issue --
that is CLAUDE.md section 4.1's repair loop, deliberately not built this round (out of scope
for "two connectors and nothing else," and better designed against a real failure than an
imagined one).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
STORE_DIR = REPO_ROOT / "store" / "observations"


def main(argv=None) -> int:
    csv_files = sorted(STORE_DIR.glob("*.csv"))
    if not csv_files:
        print("collect.report_failures: no store files found -- nothing to report")
        return 0

    latest = csv_files[-1]
    df = pd.read_csv(latest, dtype=str, keep_default_na=False, na_values=[""])
    if df.empty or "collection_run_id" not in df.columns:
        print("collect.report_failures: no rows to check")
        return 0

    last_run_id = df["collection_run_id"].iloc[-1]
    last_run = df[df["collection_run_id"] == last_run_id]
    failures = last_run[last_run["availability_status"] != "observed"]

    if failures.empty:
        print(f"collect.report_failures: run {last_run_id} -- no failures")
        return 0

    print(f"collect.report_failures: run {last_run_id} -- {len(failures)} failure(s):")
    for _, row in failures.iterrows():
        print(f"  - {row['connector_id']}: {row['availability_status']}: {row['status_detail']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
