# Gemini CLI OCR Workflow

Use Gemini CLI to extract text from image-based doctor pages where DOM extraction fails.

**THIS STEP IS MANDATORY** when image-based content is detected. Do NOT skip OCR and report "OCR needed" - you MUST execute Gemini CLI and return the extracted data.

## When to Use

Trigger conditions (any of):
- Doctor page has fewer than 5 text nodes containing names/credentials
- Page content is primarily rendered as images
- DOM selectors from doctor-navigation.md return no results
- Known image-heavy clinic platform detected
- Social channel info (e.g., KakaoTalk ID) only visible in images

## Procedure

### 1. Capture Screenshot

Use Playwright to screenshot the doctor section:
```
browser_take_screenshot -> save to data/clinic-results/screenshots/hospital_{no}_doctors.png
```

If multiple doctor cards exist, screenshot each separately for better OCR accuracy.

### 2. Convert to JPEG

**CRITICAL**: Gemini CLI crashes with heap out of memory on PNG files. Always convert to JPEG first:

```bash
sips -s format jpeg -s formatOptions 85 data/clinic-results/screenshots/hospital_{no}_doctors.png --out data/clinic-results/screenshots/hospital_{no}_doctors.jpg
```

Target: under 500KB file size. If still too large, reduce width:
```bash
sips --resampleWidth 1024 -s format jpeg -s formatOptions 85 input.png --out output.jpg
```

### 3. Call Gemini CLI

**IMPORTANT**: Do NOT use stdin (`< image.jpg`). Instead, reference the file path in the prompt and use `-y` flag for auto-approval:

```bash
gemini -p "Read the image file at data/clinic-results/screenshots/hospital_{no}_doctors.jpg and extract all Korean text about doctors/medical staff. Return ONLY valid JSON:
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
}" -y 2>&1 | grep -A 200 '```'
```

Key flags:
- `-p "prompt"`: Non-interactive headless mode
- `-y`: YOLO mode - auto-approves read_file tool to access the image
- `2>&1 | grep -A 200 '```'`: Filters to only the JSON code block output

### 4. Parse and Validate

- Parse JSON output from Gemini (extract content between ``` markers)
- Validate each doctor has at least a name
- Mark all extracted doctors with `ocr_source: true`
- If Gemini returns invalid JSON, retry once with simplified prompt, then skip

### 5. Merge Results

- Combine OCR results with any DOM-extracted data
- De-duplicate by doctor name
- Prefer DOM data over OCR when both available

## Error Handling

- Gemini CLI not available: Skip OCR, log warning, proceed with DOM-only results
- Gemini timeout (>60s): Kill process, proceed without OCR
- Invalid JSON response: Retry once with simplified prompt, then skip
- PNG heap crash: Always convert to JPEG first (see Step 2)
- Image too large (>1MB JPEG): Resize to max 1024px width before sending
