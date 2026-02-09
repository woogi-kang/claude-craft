# Data Models

JSON schema definitions for crawl results.

## HospitalCrawlResult

Top-level result object returned by the agent after crawling one hospital.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| hospital_no | int | yes | Unique hospital identifier from CSV |
| name | string | yes | Hospital name |
| url | string | yes | Crawled URL |
| category | string | no | URL category (custom_domain, blog, etc.) |
| phone | string | no | Phone number |
| address | string | no | Address |
| status | string | yes | "success", "partial", "failed" |
| social_channels | array | yes | List of SocialChannel objects |
| doctors | array | yes | List of DoctorInfo objects |
| errors | array | yes | List of error strings |

## SocialChannel

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| platform | string | yes | KakaoTalk, NaverTalk, Line, WeChat, WhatsApp, Telegram, FacebookMessenger, Instagram, YouTube, NaverBlog, Facebook |
| url | string | yes | Channel URL |
| extraction_method | string | no | dom_static, dom_dynamic, floating_element, qr_decode, widget_sdk |
| confidence | float | no | 0.0-1.0, default 1.0 |

## DoctorInfo

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | yes | Doctor name (Korean) |
| name_english | string | no | English name if available |
| role | string | no | director, specialist, resident, nurse, staff |
| photo_url | string | no | Profile photo URL |
| education | array[string] | no | Education history |
| career | array[string] | no | Career history |
| credentials | array[string] | no | Certifications, memberships |
| ocr_source | boolean | no | true if extracted via Gemini OCR |
