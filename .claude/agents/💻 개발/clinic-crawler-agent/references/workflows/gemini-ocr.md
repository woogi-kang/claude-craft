# Gemini CLI OCR Workflow

Use Gemini CLI to extract text from image-based doctor pages where DOM extraction fails.

**THIS STEP IS MANDATORY** when image-based content is detected and Gemini CLI is installed. Do NOT skip OCR and report "OCR needed" - you MUST execute Gemini CLI and return the extracted data. The only acceptable reason to skip OCR is when Gemini CLI is not installed on the system.

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
browser_take_screenshot -> save to data/clinic-results/screenshots/hospital_{no}_doctors_{ts}.png
```

**Unique filename**: Use timestamp to prevent collisions in batch operations.

If multiple doctor cards exist, screenshot each separately for better OCR accuracy.

**Long page handling**: If page height > viewport height:
1. Take screenshot of current viewport
2. Scroll down by viewport height
3. Take additional screenshot
4. Repeat until bottom reached (max 10 screenshots)
5. OCR each screenshot separately, merge results

**Validate screenshot**: Check file size > 1KB. If smaller, screenshot is likely corrupted - retake once.

### 2. Convert to JPEG

**CRITICAL**: Gemini CLI crashes with heap out of memory on PNG files. Always convert to JPEG first.

**macOS (sips)**:
```bash
sips -s format jpeg -s formatOptions 85 data/clinic-results/screenshots/hospital_{no}_doctors_{ts}.png --out data/clinic-results/screenshots/hospital_{no}_doctors_{ts}.jpg
```

**Cross-platform fallback** (if sips not available):
```bash
# Option 1: Python PIL/Pillow
python3 -c "from PIL import Image; Image.open('input.png').convert('RGB').save('output.jpg', quality=85)"

# Option 2: ImageMagick
convert input.png -quality 85 output.jpg
```

**Low contrast detection**: Before OCR, check image quality:
```bash
python3 -c "
from PIL import Image, ImageStat
img = Image.open('output.jpg').convert('L')
stat = ImageStat.Stat(img)
if stat.var[0] < 500: print('LOW_CONTRAST')
"
```
If low contrast detected, enhance before OCR:
```bash
python3 -c "from PIL import Image, ImageEnhance; img=Image.open('output.jpg'); ImageEnhance.Contrast(img).enhance(1.5).save('output_enhanced.jpg', quality=85)"
```

Target: under 500KB file size. If still too large, reduce width:
```bash
sips --resampleWidth 1024 -s format jpeg -s formatOptions 85 input.png --out output.jpg
```

### 3. Call Gemini CLI

**IMPORTANT**: Do NOT use stdin (`< image.jpg`). Instead, reference the file path in the prompt and use `-y` flag for auto-approval.

**Capture stderr separately** to detect auth errors and failures:

```bash
STDERR_FILE=$(mktemp)
timeout 60 gemini -p "Read the image file at data/clinic-results/screenshots/hospital_{no}_doctors_{ts}.jpg and extract all Korean text about doctors/medical staff. Return ONLY valid JSON:
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
}" -y --include-directories data/clinic-results/screenshots 2>"$STDERR_FILE" | tee /tmp/gemini_out_{no}.txt
EXIT_CODE=$?
STDERR=$(cat "$STDERR_FILE")
rm -f "$STDERR_FILE"

# Check for failures
if [ $EXIT_CODE -ne 0 ]; then
  if echo "$STDERR" | grep -qi "authentication\|unauthorized\|401"; then
    echo "FATAL: Gemini API authentication failed"
  elif echo "$STDERR" | grep -qi "rate.limit\|429"; then
    echo "RATE_LIMITED"
  fi
fi
```

Key flags:
- `-p "prompt"`: Non-interactive headless mode
- `-y`: YOLO mode - auto-approves read_file tool to access the image
- `--include-directories data/clinic-results/screenshots`: Limits file scanning to screenshots only
- `timeout 60`: Kill if Gemini takes longer than 60 seconds

**Rate limit handling**: Exponential backoff (3 retries max):
- 1st rate limit: wait 60s, retry
- 2nd rate limit: wait 120s, retry
- 3rd rate limit: wait 240s, retry
- 4th rate limit: skip OCR for this hospital

**API key expiration**: If authentication error detected, halt OCR for all remaining hospitals in batch.

### 4. Parse and Validate

**Multi-strategy JSON extraction** (Gemini doesn't always return markdown code blocks):

Strategy 1: Extract from markdown code block (``` markers)
```bash
grep -A 200 '```' /tmp/gemini_out_{no}.txt | sed '1d;/```/,$d'
```

Strategy 2: Find raw JSON (if no code block markers)
```bash
python3 -c "
import json, re, sys
text = open('/tmp/gemini_out_{no}.txt').read()
# Try code blocks first
blocks = re.findall(r'\`\`\`(?:json)?\s*\n(.*?)\n\`\`\`', text, re.DOTALL)
for b in blocks:
    try: print(json.dumps(json.loads(b))); sys.exit(0)
    except: pass
# Try raw JSON
matches = re.findall(r'(\{.*?\"doctors\".*?\})', text, re.DOTALL)
for m in matches:
    try: print(json.dumps(json.loads(m))); sys.exit(0)
    except: pass
print('PARSE_FAILED')
"
```

**Validate each doctor**:
- Name must be >= 2 characters
- Korean name should have 2-5 Korean characters
- Name should not end with truncation markers (digits, jamo like ㅣㅜ)
- Skip doctors that fail validation, log warning
- Mark all valid doctors with `ocr_source: true`
- If Gemini returns invalid JSON, retry once with simplified prompt, then skip

### 5. Merge Results

- Combine OCR results with any DOM-extracted data
- De-duplicate by doctor name
- Prefer DOM data over OCR when both available

### 6. Cleanup Screenshots

After successful OCR extraction and DB save:
```bash
rm -f data/clinic-results/screenshots/hospital_{no}_*.png
rm -f data/clinic-results/screenshots/hospital_{no}_*.jpg
```

Keep screenshots only if OCR failed (for manual review or re-attempt).

## Error Handling

- **Gemini CLI not installed**: Skip OCR, log warning, proceed with DOM-only results. This is the ONLY case where skipping OCR is acceptable. When Gemini CLI is available, OCR is MANDATORY for image-based pages.
- **Gemini timeout (>60s)**: Kill process via `timeout` command, proceed without OCR for this hospital
- **Invalid JSON response**: Retry once with simplified prompt (plain text extraction), then skip
- **Response format variation**: Use multi-strategy JSON extraction (code block → raw JSON → regex). See Step 4.
- **PNG heap crash**: Always convert to JPEG first (see Step 2). This is a known Gemini CLI bug.
- **Image too large (>1MB JPEG)**: Resize to max 1024px width before sending
- **Project scan slow**: Use `--include-directories` flag to limit file scan scope (see Step 3)
- **Rate limit exceeded**: Exponential backoff with 3 retries (60s, 120s, 240s), then skip OCR for this hospital
- **API key expiration mid-batch**: Detect auth error in stderr, halt OCR for all remaining hospitals in batch
- **sips not available (non-macOS)**: Fallback to PIL/Pillow or ImageMagick for PNG→JPEG conversion
- **Low contrast screenshot**: Detect via PIL variance check (<500), enhance contrast 1.5x before OCR
- **Long page (exceeds viewport)**: Take multiple viewport screenshots, OCR each separately, merge results
- **Partial/garbled OCR result**: Validate name >= 2 Korean characters, no truncation markers (digits, jamo)
- **Screenshot filename collision**: Use timestamp + hospital_no in filename to prevent batch collisions
- **Corrupted screenshot (<1KB)**: Re-take screenshot once, skip OCR if still corrupt
