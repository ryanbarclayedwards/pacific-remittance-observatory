"""Golden test for the OrbitRemit connector.

Runs parse_comparison_table() / build_observations() against a committed fixture only -- no
network call. Round 4: rebuilt to emit one observation per table row (all nine amounts), not a
single hand-picked row -- see the connector's own module docstring for why.
"""
from datetime import datetime, timezone
from pathlib import Path

import pytest

from collect.archive import ARCHIVE_ROOT
from collect.orbitremit.connector import (
    PROMO_CAP_AUD,
    SUPERSEDES_500_AUD_OBSERVATION_ID,
    ParseError,
    build_observations,
    parse_comparison_table,
    parse_meta_description_rate,
)

FIXTURE = Path(__file__).parent / "fixtures" / "orbitremit" / "aud-to-top-2026-09-09.html"


def _fixture_text() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_comparison_table_finds_all_nine_rows():
    table = parse_comparison_table(_fixture_text())
    assert set(table) == {5.0, 10.0, 25.0, 50.0, 100.0, 500.0, 1000.0, 5000.0, 10000.0}
    assert table[500.0] == 866.82
    assert table[100.0] == 173.36
    assert table[1000.0] == 1692.37
    assert table[10000.0] == 16552.18


def test_parse_comparison_table_shows_the_promo_tier_pattern():
    table = parse_comparison_table(_fixture_text())
    assert table[100.0] / 100.0 == pytest.approx(1.7336, abs=1e-4)
    assert table[1000.0] / 1000.0 < table[500.0] / 500.0


def test_meta_description_rate_matches_the_1000_aud_row_exactly():
    # Round 4 correction: this is not a third, unexplained rate -- it's the 1,000 AUD row's
    # own implied rate.
    table = parse_comparison_table(_fixture_text())
    meta_rate = parse_meta_description_rate(_fixture_text())
    assert meta_rate == pytest.approx(table[1000.0] / 1000.0, abs=1e-6)


def test_parse_comparison_table_raises_if_no_streaming_payload():
    with pytest.raises(ParseError):
        parse_comparison_table("<html><body>no next_f push here</body></html>")


def test_build_observations_emits_one_row_per_table_entry():
    table = parse_comparison_table(_fixture_text())
    collected_at = datetime(2026, 9, 9, 12, 0, 0, tzinfo=timezone.utc)

    obs_list = build_observations(
        table=table,
        sha256="c" * 64,
        archive_path=ARCHIVE_ROOT / "orbitremit" / "2026" / "09" / "09" / ("c" * 64 + ".json.gz"),
        collected_at=collected_at,
        collection_run_id="run-test",
    )

    assert len(obs_list) == len(table)
    amounts = {o["amount_sent"] for o in obs_list}
    assert amounts == set(table)


def test_build_observations_flags_sub_cap_rows_as_purely_promotional():
    table = parse_comparison_table(_fixture_text())
    obs_list = build_observations(
        table=table,
        sha256="c" * 64,
        archive_path=ARCHIVE_ROOT / "orbitremit" / "2026" / "09" / "09" / ("c" * 64 + ".json.gz"),
        collected_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
        collection_run_id="run-test",
    )
    row_100 = next(o for o in obs_list if o["amount_sent"] == 100.0)
    assert row_100["rate_is_promotional"] is True
    assert "entire" in row_100["promotion_detail"].lower()
    assert row_100["fee"] is None


def test_build_observations_flags_above_cap_rows_as_blended():
    table = parse_comparison_table(_fixture_text())
    obs_list = build_observations(
        table=table,
        sha256="c" * 64,
        archive_path=ARCHIVE_ROOT / "orbitremit" / "2026" / "09" / "09" / ("c" * 64 + ".json.gz"),
        collected_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
        collection_run_id="run-test",
    )
    row_1000 = next(o for o in obs_list if o["amount_sent"] == 1000.0)
    assert row_1000["rate_is_promotional"] is True
    assert "blend" in row_1000["promotion_detail"].lower()


def test_build_observations_supersedes_only_the_500_aud_row():
    table = parse_comparison_table(_fixture_text())
    obs_list = build_observations(
        table=table,
        sha256="c" * 64,
        archive_path=ARCHIVE_ROOT / "orbitremit" / "2026" / "09" / "09" / ("c" * 64 + ".json.gz"),
        collected_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
        collection_run_id="run-test",
    )
    row_500 = next(o for o in obs_list if o["amount_sent"] == PROMO_CAP_AUD)
    assert row_500["supersedes"] == SUPERSEDES_500_AUD_OBSERVATION_ID
    assert row_500["correction_reason"] is not None

    others = [o for o in obs_list if o["amount_sent"] != PROMO_CAP_AUD]
    assert all(o["supersedes"] is None for o in others)
    assert all(o["correction_reason"] is None for o in others)


def test_build_observations_raises_on_empty_table():
    with pytest.raises(ParseError):
        build_observations(
            table={},
            sha256="d" * 64,
            archive_path=ARCHIVE_ROOT / "orbitremit" / "2026" / "09" / "09" / ("d" * 64 + ".json.gz"),
            collected_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
            collection_run_id="run-test",
        )
