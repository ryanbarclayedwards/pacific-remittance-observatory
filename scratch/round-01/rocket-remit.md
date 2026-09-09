# Rocket Remit — evidence

Date checked: 2026-09-09
Domain: rocketremit.com

## URLs fetched
- https://www.rocketremit.com/robots.txt
- https://www.rocketremit.com/send_money_to_pacific_islands_australia/
- https://www.rocketremit.com/country/transfer_money_png/
- https://www.rocketremit.com/

## robots.txt (verbatim, Yoast block)
```
User-agent: *
Disallow:

Sitemap: https://www.rocketremit.com/sitemap_index.xml
```
Permits all crawling.

## Findings
- AU origin confirmed: "transfer your money from Australia to Cook Islands, Fiji, Samoa, Tonga or Vanuatu." NZ origin also referenced elsewhere (mHITs press releases; not independently re-verified this session).
- Destinations from AU page: Cook Islands, Fiji, Samoa, Tonga, Vanuatu. A separate country page confirms PNG (bank deposit at ANZ/WBC/BSP/Kina Bank), and other sources (mHITs press releases, not fetched this session) mention Solomon Islands.
- No public FX rate table or fee schedule found on any checked page. PNG page states only a vague range: "fees typically ranging from AUD 0–5 depending on the destination and delivery method."
- No quote calculator accessible without an account. Homepage has a "Get Rate" call-to-action but the surrounding text and FAQ ("Before confirming your transfer, you will always see the exchange rate, transfer fee, and total amount your recipient will receive") indicate this happens only inside the signup/login flow, not before it. Homepage explicitly pushes "Sign up" / "Login" as the entry point.
- No CAPTCHA encountered on the pages checked (none of them require interaction to view).

## Tier assessment
Tier 3 — the actual quote (rate + fee) is gated behind account creation. No public tariff table and no public pre-login calculator were found despite checking the homepage and two destination-specific pages. This could be wrong if a calculator exists elsewhere on the site that wasn't found — flagged as a confidence gap below.

## Confidence flag
Did not exhaustively crawl the site (courtesy constraint) — a pre-login quote widget could exist on a page not checked (e.g. behind the "Get Rate" button, which was not clicked because content wasn't available to inspect what it does without a live browser session; the Chrome browser tool was unavailable this session — extension not connected). Worth a follow-up check with a working browser session before finalising Tier 3 for this provider.
