# Crawl Workflow

End-to-end crawl procedure for a single hospital website.

## Step 1: Initialize

- Validate URL format (http/https)
- Prepare result structure: hospital_no, name, url, social_channels, doctors, errors

## Step 2: Navigate and Dismiss Popups

1. `browser_navigate` to hospital URL
2. `browser_snapshot` to check page state
3. If popup detected, apply dismissal strategies (see patterns/popup-dismissal.md)
4. `browser_snapshot` again to verify clean state
5. Max 3 popup dismissal attempts, then proceed regardless

## Step 3: Extract Social Channels

Three-pass strategy (see patterns/social-channels.md):

**Pass 1 - Static DOM:**
```
browser_snapshot -> scan for social platform URLs in href attributes
Check: footer, sidebar, header, floating elements
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

## Step 4: Navigate to Doctor Page

1. `browser_snapshot` to scan navigation menu
2. Match menu labels from patterns/doctor-navigation.md (primary first, then secondary)
3. If submenu parent found, click to expand, then find doctor link
4. `browser_click` on doctor menu item
5. `browser_snapshot` to verify doctor page loaded

## Step 5: Extract Doctor Information

**Option A - DOM Extraction (preferred):**
- Use content selectors from patterns/doctor-navigation.md
- Extract: name, role, photo_url, credentials, education, career

**Option B - Gemini OCR (fallback for image-based pages):**
- Trigger condition: fewer than 5 text nodes with doctor-related content
- Follow workflows/gemini-ocr.md procedure
- Mark results with `ocr_source: true`

## Step 6: Save Results

Call storage script (see workflows/storage.md):
```bash
python scripts/clinic-storage/storage_manager.py save \
  --json '<result_json>' \
  --db data/clinic-results/hospitals.db
```
