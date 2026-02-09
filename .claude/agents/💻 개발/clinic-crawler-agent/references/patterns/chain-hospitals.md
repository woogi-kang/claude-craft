# Chain Hospital Patterns

Known chain hospital domains with branch counts and optimization strategy.

## Known Chains

| Domain | Branches | URL Pattern | Notes |
|--------|----------|-------------|-------|
| velyb.kr | 55 | subdomain | All branches use same URL. Branch via popup or content. |
| maypure.co.kr | 41 | path | Branches via path segments |
| tonesclinic.co.kr | 23 | path | Non-standard menu names. SNS in dedicated menu. |
| hus-hu.com | 15 | subdomain | Standard layout |
| ckbclinic.com | 12 | path | Standard layout |
| izakclinic.com | 10 | path | Standard layout |
| aoziclinic.co.kr | 9 | path | Standard layout |
| lineaclinic.com | 8 | subdomain | Standard layout |
| orskin.co.kr | 7 | path | Standard layout |
| renewme.co.kr | 7 | path | Standard layout |

## URL Pattern Types

**subdomain**: Each branch has a unique subdomain (e.g., `gangnam.velyb.kr`, `sinsa.velyb.kr`)
**path**: Each branch uses a path segment (e.g., `maypure.co.kr/gangnam`, `maypure.co.kr/sinsa`)

## Optimization Strategy

1. Crawl one sample branch per chain domain
2. Record successful CSS selectors for social links and doctor pages
3. Verify selectors on 2-3 random sibling branches
4. If verification passes, apply selectors to all remaining siblings
5. If verification fails, fall back to per-hospital full crawl

## Chain Detection

A domain is considered a chain when 3+ hospitals share the same base domain.
Use `tldextract` or manual domain parsing to group hospitals by domain.
