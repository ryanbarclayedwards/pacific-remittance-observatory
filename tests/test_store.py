"""Golden tests for collect/store.py's append-only writer and its schema-growth migration
(Round 4, reports/04-historical.md) -- run against a temp directory, never the real store/.
"""
import csv

import pytest

from collect.store import _migrate_header_if_needed, append_observations


def test_new_file_gets_header_and_rows(tmp_path, monkeypatch):
    import collect.store as store_mod

    monkeypatch.setattr(store_mod, "STORE_DIR", tmp_path)
    append_observations([{"observation_id": "a", "provider_id": "x"}], month="2099-01")

    path = tmp_path / "2099-01.csv"
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows[0][0] == "observation_id"
    idx = rows[0].index("observation_id")
    assert rows[1][idx] == "a"


def test_migration_widens_header_and_backfills_null_without_touching_old_values(tmp_path):
    path = tmp_path / "narrow.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["a", "b"])
        w.writerow(["1", "2"])
        w.writerow(["3", "4"])

    _migrate_header_if_needed(path, ["a", "b", "c", "d"])

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["a", "b", "c", "d"]
    assert rows[1] == ["1", "2", "", ""]
    assert rows[2] == ["3", "4", "", ""]


def test_migration_is_a_noop_when_header_already_current(tmp_path):
    path = tmp_path / "current.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["a", "b"])
        w.writerow(["1", "2"])

    _migrate_header_if_needed(path, ["a", "b"])

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows == [["a", "b"], ["1", "2"]]


def test_migration_refuses_a_non_prefix_mismatch(tmp_path):
    path = tmp_path / "reordered.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["b", "a"])  # reordered, not a clean prefix extension
        w.writerow(["1", "2"])

    with pytest.raises(RuntimeError):
        _migrate_header_if_needed(path, ["a", "b", "c"])


def test_append_observations_migrates_then_appends(tmp_path, monkeypatch):
    import collect.store as store_mod

    monkeypatch.setattr(store_mod, "STORE_DIR", tmp_path)
    monkeypatch.setattr(store_mod, "_schema_columns", lambda: ["observation_id", "amount_sent", "new_field"])

    path = tmp_path / "2099-02.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["observation_id", "amount_sent"])
        w.writerow(["old-1", "100"])

    append_observations([{"observation_id": "new-1", "amount_sent": 200, "new_field": True}], month="2099-02")

    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    assert rows[0] == ["observation_id", "amount_sent", "new_field"]
    assert rows[1] == ["old-1", "100", ""]  # old row: untouched value, backfilled null
    assert rows[2] == ["new-1", "200", "true"]
