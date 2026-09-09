"""Golden tests for challenge-page detection (Round 3, reports/03-endpoints.md).

Positive case runs against the real Incapsula challenge page ANZ NZ served in Round 2
(tests/fixtures/challenge-pages/incapsula-anz-nz.html) -- not a synthetic example. Negative
cases guard against the specific false positives Round 2's sweep actually produced: Wise's own
bundled "Captcha" error-message strings, Western Union's Akamai *hostname* (not a challenge),
and Remitly's unrelated `this.blocked` JS variable.
"""
from datetime import datetime, timezone
from pathlib import Path

import pytest

from collect.archive import archive_bytes, detect_challenge, read_archived_body, read_archived_bytes

FIXTURE = Path(__file__).parent / "fixtures" / "challenge-pages" / "incapsula-anz-nz.html"


def test_detects_the_real_anz_nz_incapsula_challenge():
    body = FIXTURE.read_text(encoding="utf-8")
    marker = detect_challenge(body)
    assert marker is not None
    assert "Incapsula" in marker


def test_no_false_positive_on_wise_bundled_captcha_strings():
    # Actual substring pulled from wise.body.html in Round 2's sweep -- a bundled UI
    # localisation string, not a challenge served to this request.
    body = (
        '{"security.web.captcha.error.message":"Captcha verification failed to load. '
        'See ou...","security.web.captcha.not-initialized-error.message":"Captcha not '
        'initialized."}'
    )
    assert detect_challenge(body) is None


def test_no_false_positive_on_akamai_hostname():
    # Actual substring pulled from western-union.body.html -- an Akamai mPulse RUM beacon
    # hostname embedded in a real page, not a challenge.
    body = '"htyuw6dijbdli2vbigca-f-8f47f10ed-clientnsv4-s.akamaihd.net"'
    assert detect_challenge(body) is None


def test_no_false_positive_on_unrelated_js_blocked_variable():
    # Actual substring pulled from remitly.body.html -- a New Relic agent's internal state
    # variable named "blocked", nothing to do with bot management.
    body = "entIdentifier=e,this.ee=n.ee.get(e),this.featureName=t,this.blocked=!1}"
    assert detect_challenge(body) is None


def test_no_false_positive_on_ordinary_real_page():
    body = "<html><head><title>Foreign exchange rates - CommBank</title></head><body>real content</body></html>"
    assert detect_challenge(body) is None


def test_archive_bytes_round_trips_binary_content_exactly(tmp_path, monkeypatch):
    # Round 4 fix: archive_bytes() used to decode every body as UTF-8 with errors="replace",
    # which would silently corrupt a real binary payload (an .xlsx, a .pdf) on first use.
    import collect.archive as archive_mod

    monkeypatch.setattr(archive_mod, "ARCHIVE_ROOT", tmp_path)

    binary_body = bytes(range(256)) * 4  # not valid UTF-8 -- exercises the base64 path
    sha256, path = archive_bytes(
        "test-provider", "https://example.test/file.xlsx", 200, {}, binary_body,
        fetched_at=datetime(2026, 9, 10, tzinfo=timezone.utc),
    )

    recovered = read_archived_bytes(path)
    assert recovered == binary_body

    with pytest.raises(ValueError):
        read_archived_body(path)  # binary content -- read_archived_body must refuse, not mangle it


def test_archive_bytes_round_trips_text_content_exactly(tmp_path, monkeypatch):
    import collect.archive as archive_mod

    monkeypatch.setattr(archive_mod, "ARCHIVE_ROOT", tmp_path)

    text_body = "<html>café — real unicode text</html>".encode("utf-8")
    sha256, path = archive_bytes(
        "test-provider", "https://example.test/page.html", 200, {}, text_body,
        fetched_at=datetime(2026, 9, 10, tzinfo=timezone.utc),
    )

    assert read_archived_body(path) == text_body.decode("utf-8")
    assert read_archived_bytes(path) == text_body
