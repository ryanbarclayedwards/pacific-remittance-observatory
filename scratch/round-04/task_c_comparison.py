"""Task C: compute cost_pct for the 2023 audit against the backfilled NRBT benchmark, and
compare to the audit's own reported Cost_PP. Report-support script, not part of the collect/
package -- this computes a derived field (cost_pct) for analysis only, per schema.json's own
policy that derived fields are never stored in the observation store itself.
"""
import re
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STORE_DIR = REPO_ROOT / "store" / "observations"

def load_month(month):
    df = pd.read_csv(STORE_DIR / f"{month}.csv", dtype=str, keep_default_na=False, na_values=[""])
    return df

months = ["2023-03", "2023-04", "2023-07", "2023-08"]
frames = [load_month(m) for m in months]
df = pd.concat(frames, ignore_index=True)

audit = df[df["source_system"] == "devpolicy_manual_audit"].copy()
nrbt = df[(df["provider_id"] == "nrbt") & (df["connector_id"] == "benchmarks.nrbt.historical_backfill")].copy()

audit["date"] = pd.to_datetime(audit["collected_at"]).dt.date
nrbt["date"] = pd.to_datetime(nrbt["provider_quote_timestamp"]).dt.date

nrbt_lookup = {(row["date"], row["origin_currency"]): float(row["provider_fx_rate"]) for _, row in nrbt.iterrows()}

audit["amount_sent"] = audit["amount_sent"].astype(float)
audit["amount_received"] = audit["amount_received"].astype(float)

def compute_row(row):
    key = (row["date"], row["origin_currency"])
    benchmark_rate = nrbt_lookup.get(key)
    if benchmark_rate is None:
        return pd.Series({"benchmark_rate": None, "cost_pct_nrbt": None})
    benchmark_receive = row["amount_sent"] * benchmark_rate
    implicit_cost = benchmark_receive - row["amount_received"]
    cost_pct = implicit_cost / benchmark_receive * 100
    return pd.Series({"benchmark_rate": benchmark_rate, "cost_pct_nrbt": cost_pct})

audit = pd.concat([audit, audit.apply(compute_row, axis=1)], axis=1)

# Extract the paper's own Cost_PP from notes text
def extract_cost_pp(notes):
    m = re.search(r"Cost_PP: ([\-0-9.]+)", notes)
    return float(m.group(1)) if m else None

audit["cost_pp_paper"] = audit["notes"].apply(extract_cost_pp)

matched = audit.dropna(subset=["cost_pct_nrbt", "cost_pp_paper"]).copy()
print(f"total audit rows: {len(audit)}")
print(f"matched to an NRBT benchmark: {len(matched)}")
print(f"unmatched (no NRBT rate for that date/currency): {len(audit) - len(matched)}")
print()

# Correlation and direction
corr = matched["cost_pct_nrbt"].corr(matched["cost_pp_paper"])
print(f"Pearson correlation (my cost_pct_nrbt vs paper's cost_pp): {corr:.4f}")

both_positive = ((matched["cost_pct_nrbt"] > 0) & (matched["cost_pp_paper"] > 0)).mean()
print(f"share of rows where both are positive (same direction): {both_positive:.4f}")

diff = matched["cost_pct_nrbt"] - matched["cost_pp_paper"]
print(f"mean(cost_pct_nrbt - cost_pp_paper): {diff.mean():.4f}")
print(f"median: {diff.median():.4f}, std: {diff.std():.4f}")
print(f"min: {diff.min():.4f}, max: {diff.max():.4f}")
print()

# Ranking agreement per date+corridor+website: does the same provider come out cheapest?
matched["corridor_key"] = matched["origin_currency"] + "_" + matched["source_url"]
groups = matched.groupby(["date", "corridor_key"])
rank_agree = 0
rank_total = 0
for key, g in groups:
    if len(g) < 2:
        continue
    rank_total += 1
    cheapest_nrbt = g.loc[g["cost_pct_nrbt"].idxmin(), "provider_id"]
    cheapest_paper = g.loc[g["cost_pp_paper"].idxmin(), "provider_id"]
    if cheapest_nrbt == cheapest_paper:
        rank_agree += 1
print(f"date x corridor groups with >=2 providers: {rank_total}")
print(f"same cheapest-provider identified by both benchmarks: {rank_agree} ({rank_agree/rank_total*100:.1f}%)")
print()

# Spearman rank correlation within each date x corridor group, then average
spearmans = []
for key, g in groups:
    if len(g) < 3:
        continue
    rho = g["cost_pct_nrbt"].corr(g["cost_pp_paper"], method="spearman")
    if pd.notna(rho):
        spearmans.append(rho)
print(f"groups with >=3 providers used for within-day rank correlation: {len(spearmans)}")
print(f"mean within-day Spearman rank correlation: {sum(spearmans)/len(spearmans):.4f}")

audit.to_csv(Path(__file__).parent / "task_c_full_comparison.csv", index=False)
print()
print("Full row-level comparison saved to scratch/round-04/task_c_full_comparison.csv")
