"""Golden test for the NRBT benchmark connector.

Runs parse_rates() / parse_last_updated() / build_observation() against a committed fixture
only -- no network call. If this test fails, the fixture and the parser have diverged; the
repair loop (CLAUDE.md section 4.1) starts here, not by re-fetching the live page.
"""
from datetime import datetime, timezone
from pathlib import Path

import pytest

from collect.archive import ARCHIVE_ROOT
from collect.benchmarks.nrbt.connector import (
    ParseError,
    build_observation,
    parse_last_updated,
    parse_rates,
)

FIXTURE = Path(__file__).parent / "fixtures" / "nrbt" / "exchange-rates-2026-09-09.html"


def _fixture_text() -> str:
    return FIXTURE.read_text(encoding="utf-8")


def test_parse_rates_extracts_all_five_known_currencies():
    rates = parse_rates(_fixture_text())
    assert set(rates) == {"AUD", "FJD", "NZD", "USD", "WST"}


def test_parse_rates_nzd_matches_fixture_exactly():
    rates = parse_rates(_fixture_text())
    assert rates["NZD"] == {"buy": 0.7367, "mid": 0.7210, "sell": 0.7052}


def test_parse_last_updated():
    assert parse_last_updated(_fixture_text()) == "09 September 2026"


def test_parse_rates_raises_on_missing_table():
    with pytest.raises(ParseError):
        parse_rates("<html><body>no table here</body></html>")


def test_build_observation_inverts_mid_rate_to_top_per_nzd():
    rates = parse_rates(_fixture_text())
    last_updated = parse_last_updated(_fixture_text())
    collected_at = datetime(2026, 9, 9, 11, 0, 0, tzinfo=timezone.utc)

    obs = build_observation(
        rates=rates,
        last_updated_text=last_updated,
        sha256="a" * 64,
        archive_path=ARCHIVE_ROOT / "nrbt" / "2026" / "09" / "09" / ("a" * 64 + ".json.gz"),
        collected_at=collected_at,
        collection_run_id="run-test",
    )

    # NRBT publishes NZD per 1 TOP (MID 0.7210). Our convention is TOP per 1 NZD.
    expected_top_per_nzd = 1 / 0.7210
    assert obs["provider_fx_rate"] == expected_top_per_nzd
    assert obs["amount_received"] == expected_top_per_nzd
    assert obs["amount_sent"] == 1.0
    assert obs["origin_currency"] == "NZD"
    assert obs["destination_currency"] == "TOP"
    assert obs["provider_id"] == "nrbt"
    assert obs["collection_method"] == "published_tariff"
    assert obs["availability_status"] == "observed"
    assert obs["raw_payload_sha256"] == "a" * 64
    assert obs["source_last_updated"] == "09 September 2026"
    # Benchmark rows don't benchmark themselves.
    assert obs["benchmark_fx_rate"] is None
    assert obs["fee"] is None


def test_build_observation_raises_if_nzd_missing():
    with pytest.raises(ParseError):
        build_observation(
            rates={"AUD": {"buy": 0.6, "mid": 0.59, "sell": 0.58}},
            last_updated_text="09 September 2026",
            sha256="b" * 64,
            archive_path=ARCHIVE_ROOT / "nrbt" / "2026" / "09" / "09" / ("b" * 64 + ".json.gz"),
            collected_at=datetime(2026, 9, 9, tzinfo=timezone.utc),
            collection_run_id="run-test",
        )


def test_build_observation_inverts_mid_rate_to_top_per_aud():
    # Round 3: the connector emits one observation per configured origin currency, not just
    # NZD -- this is the AUD leg the AU->Tonga (OrbitRemit) corridor needs to close cost_pct.
    rates = parse_rates(_fixture_text())
    last_updated = parse_last_updated(_fixture_text())
    collected_at = datetime(2026, 9, 9, 11, 0, 0, tzinfo=timezone.utc)

    obs = build_observation(
        rates=rates,
        last_updated_text=last_updated,
        sha256="e" * 64,
        archive_path=ARCHIVE_ROOT / "nrbt" / "2026" / "09" / "09" / ("e" * 64 + ".json.gz"),
        collected_at=collected_at,
        collection_run_id="run-test",
        origin_currency="AUD",
    )

    expected_top_per_aud = 1 / rates["AUD"]["mid"]
    assert obs["provider_fx_rate"] == expected_top_per_aud
    assert obs["origin_currency"] == "AUD"
    assert obs["origin_country_iso3"] == "AUS"
    assert obs["destination_currency"] == "TOP"
