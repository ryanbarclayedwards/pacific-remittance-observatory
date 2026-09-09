"""OrbitRemit -- AUD -> TOP connector (Tier 2, public_quote).

Round 3 (reports/03-endpoints.md): a raw-fetch endpoint-discovery pass for OrbitRemit's
client-side rate widget found no discoverable JSON/XHR API in the page's linked static assets
or its Next.js streaming payload -- but the streaming payload itself
(`self.__next_f.push([...])` chunks, part of the raw server-rendered HTML, no JS execution
needed) already contains a full server-rendered comparison table of AUD amounts against their
TOP received amounts. That table is what this connector parses -- not an endpoint, but genuine
server-rendered content, exactly what CLAUDE.md section 3's Tier 1/2 distinction cares about
(reachable without defeating anything).

**The rate is not a single clean number.** The comparison table's implied rate varies by
amount: ~1.7336 TOP/AUD for amounts up to 500 AUD (matching OrbitRemit's own advertised
"promotional rate for new customers, capped at the first $500 AUD" -- see
scratch/round-01/orbitremit.md), declining toward ~1.65 TOP/AUD for larger amounts. The page's
own <meta name="description"> states a third figure (1.69237) that does not match any single
table entry. This connector picks the table's 500 AUD row specifically -- the last row still at
the promotional rate -- and stores the *implied* rate (amount_received / amount_sent) rather
than asserting a single "the rate," with the discrepancy disclosed in status_detail. No fee
amount was found anywhere in raw bytes; `fee` is null, not assumed.
"""
from __future__ import annotations

import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from collect.archive import ARCHIVE_ROOT, fetch_and_archive

PROVIDER_ID = "orbitremit"
PROVIDER_NAME_RAW = "OrbitRemit"
SOURCE_URL = "https://www.orbitremit.com/currency-converter/aud-to-top"
CONNECTOR_ID = "orbitremit"
CONNECTOR_VERSION = "0.1.0"
METHODOLOGY_VERSION = "0.3"

TARGET_AMOUNT_SENT = 500.0  # AUD -- the last row still at OrbitRemit's own advertised promo rate

NEXT_F_PUSH_RE = re.compile(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', re.S)
COMPARISON_ROW_RE = re.compile(r'"children":"([\d,]+) AUD"\}\].*?"children":"([\d,.]+) TOP"')


class ParseError(Exception):
    pass


def parse_comparison_table(html_text: str) -> dict[float, float]:
    """Extract {amount_sent_aud: amount_received_top} from the server-rendered comparison
    table embedded in the page's Next.js streaming payload."""
    chunks = NEXT_F_PUSH_RE.findall(html_text)
    if not chunks:
        raise ParseError("no self.__next_f.push chunks found on the page")

    full = "".join(chunks)
    try:
        full_text = full.encode().decode("unicode_escape")
    except UnicodeDecodeError as exc:
        raise ParseError(f"failed to decode streaming payload: {exc}")

    pairs = COMPARISON_ROW_RE.findall(full_text)
    if not pairs:
        raise ParseError("no AUD/TOP comparison-table rows found in the streaming payload")

    table: dict[float, float] = {}
    for sent_s, received_s in pairs:
        sent = float(sent_s.replace(",", ""))
        received = float(received_s.replace(",", ""))
        table[sent] = received
    return table


def parse_meta_description_rate(html_text: str) -> float | None:
    """The page's <meta name="description"> also states a rate figure -- captured for
    disclosure alongside the comparison-table rate, not used as the observation's own rate
    (see module docstring: the two don't match)."""
    m = re.search(r'\$1 AUD = ([\d.]+) TOP', html_text)
    return float(m.group(1)) if m else None


def build_observation(
    *,
    table: dict[float, float],
    meta_rate: float | None,
    sha256: str,
    archive_path: Path,
    collected_at: datetime,
    collection_run_id: str,
) -> dict:
    if TARGET_AMOUNT_SENT not in table:
        raise ParseError(f"{TARGET_AMOUNT_SENT} AUD row not found in the parsed comparison table")

    amount_received = table[TARGET_AMOUNT_SENT]
    implied_rate = amount_received / TARGET_AMOUNT_SENT

    meta_note = (
        f"the page's own meta description separately states $1 AUD = {meta_rate} TOP, which "
        f"matches neither this nor any other comparison-table row -- both are recorded as "
        f"observed, not reconciled into one 'true' rate."
        if meta_rate is not None
        else "the page's meta description rate was not found this run."
    )

    return {
        "observation_id": str(uuid.uuid4()),
        "collection_run_id": collection_run_id,
        "supersedes": None,
        "correction_reason": None,
        "collected_at": collected_at.isoformat(),
        "provider_quote_timestamp": None,
        "source_last_updated": None,
        "quote_validity_text": None,
        "collection_method": "public_quote",
        "source_system": "collector",
        "source_url": SOURCE_URL,
        "connector_id": CONNECTOR_ID,
        "connector_version": CONNECTOR_VERSION,
        "methodology_version": METHODOLOGY_VERSION,
        "origin_country_iso3": "AUS",
        "origin_currency": "AUD",
        "destination_country_iso3": "TON",
        "destination_currency": "TOP",
        "amount_sent": TARGET_AMOUNT_SENT,
        "amount_sent_includes_fee": None,
        "provider_id": PROVIDER_ID,
        "provider_name_raw": PROVIDER_NAME_RAW,
        "provider_name_canonical": PROVIDER_NAME_RAW,
        "provider_type": "global_mto",
        "option_id": None,
        "option_name_raw": None,
        "funding_method": None,
        "delivery_method": None,
        "amount_received": amount_received,
        "fee": None,
        "fee_currency": None,
        "fee_is_promotional": None,
        "provider_fx_rate": implied_rate,
        "benchmark_fx_rate": None,
        "benchmark_source": None,
        "benchmark_observation_id": None,
        "speed_text": None,
        "speed_hours_min": None,
        "speed_hours_max": None,
        "availability_status": "observed",
        "status_detail": (
            f"OrbitRemit's own server-rendered comparison table states {TARGET_AMOUNT_SENT:.0f} "
            f"AUD -> {amount_received} TOP, an implied rate of {implied_rate:.6f} TOP/AUD. This "
            f"is the last table row still at OrbitRemit's own advertised promotional rate for "
            f"new customers, capped at the first $500 AUD (scratch/round-01/orbitremit.md) -- "
            f"not a rate a repeat customer or a larger transfer would necessarily get; the same "
            f"table shows the implied rate declining toward ~1.65 for amounts above $500. No "
            f"fee amount was found anywhere in raw bytes -- fee is null, not assumed zero. And "
            f"{meta_note}"
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
    availability_status: str,
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
        "collection_method": "public_quote",
        "source_system": "collector",
        "source_url": SOURCE_URL,
        "connector_id": CONNECTOR_ID,
        "connector_version": CONNECTOR_VERSION,
        "methodology_version": METHODOLOGY_VERSION,
        "origin_country_iso3": "AUS",
        "origin_currency": "AUD",
        "destination_country_iso3": "TON",
        "destination_currency": "TOP",
        "amount_sent": TARGET_AMOUNT_SENT,
        "amount_sent_includes_fee": None,
        "provider_id": PROVIDER_ID,
        "provider_name_raw": PROVIDER_NAME_RAW,
        "provider_name_canonical": PROVIDER_NAME_RAW,
        "provider_type": "global_mto",
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
    result = fetch_and_archive(PROVIDER_ID, SOURCE_URL)
    collected_at = result.fetched_at

    if result.challenge is not None:
        return [
            error_observation(
                reason=f"challenge page detected ({result.challenge!r}) fetching {SOURCE_URL}",
                sha256=result.sha256,
                archive_path=result.archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
                availability_status="blocked",
            )
        ]

    if result.status_code != 200:
        return [
            error_observation(
                reason=f"HTTP {result.status_code} fetching {SOURCE_URL}",
                sha256=result.sha256,
                archive_path=result.archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
                availability_status="error",
            )
        ]

    try:
        table = parse_comparison_table(result.body_text)
        meta_rate = parse_meta_description_rate(result.body_text)
        return [
            build_observation(
                table=table,
                meta_rate=meta_rate,
                sha256=result.sha256,
                archive_path=result.archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
            )
        ]
    except ParseError as exc:
        return [
            error_observation(
                reason=f"parse error: {exc}",
                sha256=result.sha256,
                archive_path=result.archive_path,
                collected_at=collected_at,
                collection_run_id=collection_run_id,
                availability_status="error",
            )
        ]
