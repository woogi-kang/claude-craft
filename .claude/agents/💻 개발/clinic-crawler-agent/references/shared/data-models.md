# Data Models

JSON schema definitions for crawl results. Schema version: 2.0.0.

## HospitalCrawlResult

Top-level result object returned by the agent after crawling one hospital.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| schema_version | string | no | Schema version (default: "2.0.0") |
| hospital_no | int | yes | Unique hospital identifier from CSV |
| name | string | yes | Hospital name (Unicode NFC normalized) |
| url | string | yes | Crawled URL |
| final_url | string | no | Final URL after redirects (if different from url) |
| category | string | no | URL category (custom_domain, blog, etc.) |
| phone | string | no | Phone number |
| address | string | no | Address (Unicode NFC normalized) |
| status | string | yes | See Status Values below |
| cms_platform | string | no | Detected CMS (modoo, imweb, cafe24, wordpress, etc.) |
| social_channels | array | yes | List of SocialChannel objects |
| doctors | array | yes | List of DoctorInfo objects |
| errors | array | yes | List of error strings or ErrorInfo objects |

### Status Values

| Value | Meaning | Re-crawl? |
|-------|---------|-----------|
| success | All data extracted | After 7 days |
| partial | Some data missing | Immediately |
| failed | Crawl failed | Immediately |
| archived | Site permanently offline | Never |
| requires_manual | CAPTCHA/login required | Never |
| age_restricted | 19+ verification needed | Never |
| unsupported | Flash/ActiveX content | Never |

## SocialChannel

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| platform | string | yes | See Platform Enum below |
| url | string | yes | Channel URL (or phone number for Phone/SMS) |
| extraction_method | string | no | See Extraction Methods below |
| confidence | float | no | 0.0-1.0, default 1.0 |
| status | string | no | "active" (default) or "dead" |

### Platform Enum
KakaoTalk, NaverTalk, NaverBooking, Line, WeChat, WhatsApp, Telegram, FacebookMessenger, Instagram, YouTube, NaverBlog, Facebook, Phone, SMS

### Extraction Methods
dom_static, dom_dynamic, floating_element, iframe, structured_data, widget_sdk, scroll_triggered, qr_decode, deep_link, ocr, phone_text

## DoctorInfo

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Doctor name (Korean, NFC normalized, honorifics removed) |
| name_english | string | no | English name if available |
| role | string | no | Korean role: 원장, 대표원장, 부원장, 전문의, 의사, 레지던트, 인턴 |
| photo_url | string | no | Profile photo URL (img src or background-image) |
| education | array[string] | no | Education history (split from combined strings) |
| career | array[string] | no | Career history (split from combined strings) |
| credentials | array[string] | no | Certifications, memberships |
| branch | string | no | Branch name for multi-branch sites |
| branches | array[string] | no | Multiple branches if doctor works at several |
| extraction_source | string | no | "doctor_page", "main_page", "profile_page" |
| ocr_source | boolean | no | true if extracted via Gemini OCR |

## ErrorInfo

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | yes | Error category (see error-handling.md) |
| message | string | yes | Human-readable error description |
| step | string | no | Which workflow step failed |
| retryable | boolean | no | Whether this error is transient |
