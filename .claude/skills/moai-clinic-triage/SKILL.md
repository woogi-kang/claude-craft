---
name: moai-clinic-triage
description: >
  URL classification rules for skin clinic crawl pipeline. Covers category
  detection (custom domain, blog, social platform, builder), chain hospital
  identification by shared domain analysis, and platform detection signatures.
  Use when classifying hospital URLs, identifying chain hospitals, or
  detecting website platforms.
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
  tags: "clinic, triage, classification, chain, platform, url"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 3000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "triage"
    - "classify"
    - "chain hospital"
    - "url category"
    - "platform detect"
  agents:
    - "clinic-crawler-agent"
  phases:
    - "plan"
    - "run"
---

# Clinic URL Triage

## Categories

- **custom_domain**: Hospital's own website (e.g., goeunmiin.co.kr)
- **blog_naver**: Naver blog as homepage (blog.naver.com/*)
- **kakao_channel**: Kakao channel page (pf.kakao.com/*)
- **instagram**: Instagram profile as homepage
- **youtube**: YouTube channel as homepage
- **imweb**: imweb.me builder-hosted sites
- **mobidoc**: mobidoc.co.kr medical site builder
- **google_sites**: Google Sites hosted
- **no_url**: No URL available in CSV
- **dead_link**: URL returns error/timeout
- **invalid_url**: Malformed or garbage URL value

## Chain Detection

Hospitals sharing the same registered domain (via tldextract) with 3+ branches are classified as chains.

Known major chains:
- velyb.kr (55 branches) - All share same URL, differentiated by content
- maypure.co.kr (41) - Path-based branch differentiation
- tonesclinic.co.kr (23) - Path-based, non-standard menu labels
- hus-hu.com (15), ckbclinic.com (12), izakclinic.com (10)

## Platform Detection

Check HTML content and server headers for:
- imweb: "imweb" in HTML or server header
- mobidoc: "mobidoc" in HTML
- wordpress: "wp-content" or "wordpress" in HTML
- nextjs: "_next" or "__next" in HTML
- wix: "wixsite" in HTML

## Data Quality Issues

Watch for these CSV edge cases:
- URL value is "ㅇ", "-", or empty string
- URL is "http://" with no domain
- Duplicate URLs across homepage and naver_website columns
- URLs without protocol prefix (need https:// prepend)
- 62 no-protocol URLs in the dataset
