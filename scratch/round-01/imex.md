# IMEX Money Transfer — evidence

Date checked: 2026-09-09

## Site
https://imexpacificmoney.com/ (head office Logan Central, Queensland, per WebSearch snippet from an unrelated Remitly listing page — background only).

## robots.txt
`https://imexpacificmoney.com/robots.txt` → HTTP 200. Yoast SEO default block:
```
User-agent: *
Disallow:
Sitemap: https://imexpacificmoney.com/sitemap_index.xml
```
Empty Disallow under `User-agent: *` — permits crawling generally, no path-specific restriction found.

## Homepage — WebFetch summary
- Serves **New Zealand → Samoa and Tonga only**, per the content fetched. No mention of Australia origin on the homepage itself (a Remitly partner-listing page found via WebSearch separately mentions an Australian phone number for "Rowena Financial Services/IMEX Money Transfer," which is a third-party page, not IMEX's own site — flagged, not relied on).
- No dedicated FX rate page. Homepage shows "1 NZD = – –" with what the fetch described as a loading placeholder — consistent with a JS-rendered rate that a static fetch cannot evaluate. Not confirmed either way whether it resolves to a real number for an anonymous visitor.
- Flat fee disclosed in prose: "$8 NZD" transaction fee (also stated in Terms & Conditions at `https://imexpacificmoney.com/terms-conditions/`, confirmed by a second WebSearch listing). No tiered fee schedule document found.
- No calculator page found in navigation/content besides the homepage widget described above.
- Account required: registration + photo ID + proof of address required to send, per fetched content.
- Login: `https://app.imexpacificmoney.com/login`; Sign-up: `https://app.imexpacificmoney.com/signup`.

## Tier assessment
**Tier 3 (leaning; see confidence flag) — no confirmed public FX table or fee schedule document, account required to transact.** The flat $8 NZD fee is publicly disclosed in prose (arguably a minimal fee schedule), but there is no public FX rate table to reconstruct a quote arithmetically, so it does not qualify as Tier 1. It does not clearly have a working public calculator either, so not Tier 2 on current evidence.

## Confidence flags
- Whether the homepage rate widget ("1 NZD = – –") resolves to a real number without login was not confirmed — static fetch cannot execute JS. This is the swing fact between Tier 2 and Tier 3; recommend a follow-up check with a JS-capable tool before this is treated as settled.
- Australia-origin claim is unconfirmed on IMEX's own site; the only AU reference found was on a third-party (Remitly) page.
- IMEX's registered business name variants ("Rowena Financial Services") not reconciled here.
