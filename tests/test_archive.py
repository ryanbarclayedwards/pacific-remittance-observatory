"""Golden tests for challenge-page detection (Round 3, reports/03-endpoints.md).

Positive case runs against the real Incapsula challenge page ANZ NZ served in Round 2
(tests/fixtures/challenge-pages/incapsula-anz-nz.html) -- not a synthetic example. Negative
cases guard against the specific false positives Round 2's sweep actually produced: Wise's own
bundled "Captcha" error-message strings, Western Union's Akamai *hostname* (not a challenge),
and Remitly's unrelated `this.blocked` JS variable.
"""
from pathlib import Path

from collect.archive import detect_challenge

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
