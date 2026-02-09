# Gemini CLI OCR Workflow

Use Gemini CLI to extract text from image-based doctor pages where DOM extraction fails.

## When to Use

Trigger conditions (any of):
- Doctor page has fewer than 5 text nodes containing names/credentials
- Page content is primarily rendered as images
- DOM selectors from doctor-navigation.md return no results
- Known image-heavy clinic platform detected

## Procedure

### 1. Capture Screenshot

Use Playwright to screenshot the doctor section:
```
browser_take_screenshot -> save to data/clinic-results/screenshots/hospital_{no}_doctors.png
```

If multiple doctor cards exist, screenshot each separately for better OCR accuracy.

### 2. Call Gemini CLI

```bash
gemini -p "Analyze this Korean skin clinic doctor page image.
Extract ALL doctors/medical staff with the following JSON format:
{
  \"doctors\": [
    {
      \"name\": \"Korean name\",
      \"name_english\": \"English name if shown\",
      \"role\": \"원장/전문의/etc\",
      \"credentials\": [\"list of credentials\"],
      \"education\": [\"list of education\"],
      \"career\": [\"list of career history\"]
    }
  ]
}
Return ONLY valid JSON. Extract Korean text accurately." < data/clinic-results/screenshots/hospital_{no}_doctors.png
```

### 3. Parse and Validate

- Parse JSON output from Gemini
- Validate each doctor has at least a name
- Mark all extracted doctors with `ocr_source: true`
- If Gemini returns invalid JSON, log error and skip OCR

### 4. Merge Results

- Combine OCR results with any DOM-extracted data
- De-duplicate by doctor name
- Prefer DOM data over OCR when both available

## Error Handling

- Gemini CLI not available: Skip OCR, log warning, proceed with DOM-only results
- Gemini timeout (>30s): Kill process, proceed without OCR
- Invalid JSON response: Retry once with simplified prompt, then skip
- Image too large: Resize to max 2048px width before sending
