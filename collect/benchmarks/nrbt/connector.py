"""National Reserve Bank of Tonga -- daily benchmark rate connector.

Tier 1 (published_tariff): a public daily rate table, no account, no calculator involved.
Contract: fetch -> hash -> archive -> parse -> normalise -> validate -> append, per
CLAUDE.md section 2.2. This module only fetches and archives live; parse() and
build_observation() are pure functions of already-archived bytes, so the golden test in
tests/test_nrbt.py runs them offline against a committed fixture, never the network.

Quote orientation (METHODOLOGY.md section 2.4, "must be standardised and documented"): NRBT
publishes BUY/MID/SELL as *foreign currency per 1 TOP* (e.g. NZD 0.7210 means 1 TOP = 0.7210
NZD). This project's benchmark_fx_rate / provider_fx_rate convention is *destination currency
per 1 origin currency unit* -- so the published MID rate is inverted before being stored, for
whichever origin currency is requested. Both the raw published figure and the inverted figure
are recorded in status_detail so the inversion is checkable, not just asserted.

Round 3 (reports/03-endpoints.md): emits one observation per configured origin currency, not
just NZD. NRBT's page publishes AUD alongside NZD on the same fetch -- once SPRINT-01's corridor
policy stopped fixing the corridor to NZ->Tonga (any provider that survives sets the corridor),
there was no reason to keep discarding the AUD figure this connector was already parsing.
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from selectolax.parser import HTMLParser

from collect.archive import ARCHIVE_ROOT, fetch_and_archive

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

# Origin currencies this connector emits a benchmark observation for, and their ISO3 country.
# Extend deliberately when a new corridor actually needs a new origin currency -- not
# speculatively for every currency NRBT happens to publish.
ORIGIN_CURRENCIES = {
    "NZD": "NZL",
    "AUD": "AUS",
}


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
    origin_currency: str = "NZD",
) -> dict:
    """Pure function: archived-parse-result -> one schema-shaped observation dict for
    <origin_currency>/TOP.

    Raises ParseError if origin_currency's row is missing -- the caller turns that into an
    error observation rather than emitting a row with a guessed rate.
    """
    if origin_currency not in ORIGIN_CURRENCIES:
        raise ParseError(f"origin_currency {origin_currency!r} is not in ORIGIN_CURRENCIES")

    row = rates.get(origin_currency)
    if row is None:
        raise ParseError(f"{origin_currency} row not found in parsed rate table")

    published_mid_per_top = row["mid"]
    top_per_origin = 1 / published_mid_per_top

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
        "origin_country_iso3": ORIGIN_CURRENCIES[origin_currency],
        "origin_currency": origin_currency,
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
        "amount_received": top_per_origin,
        "fee": None,
        "fee_currency": None,
        "fee_is_promotional": None,
        "provider_fx_rate": top_per_origin,
        "benchmark_fx_rate": None,
        "benchmark_source": None,
        "benchmark_observation_id": None,
        "speed_text": None,
        "speed_hours_min": None,
        "speed_hours_max": None,
        "availability_status": "observed",
        "status_detail": (
            f"NRBT published BUY {row['buy']} / MID {row['mid']} / SELL {row['sell']} "
            f"{origin_currency} per 1 TOP. This row's provider_fx_rate and amount_received are "
            f"the MID rate inverted to TOP per 1 {origin_currency} ({top_per_origin:.6f}), per "
            f"METHODOLOGY.md section 2.4's quote-orientation convention. This is a benchmark "
            f"rate observation, not a transfer quote -- fee and amount_sent_includes_fee are "
            f"not applicable and are null, not zero."
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
    origin_currency: str = "NZD",
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
        "origin_country_iso3": ORIGIN_CURRENCIES.get(origin_currency, "NZL"),
        "origin_currency": origin_currency,
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
    """Live entry point: fetch -> archive -> check for a challenge -> parse -> normalise.
    One network call, via the common fetch_and_archive() path (Round 3, section 1.5's
    challenge-detection requirement)."""
    result = fetch_and_archive(PROVIDER_ID, SOURCE_URL)
    collected_at = result.fetched_at
    sha256, archive_path = result.sha256, result.archive_path

    if result.connection_error is not None:
        return [
            error_observation(
                reason=f"connection failed fetching {SOURCE_URL}: {result.connection_error}",
                sha256=sha256,
                archive_path=archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
                availability_status="error",
            )
        ]

    if result.challenge is not None:
        return [
            error_observation(
                reason=f"challenge page detected ({result.challenge!r}) fetching {SOURCE_URL}",
                sha256=sha256,
                archive_path=archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
                availability_status="blocked",
            )
        ]

    if result.status_code != 200:
        return [
            error_observation(
                reason=f"HTTP {result.status_code} fetching {SOURCE_URL}",
                sha256=sha256,
                archive_path=archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
                availability_status="error",
            )
        ]

    body = result.body_text
    try:
        rates = parse_rates(body)
        last_updated = parse_last_updated(body)
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

    observations = []
    for origin_currency in ORIGIN_CURRENCIES:
        try:
            observations.append(
                build_observation(
                    rates=rates,
                    last_updated_text=last_updated,
                    sha256=sha256,
                    archive_path=archive_path,
                    collected_at=collected_at,
                    collection_run_id=collection_run_id,
                    origin_currency=origin_currency,
                )
            )
        except ParseError as exc:
            observations.append(
                error_observation(
                    reason=f"parse error: {exc}",
                    sha256=sha256,
                    archive_path=archive_path,
                    collected_at=collected_at,
                    collection_run_id=collection_run_id,
                    availability_status="error",
                    origin_currency=origin_currency,
                )
            )
    return observations
