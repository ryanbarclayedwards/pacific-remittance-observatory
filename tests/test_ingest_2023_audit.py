"""Golden tests for the 2023 manual audit ingestion (Round 4, reports/04-historical.md,
Task A). Uses small synthetic rows shaped like the real CSVs, not the full files -- fast,
offline, and exercises the specific decisions this import makes deliberately.
"""
from pathlib import Path

import pytest

from collect.archive import ARCHIVE_ROOT
from collect.ingest_2023_audit import (
    WAVES,
    BlankRow,
    build_observation,
    resolve_provider,
)


def test_resolve_provider_base_case():
    assert resolve_provider("Moneygram", "AUSTON") == ("moneygram", "MoneyGram", "global_mto")


def test_resolve_provider_strips_parenthetical_suffix():
    provider_id, name, ptype = resolve_provider("Moneygram (Online)", "AUSTON")
    assert provider_id == "moneygram"


def test_resolve_provider_is_corridor_conditional_for_anz():
    au = resolve_provider("ANZ", "AUSTON")
    nz = resolve_provider("ANZ", "NZTON")
    assert au[0] == "anz-australia"
    assert nz[0] == "anz-new-zealand"
    assert au[0] != nz[0]


def test_resolve_provider_raises_blankrow_on_empty_string():
    with pytest.raises(BlankRow):
        resolve_provider("", "AUSTON")


def test_resolve_provider_raises_keyerror_on_unknown_name():
    with pytest.raises(KeyError):
        resolve_provider("Some New Provider Nobody Mapped", "AUSTON")


def _archive_path():
    return ARCHIVE_ROOT / "manual-audit-2023" / "2026" / "09" / "10" / ("a" * 64 + ".json.gz")


def test_build_observation_audit2_basic_fields():
    # A real row from audit2.csv (25/07/2023, Saver Pacific, NZTON, Ave Paanga Pau) -- matches
    # CLAIMS.md C2 exactly: NZ$200 -> TOP 284.10, fee 0, rate 1.42.
    row = {
        "date": "25/07/2023",
        "website": "2",
        "corridor": "NZTON",
        "mtos": "Ave Paanga Pau",
        "modeoftransaction": "Prepaid - Account",
        "speed": "Less than one hour",
        "amountreceived": "284.1",
        "FXrate": "1.42",
        "Fee ": "0",
        "Cost_PP": "2.7",
        "200AUD_NZD": "291.98",
    }
    obs = build_observation(
        row=row,
        wave_key="audit2",
        wave_cfg=WAVES["audit2"],
        collection_run_id="test-run",
        sha256="a" * 64,
        archive_path=_archive_path(),
    )
    assert obs is not None
    assert obs["amount_sent"] == 200.0
    assert obs["amount_received"] == 284.1
    assert obs["fee"] == 0.0
    assert obs["provider_fx_rate"] == 1.42
    assert obs["origin_currency"] == "NZD"
    assert obs["destination_currency"] == "TOP"
    assert obs["provider_id"] == "ave-paanga-pau"
    assert obs["collection_method"] == "manual_audit"
    assert obs["source_system"] == "devpolicy_manual_audit"
    assert obs["amount_sent_includes_fee"] is None  # deliberately, see module docstring
    assert obs["collected_at"].startswith("2023-07-25")
    assert "2.7" in obs["notes"]  # original Cost_PP preserved for traceability


def test_build_observation_returns_none_for_vanuatu_corridor():
    row = {
        "date": "25/07/2023",
        "website": "1",
        "corridor": "AUSVAN",
        "mtos": "ANZ",
        "modeoftransaction": "Online - Account",
        "speed": "Next day",
        "amountreceived": "100",
        "FXrate": "50",
        "Fee ": "0",
        "Cost_PP": "1",
        "200AUD_NZD": "100",
    }
    obs = build_observation(
        row=row,
        wave_key="audit2",
        wave_cfg=WAVES["audit2"],
        collection_run_id="test-run",
        sha256="a" * 64,
        archive_path=_archive_path(),
    )
    assert obs is None


def test_build_observation_funding_delivery_split():
    row = {
        "date": "25/07/2023",
        "website": "1",
        "corridor": "AUSTON",
        "mtos": "Western Union (Cash)",
        "modeoftransaction": "Cash - Cash",
        "speed": "Instant",
        "amountreceived": "293.71",
        "FXrate": "1.51",
        "Fee ": "5",
        "Cost_PP": "7.17",
        "200AUD_NZD": "318.62",
    }
    obs = build_observation(
        row=row,
        wave_key="audit2",
        wave_cfg=WAVES["audit2"],
        collection_run_id="test-run",
        sha256="a" * 64,
        archive_path=_archive_path(),
    )
    assert obs["funding_method"] == "Cash"
    assert obs["delivery_method"] == "Cash"
    assert obs["provider_id"] == "western-union"
    assert obs["option_name_raw"] == "Western Union (Cash)"
    assert obs["fee_currency"] == "AUD"
