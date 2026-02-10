# Troubleshooting Guide

Common issues and solutions for the clinic crawler agent.

## Browser Issues

### Q: Browser not responding / health check fails
**Symptom**: `browser_evaluate("1+1")` returns error or times out.
**Solution**:
1. The browser tab may have crashed. Try navigating to `about:blank` first.
2. If batch crawling, restart browser every 15 hospitals (automatic).
3. Check if browser memory exceeds 500MB (restart threshold).

### Q: Page loads but snapshot returns empty DOM
**Symptom**: `browser_snapshot` returns very few elements.
**Solution**:
1. SPA site detected. The dynamic wait (MutationObserver) should handle this automatically.
2. If still empty after 10s timeout, check if the site requires JavaScript frameworks not supported.
3. Try `browser_evaluate("document.body.innerHTML.length")` to verify content exists.

### Q: CloudFlare blocking persists after 15s wait
**Symptom**: "Checking your browser" page stays visible.
**Solution**:
1. The site has aggressive bot protection. Mark as `requires_manual`.
2. Do NOT attempt CAPTCHA bypass - mark and skip.
3. Consider adding the domain to a manual-review list.

## OCR Issues

### Q: Gemini CLI "heap out of memory" error
**Symptom**: Process crashes with OOM when processing image.
**Cause**: PNG files cause this. Gemini CLI has a known bug with PNG processing.
**Solution**: Always convert PNG to JPEG first via `sips` (macOS) or PIL fallback. This is mandatory.

### Q: Gemini CLI authentication error
**Symptom**: stderr contains "authentication" or "401" or "unauthorized".
**Solution**:
1. Run `gemini --version` to check CLI is installed.
2. Re-authenticate: `gemini auth login`
3. If mid-batch, the agent auto-switches to macOS Vision or Tesseract fallback.

### Q: OCR returns garbled/partial text
**Symptom**: Doctor names are truncated or contain jamo characters.
**Solution**:
1. Check image quality - low contrast images need enhancement (automatic in pipeline).
2. Try reducing image width to 1200px (large images may confuse OCR).
3. If Gemini fails, the agent auto-falls back to Vision/Tesseract.
4. Doctors with `ocr_confidence < 0.4` are flagged as low-confidence.

### Q: OCR rate limit exceeded
**Symptom**: "RATE_LIMITED" in output, multiple retries.
**Solution**:
1. Exponential backoff handles this automatically (60s, 120s, 240s).
2. After 4th rate limit, auto-fallback to next OCR provider.
3. For large batches, consider running during off-peak hours.

## Extraction Issues

### Q: No social channels found on a site that clearly has them
**Symptom**: `social_channels` array is empty despite visible links.
**Possible causes and solutions**:
1. **Shadow DOM**: Links inside web components. Pass 2 now includes Shadow DOM traversal.
2. **iframe**: Chat widgets in iframes. Pass 1.5 handles this.
3. **Dynamic loading**: Links loaded via JavaScript. Pass 2 + Pass 2.5 (scroll) handle this.
4. **Obfuscated**: Links encoded in base64 or onclick handlers. Pass 2 decodes these.
5. **QR code only**: WeChat links often exist only as QR images. Pass 3 uses OCR.

### Q: Doctor page not found despite existing menu
**Symptom**: Step 5 reports no doctor menu, but site has one.
**Possible causes**:
1. Non-standard menu label. Check `doctor-navigation.md` for supported labels and add new ones.
2. Menu is rendered via JavaScript after page load. AJAX detection should catch this.
3. Menu inside a hamburger/mobile menu. Try expanding mobile nav first.
4. The fallback chain now includes sitemap.xml check before main page scan.

### Q: Same doctor appears multiple times
**Symptom**: Duplicate entries in doctors array.
**Solution**: Cross-branch dedup merges by name. If still duplicating:
1. Check if name parsing splits incorrectly (e.g., "박미래 원장" → two entries).
2. Pagination may re-extract first page. The agent deduplicates by name after merge.

## Storage Issues

### Q: "Database is locked" error
**Symptom**: sqlite3.OperationalError during batch save.
**Solution**:
1. WAL mode is now enabled by default (handles concurrent access).
2. `busy_timeout=5000` gives 5 seconds of retry.
3. If multiple agents write simultaneously, this is expected and handled.

### Q: Storage script fails with "Invalid JSON"
**Symptom**: JSON parsing error when saving.
**Solution**:
1. Use `--json-file` instead of `--json` to avoid shell escaping issues.
2. Write JSON to a temp file first, then pass the file path.
3. Check for special characters in hospital names or URLs.

### Q: CSV export has garbled Korean text
**Symptom**: Korean characters display incorrectly in Excel.
**Solution**: Export uses `utf-8-sig` encoding (BOM) which Excel recognizes. If still garbled:
1. Open CSV in Excel via Data > From Text with UTF-8 encoding selected.
2. Check if the source data had encoding issues (see `encoding_error` status).

## Batch Issues

### Q: Batch stops after 5 consecutive failures
**Symptom**: Agent halts and reports "cascading failure".
**Solution**:
1. This is a safety mechanism. Check the failure pattern with `retry-queue` command.
2. Common cause: network issues or target site blocking your IP.
3. Wait 10-30 minutes, then resume from checkpoint.
4. Use `dashboard` command to see failure pattern breakdown.

### Q: How to resume an interrupted batch
**Solution**:
1. The agent writes progress to `batch-{id}.jsonl` checkpoint files.
2. Re-invoke with the same batch range - already-completed hospitals are skipped.
3. Use `dashboard` to see current progress before resuming.
