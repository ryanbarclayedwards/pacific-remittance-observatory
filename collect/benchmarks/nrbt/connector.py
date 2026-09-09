"""National Reserve Bank of Tonga -- daily benchmark rate connector.

Tier 1 (published_tariff): a public daily rate table, no account, no calculator involved.
Contract: fetch -> hash -> archive -> parse -> normalise -> validate -> append, per
CLAUDE.md section 2.2. This module only fetches and archives live; parse() and
build_observation() are pure functions of already-archived bytes, so the golden test in
tests/test_nrbt.py runs them offline against a committed fixture, never the network.

Quote orientation (METHODOLOGY.md section 2.4, "must be standardised and documented"): NRBT
publishes BUY/MID/SELL as *foreign currency per 1 TOP* (e.g. NZD 0.7210 means 1 TOP = 0.7210
NZD). This project's benchmark_fx_rate / provider_fx_rate convention is *destination currency
per 1 origin currency unit* -- for NZ -> Tonga that is TOP per NZD -- so the published MID rate
is inverted before being stored. Both the raw published figure and the inverted figure are
recorded in status_detail so the inversion is checkable, not just asserted.
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from selectolax.parser import HTMLParser

from collect.archive import ARCHIVE_ROOT, archive_bytes, fetch, read_archived_body

PROVIDER_ID = "nrbt"
PROVIDER_NAME_RAW = "National Reserve Bank of Tonga"
SOURCE_URL = "https://www.reservebank.to/index.php/financial-system/financial-markets/exchange-rates"
CONNECTOR_ID = "benchmarks.nrbt"
CONNECTOR_VERSION = "0.1.0"
METHODOLOGY_VERSION = "0.2"

# Only the currency names this project currently needs to recognise. An unrecognised row is
# skipped, not guessed at -- extend this map deliberately when a new currency is needed.
CURRENCY_NAME_TO_ISO = {
    "new zealand dollar": "NZD",
    "australian dollar": "AUD",
    "fijian dollar": "FJD",
    "samoan tala": "WST",
    "united states dollar": "USD",
}

LAST_UPDATED_RE = re.compile(r"Last Updated:\s*([0-9]{1,2} \w+ \d{4})")


class ParseError(Exception):
    pass


def parse_rates(html_text: str) -> dict[str, dict[str, float]]:
    """Extract {iso_code: {"buy":.., "mid":.., "sell":..}} from the exchange-rates table.

    Targets table.table-custom-4c specifically (the table's own CSS class on this page) rather
    than "the first table on the page" or a stripped-text regex, so a layout change elsewhere
    on the page can't silently feed the parser the wrong table.
    """
    tree = HTMLParser(html_text)
    table = tree.css_first("table.table-custom-4c")
    if table is None:
        raise ParseError("no table.table-custom-4c found on the page")

    rows = table.css("tbody tr")
    if not rows:
        raise ParseError("table.table-custom-4c has no tbody rows")

    results: dict[str, dict[str, float]] = {}
    for row in rows:
        cells = [c.text(strip=True) for c in row.css("td")]
        if len(cells) != 4:
            continue
        name, buy_s, mid_s, sell_s = cells
        iso = CURRENCY_NAME_TO_ISO.get(name.strip().lower())
        if iso is None:
            continue
        try:
            results[iso] = {"buy": float(buy_s), "mid": float(mid_s), "sell": float(sell_s)}
        except ValueError:
            raise ParseError(f"row for {name!r} has non-numeric rate: {cells!r}")

    return results


def parse_last_updated(html_text: str) -> str | None:
    m = LAST_UPDATED_RE.search(html_text)
    return m.group(1) if m else None


def build_observation(
    *,
    rates: dict[str, dict[str, float]],
    last_updated_text: str | None,
    sha256: str,
    archive_path: Path,
    collected_at: datetime,
    collection_run_id: str,
) -> dict:
    """Pure function: archived-parse-result -> one schema-shaped observation dict for NZD/TOP.

    Raises ParseError if NZD is missing -- the caller turns that into an error observation
    rather than emitting a row with a guessed rate.
    """
    nzd = rates.get("NZD")
    if nzd is None:
        raise ParseError("NZD row not found in parsed rate table")

    published_mid_nzd_per_top = nzd["mid"]
    top_per_nzd = 1 / published_mid_nzd_per_top

    return {
        "observation_id": str(uuid.uuid4()),
        "collection_run_id": collection_run_id,
        "supersedes": None,
        "correction_reason": None,
        "collected_at": collected_at.isoformat(),
        "provider_quote_timestamp": None,
        "source_last_updated": last_updated_text,
        "quote_validity_text": None,
        "collection_method": "published_tariff",
        "source_system": "collector",
        "source_url": SOURCE_URL,
        "connector_id": CONNECTOR_ID,
        "connector_version": CONNECTOR_VERSION,
        "methodology_version": METHODOLOGY_VERSION,
        "origin_country_iso3": "NZL",
        "origin_currency": "NZD",
        "destination_country_iso3": "TON",
        "destination_currency": "TOP",
        "amount_sent": 1.0,
        "amount_sent_includes_fee": None,
        "provider_id": PROVIDER_ID,
        "provider_name_raw": PROVIDER_NAME_RAW,
        "provider_name_canonical": PROVIDER_NAME_RAW,
        "provider_type": "other",
        "option_id": None,
        "option_name_raw": None,
        "funding_method": None,
        "delivery_method": None,
        "amount_received": top_per_nzd,
        "fee": None,
        "fee_currency": None,
        "fee_is_promotional": None,
        "provider_fx_rate": top_per_nzd,
        "benchmark_fx_rate": None,
        "benchmark_source": None,
        "benchmark_observation_id": None,
        "speed_text": None,
        "speed_hours_min": None,
        "speed_hours_max": None,
        "availability_status": "observed",
        "status_detail": (
            f"NRBT published BUY {nzd['buy']} / MID {nzd['mid']} / SELL {nzd['sell']} NZD per "
            f"1 TOP. This row's provider_fx_rate and amount_received are the MID rate inverted "
            f"to TOP per 1 NZD ({top_per_nzd:.6f}), per METHODOLOGY.md section 2.4's quote-"
            f"orientation convention. This is a benchmark rate observation, not a transfer "
            f"quote -- fee and amount_sent_includes_fee are not applicable and are null, not "
            f"zero."
        ),
        "raw_payload_sha256": sha256,
        "raw_payload_path": str(archive_path.relative_to(ARCHIVE_ROOT.parent)),
        "notes": None,
    }


def error_observation(
    *,
    reason: str,
    sha256: str | None,
    archive_path: Path | None,
    collected_at: datetime,
    collection_run_id: str,
    availability_status: str = "error",
) -> dict:
    return {
        "observation_id": str(uuid.uuid4()),
        "collection_run_id": collection_run_id,
        "supersedes": None,
        "correction_reason": None,
        "collected_at": collected_at.isoformat(),
        "provider_quote_timestamp": None,
        "source_last_updated": None,
        "quote_validity_text": None,
        "collection_method": "published_tariff",
        "source_system": "collector",
        "source_url": SOURCE_URL,
        "connector_id": CONNECTOR_ID,
        "connector_version": CONNECTOR_VERSION,
        "methodology_version": METHODOLOGY_VERSION,
        "origin_country_iso3": "NZL",
        "origin_currency": "NZD",
        "destination_country_iso3": "TON",
        "destination_currency": "TOP",
        "amount_sent": 1.0,
        "amount_sent_includes_fee": None,
        "provider_id": PROVIDER_ID,
        "provider_name_raw": PROVIDER_NAME_RAW,
        "provider_name_canonical": PROVIDER_NAME_RAW,
        "provider_type": "other",
        "option_id": None,
        "option_name_raw": None,
        "funding_method": None,
        "delivery_method": None,
        "amount_received": None,
        "fee": None,
        "fee_currency": None,
        "fee_is_promotional": None,
        "provider_fx_rate": None,
        "benchmark_fx_rate": None,
        "benchmark_source": None,
        "benchmark_observation_id": None,
        "speed_text": None,
        "speed_hours_min": None,
        "speed_hours_max": None,
        "availability_status": availability_status,
        "status_detail": reason,
        "raw_payload_sha256": sha256 or "0" * 64,
        "raw_payload_path": str(archive_path.relative_to(ARCHIVE_ROOT.parent)) if archive_path else None,
        "notes": None,
    }


def run(collection_run_id: str) -> list[dict]:
    """Live entry point: fetch -> archive -> parse -> normalise. One network call."""
    collected_at = datetime.now(timezone.utc)
    resp = fetch(SOURCE_URL)
    sha256, archive_path = archive_bytes(
        PROVIDER_ID, SOURCE_URL, resp.status_code, dict(resp.headers), resp.content, fetched_at=collected_at
    )

    if resp.status_code != 200:
        return [
            error_observation(
                reason=f"HTTP {resp.status_code} fetching {SOURCE_URL}",
                sha256=sha256,
                archive_path=archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
                availability_status="error",
            )
        ]

    body = read_archived_body(archive_path)
    try:
        rates = parse_rates(body)
        last_updated = parse_last_updated(body)
        return [
            build_observation(
                rates=rates,
                last_updated_text=last_updated,
                sha256=sha256,
                archive_path=archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
            )
        ]
    except ParseError as exc:
        return [
            error_observation(
                reason=f"parse error: {exc}",
                sha256=sha256,
                archive_path=archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
                availability_status="error",
            )
        ]
