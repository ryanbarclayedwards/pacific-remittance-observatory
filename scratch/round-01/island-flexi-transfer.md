# Island Flexi Transfer — evidence

Date checked: 2026-09-09

## Site
https://www.islandflexi.com/ — small Melbourne, Victoria-based operator serving the Tongan community (ABN 54786462424 stated on-site).

## robots.txt
`https://www.islandflexi.com/robots.txt` → HTTP 404 Not Found. No robots.txt present.

## Homepage — WebFetch summary
- Serves AU→Tonga (destination not explicit on the fetched homepage text itself, but consistent with all third-party listings found — sendmoneypacific.org, World Bank RPW node, SaverPacific — which all describe it as an AU–Tonga operator).
- No FX rate table.
- No fee schedule.
- No calculator of any kind.
- The entire "send money" mechanism is: click a button labelled "CLICK HERE TO SEND MONEY" which links to a **Google Form** (`https://docs.google.com/forms/d/e/1FAIpQLSfDxEzRpc5tgg0sB7ju0y84c-tk2pbBXAeKhVj3zXaPMxJWOg/viewform`), then pay by bank deposit (Osko / BSB+account) to the operator's own account.

## Tier assessment
**Tier 3 — no public quote surface of any kind.** There is nothing to reconstruct arithmetically (no FX table, no fee schedule) and nothing to query as a calculator (a Google Form intake is not a quote mechanism — it collects a request, it doesn't return a price). This is as clear a Tier 3 case as the batch produced.

## Confidence flags
- Destination (Tonga) inferred from third-party listings (sendmoneypacific.org, World Bank RPW, SaverPacific), not stated in the fetched homepage text itself. Recommend treating "Tonga" as high-confidence but not first-party-confirmed from today's fetch alone.
- Did not fetch the Google Form itself (out of scope — it is not a data source and entering it risks looking like a real transaction attempt).
