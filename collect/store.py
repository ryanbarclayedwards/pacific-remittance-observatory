"""Append observations to store/observations/<YYYY-MM>.csv.

Append-only, per CLAUDE.md sections 1.3 and 2.1: this module only ever appends rows to the
current month's file, in the schema's own property order, and never rewrites or deletes an
existing row.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "observation.schema.json"
STORE_DIR = REPO_ROOT / "store" / "observations"


def _schema_columns() -> list[str]:
    schema = json.loads(SCHEMA_PATH.read_text())
    return list(schema["properties"].keys())


def _cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def append_observations(observations: list[dict], *, month: str) -> Path:
    """month: 'YYYY-MM'. Caller derives it from each observation's own collected_at -- this
    function never guesses a date on the caller's behalf."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    path = STORE_DIR / f"{month}.csv"
    columns = _schema_columns()
    is_new = not path.exists()

    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(columns)
        for obs in observations:
            writer.writerow([_cell(obs.get(c)) for c in columns])

    return path
