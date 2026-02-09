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
2. **Popup Handling**: Always dismiss popups (including cookie consent, widget overlays) before interaction
3. **Six-Pass Social Extraction**: static DOM -> iframe -> structured data -> dynamic JS -> scroll -> QR/images -> validation
4. **Chain Optimization**: Reuse selectors across same-domain branches
5. **Structured Output**: Return JSON matching data-models schema v2.0.0
6. **Graceful Degradation**: Extract what's available, never crash on a single site
7. **OCR Fallback**: Use Gemini CLI for image-based doctor pages (cross-platform conversion)
8. **Persistent Storage**: Atomic transactions to SQLite + CSV-safe export
9. **Anti-Bot Awareness**: Detect CloudFlare/CAPTCHA/rate limits, handle ethically
10. **Batch Resilience**: Checkpoint progress, monitor failure rate, handle interruptions

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
- Skip if status is "archived", "requires_manual", "age_restricted", or "unsupported"
- Domain variant check (normalize .co.kr/.kr/.com)
- Batch checkpoint check (skip if already in batch state file)

### Step 1: Navigate and Resolve
- `browser_navigate` to URL (home page first for session init)
- **Redirect detection**: capture `window.location.href`, record `final_url` if changed
- **Mobile redirect**: if m.domain.com detected, attempt desktop version
- **i18n detection**: if non-Korean path (`/en/`, `/ja/`), navigate to Korean version
- **Error page detection**: check for "점검"/"오류" keywords, mark partial
- **Anti-bot detection**: CloudFlare challenge (wait 15s), CAPTCHA (mark requires_manual)
- **CMS detection**: identify modoo/imweb/cafe24/wordpress platforms
- **Encoding check**: detect EUC-KR, log warning

### Step 2: Dismiss Popups
- Load `references/patterns/popup-dismissal.md`, max 3 attempts
- **Cookie consent**: auto-accept "동의" buttons
- **Widget overlays**: handle Naver Reservation / Kakao Consultation popups

### Step 3: SPA Content Wait
- Check for Flash/ActiveX (mark as "unsupported" if found)
- If snapshot returns minimal DOM (< 10 nodes), wait 5s for hydration
- Check framework markers (`#__next`, `#app`, `#root`), wait additional 3s if found
- **GTM wait**: if `dataLayer` detected, wait extra 2s for injected content

### Step 4: Extract Social Channels (6-Pass)
Load `references/patterns/social-channels.md` for platform patterns.
- Pass 1: Static DOM (href scan, including tel:/sms: links)
- Pass 1.5: **iframe detection** (chat widgets, sandboxed iframes)
- Pass 1.75: **Structured data** (JSON-LD sameAs[], meta tags)
- Pass 2: Dynamic JS (onclick, SDK, **decode base64/URL encoding**)
- Pass 2.5: **Scroll-triggered** floating widgets
- Pass 3: QR/Images (Gemini OCR)
- Pass 4: **URL validation** (de-duplicate, strip tracking params, honeypot filter, dead link check, Korean phone extraction)

### Step 5: Find and Extract Doctor Information
Load `references/patterns/doctor-navigation.md` for menu labels and selectors.

1. Scan navigation menu for doctor-related labels
2. **Login/age gate check**: detect login forms or 19+ verification, skip if found
3. **Multi-branch handling**: if chain site, match branch by address city/district
4. Click the doctor menu link, **detect AJAX navigation** (DOM change without URL change)
5. **UI pattern handling**: expand tabs/accordions, navigate carousel slides, follow profile links
6. Extract: names (parse honorifics), roles (filter non-doctors), photos (including background-image), credentials (split combined strings), education, career
7. **Expandable content**: click "더보기" buttons before extraction
8. **Pagination**: detect "다음"/"더보기"/infinite scroll, iterate up to 5 pages with retry on failure
9. **Fallback**: if no doctor menu found, scan main page

**If page is image-based** (fewer than 5 text nodes with doctor info):
- Load `references/workflows/gemini-ocr.md`
- **Scroll capture**: if page exceeds viewport, take multiple screenshots
- Screenshot doctor section with `browser_take_screenshot` (unique filename with timestamp)
- Convert PNG to JPEG: `sips` (macOS) or PIL/imagemagick (cross-platform fallback)
- **Low contrast check**: enhance if needed before OCR
- Call Gemini CLI with **stderr capture**: check exit code and auth errors
- **Multi-strategy JSON parse**: try code block → raw JSON → regex extraction
- **Validate OCR results**: name >= 2 chars, no truncation
- **NEVER skip OCR when Gemini CLI is available** - you MUST execute it and parse the results. Skip only if CLI is not installed.
- Mark results with `ocr_source: true`

### Step 6: Save Results

Save to SQLite via storage script (**use --json-file to avoid shell escaping issues**):
```bash
echo '<result_json>' > /tmp/crawl_result_{no}.json
python3 scripts/clinic-storage/storage_manager.py save \
  --json-file /tmp/crawl_result_{no}.json \
  --db data/clinic-results/hospitals.db
rm -f /tmp/crawl_result_{no}.json
```

**Always check exit code** - if storage fails, return JSON result directly.
**Screenshot cleanup**: Delete PNGs/JPGs after successful save. Keep if status is "partial".
**Batch progress**: Write completion status to batch checkpoint file.

### Step 7: Return Structured Results

Return JSON matching `references/shared/data-models.md` schema v2.0.0:
- schema_version, hospital_no, name, url, final_url, status, cms_platform
- social_channels (platform, url, extraction_method, confidence, status)
- doctors (name, role, credentials, education, career, branch, branches, extraction_source, ocr_source)
- errors (type, message, step, retryable)

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

**Navigation/Access:**
- SSL errors: Continue with note in result
- Timeout: Record error, status "failed", classify transient vs permanent
- CloudFlare challenge: Wait 15s for auto-resolve, mark requires_manual if stuck
- CAPTCHA: Mark as requires_manual, do not attempt bypass
- Rate limiting (429): Adaptive backoff (2s → 5s → 60s pause)
- Age verification: Mark as age_restricted, skip ethically
- Login wall: Record as inaccessible, skip extraction

**Content:**
- No content / error page: Detect "점검"/"오류" keywords, mark "partial"
- Flash/ActiveX: Mark as "unsupported"
- Multiple popups: Max 3 dismissal attempts then proceed
- Cookie consent: Auto-accept "동의" button
- JavaScript-only sites: Use `browser_evaluate` for content extraction

**Extraction:**
- Image-based doctor pages: Trigger Gemini OCR workflow (cross-platform)
- Tabs/accordion/carousel: Expand all UI elements before extraction
- AJAX navigation: Detect DOM change without URL change
- Mixed staff: Filter by Korean role keywords
- Expandable content: Click "더보기" before extraction

**OCR:**
- Gemini CLI unavailable: Skip OCR, DOM-only extraction
- Rate limit: Exponential backoff (60s, 120s, 240s)
- API key expired: Halt OCR for batch, continue DOM-only
- Response format variation: Multi-strategy JSON extraction
- Low contrast: Enhance image before OCR
- Long pages: Multiple screenshots with scroll

**Storage:**
- Storage failure: Return JSON result even if DB save fails
- Shell escaping: Use --json-file instead of --json
- Failed overwrite: Don't overwrite success with empty failed result
- Transaction error: Atomic rollback, retry once

**Batch:**
- Batch interruption: Resume from checkpoint file
- 5+ consecutive failures: Halt batch, alert user
- Browser memory leak: Restart every 15 crawls
