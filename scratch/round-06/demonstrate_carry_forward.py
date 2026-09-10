"""Demonstrates the carry-forward resolver against the real store: re-runs Round 4's Task C
join using resolve_benchmark_rate() instead of an exact-date-only match, and reports how many
of the previously-unmatched 408 rows now resolve. Report-support script, not part of the
collect/ package -- no synthetic rows are written back to store/.
"""
import csv
from datetime import datetime
from pathlib import Path

import sys
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from collect.benchmark_lookup import load_published_rates_from_store, resolve_benchmark_rate

STORE_DIR = REPO_ROOT / "store" / "observations"

published_rates = load_published_rates_from_store()
print(f"loaded {len(published_rates)} genuinely-published NRBT (date, currency) rates")

audit_rows = []
for month in ["2023-03", "2023-04", "2023-07", "2023-08"]:
    with (STORE_DIR / f"{month}.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("source_system") == "devpolicy_manual_audit":
                audit_rows.append(row)

print(f"{len(audit_rows)} audit rows total")

resolved_direct = 0
resolved_carried = 0
unresolved = 0
max_age_seen = 0

for row in audit_rows:
    d = datetime.fromisoformat(row["collected_at"]).date()
    currency = row["origin_currency"]
    result = resolve_benchmark_rate(d, currency, published_rates)
    if result is None:
        unresolved += 1
        continue
    if result.is_carried_forward:
        resolved_carried += 1
        max_age_seen = max(max_age_seen, result.age_days)
    else:
        resolved_direct += 1

print(f"resolved directly (same-day publication): {resolved_direct}")
print(f"resolved via carry-forward: {resolved_carried} (max age seen: {max_age_seen} day(s))")
print(f"unresolved (beyond the {10}-day lookback): {unresolved}")
print(f"total resolved: {resolved_direct + resolved_carried} / {len(audit_rows)}")
