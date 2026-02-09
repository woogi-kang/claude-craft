# Error Handling

Error recovery patterns for clinic crawling.

## Error Categories

### Navigation Errors

| Error | Action | Status |
|-------|--------|--------|
| Connection timeout | Record error, skip hospital | failed |
| SSL certificate error | Retry without verification, note in result | partial |
| DNS resolution failure | Record as dead link | failed |
| HTTP 404/500 | Record error with status code | failed |
| JavaScript-only redirect | Use browser_evaluate to follow | continue |
| Redirect to different domain | Record final_url, check chain match | continue |
| i18n redirect (wrong language) | Navigate to /ko/ or root path | continue |

### SPA/CSR Errors

| Error | Action |
|-------|--------|
| Empty DOM on initial load | Wait 5000ms with browser_wait_for, re-snapshot |
| Framework detected but not hydrated | Wait additional 3000ms, re-snapshot |
| Still empty after wait | Status "partial", proceed with available content |

### Popup Errors

| Error | Action |
|-------|--------|
| Popup won't close after 3 attempts | Proceed with crawl, note warning |
| Popup blocks entire page | Try cookie suppression, then proceed |
| New popup appears after closing | Close up to 3 total, then proceed |

### Extraction Errors

| Error | Action |
|-------|--------|
| No social channels found | Record empty result (not failure) |
| Social URL is dead/invalid | Mark channel with status "dead" |
| iframe-embedded social channel | Extract iframe src, record extraction_method |
| No doctor page found | Check main page for doctor sections |
| Image-based doctor page | Trigger Gemini OCR workflow |
| Doctor page behind login | Record as inaccessible |
| Paginated doctor list | Follow pagination up to 5 pages |
| Multi-branch site | Match branch by address, extract specific |

### Storage Errors

| Error | Action |
|-------|--------|
| DB write failure | Retry once, then save as JSON file |
| Invalid JSON structure | Log validation error, save raw text |
| Disk full | Alert user, stop crawl |
| Duplicate hospital_no | Update existing record (UPSERT) |

### Gemini OCR Errors

| Error | Action |
|-------|--------|
| Gemini CLI not installed | Skip OCR, DOM-only extraction |
| Gemini timeout (>60s) | Kill process, skip OCR |
| Invalid JSON response | Retry once with simplified prompt |
| Rate limit exceeded | Wait 60s, retry once |
| Heap OOM on PNG | Convert to JPEG first (mandatory) |
| Project file scan slow | Use --include-directories flag |

### Screenshot Management

| Scenario | Action |
|----------|--------|
| OCR successful + DB saved | Delete screenshots for this hospital |
| OCR failed or status partial | Keep screenshots for manual review |
| Screenshots folder > 100MB | Warn user, suggest cleanup |

## Graceful Degradation

The agent should always return a result, even if partial:
- Failed navigation -> status: "failed", empty channels/doctors
- Partial extraction -> status: "partial", whatever was found
- Full success -> status: "success", all data populated

Never crash on a single hospital. Log the error and continue to next.

## Duplicate Crawl Prevention

Before starting a crawl, check the database:
- **Skip**: hospital exists with status "success" and crawled within 7 days
- **Re-crawl**: hospital exists with status "partial" or "failed"
- **Re-crawl**: hospital exists but crawled over 7 days ago
- **New crawl**: hospital not in database

This prevents wasting time re-crawling recently successful hospitals while allowing retry of failures.
