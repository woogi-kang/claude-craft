# Error Handling

Error recovery patterns for clinic crawling.

## Error Categories

### Navigation Errors

| Error | Action | Status |
|-------|--------|--------|
| Connection timeout | Record error, skip hospital | failed |
| SSL certificate error | Retry without verification, note in result | partial |
| SSL hostname mismatch | Log specific error, proceed with verification off | partial |
| DNS resolution failure | Record as dead link | failed |
| DNS slow resolution (>30s) | Mark as retryable_network_error | failed |
| HTTP 404/500 | Record error with status code | failed |
| HTTP 429 rate limit | Wait `retry-after` header or 60s, retry once | continue |
| HTTP 503 service unavailable | Retry once after 5s delay | failed |
| JavaScript-only redirect | Use browser_evaluate to follow | continue |
| Redirect to different domain | Record final_url, check chain match | continue |
| Multi-hop redirect chain (2+) | Log full chain, validate intermediate domains | continue |
| i18n redirect (wrong language) | Navigate to /ko/ or root path | continue |
| Redirect to mobile (m.domain) | Attempt desktop URL, fallback to mobile | continue |

### Browser Errors

| Error | Action |
|-------|--------|
| Browser tab/process crash | Health check via `browser_evaluate("1+1")`, mark partial if dead |
| Browser memory > 500MB | Restart browser instance, continue crawl |
| JavaScript alert/confirm/prompt | Use `browser_handle_dialog` to dismiss |
| Content-Security-Policy blocks evaluate | Wrap in try-catch, proceed with partial info |

### Anti-Bot / Access Errors

| Error | Action |
|-------|--------|
| CloudFlare challenge page | Wait 15s for auto-resolve, retry once, skip if stuck |
| CAPTCHA detected (reCAPTCHA/hCaptcha) | Mark as requires_manual, skip hospital |
| IP rate limiting (consecutive 429s) | Adaptive backoff: 2s → 5s → 60s pause |
| User-agent blocking | Retry with realistic Chrome UA string |
| Bot detection (navigator.webdriver) | Inject stealth props, proceed with partial if still blocked |
| Cookie consent wall | Auto-accept "동의" button, proceed |
| Age verification (19+) | Record as age_restricted, do not bypass |
| Session-based protection | Navigate home page first to initialize session cookie |

### SPA/CSR Errors

| Error | Action |
|-------|--------|
| Empty DOM on initial load | Wait 5000ms with browser_wait_for, re-snapshot |
| Framework detected but not hydrated | Wait additional 3000ms, re-snapshot |
| Still empty after wait | Status "partial", proceed with available content |
| Error page masquerading as content | Detect "점검", "오류", "유지보수" keywords, mark partial |

### Popup Errors

| Error | Action |
|-------|--------|
| Popup won't close after 3 attempts | Proceed with crawl, note warning |
| Popup blocks entire page | Try cookie suppression, then proceed |
| New popup appears after closing | Close up to 3 total, then proceed |
| Naver Reservation widget popup | Close parent container or click outside |
| Kakao Consultation SDK popup | Call `Kakao.Channel.hideButton()` if available |

### Extraction Errors

| Error | Action |
|-------|--------|
| No social channels found | Record empty result (not failure) |
| Social URL is dead/invalid | Mark channel with status "dead" |
| iframe-embedded social channel | Extract iframe src, record extraction_method |
| Sandboxed iframe | Read src from parent DOM instead of iframe content |
| Obfuscated links (base64/encoded) | Decode atob()/decodeURIComponent() in Pass 2 |
| No doctor page found | Check main page for doctor sections |
| Image-based doctor page | Trigger Gemini OCR workflow |
| Doctor page behind login | Detect login form/회원 text, record as requires_manual |
| Paginated doctor list | Follow pagination up to 5 pages |
| Pagination connection drop | Retry click once, save partial if fails again |
| Multi-branch site | Match branch by address, extract specific |
| Tabs/accordion doctor UI | Click each tab/section to expand before extraction |
| Slider/carousel doctors | Click next arrow to reveal all slides, extract each |
| Separate doctor profile pages | Follow each link, extract, return to list |
| Expandable "더보기" content | Click expand buttons before extraction |
| Mixed staff types | Filter by Korean role keywords (원장/전문의/의사 only) |
| AJAX navigation (URL unchanged) | Detect DOM change via snapshot diff after click |
| GTM-delayed social injection | Wait 2s extra if dataLayer detected |

### Storage Errors

| Error | Action |
|-------|--------|
| DB write failure | Retry once, then save as JSON file |
| Transaction rollback | All 4 tables rolled back atomically, retry once |
| Invalid JSON structure | Log validation error, save raw text |
| Shell escaping issue | Use --json-file instead of --json |
| Disk full | Alert user, stop crawl |
| Duplicate hospital_no | Update existing record (UPSERT) |
| Failed overwrite of success | Skip save if new status=failed with no data |
| Unicode NFC/NFD mismatch | Normalize all text to NFC before storage |
| CSV injection in export | Escape formula prefixes (=, +, -, @) |

### Gemini OCR Errors

| Error | Action |
|-------|--------|
| Gemini CLI not installed | Skip OCR, DOM-only extraction |
| Gemini timeout (>60s) | Kill process, skip OCR |
| Invalid JSON response | Retry once with simplified prompt |
| Response format variation | Try multiple JSON extraction strategies (code block, raw, regex) |
| Rate limit exceeded | Exponential backoff: 60s, 120s, 240s, then skip |
| Heap OOM on PNG | Convert to JPEG first (mandatory) |
| Project file scan slow | Use --include-directories flag |
| sips not available (non-macOS) | Fallback to PIL/Pillow or imagemagick |
| Gemini stderr lost in pipe | Capture stderr to separate file, check exit code |
| API key expiration mid-batch | Detect auth error, halt OCR for remaining hospitals |
| Long page needs scroll | Take multiple viewport screenshots, OCR each |
| Low contrast screenshot | Detect via variance check, enhance contrast before OCR |
| Partial/garbled OCR result | Validate: name >= 2 chars, no truncation markers |
| Screenshot filename collision | Use timestamp + attempt number in filename |

### Screenshot Management

| Scenario | Action |
|----------|--------|
| OCR successful + DB saved | Delete screenshots for this hospital |
| OCR failed or status partial | Keep screenshots for manual review |
| Screenshots folder > 100MB | Warn user, suggest cleanup |
| Batch interruption (Ctrl+C) | Cleanup temp files via signal handler |
| Corrupted screenshot (<1KB) | Re-take screenshot, skip OCR if still corrupt |

### Batch Operation Errors

| Error | Action |
|-------|--------|
| Batch interrupted mid-crawl | Resume from checkpoint file (batch-{id}.jsonl) |
| 5+ consecutive failures | Halt batch, report cascading failure |
| Failure rate > 30% over 10 crawls | Pause and alert user |
| Browser memory leak | Restart browser every 15 crawls or 250MB |
| No debug log for failed crawl | Write per-hospital log to crawl-logs/ directory |

## Graceful Degradation

The agent should always return a result, even if partial:
- Failed navigation -> status: "failed", empty channels/doctors
- Partial extraction -> status: "partial", whatever was found
- Full success -> status: "success", all data populated
- Permanently offline -> status: "archived", no further re-crawl

Never crash on a single hospital. Log the error and continue to next.

## Status Values

| Status | Meaning | Re-crawl? |
|--------|---------|-----------|
| success | All data extracted | After 7 days |
| partial | Some data missing | Immediately |
| failed | Crawl failed | Immediately |
| archived | Site permanently offline | Never (manual only) |
| requires_manual | CAPTCHA/login required | Never (manual only) |
| age_restricted | 19+ verification needed | Never (manual only) |
| unsupported | Flash/ActiveX content | Never (manual only) |

## Duplicate Crawl Prevention

Before starting a crawl, check the database:
- **Skip**: hospital exists with status "success" and crawled within 7 days
- **Skip**: hospital exists with status "archived", "requires_manual", or "age_restricted"
- **Re-crawl**: hospital exists with status "partial" or "failed"
- **Re-crawl**: hospital exists but crawled over 7 days ago
- **New crawl**: hospital not in database

Compare dates in UTC: `datetime.now(timezone.utc) - crawled_at < timedelta(days=7)`.

## Error Page Detection

After each major navigation, check if page is an error/maintenance page:
- Korean error keywords: "점검", "불가", "오류", "유지보수", "에러", "서비스 중단"
- If error text is > 30% of page text content, mark as partial
- Do not extract social channels or doctors from error pages

## Transient vs Permanent Failure Classification

| Transient (retry) | Permanent (no retry) |
|-------------------|---------------------|
| Connection timeout | HTTP 404 |
| HTTP 429/503 | DNS resolution failure |
| Rate limit | SSL invalid cert |
| Connection reset | Site permanently offline |
| Browser crash | CAPTCHA/login required |
