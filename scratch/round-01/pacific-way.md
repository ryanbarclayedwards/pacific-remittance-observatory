# Pacific Way Money Transfer — evidence

Date checked: 2026-09-09
Domain: pacificwaymoneytransfer.com

## URLs attempted
- https://www.pacificwaymoneytransfer.com/robots.txt — FAILED
- https://pacificwaymoneytransfer.com/robots.txt — FAILED

## Anomaly (verbatim tool error)
```
Hostname/IP does not match certificate's altnames: Host: www.pacificwaymoneytransfer.com. is not in the cert's altnames: DNS:cpanel.pacificwaymoneytransfer.com, DNS:mail.pacificwaymoneytransfer.com, DNS:webdisk.pacificwaymoneytransfer.com, DNS:webmail.pacificwaymoneytransfer.com
```
Same error (with altnames list identical) on the bare domain without `www`. The TLS certificate installed on the server covers only cPanel/mail/webdisk/webmail subdomains — not the apex or `www` hostname visitors would actually use. This is a real server misconfiguration, not a WebFetch quirk: a standards-compliant HTTPS client cannot validate this host at all.

No attempt was made to bypass certificate validation — that would be circumventing a security control, which is out of scope regardless of collection tier.

## Background only (from search snippets, NOT independently verified — no page was successfully fetched)
Search results reference `pacificwaymoneytransfer.com/send-money/` and `pacificwaymoneytransfer.com/locations/`, describing an AU+NZ → Samoa cash-pickup/bank-deposit service, agent network Brisbane/Sydney/Melbourne + NZ outlets. This is second-hand and unverified; treat as a hypothesis only.

## Tier assessment
Tier 3 — unreachable via a certificate-validating client. Cannot determine FX table, fee schedule, calculator, robots.txt, or account requirements because no page could be safely fetched. This is a distinct failure mode from a bot wall or CAPTCHA: the provider's own infrastructure is broken for ordinary secure browsing, not merely for automation.
