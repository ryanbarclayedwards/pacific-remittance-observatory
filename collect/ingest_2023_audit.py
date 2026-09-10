"""Ingest the 2023 manual remittance-cost audit (Round 4, reports/04-historical.md, Task A).

Not a connector -- deliberately not registered in collect.run.CONNECTORS. A one-off import of
data the maintainer already held (CLAIMS.md C1), located this round at hm-ds/Data/audit1.csv
and hm-ds/Data/audit2.csv -- two separate audit waves conducted by hand against two comparison
platforms (Send Money Pacific, Saver Pacific), not by this project's own collectors:

  audit1.csv: 2023-03-28 to 2023-04-25 (29 dates), corridors AUSTON/AUSVAN/NZTON/NZVAN.
  audit2.csv: 2023-07-25 to 2023-08-07 (14 dates), corridors AUSTON/NZTON only.

Only Tonga corridors (AUSTON, NZTON) are imported -- this project has no Vanuatu benchmark
(Reserve Bank of Vanuatu's TLS chain stays broken and unworked-around, Round 1/2) and Task A's
scope is Tonga. The Vanuatu rows in audit1.csv are real and left in the source file, just not
ingested this round.

Field mapping decided by direct arithmetic verification against the raw CSVs (not assumed):
amount_sent is a fixed 200 units of the origin currency for every row (confirmed by the
benchmark columns' own naming -- audit2's "200AUD_NZD" -- and by back-solving amount_received
against fee and fxrate for ~1,000+ rows). fee is denominated in the origin currency. Whether fee
is deducted from the 200 before conversion or charged on top of it varies by row -- most rows
fit "deducted before conversion" but at least one (Western Union Cash, NZTON, 2023-07-26) fits
"charged on top" far better and fits "deducted" badly (a 5.94-unit gap against a ~1-unit
tolerance everywhere else). The source data doesn't state which convention applies per row, so
`amount_sent_includes_fee` is left null throughout, deliberately, rather than inferred from
which formula happens to fit best -- CLAUDE.md section 1.1: reasoning about what a value
probably was is not the same as observing it.

Schema fields NOT populated by this import, why: `Rank` (the audit's own daily provider
ranking) and `Date2`/`Thu`/`Weekend` (day-of-week flags, trivially derivable from `collected_at`)
are not imported -- rank is an explicitly excluded derived field (schema.json's own $comment),
and the day-of-week flags are redundant metadata, not new facts. `Cost_PP` (the audit's own
precomputed cost) and the audit's own embedded benchmark figures (`AUD_Paanga` etc.) are
preserved verbatim in `notes` for traceability -- not stored as this project's own
`benchmark_fx_rate`, because that field is reserved for this project's own NRBT-sourced
benchmark (METHODOLOGY.md section 2.3) and populating it from a different, undocumented
benchmark methodology would misrepresent what it means. `speed_hours_min`/`speed_hours_max` are
left null -- converting text like "Next day" or "1-3 days" into a numeric hour range would be
inventing precision the source doesn't state; `speed_text` carries the raw label instead.
"""
from __future__ import annotations

import csv
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from collect.archive import ARCHIVE_ROOT, archive_bytes
from collect.store import append_observations

REPO_ROOT = Path(__file__).resolve().parent.parent
HM_DS_DATA = REPO_ROOT / "hm-ds" / "Data"
METHODOLOGY_VERSION = "0.4"
CONNECTOR_ID = "manual_audit.2023_import"
CONNECTOR_VERSION = "0.1.0"

# The archive's own fetch date: when this project actually acquired the CSV files, not when
# the underlying observations happened (that's collected_at, per row, below).
ARCHIVED_AT = datetime(2026, 9, 10, tzinfo=timezone.utc)

WAVES = {
    "audit1": {
        "file": HM_DS_DATA / "audit1.csv",
        "date_field": "Date",
        "website_field": "Website",
        "corridor_field": "Corridor",
        "mtos_field": "MTOs",
        "mode_field": "modeoftransaction",
        "speed_field": "Speed",
        "received_field": "amountreceived ",
        "rate_field": "fxrate",
        "fee_field": "Fee ",
        "cost_pp_field": "Cost_PP",
        "benchmark_note": lambda row, corridor: (
            f"original audit AUD benchmark (200 AUD->TOP): {row.get('AUD_Paanga')}; "
            f"NZD benchmark (200 NZD->TOP): {row.get('NZD_Paanga')}"
        ),
    },
    "audit2": {
        "file": HM_DS_DATA / "audit2.csv",
        "date_field": "date",
        "website_field": "website",
        "corridor_field": "corridor",
        "mtos_field": "mtos",
        "mode_field": "modeoftransaction",
        "speed_field": "speed",
        "received_field": "amountreceived",
        "rate_field": "FXrate",
        "fee_field": "Fee ",
        "cost_pp_field": "Cost_PP",
        "benchmark_note": lambda row, corridor: (
            f"original audit benchmark (200 {'-'.join(['AUD' if corridor=='AUSTON' else 'NZD'])}->TOP): "
            f"{row.get('200AUD_NZD')}"
        ),
    },
}

CORRIDORS = {
    "AUSTON": {"origin_country": "AUS", "origin_currency": "AUD", "dest_country": "TON", "dest_currency": "TOP"},
    "NZTON": {"origin_country": "NZL", "origin_currency": "NZD", "dest_country": "TON", "dest_currency": "TOP"},
}

WEBSITES = {
    "1": ("Send Money Pacific", "https://sendmoneypacific.org/"),
    "2": ("Saver Pacific", "https://saverpacific.com/"),
}

# (raw base name) -> (provider_id, provider_name_canonical, provider_type). Slugs match
# PROVIDERS.md's Round 1 naming exactly where the same entity was already triaged there
# (CLAIMS.md E3: provider identity harmonisation across vintages).
BASE_PROVIDERS = {
    "Moneygram": ("moneygram", "MoneyGram", "global_mto"),
    "Ave Paanga Pau": ("ave-paanga-pau", "'Ave Pa'anga Pau", "corridor_specialist"),
    "KlickEX": ("klickex", "KlickEx", "corridor_specialist"),
    "Ria": ("ria-money-transfer", "Ria Money Transfer", "global_mto"),
    "OFX": ("ofx", "OFX", "global_mto"),
    "Western Union": ("western-union", "Western Union", "global_mto"),
    "NAB": ("nab", "National Australia Bank", "bank"),
    "ASB": ("asb", "ASB", "bank"),
    "Kiwi Bank": ("kiwibank", "Kiwibank", "bank"),
    "Wantok": ("wantok-money", "WanTok Money", "corridor_specialist"),
    "iMEX": ("imex", "IMEX Money Transfer", "corridor_specialist"),
}
# Providers that are genuinely different legal entities depending on origin country.
CORRIDOR_CONDITIONAL_PROVIDERS = {
    "ANZ": {
        "AUSTON": ("anz-australia", "ANZ (Australia)", "bank"),
        "NZTON": ("anz-new-zealand", "ANZ (New Zealand)", "bank"),
    },
    "Westpac": {
        "AUSTON": ("westpac-australia", "Westpac (Australia)", "bank"),
        "NZTON": ("westpac-new-zealand", "Westpac (New Zealand)", "bank"),
    },
}

PAREN_SUFFIX_RE = re.compile(r"\s*\([^)]*\)\s*$")


class BlankRow(Exception):
    """The row has no provider recorded at all -- a genuine placeholder in the source (e.g.
    audit1.csv has 12 rows for Saver Pacific / AUSTON / 2023-04-03 with every provider field
    empty but Rank and the day's benchmark still filled in -- read as "no options were
    available or recorded that day," not a parsing gap)."""


def resolve_provider(raw_mtos: str, corridor: str) -> tuple[str, str, str]:
    if raw_mtos.strip() == "":
        raise BlankRow()
    base = PAREN_SUFFIX_RE.sub("", raw_mtos).strip()
    if base in CORRIDOR_CONDITIONAL_PROVIDERS:
        return CORRIDOR_CONDITIONAL_PROVIDERS[base][corridor]
    if base in BASE_PROVIDERS:
        return BASE_PROVIDERS[base]
    raise KeyError(f"unrecognised provider base name {base!r} (raw: {raw_mtos!r}) -- add it to the map, don't guess")


def parse_date(d: str) -> datetime:
    day, month, year = d.strip().split("/")
    return datetime(int(year), int(month), int(day), tzinfo=timezone.utc)


def _float_or_none(s: str) -> float | None:
    s = s.strip()
    return float(s) if s else None


def build_observation(
    *, row: dict, wave_key: str, wave_cfg: dict, collection_run_id: str, sha256: str, archive_path: Path
) -> dict | None:
    corridor = row[wave_cfg["corridor_field"]].strip()
    if corridor not in CORRIDORS:
        return None  # Vanuatu rows -- not this round's scope, see module docstring

    website_code = row[wave_cfg["website_field"]].strip()
    website_name, website_url = WEBSITES[website_code]

    raw_mtos = row[wave_cfg["mtos_field"]].strip()
    provider_id, provider_name_canonical, provider_type = resolve_provider(raw_mtos, corridor)

    mode = row[wave_cfg["mode_field"]].strip()
    if " - " in mode:
        funding_method, delivery_method = [p.strip() for p in mode.split(" - ", 1)]
    else:
        funding_method, delivery_method = mode, None

    cur = CORRIDORS[corridor]
    date = parse_date(row[wave_cfg["date_field"]])
    fee = _float_or_none(row[wave_cfg["fee_field"]])
    amount_received = _float_or_none(row[wave_cfg["received_field"]])
    provider_fx_rate = _float_or_none(row[wave_cfg["rate_field"]])
    cost_pp = row.get(wave_cfg["cost_pp_field"], "").strip()

    notes = (
        f"Original audit's own reported Cost_PP: {cost_pp} (methodology/benchmark undocumented "
        f"in source -- not this project's NRBT benchmark). "
        f"{wave_cfg['benchmark_note'](row, corridor)} (undocumented methodology)."
    )

    return {
        "observation_id": str(uuid.uuid4()),
        "collection_run_id": collection_run_id,
        "supersedes": None,
        "correction_reason": None,
        "collected_at": date.isoformat(),
        "provider_quote_timestamp": None,
        "source_last_updated": None,
        "quote_validity_text": None,
        "collection_method": "manual_audit",
        "source_system": "devpolicy_manual_audit",
        "source_url": website_url,
        "connector_id": CONNECTOR_ID,
        "connector_version": CONNECTOR_VERSION,
        "methodology_version": METHODOLOGY_VERSION,
        "origin_country_iso3": cur["origin_country"],
        "origin_currency": cur["origin_currency"],
        "destination_country_iso3": cur["dest_country"],
        "destination_currency": cur["dest_currency"],
        "amount_sent": 200.0,
        "amount_sent_includes_fee": None,  # deliberately -- see module docstring
        "provider_id": provider_id,
        "provider_name_raw": raw_mtos,
        "provider_name_canonical": provider_name_canonical,
        "provider_type": provider_type,
        "option_id": None,
        "option_name_raw": raw_mtos,
        "funding_method": funding_method,
        "delivery_method": delivery_method,
        "amount_received": amount_received,
        "fee": fee,
        "fee_currency": cur["origin_currency"] if fee is not None else None,
        "fee_is_promotional": None,
        "rate_is_promotional": None,
        "promotion_detail": None,
        "provider_fx_rate": provider_fx_rate,
        "benchmark_fx_rate": None,
        "benchmark_source": None,
        "benchmark_observation_id": None,
        "speed_text": row[wave_cfg["speed_field"]].strip() or None,
        "speed_hours_min": None,
        "speed_hours_max": None,
        "availability_status": "observed",
        "status_detail": (
            f"Manual audit observation, wave {wave_key!r} (Round 4 ingestion, "
            f"reports/04-historical.md Task A). Observed via the {website_name} comparison "
            f"site. amount_sent is a fixed 200 units of the origin currency, confirmed by "
            f"arithmetic against amount_received/fee/rate across the wave, not assumed from a "
            f"single row."
        ),
        "raw_payload_sha256": sha256,
        "raw_payload_path": str(archive_path.relative_to(ARCHIVE_ROOT.parent)),
        "notes": notes,
    }


def run(*, dry_run: bool = False) -> None:
    for wave_key, wave_cfg in WAVES.items():
        path = wave_cfg["file"]
        if not path.exists():
            print(f"ingest_2023_audit: source file not found: {path}", file=sys.stderr)
            sys.exit(1)

        raw_bytes = path.read_bytes()
        sha256, archive_path = archive_bytes(
            "manual-audit-2023", f"local-file:{path.name}", 200, {}, raw_bytes, fetched_at=ARCHIVED_AT
        )
        print(f"ingest_2023_audit: archived {path.name} as {sha256} -> {archive_path}")

        with path.open("r", newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))

        collection_run_id = (
            f"manual-audit-2023-{wave_key}-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
        )

        by_month: dict[str, list[dict]] = {}
        skipped_vanuatu = 0
        skipped_unrecognised = 0
        skipped_blank = 0
        for row in rows:
            if row[wave_cfg["website_field"]].strip() == "":
                continue  # a handful of fully-blank rows in the raw CSV
            corridor = row[wave_cfg["corridor_field"]].strip()
            if corridor not in CORRIDORS:
                skipped_vanuatu += 1
                continue
            try:
                obs = build_observation(
                    row=row,
                    wave_key=wave_key,
                    wave_cfg=wave_cfg,
                    collection_run_id=collection_run_id,
                    sha256=sha256,
                    archive_path=archive_path,
                )
            except BlankRow:
                skipped_blank += 1
                continue
            except KeyError as exc:
                skipped_unrecognised += 1
                print(f"  skipped (unrecognised provider): {exc}")
                continue
            if obs is None:
                skipped_vanuatu += 1
                continue
            month = row[wave_cfg["date_field"]].strip()
            month = f"{parse_date(month):%Y-%m}"
            by_month.setdefault(month, []).append(obs)

        total = sum(len(v) for v in by_month.values())
        print(
            f"ingest_2023_audit: {wave_key}: {total} observations across {len(by_month)} "
            f"month-files ({skipped_vanuatu} Vanuatu rows skipped, {skipped_blank} blank "
            f"placeholder rows skipped, {skipped_unrecognised} unrecognised-provider rows "
            f"skipped)"
        )

        if not dry_run:
            for month in sorted(by_month):
                append_observations(by_month[month], month=month)

    if dry_run:
        print("ingest_2023_audit: --dry-run, not writing")
    else:
        print("ingest_2023_audit: done")


def main(argv=None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    run(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
