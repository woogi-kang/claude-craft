# Crawl Workflow

End-to-end crawl procedure for a single hospital website.

## Step Failure Matrix

Each step has a defined failure policy:

| Step | On Failure | Status | Continue? |
|------|-----------|--------|-----------|
| Step 0 | URL invalid or skip condition met | skipped | No |
| Step 1 | Navigation/anti-bot/error page | failed | No (Step 4-6 skipped) |
| Step 2 | Popup won't close after 3 attempts | warn | Yes (popups may block content) |
| Step 3 | SPA content never loads | partial | Yes (extract what's available) |
| Step 4 | No social channels found | ok | Yes (empty array, not failure) |
| Step 5 | No doctor menu found | ok | Yes (try sitemap, then main page fallback) |
| Step 6 | Extraction fails / OCR fails | partial | Yes (save partial results) |
| Step 7 | Storage fails | error | Return JSON result directly |

Rollback rules:
- Step 1 failure → skip all extraction, save failed status immediately
- Step 2 failure → log warning, proceed (extraction may be incomplete)
- Step 4+5 both empty → status "partial" (site accessible but no data found)
- Step 6 OCR failure → keep DOM results, mark `ocr_source: false`
- Step 7 storage failure → retry once, then return JSON to caller

## Step 0: Pre-flight Check

- Validate URL format (http/https)
- **robots.txt check**: Before any page access, check `/robots.txt`:
  ```bash
  browser_navigate to {base_url}/robots.txt
  ```
  - Parse `Disallow` directives for relevant paths (`/doctor`, `/staff`, `/about`)
  - If target paths are disallowed: mark status "robots_blocked", skip hospital
  - If `Crawl-delay` directive exists: apply delay between requests (min 1s, max 30s)
  - If robots.txt returns 404 or empty: proceed normally (no restrictions)
  - Cache robots.txt per domain (reuse for chain hospital siblings)
- **Duplicate check**: Query DB for existing hospital_no
  ```bash
  python3 -c "import sqlite3; c=sqlite3.connect('data/clinic-results/hospitals.db'); r=c.execute('SELECT status, crawled_at FROM hospitals WHERE hospital_no=?',({no},)).fetchone(); print(r)"
  ```
  - If exists with status "success" and crawled within 7 days: skip (return cached)
  - If exists with status "archived", "requires_manual", "age_restricted", "unsupported", "encoding_error", or "robots_blocked": skip
  - If exists with status "partial" or "failed": re-crawl
  - If not exists: proceed
- **Domain variant check**: Normalize domain (strip .co.kr/.kr/.com) to detect duplicate crawls of same hospital at different TLDs
- **Batch checkpoint**: If running in batch mode, check `batch-{id}.jsonl` to skip already-completed hospitals
- Prepare result structure: hospital_no, name, url, social_channels, doctors, errors

## Step 1: Navigate and Resolve

1. **Session initialization**: Navigate to home page first (ensures session cookies are set)
2. `browser_navigate` to hospital URL
3. `browser_snapshot` to check page state
4. **Browser health check**: Run `browser_evaluate("1+1")` to verify browser is responsive
5. **Redirect detection**: Use `browser_evaluate` to capture `window.location.href`
   - If final URL differs from input URL, record `final_url` in result
   - Check if redirected domain matches a known chain (see patterns/chain-hospitals.md)
   - Log full redirect chain if multi-hop (2+ redirects)
6. **Mobile redirect detection**: If URL contains `/m.`, `/mobile/`, or `m.` subdomain:
   - Attempt desktop version by removing mobile path prefix
   - If desktop has more content, use desktop version
7. **i18n detection**: Check URL path for language segments
   - If path contains `/en/`, `/ja/`, `/zh/`: navigate to Korean version (`/ko/` or root `/`)
   - Check `<html lang>` attribute: if not `ko`, look for Korean language switcher
8. **Error page detection**: Check page text for Korean error keywords
   - "점검", "불가", "오류", "유지보수" → mark as partial, do not extract
9. **Encoding detection**: Check `document.characterSet`
   - If EUC-KR or ISO-2022-KR detected, log warning (Playwright handles conversion)
   - **Garbled text detection**: After snapshot, check for encoding corruption:
     ```javascript
     const text = document.body.innerText;
     const garbledRatio = (text.match(/[?�\ufffd]/g) || []).length / Math.max(text.length, 1);
     if (garbledRatio > 0.1) return 'ENCODING_CORRUPT';
     ```
   - If garbled ratio > 10%, mark status "encoding_error" and log for manual review
   - If garbled ratio 1-10%, proceed with warning (partial corruption)
10. **CloudFlare/CAPTCHA detection**:
    - If page shows "Checking your browser" or CAPTCHA, wait 15s for auto-resolve
    - If still blocked, mark as requires_manual and skip
11. **CMS detection**: Check for platform markers (see patterns/cms-platforms section below)

## Step 2: Dismiss Popups

1. `browser_snapshot` to check for popups/modals
2. If popup detected, apply dismissal strategies (see patterns/popup-dismissal.md)
3. **Cookie consent handling**: If "쿠키 동의" or "개인정보 동의" detected, auto-accept
4. **Widget popup handling**: Check for Naver Reservation or Kakao Consultation widget overlays
5. `browser_snapshot` again to verify clean state
6. Max 3 popup dismissal attempts, then proceed regardless

## Step 3: Wait for Content (SPA Handling)

1. After popup dismissal, check if page content is loaded
2. **Unsupported content detection**: Check for Flash/ActiveX (`embed[type*="flash"]`, `object[classid*="ActiveX"]`)
   - If found, record as status "unsupported" with error message
3. **SPA detection**: If `browser_snapshot` returns minimal DOM (< 10 meaningful nodes):
   - **Dynamic wait with MutationObserver** (preferred over fixed timeout):
     ```javascript
     await new Promise((resolve) => {
       let timer;
       const observer = new MutationObserver(() => {
         clearTimeout(timer);
         timer = setTimeout(() => { observer.disconnect(); resolve('stable'); }, 2000);
       });
       observer.observe(document.body, { childList: true, subtree: true });
       // Hard timeout: 10s max wait
       setTimeout(() => { observer.disconnect(); resolve('timeout'); }, 10000);
       // Kick-start: if no mutations within 2s, resolve immediately
       timer = setTimeout(() => { observer.disconnect(); resolve('idle'); }, 2000);
     });
     ```
   - Re-take `browser_snapshot` after stabilization
   - **Framework marker check**: If still sparse, check for:
     ```javascript
     document.querySelector('#__next') || document.querySelector('#app') || document.querySelector('#root') || document.querySelector('[data-reactroot]')
     ```
   - If framework detected but content sparse, wait additional 3000ms for hydration
4. **GTM detection**: If `window.dataLayer` or `window.gtag` exists, wait additional 2000ms for GTM-injected content
5. If content still not loaded after dynamic wait, record as "partial" and proceed with available content

## Step 4: Extract Social Channels

Six-pass strategy (see patterns/social-channels.md):

**Pass 1 - Static DOM:**
```
browser_snapshot -> scan for social platform URLs in href attributes
Check: footer, sidebar, header, floating elements
Include: tel: and sms: links as Phone/SMS channels
```

**Pass 1.5 - iframe Detection:**
```
browser_evaluate -> find all iframe elements (including sandboxed)
For each iframe with src containing social platform domains:
  - Record iframe src as social channel
  - If iframe src is a chat widget, extract channel URL
  - For sandboxed iframes, read src from parent DOM
```

**Pass 1.75 - Structured Data:**
```
browser_evaluate -> parse all <script type="application/ld+json">
Extract: sameAs[] arrays, contactPoint.telephone
Also check: <meta property="og:*"> tags for social links
```

**Pass 2 - Dynamic JavaScript:**
```
browser_evaluate -> check onclick handlers, SDK scripts, JS variables
Look for: Kakao Channel SDK, chat widgets, hidden links
Decode: base64 (atob), URL-encoded links in onclick handlers
Detect: setTimeout/Promise-wrapped window.open() calls
Check widget SDK params: ChannelIO.boot(), window.tawk_chat, Crisp.chat
```

**Pass 2.5 - Scroll-triggered elements:**
```
browser_evaluate -> scroll to 50% page height, dispatch scroll event
Wait 2s for lazy-loaded floating chat buttons to appear
Re-scan for position:fixed elements not found in Pass 1
```

**Pass 3 - QR Codes (optional):**
```
Find img tags with QR-related attributes
Screenshot QR images -> Gemini CLI decode
```

**Pass 4 - URL Validation:**
For each extracted social channel URL:
- Verify URL format is valid (parseable, has scheme)
  - Accept deep link schemes: kakao://, line://, weixin://, tel:, sms:
- Remove tracking parameters (?utm_*, ?ref=*, ?fbclid=*, ?gclid=*)
- De-duplicate by normalized URL
- Filter honeypot links: skip CSS-hidden elements (display:none, opacity:0, offsetHeight:0)
- Record extraction_method for each channel
- **Korean phone format**: Extract 010-XXXX-XXXX or +82 patterns as Phone platform

## Step 5: Navigate to Doctor Page

1. `browser_snapshot` to scan navigation menu
2. Match menu labels from patterns/doctor-navigation.md (primary first, then secondary)
3. If submenu parent found, click to expand, then find doctor link
4. `browser_click` on doctor menu item
5. **AJAX-aware verification**: Check for DOM content change (not just URL change)
   - Use `browser_wait_for` with doctor-related selectors (`.doctor-card`, `.staff-item`)
   - If no URL change but DOM changed, doctor page loaded via AJAX
6. **Login wall detection**: Check for `[type="password"]`, `.login-form`, "회원"/"로그인" text
   - If login detected, record as "requires_manual" and skip extraction
7. **Age verification detection**: Check for "만 19세", "성인 인증" text
   - If found, record as "age_restricted" and skip

**Multi-branch site handling:**
- If site has branch selector/tabs (detected by address mismatch):
  - Look for branch list matching the target hospital address
  - Click the matching branch tab/link before extracting doctors
  - Match by city/district name (e.g., "하남" from "경기도 하남시")

**No doctor menu found (fallback chain):**
If no menu label matched after checking all primary/secondary/submenu labels:

1. **Sitemap fallback** (try first):
   - Navigate to `{base_url}/sitemap.xml`
   - If found, parse XML for URLs containing doctor-related segments:
     - `/doctor`, `/doctors`, `/staff`, `/team`, `/about`, `/introduce`
     - `/의료진`, `/원장`, `/전문의`
   - Navigate to the first matching URL and attempt extraction
   - Record with `extraction_source: "sitemap"`

2. **Main page fallback** (if sitemap fails or not found):
   - Go back to homepage
   - Scan main page for doctor-related content (hero section, about section)
   - If found, extract from main page with `extraction_source: "main_page"`

## Step 6: Extract Doctor Information

**Option A - DOM Extraction (preferred):**
- Use content selectors from patterns/doctor-navigation.md
- Extract: name, role, photo_url, credentials, education, career
- **Background-image photos**: Check `getComputedStyle(el).backgroundImage` if no `<img>` found
- **Credential splitting**: Split multi-item strings by `/`, `,`, `•` separators
- **Staff filtering**: Only keep 원장/대표원장/전문의/의사/부원장 roles; exclude 간호사/상담사/코디네이터
- **Name parsing**: Split "박미래 원장" into name="박미래", role="원장"

**UI Pattern Handling (before extraction):**
- **Tabs/Accordion**: Detect `[role="tab"]`, `.accordion-item`; click each to expand before extracting
- **Slider/Carousel**: Detect `.swiper`, `.carousel`, `.slider`; click next arrow until back to first slide
- **Separate profile pages**: If doctor list has links to individual pages, follow each link and extract
- **Expandable content**: Click all "더보기"/"read more" buttons to reveal hidden credentials

**Option B - Gemini OCR (fallback for image-based pages):**
- Trigger condition: fewer than 5 text nodes with doctor-related content
- **Scroll capture**: If page is longer than viewport, take multiple screenshots
- Follow workflows/gemini-ocr.md procedure
- Mark results with `ocr_source: true`

**Pagination handling:**
After extracting doctors from current page:
1. Check for pagination elements: "다음", "next", page numbers, "더보기" (load more)
2. **Infinite scroll**: If no pagination UI but `scrollHeight > innerHeight`, scroll down 5 times with 2s waits
3. If pagination found:
   - Click next page / load more button
   - **Retry on failure**: If click fails (timeout/connection drop), retry once with 5s delay
   - Wait for content update (`browser_wait_for` or snapshot diff)
   - Extract additional doctors
   - Repeat until no more pages or max 5 pages
4. Merge all pages into single doctors array
5. **Cross-branch dedup**: If same doctor name appears across branches, merge with `branches: []` array

## Step 7: Save Results

Call storage script (see workflows/storage.md):

**Preferred method** - Write JSON to temp file first to avoid shell escaping issues:
```bash
# Write result JSON to temp file (avoids shell quote escaping problems)
echo '<result_json>' > /tmp/crawl_result_{no}.json
python3 scripts/clinic-storage/storage_manager.py save \
  --json-file /tmp/crawl_result_{no}.json \
  --db data/clinic-results/hospitals.db
rm -f /tmp/crawl_result_{no}.json
```

**Alternative** - Direct JSON (only if no special characters in data):
```bash
python3 scripts/clinic-storage/storage_manager.py save \
  --json '<result_json>' \
  --db data/clinic-results/hospitals.db
```

**Always check exit code** - if storage fails, the agent should still return the JSON result.
For full error recovery patterns, see `references/shared/error-handling.md`.

**Screenshot cleanup:**
After successful save, remove temporary screenshot files:
```bash
rm -f data/clinic-results/screenshots/hospital_{no}_*.png
rm -f data/clinic-results/screenshots/hospital_{no}_*.jpg
```
Keep screenshots only if status is "partial" (for potential manual review or re-OCR).
