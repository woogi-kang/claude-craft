---
name: moai-clinic-chain
description: >
  Chain hospital optimization patterns for skin clinic crawl pipeline.
  Covers domain grouping, selector reuse strategy, branch URL patterns
  (subdomain vs path-based), and known chain hospital registry.
  Use when optimizing crawl for chain hospitals sharing the same domain.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Read Grep Glob Bash
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-02-06"
  modularized: "false"
  tags: "clinic, chain, hospital, optimization, selector, reuse, domain"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 3000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "chain hospital"
    - "chain domain"
    - "selector reuse"
    - "branch"
    - "franchise"
    - "체인"
    - "프랜차이즈"
  agents:
    - "clinic-crawler-agent"
  phases:
    - "run"
---

# Chain Hospital Optimization

## Concept

~697 hospitals across ~40 domains share the same website template. Instead of individually crawling each, we:

1. Crawl ONE sample branch per chain domain
2. Record CSS selectors that successfully extracted data
3. Verify selectors on 2-3 random siblings
4. If verification passes, apply to ALL remaining siblings
5. If verification fails, fall back to per-hospital crawl

This reduces ~697 crawls to ~40 initial + ~120 verification = ~160 total.

## Known Chains

| Domain | Branches | URL Pattern | Notes |
|--------|----------|-------------|-------|
| velyb.kr | 55 | subdomain | Same URL for all branches, content varies |
| maypure.co.kr | 41 | path | Branch name in URL path |
| tonesclinic.co.kr | 23 | path | Non-standard menu names |
| hus-hu.com | 15 | subdomain | - |
| ckbclinic.com | 12 | path | - |
| izakclinic.com | 10 | path | - |
| aoziclinic.co.kr | 9 | path | - |
| lineaclinic.com | 8 | subdomain | - |
| orskin.co.kr | 7 | path | - |
| renewme.co.kr | 7 | path | - |

## URL Patterns

**Subdomain pattern**: Each branch has its own subdomain
- gangnam.velyb.kr, sinsa.velyb.kr

**Path pattern**: Branches differentiated by URL path
- maypure.co.kr/gangnam, maypure.co.kr/sinsa

## Selector Storage

After successful crawl, store in chain_patterns table:
```json
{
  "social": {
    "footer_social": "footer .social-links a",
    "floating_kakao": ".floating-btn .kakao"
  },
  "doctor": {
    "menu_selector": "nav a:contains('의료진')",
    "doctor_card": ".doctor-card",
    "name_selector": ".doctor-card .name",
    "photo_selector": ".doctor-card img"
  },
  "popup": {
    "close_selector": ".popup .close-btn"
  }
}
```

## Verification Strategy

Before applying to all siblings:
1. Pick 2-3 random sibling branches
2. Apply saved selectors
3. Check if social links and doctor count are non-zero
4. If >66% siblings succeed, mark chain as verified
5. Record verified_count in chain_patterns table

## Special Cases

### velyb.kr (55 branches)
All branches use the SAME URL. The branch is selected via a popup or internal navigation. Need special handling to select the correct branch before extracting data.

### tonesclinic.co.kr (23 branches)
Uses non-standard menu labels. "SNS" instead of typical social-related labels. Doctor page under unconventional menu hierarchy.

## Reference

See: clinic-crawl/patterns/chain_hospitals.json
See: clinic-crawl/clinic_crawl/storage.py (chain_patterns table)
