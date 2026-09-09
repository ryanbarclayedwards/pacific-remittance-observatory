"""Shared fetch and archive helpers.

fetch() -> archive_bytes() -> (sha256, path) is the first two steps of the CLAUDE.md section
2.2 lifecycle (fetch -> hash -> archive -> parse -> normalise -> validate -> append) shared by
every connector. Nothing here parses or interprets a payload for its OWN meaning -- that is
each connector's own job, against the archived bytes, never against a live re-fetch. The one
exception is detect_challenge(): every connector must be able to tell a real page from a bot
challenge or interstitial before attempting to parse it as content (Round 3,
reports/03-endpoints.md), so that check lives here, in the common fetch path, rather than being
left to each connector to remember on its own.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import httpx

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "archive"

# Round 4 correction (reports/04-historical.md): the repository URL previously here
# ("github.com/devpolicy/...") was a placeholder that was never actually verified as real --
# flagged and removed rather than continuing to send an unverified claim to every site this
# project fetches from. Replace with the real repository URL once the maintainer publishes it
# (CLAUDE.md section 1.5 requires an honest contact URL, not a plausible-looking one).
USER_AGENT = (
    "PacificRemittanceObservatory/0.1 "
    "(Development Policy Centre, ANU -- repository URL to be added once published)"
)

# Strong, structural phrases specific to known bot-challenge/interstitial products. Deliberately
# conservative: Round 2's sweep found several false-positive-prone strings in genuine pages
# (Wise's own bundled "Captcha" error-message strings, Western Union's Akamai *hostname*,
# Remitly's unrelated `this.blocked` JS variable) -- a marker here must be a phrase a real page
# would essentially never contain incidentally. Extend this list only from an actually-observed
# challenge page, not from guessing.
CHALLENGE_MARKERS = (
    "Incapsula incident ID",
    "_Incapsula_Resource",
    "Pardon Our Interruption",
    "Attention Required! | Cloudflare",
    "Checking your browser before accessing",
    "Enable JavaScript and cookies to continue",
    "Please verify you are a human",
    "Please complete the security check to access",
    "Access to this page has been denied",
)


def detect_challenge(body_text: str) -> str | None:
    """Returns the matched marker string if body_text looks like a bot-challenge or
    interstitial page, else None. A hit means: record availability_status = "blocked" and
    stop -- never attempt to parse the body as real content (CLAUDE.md section 1.5)."""
    for marker in CHALLENGE_MARKERS:
        if marker in body_text:
            return marker
    return None


@dataclass
class FetchResult:
    url: str
    status_code: int
    headers: dict
    body_text: str
    sha256: str
    archive_path: Path
    fetched_at: datetime
    challenge: str | None


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

    Body encoding (fixed Round 4, reports/04-historical.md): a real payload isn't always UTF-8
    text -- an .xlsx or .pdf source is binary. Round 3's version of this function silently
    corrupted any non-UTF-8 body via `errors="replace"`, which would have quietly mangled a
    binary archive on first real use. Text bodies are stored as UTF-8 text as before (encoding
    "utf-8"); anything that doesn't decode cleanly is stored base64-encoded (encoding "base64")
    instead, byte-for-byte recoverable either way.

    Returns (sha256_hex, archive_path). Idempotent: fetching byte-identical content twice
    writes the same file once.
    """
    fetched_at = fetched_at or datetime.now(timezone.utc)
    sha256 = hashlib.sha256(body).hexdigest()

    try:
        body_text = body.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        body_text = base64.b64encode(body).decode("ascii")
        encoding = "base64"

    envelope = {
        "url": url,
        "fetched_at": fetched_at.isoformat(),
        "status_code": status_code,
        "headers": {k: v for k, v in headers.items()},
        "encoding": encoding,
        "body": body_text,
    }

    day_dir = ARCHIVE_ROOT / provider_slug / f"{fetched_at:%Y}" / f"{fetched_at:%m}" / f"{fetched_at:%d}"
    day_dir.mkdir(parents=True, exist_ok=True)
    path = day_dir / f"{sha256}.json.gz"

    if not path.exists():
        with gzip.open(path, "wt", encoding="utf-8") as f:
            json.dump(envelope, f, ensure_ascii=False)

    return sha256, path


def read_archived_bytes(path: Path) -> bytes:
    """Read back the exact raw bytes originally archived, regardless of encoding. The
    byte-for-byte source of truth -- prefer this over read_archived_body() for anything that
    isn't known to be text (a spreadsheet, a PDF, an image)."""
    with gzip.open(path, "rt", encoding="utf-8") as f:
        envelope = json.load(f)
    if envelope.get("encoding") == "base64":
        return base64.b64decode(envelope["body"])
    return envelope["body"].encode("utf-8")


def read_archived_body(path: Path) -> str:
    """Read back the raw body as text from an archived .json.gz file -- used by golden tests
    to prove a parser runs against exactly what was archived, not a live re-fetch. Raises if
    the archived body is binary (base64-encoded) -- use read_archived_bytes() for that."""
    with gzip.open(path, "rt", encoding="utf-8") as f:
        envelope = json.load(f)
    if envelope.get("encoding") == "base64":
        raise ValueError(f"{path} holds binary content -- use read_archived_bytes() instead")
    return envelope["body"]


def fetch_and_archive(
    provider_slug: str, url: str, *, user_agent: str = USER_AGENT, timeout: float = 30.0
) -> FetchResult:
    """The common fetch path every connector should use: fetch -> hash -> archive -> check for
    a challenge page, in one call. Always archives the response, even a challenge page -- a
    block is a finding and gets recorded, per CLAUDE.md section 1.5, not silently dropped.

    Callers must check `.challenge` before attempting to parse `.body_text` as real content:
    a non-None value means stop and emit availability_status = "blocked", never parse further.
    """
    fetched_at = datetime.now(timezone.utc)
    resp = fetch(url, user_agent=user_agent, timeout=timeout)
    sha256, path = archive_bytes(
        provider_slug, url, resp.status_code, dict(resp.headers), resp.content, fetched_at=fetched_at
    )
    try:
        body_text = read_archived_body(path)
        challenge = detect_challenge(body_text)
    except ValueError:
        # Binary content (e.g. a PDF/xlsx fee schedule) -- not text, so not a text-based
        # challenge page either. The connector calling this is responsible for choosing
        # read_archived_bytes() instead of relying on .body_text.
        body_text = ""
        challenge = None
    return FetchResult(
        url=url,
        status_code=resp.status_code,
        headers=dict(resp.headers),
        body_text=body_text,
        sha256=sha256,
        archive_path=path,
        fetched_at=fetched_at,
        challenge=challenge,
    )
