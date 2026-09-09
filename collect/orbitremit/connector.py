"""OrbitRemit -- AUD -> TOP connector (Tier 2, public_quote).

Round 3 (reports/03-endpoints.md): a raw-fetch endpoint-discovery pass for OrbitRemit's
client-side rate widget found no discoverable JSON/XHR API in the page's linked static assets
or its Next.js streaming payload -- but the streaming payload itself
(`self.__next_f.push([...])` chunks, part of the raw server-rendered HTML, no JS execution
needed) already contains a full server-rendered comparison table of AUD amounts against their
TOP received amounts. That table is what this connector parses -- not an endpoint, but genuine
server-rendered content, exactly what CLAUDE.md section 3's Tier 1/2 distinction cares about
(reachable without defeating anything).

**Round 4 correction (reports/04-historical.md):** Round 3's first version of this connector
picked a single row (500 AUD) and stored it as if it were "the" quote. That was wrong in two
ways the maintainer corrected: (1) 500 AUD sits exactly at the peak of a new-customer
promotional distortion, so a cost comparison built from it doesn't generalise -- reported as if
it did; (2) the promotional structure was then invisible in the data, buried in a row-selection
choice a future reader couldn't see. This version stores every row in the table as its own
observation, with `rate_is_promotional` / `promotion_detail` (schema v0.2) making the
distortion visible in the data itself rather than in this docstring.

The table's implied rate is ~1.7336 TOP/AUD for AUD amounts up to and including 500 (matching
OrbitRemit's own advertised "promotional rate for new customers, capped at the first $500 AUD",
scratch/round-01/orbitremit.md), and declines for larger amounts as the promotional portion
becomes a smaller share of a blended send. The page's <meta name="description"> separately
states "$1 AUD = 1.69237 TOP" -- this is not a third, unexplained figure (Round 3's connector
described it that way; that was wrong): 1692.37 / 1000 is exactly 1.69237, so the meta
description is simply quoting the table's own 1,000 AUD row's implied rate.

No fee amount was found anywhere in raw bytes for any row; `fee` is null throughout, not
assumed.
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
CONNECTOR_VERSION = "0.2.0"
METHODOLOGY_VERSION = "0.4"

PROMO_CAP_AUD = 500.0  # OrbitRemit's own advertised cap for the new-customer promotional rate

# The Round 3 observation this round's 500 AUD row corrects (adds rate_is_promotional /
# promotion_detail, which schema v0.1 had no field for). Not a live lookup -- a fixed,
# documented fact about this specific historical row, per CLAUDE.md section 1.3: corrections
# are new rows with supersedes, never a rewrite of the old one.
SUPERSEDES_500_AUD_OBSERVATION_ID = "50ae569e-b6d1-43d1-b092-e6bc25db7eee"

NEXT_F_PUSH_RE = re.compile(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', re.S)
COMPARISON_ROW_RE = re.compile(r'"children":"([\d,]+) AUD"\}\].*?"children":"([\d,.]+) TOP"')

# The table's last row (as served 2026-09-09) is not inlined like the other eight -- React's
# streaming format hoists it into two separately-numbered chunks and references them by id
# (e.g. "children":"$L56"..."$L57") instead of embedding the text directly in the row. Resolve
# that one reference pair explicitly rather than silently dropping the ninth amount.
REFERENCED_ROW_RE = re.compile(r'"children":"\$L(\d+)"\}\],"\$L(\d+)"')


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

    ref_match = REFERENCED_ROW_RE.search(full_text)
    if ref_match:
        amount_ref, received_ref = ref_match.groups()
        amount_m = re.search(rf'\n{amount_ref}:.*?"children":"([\d,]+) AUD"', full_text)
        received_m = re.search(rf'\n{received_ref}:.*?"children":"([\d,.]+) TOP"', full_text)
        if amount_m and received_m:
            sent = float(amount_m.group(1).replace(",", ""))
            received = float(received_m.group(1).replace(",", ""))
            table[sent] = received
        # If the reference doesn't resolve, the inline rows already found still stand -- a
        # missing ninth row is a gap to disclose (see build_observations' caller), not a
        # reason to fail every other row too.

    return table


def parse_meta_description_rate(html_text: str) -> float | None:
    """The page's <meta name="description"> also states a rate figure. It is not an
    independent third rate -- it equals the table's 1,000 AUD row's implied rate exactly
    (1692.37 / 1000 = 1.69237) -- captured here only to show that arithmetic, not used as an
    observation's own rate."""
    m = re.search(r'\$1 AUD = ([\d.]+) TOP', html_text)
    return float(m.group(1)) if m else None


def _promotion_fields(amount_sent: float, implied_rate: float) -> tuple[bool, str]:
    """Every row in the table sits at or downstream of OrbitRemit's advertised promotional cap
    -- rate_is_promotional is True for all of them, but the detail differs: at or under the
    cap, the whole amount is at the promotional rate; above it, the rate is a blend."""
    if amount_sent <= PROMO_CAP_AUD:
        detail = (
            f"The entire {amount_sent:.0f} AUD send qualifies for OrbitRemit's advertised "
            f"promotional rate for new customers, capped at the first {PROMO_CAP_AUD:.0f} AUD "
            f"(scratch/round-01/orbitremit.md). Implied rate {implied_rate:.6f} TOP/AUD."
        )
        return True, detail

    detail = (
        f"Blended rate: the first {PROMO_CAP_AUD:.0f} AUD of this {amount_sent:.0f} AUD send "
        f"benefits from OrbitRemit's advertised promotional rate for new customers "
        f"(~1.7336 TOP/AUD, per the table's own sub-{PROMO_CAP_AUD:.0f} rows); the remaining "
        f"{amount_sent - PROMO_CAP_AUD:.0f} AUD is priced at an implied standard rate of "
        f"~1.6511 TOP/AUD -- an unpublished estimate derived by fitting OrbitRemit's own table, "
        f"not itself a separately observed figure. This row's provider_fx_rate "
        f"({implied_rate:.6f}) is the resulting blend, not a pure standard rate."
    )
    return True, detail


def build_observations(
    *,
    table: dict[float, float],
    sha256: str,
    archive_path: Path,
    collected_at: datetime,
    collection_run_id: str,
) -> list[dict]:
    """Pure function: archived-parse-result -> one schema-shaped observation dict per row in
    the comparison table. Raises ParseError if the table is empty."""
    if not table:
        raise ParseError("comparison table is empty")

    observations = []
    for amount_sent in sorted(table):
        amount_received = table[amount_sent]
        implied_rate = amount_received / amount_sent
        rate_is_promotional, promotion_detail = _promotion_fields(amount_sent, implied_rate)

        supersedes = (
            SUPERSEDES_500_AUD_OBSERVATION_ID if amount_sent == PROMO_CAP_AUD else None
        )
        correction_reason = (
            "Round 3's single-row observation for 500 AUD lacked rate_is_promotional / "
            "promotion_detail (schema v0.1 had no field for a promotional rate, only a "
            "promotional fee) and was reported alongside a cost comparison that did not "
            "generalise beyond this one row. This row adds the missing fields; see "
            "reports/04-historical.md."
            if supersedes
            else None
        )

        observations.append(
            {
                "observation_id": str(uuid.uuid4()),
                "collection_run_id": collection_run_id,
                "supersedes": supersedes,
                "correction_reason": correction_reason,
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
                "amount_sent": amount_sent,
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
                "rate_is_promotional": rate_is_promotional,
                "promotion_detail": promotion_detail,
                "provider_fx_rate": implied_rate,
                "benchmark_fx_rate": None,
                "benchmark_source": None,
                "benchmark_observation_id": None,
                "speed_text": None,
                "speed_hours_min": None,
                "speed_hours_max": None,
                "availability_status": "observed",
                "status_detail": (
                    f"From OrbitRemit's own server-rendered comparison table: "
                    f"{amount_sent:.0f} AUD -> {amount_received} TOP. fee is null, not "
                    f"assumed zero -- no fee amount was found anywhere in raw bytes on this "
                    f"page."
                ),
                "raw_payload_sha256": sha256,
                "raw_payload_path": str(archive_path.relative_to(ARCHIVE_ROOT.parent)),
                "notes": None,
            }
        )
    return observations


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
        "amount_sent": PROMO_CAP_AUD,
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
        "rate_is_promotional": None,
        "promotion_detail": None,
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
        return build_observations(
            table=table,
            sha256=result.sha256,
            archive_path=result.archive_path,
            collected_at=collected_at,
            collection_run_id=collection_run_id,
        )
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
