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
| No doctor page found | Check main page for doctor sections |
| Image-based doctor page | Trigger Gemini OCR workflow |
| Doctor page behind login | Record as inaccessible |

### Storage Errors

| Error | Action |
|-------|--------|
| DB write failure | Retry once, then save as JSON file |
| Invalid JSON structure | Log validation error, save raw text |
| Disk full | Alert user, stop crawl |

### Gemini OCR Errors

| Error | Action |
|-------|--------|
| Gemini CLI not installed | Skip OCR, DOM-only extraction |
| Gemini timeout (>30s) | Kill process, skip OCR |
| Invalid JSON response | Retry once with simplified prompt |
| Rate limit exceeded | Wait 60s, retry once |

## Graceful Degradation

The agent should always return a result, even if partial:
- Failed navigation -> status: "failed", empty channels/doctors
- Partial extraction -> status: "partial", whatever was found
- Full success -> status: "success", all data populated

Never crash on a single hospital. Log the error and continue to next.
