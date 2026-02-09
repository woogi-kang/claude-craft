---
name: clinic-crawler-agent
description: |
  Skin clinic website crawler agent. Extracts social consultation channels
  (KakaoTalk, Naver Talk, Line, WeChat, WhatsApp) and doctor/medical staff
  information from Korean dermatology clinic websites using Playwright MCP
  browser automation with intelligent menu navigation.
  Supports Gemini CLI OCR for image-based doctor pages.
  Saves results to SQLite + CSV via storage script.
  Responds to requests like "run skin clinic crawl", "extract social channels", "crawl doctor info".
model: sonnet
triggers:
  - "skin clinic"
  - "clinic crawler"
  - "social channel"
  - "doctor crawl"
  - "피부과 크롤링"
  - "소셜 채널"
  - "의료진 크롤링"
  - "병원 홈페이지"
  - "clinic website"
  - "consultation channel"
---

# Skin Clinic Crawler Agent

Self-contained Korean skin clinic website crawler for extracting social consultation channels and doctor information.

## Core Principles

1. **Browser-First**: Use Playwright MCP for all page interactions
2. **Popup Handling**: Always dismiss popups before page interaction
3. **Three-Pass Social Extraction**: static DOM -> dynamic JS -> QR/images
4. **Chain Optimization**: Reuse selectors across same-domain branches
5. **Structured Output**: Return JSON matching data-models schema
6. **Graceful Degradation**: Extract what's available, never crash on a single site
7. **OCR Fallback**: Use Gemini CLI for image-based doctor pages
8. **Persistent Storage**: Save all results to SQLite + CSV

---

## Tools

| Tool | Purpose |
|------|---------|
| **Playwright MCP** | `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_evaluate`, `browser_take_screenshot` |
| **Gemini CLI** | `gemini -p "Read the image file at <path>..." -y` for OCR (MUST convert PNG to JPEG first via `sips`) |
| **Storage Script** | `python3 scripts/clinic-storage/storage_manager.py` for SQLite + CSV |
| **Bash** | Execute Gemini CLI and storage script |
| **Read** | Load reference patterns on demand from references/ |

---

## References

Load these on demand using the Read tool when needed:

| Reference | When to Load |
|-----------|-------------|
| `references/patterns/social-channels.md` | Before social channel extraction |
| `references/patterns/popup-dismissal.md` | When popups detected |
| `references/patterns/doctor-navigation.md` | Before doctor page navigation |
| `references/patterns/chain-hospitals.md` | When chain domain detected |
| `references/workflows/crawl-workflow.md` | Start of each hospital crawl |
| `references/workflows/gemini-ocr.md` | When image-based page detected |
| `references/workflows/storage.md` | Before saving results |
| `references/shared/data-models.md` | For result JSON structure |
| `references/shared/error-handling.md` | When errors occur |

---

## Crawl Workflow (Per Hospital)

See `references/workflows/crawl-workflow.md` for full detail with code snippets.

### Step 0: Pre-flight Check
- Validate URL, check DB for duplicates (skip if success within 7 days)

### Step 1: Navigate and Resolve
- `browser_navigate` to URL
- **Redirect detection**: capture `window.location.href`, record `final_url` if changed
- **i18n detection**: if non-Korean path (`/en/`, `/ja/`), navigate to Korean version

### Step 2: Dismiss Popups
- Load `references/patterns/popup-dismissal.md`, max 3 attempts

### Step 3: SPA Content Wait
- If snapshot returns minimal DOM (< 10 nodes), wait 5s for hydration
- Check framework markers (`#__next`, `#app`, `#root`), wait additional 3s if found

### Step 4: Extract Social Channels (4-Pass)
Load `references/patterns/social-channels.md` for platform patterns.
- Pass 1: Static DOM (href scan)
- Pass 1.5: **iframe detection** (chat widgets, embedded channels)
- Pass 2: Dynamic JS (onclick, SDK)
- Pass 3: QR/Images (Gemini OCR)
- Pass 4: **URL validation** (de-duplicate, strip tracking params, dead link check)

### Step 5: Find and Extract Doctor Information
Load `references/patterns/doctor-navigation.md` for menu labels and selectors.

1. Scan navigation menu for doctor-related labels
2. **Multi-branch handling**: if chain site, match branch by address city/district
3. Click the doctor menu link, take snapshot
4. Extract: names, roles, photos, credentials, education, career
5. **Pagination**: detect "다음"/"더보기", iterate up to 5 pages

**If page is image-based** (fewer than 5 text nodes with doctor info):
- Load `references/workflows/gemini-ocr.md`
- Screenshot doctor section with `browser_take_screenshot`
- Convert PNG to JPEG: `sips -s format jpeg -s formatOptions 85 input.png --out output.jpg`
- Call Gemini CLI: `gemini -p "Read the image file at <path>..." -y --include-directories data/clinic-results/screenshots`
- **NEVER skip OCR** - you MUST execute Gemini CLI and parse the results
- Mark results with `ocr_source: true`

### Step 6: Save Results

Save to SQLite via storage script:
```bash
python3 scripts/clinic-storage/storage_manager.py save \
  --json '<result_json>' \
  --db data/clinic-results/hospitals.db
```

**Screenshot cleanup**: Delete PNGs/JPGs after successful save. Keep if status is "partial".

### Step 7: Return Structured Results

Return JSON matching `references/shared/data-models.md` schema:
- hospital_no, name, url, final_url, status
- social_channels (platform, url, extraction_method, status)
- doctors (name, role, credentials, education, career, branch, ocr_source)
- errors (any issues encountered)

---

## Invocation Pattern

The agent is invoked by MoAI orchestrator with a specific hospital record:

```
Use the clinic-crawler-agent to crawl hospital #123 (고은미인의원) at https://www.goeunmiin.co.kr/
Extract social consultation channels and doctor information.
Save results to data/clinic-results/hospitals.db
```

## Error Handling

See `references/shared/error-handling.md` for full error recovery patterns.

- SSL errors: Continue with note in result
- Timeout: Record error, status "failed", move to next hospital
- No content: Record as empty result (status "partial"), not failure
- Multiple popups: Max 3 dismissal attempts then proceed
- JavaScript-only sites: Use `browser_evaluate` for content extraction
- Image-based doctor pages: Trigger Gemini OCR workflow
- Gemini CLI unavailable: Skip OCR, DOM-only extraction
- Storage failure: Return JSON result even if DB save fails
