"""python -m normalise.validate --strict

CI gate (CLAUDE.md section 5): validates every row in store/observations/*.csv against
schema/observation.schema.json, confirms every raw_payload_sha256 resolves to a real file
under archive/, and checks the arithmetic sanity gates (amount_received > 0, fee >= 0,
amount_sent > 0) for rows with availability_status = "observed". Read-only; never writes.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "observation.schema.json"
STORE_DIR = REPO_ROOT / "store" / "observations"
ARCHIVE_ROOT = REPO_ROOT / "archive"

BOOLEAN_FIELDS = {
    "amount_sent_includes_fee", "fee_is_promotional", "rate_is_promotional",
    "benchmark_is_carried_forward",
}
NUMBER_FIELDS = {
    "amount_sent", "amount_received", "fee", "provider_fx_rate", "benchmark_fx_rate",
    "speed_hours_min", "speed_hours_max",
}
# JSON Schema's "integer" type rejects a Python float (even 5.0) -- these need int(), not
# float(), or every row with a real value here would fail validation.
INTEGER_FIELDS = {"benchmark_age_days"}


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text())


def row_to_observation(row: dict, schema_props: dict) -> dict:
    """CSV cells are all strings; coerce back to the JSON types the schema expects. A cell
    that pandas parsed as NaN (i.e. the CSV cell was empty) becomes None, never a default."""
    obs: dict = {}
    for key, value in row.items():
        if key not in schema_props:
            continue
        if value is None or (isinstance(value, float) and pd.isna(value)):
            obs[key] = None
            continue
        if key in BOOLEAN_FIELDS:
            obs[key] = str(value).strip().lower() in ("true", "1")
            continue
        if key in INTEGER_FIELDS:
            obs[key] = int(float(value))
            continue
        if key in NUMBER_FIELDS:
            obs[key] = float(value)
            continue
        obs[key] = value
    return obs


def check_archive_resolves(obs: dict) -> str | None:
    sha = obs.get("raw_payload_sha256")
    if not sha:
        return "missing raw_payload_sha256"

    path = obs.get("raw_payload_path")
    if path:
        full = REPO_ROOT / path
        if not full.is_file():
            return f"raw_payload_path {path!r} does not exist"
        if full.name != f"{sha}.json.gz":
            return f"raw_payload_path {path!r} does not match raw_payload_sha256 {sha!r}"
        return None

    if not list(ARCHIVE_ROOT.rglob(f"{sha}.json.gz")):
        return f"raw_payload_sha256 {sha!r} does not resolve to any file under archive/"
    return None


def check_arithmetic(obs: dict) -> list[str]:
    errors = []
    if obs.get("availability_status") != "observed":
        return errors
    if obs.get("amount_sent") is not None and obs["amount_sent"] <= 0:
        errors.append(f"amount_sent must be > 0, got {obs['amount_sent']}")
    if obs.get("amount_received") is not None and obs["amount_received"] <= 0:
        errors.append(f"amount_received must be > 0, got {obs['amount_received']}")
    if obs.get("fee") is not None and obs["fee"] < 0:
        errors.append(f"fee must be >= 0, got {obs['fee']}")
    return errors


def validate_all() -> tuple[int, list[str]]:
    schema = load_schema()
    props = schema["properties"]

    csv_files = sorted(STORE_DIR.glob("*.csv")) if STORE_DIR.is_dir() else []
    if not csv_files:
        return 0, []

    total_rows = 0
    all_errors: list[str] = []

    for csv_path in csv_files:
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False, na_values=[""])
        for i, row in df.iterrows():
            row_label = f"{csv_path.name}:{i + 2}"  # +2: header row, 1-indexed
            total_rows += 1
            obs = row_to_observation(row.to_dict(), props)

            try:
                jsonschema.validate(obs, schema)
            except jsonschema.ValidationError as exc:
                all_errors.append(f"{row_label}: schema violation: {exc.message}")
                continue

            archive_error = check_archive_resolves(obs)
            if archive_error:
                all_errors.append(f"{row_label}: {archive_error}")

            for arithmetic_error in check_arithmetic(obs):
                all_errors.append(f"{row_label}: {arithmetic_error}")

    return total_rows, all_errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="exit non-zero on any error (the CI mode)")
    parser.parse_args(argv)

    total_rows, errors = validate_all()
    print(f"normalise.validate: checked {total_rows} row(s) across store/observations/")

    if errors:
        print(f"{len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("all rows valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
