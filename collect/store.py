"""Append observations to store/observations/<YYYY-MM>.csv.

Append-only, per CLAUDE.md sections 1.3 and 2.1: this module only ever appends rows to the
current month's file, in the schema's own property order, and never rewrites or deletes an
existing row's *values*.

Schema-growth migration (added Round 4, reports/04-historical.md): a fixed-width CSV and a
versioned, growing schema are in real tension -- discovered in practice when
schema/observation.schema.json gained two columns mid-month and appending new rows to the
existing 2026-09.csv produced a ragged file pandas couldn't parse. When a month-file's header is
a strict prefix of the current schema's columns (the schema grew, nothing was removed or
reordered), this module widens that file's header and backfills every existing row's new
trailing cells as empty -- never touching any existing cell's *value*. This is a mechanical
schema-width migration, not a data correction: no observed fact changes, only the column count
catches up to a schema version bump that was itself made deliberately and disclosed (CLAUDE.md
section 1.6). Anything other than a clean prefix match (a column removed, renamed or reordered)
is refused -- that is a real data question for a human, not something this function guesses at.
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


def _read_existing_header(path: Path) -> list[str] | None:
    if not path.exists():
        return None
    with path.open("r", newline="", encoding="utf-8") as f:
        return next(csv.reader(f), None)


def _migrate_header_if_needed(path: Path, target_columns: list[str]) -> None:
    """If path's header is an older, narrower prefix of target_columns, widen it in place and
    backfill existing rows' new trailing cells as empty. No-op for a new file or one already
    current. Raises if the existing header isn't a clean prefix of target_columns -- that case
    needs a human decision, not an automatic migration."""
    existing_header = _read_existing_header(path)
    if existing_header is None or existing_header == target_columns:
        return

    if existing_header != target_columns[: len(existing_header)]:
        raise RuntimeError(
            f"{path} has a header that is not a prefix of the current schema columns -- "
            f"this needs a human decision, not an automatic migration. "
            f"existing={existing_header!r} target={target_columns!r}"
        )

    added_columns = target_columns[len(existing_header):]
    with path.open("r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    rows[0] = target_columns
    for row in rows[1:]:
        row.extend([""] * len(added_columns))

    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

    try:
        display_path = path.relative_to(REPO_ROOT)
    except ValueError:
        display_path = path
    print(
        f"collect.store: migrated {display_path} header to add {added_columns} "
        f"(schema grew; no existing row's value changed, only new trailing columns added "
        f"as null)"
    )


def append_observations(observations: list[dict], *, month: str) -> Path:
    """month: 'YYYY-MM'. Caller derives it from each observation's own collected_at -- this
    function never guesses a date on the caller's behalf."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    path = STORE_DIR / f"{month}.csv"
    columns = _schema_columns()

    _migrate_header_if_needed(path, columns)
    is_new = not path.exists()

    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(columns)
        for obs in observations:
            writer.writerow([_cell(obs.get(c)) for c in columns])

    return path
