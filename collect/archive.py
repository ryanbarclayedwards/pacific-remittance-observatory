"""Shared fetch and archive helpers.

fetch() -> archive_bytes() -> (sha256, path) is the first two steps of the CLAUDE.md section
2.2 lifecycle (fetch -> hash -> archive -> parse -> normalise -> validate -> append) shared by
every connector. Nothing here parses or interprets a payload -- that is each connector's own
job, against the archived bytes, never against a live re-fetch.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "archive"

USER_AGENT = (
    "PacificRemittanceObservatory/0.1 "
    "(+https://github.com/devpolicy/pacific-remittance-observatory; research@devpolicy.org)"
)


def fetch(url: str, *, user_agent: str = USER_AGENT, timeout: float = 30.0) -> httpx.Response:
    """A single honest GET. No retries, no header spoofing, no CAPTCHA/challenge handling.

    A non-200 response or a bot-challenge page is not retried here -- the caller decides what
    that means for availability_status. This function never tries to get past a block.
    """
    with httpx.Client(headers={"User-Agent": user_agent}, timeout=timeout, follow_redirects=True) as client:
        return client.get(url)


def archive_bytes(
    provider_slug: str,
    url: str,
    status_code: int,
    headers: dict,
    body: bytes,
    *,
    fetched_at: datetime | None = None,
) -> tuple[str, Path]:
    """Hash the raw response body, wrap it with metadata, gzip it to
    archive/<provider>/<YYYY>/<MM>/<DD>/<sha256>.json.gz.

    The hash is computed over the raw body exactly as received -- raw_payload_sha256 in an
    observation row is this value, and the archive path it must resolve to is derived from
    the same hash, so the two can never drift apart.

    Returns (sha256_hex, archive_path). Idempotent: fetching byte-identical content twice
    writes the same file once.
    """
    fetched_at = fetched_at or datetime.now(timezone.utc)
    sha256 = hashlib.sha256(body).hexdigest()

    envelope = {
        "url": url,
        "fetched_at": fetched_at.isoformat(),
        "status_code": status_code,
        "headers": {k: v for k, v in headers.items()},
        "body": body.decode("utf-8", errors="replace"),
    }

    day_dir = ARCHIVE_ROOT / provider_slug / f"{fetched_at:%Y}" / f"{fetched_at:%m}" / f"{fetched_at:%d}"
    day_dir.mkdir(parents=True, exist_ok=True)
    path = day_dir / f"{sha256}.json.gz"

    if not path.exists():
        with gzip.open(path, "wt", encoding="utf-8") as f:
            json.dump(envelope, f, ensure_ascii=False)

    return sha256, path


def read_archived_body(path: Path) -> str:
    """Read back the raw body from an archived .json.gz file -- used by golden tests to prove
    a parser runs against exactly what was archived, not a live re-fetch."""
    with gzip.open(path, "rt", encoding="utf-8") as f:
        envelope = json.load(f)
    return envelope["body"]
