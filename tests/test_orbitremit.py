"""Golden test for the OrbitRemit connector.

Runs parse_comparison_table() / build_observation() against a committed fixture only -- no
network call. The fixture is the actual page fetched during Round 2's raw-fetch sweep and
re-used for Round 3's endpoint-discovery pass, not a fresh fetch for this test specifically.
"""
from datetime import datetime, timezone
from pathlib import Path

import pytest

from collect.archive import ARCHIVE_ROOT
from collect.orbitremit.connector import (
    ParseError,
    build_observation,
    parse_comparison_table,
    parse_meta_description_rate,
)

FIXTURE = Path(__file__).parent / "fixtures" / "orbitremit" / "aud-to-top-2026-09-09.html"


def _fixture_text() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_comparison_table_finds_the_500_row():
    table = parse_comparison_table(_fixture_text())
    assert table[500.0] == 866.82


def test_parse_comparison_table_shows_the_promo_tier_pattern():
    table = parse_comparison_table(_fixture_text())
    # Amounts up to 500 AUD sit at the same ~1.7336 promotional rate; larger amounts decline.
    assert table[100.0] / 100.0 == pytest.approx(1.7336, abs=1e-4)
    assert table[1000.0] / 1000.0 < table[500.0] / 500.0


def test_parse_meta_description_rate():
    rate = parse_meta_description_rate(_fixture_text())
    assert rate == 1.69237


def test_parse_comparison_table_raises_if_no_streaming_payload():
    with pytest.raises(ParseError):
        parse_comparison_table("<html><body>no next_f push here</body></html>")


def test_build_observation_uses_the_500_aud_row():
    table = parse_comparison_table(_fixture_text())
    meta_rate = parse_meta_description_rate(_fixture_text())
    collected_at = datetime(2026, 9, 9, 12, 0, 0, tzinfo=timezone.utc)

    obs = build_observation(
        table=table,
        meta_rate=meta_rate,
        sha256="c" * 64,
        archive_path=ARCHIVE_ROOT / "orbitremit" / "2026" / "09" / "09" / ("c" * 64 + ".json.gz"),
        collected_at=collected_at,
        collection_run_id="run-test",
    )

    assert obs["amount_sent"] == 500.0
    assert obs["amount_received"] == 866.82
    assert obs["provider_fx_rate"] == pytest.approx(1.73364, abs=1e-5)
    assert obs["origin_currency"] == "AUD"
    assert obs["destination_currency"] == "TOP"
    assert obs["provider_id"] == "orbitremit"
    assert obs["collection_method"] == "public_quote"
    assert obs["availability_status"] == "observed"
    assert obs["fee"] is None
    assert obs["raw_payload_sha256"] == "c" * 64
    assert "1.69237" in obs["status_detail"]


def test_build_observation_raises_if_target_amount_missing():
    with pytest.raises(ParseError):
        build_observation(
            table={100.0: 173.36},
            meta_rate=None,
            sha256="d" * 64,
            archive_path=ARCHIVE_ROOT / "orbitremit" / "2026" / "09" / "09" / ("d" * 64 + ".json.gz"),
            collected_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
            collection_run_id="run-test",
        )
