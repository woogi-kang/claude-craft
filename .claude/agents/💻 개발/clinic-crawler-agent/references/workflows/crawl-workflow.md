# Crawl Workflow

End-to-end crawl procedure for a single hospital website.

## Step 0: Pre-flight Check

- Validate URL format (http/https)
- **Duplicate check**: Query DB for existing hospital_no
  ```bash
  python3 -c "import sqlite3; c=sqlite3.connect('data/clinic-results/hospitals.db'); r=c.execute('SELECT status, crawled_at FROM hospitals WHERE hospital_no=?',({no},)).fetchone(); print(r)"
  ```
  - If exists with status "success" and crawled within 7 days: skip (return cached)
  - If exists with status "partial" or "failed": re-crawl
  - If not exists: proceed
- Prepare result structure: hospital_no, name, url, social_channels, doctors, errors

## Step 1: Navigate and Resolve

1. `browser_navigate` to hospital URL
2. `browser_snapshot` to check page state
3. **Redirect detection**: Use `browser_evaluate` to capture `window.location.href`
   - If final URL differs from input URL, record `final_url` in result
   - Check if redirected domain matches a known chain (see patterns/chain-hospitals.md)
4. **i18n detection**: Check URL path for language segments
   - If path contains `/en/`, `/ja/`, `/zh/`: navigate to Korean version (`/ko/` or root `/`)
   - Check `<html lang>` attribute: if not `ko`, look for Korean language switcher

## Step 2: Dismiss Popups

1. `browser_snapshot` to check for popups/modals
2. If popup detected, apply dismissal strategies (see patterns/popup-dismissal.md)
3. `browser_snapshot` again to verify clean state
4. Max 3 popup dismissal attempts, then proceed regardless

## Step 3: Wait for Content (SPA Handling)

1. After popup dismissal, check if page content is loaded
2. **SPA detection**: If `browser_snapshot` returns minimal DOM (< 10 meaningful nodes):
   - Use `browser_wait_for` with selector `body *` and timeout 5000ms
   - Re-take `browser_snapshot`
   - If still empty after wait, use `browser_evaluate` to check for framework markers:
     ```javascript
     document.querySelector('#__next') || document.querySelector('#app') || document.querySelector('#root')
     ```
   - Wait additional 3000ms for hydration, then re-snapshot
3. If content still not loaded, record as "partial" and proceed with available content

## Step 4: Extract Social Channels

Three-pass strategy (see patterns/social-channels.md):

**Pass 1 - Static DOM:**
```
browser_snapshot -> scan for social platform URLs in href attributes
Check: footer, sidebar, header, floating elements
```

**Pass 1.5 - iframe Detection:**
```
browser_evaluate -> find all iframe elements
For each iframe with src containing social platform domains:
  - Record iframe src as social channel
  - If iframe src is a chat widget, extract channel URL
```

**Pass 2 - Dynamic JavaScript:**
```
browser_evaluate -> check onclick handlers, SDK scripts, JS variables
Look for: Kakao Channel SDK, chat widgets, hidden links
```

**Pass 3 - QR Codes (optional):**
```
Find img tags with QR-related attributes
Screenshot QR images -> Gemini CLI decode
```

**Pass 4 - URL Validation:**
For each extracted social channel URL:
- Verify URL format is valid (parseable, has scheme)
- Remove tracking parameters (?utm_*, ?ref=*, etc.)
- De-duplicate by normalized URL
- Record extraction_method for each channel

## Step 5: Navigate to Doctor Page

1. `browser_snapshot` to scan navigation menu
2. Match menu labels from patterns/doctor-navigation.md (primary first, then secondary)
3. If submenu parent found, click to expand, then find doctor link
4. `browser_click` on doctor menu item
5. `browser_snapshot` to verify doctor page loaded

**Multi-branch site handling:**
- If site has branch selector/tabs (detected by address mismatch):
  - Look for branch list matching the target hospital address
  - Click the matching branch tab/link before extracting doctors
  - Match by city/district name (e.g., "하남" from "경기도 하남시")

## Step 6: Extract Doctor Information

**Option A - DOM Extraction (preferred):**
- Use content selectors from patterns/doctor-navigation.md
- Extract: name, role, photo_url, credentials, education, career

**Option B - Gemini OCR (fallback for image-based pages):**
- Trigger condition: fewer than 5 text nodes with doctor-related content
- Follow workflows/gemini-ocr.md procedure
- Mark results with `ocr_source: true`

**Pagination handling:**
After extracting doctors from current page:
1. Check for pagination elements: "다음", "next", page numbers, "더보기" (load more)
2. If pagination found:
   - Click next page / load more button
   - Wait for content update (`browser_wait_for` or snapshot diff)
   - Extract additional doctors
   - Repeat until no more pages or max 5 pages
3. Merge all pages into single doctors array

## Step 7: Save Results

Call storage script (see workflows/storage.md):
```bash
python3 scripts/clinic-storage/storage_manager.py save \
  --json '<result_json>' \
  --db data/clinic-results/hospitals.db
```

**Screenshot cleanup:**
After successful save, remove temporary screenshot files:
```bash
rm -f data/clinic-results/screenshots/hospital_{no}_*.png
rm -f data/clinic-results/screenshots/hospital_{no}_*.jpg
```
Keep screenshots only if status is "partial" (for potential manual review or re-OCR).
