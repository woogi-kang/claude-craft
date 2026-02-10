# OCR Workflow

Multi-provider OCR pipeline for extracting text from image-based doctor pages where DOM extraction fails.

**THIS STEP IS MANDATORY** when image-based content is detected and any OCR provider is available. Do NOT skip OCR and report "OCR needed" - you MUST execute OCR and return the extracted data. The only acceptable reason to skip OCR is when NO OCR provider is available on the system.

## OCR Provider Chain

Providers are tried in priority order. If one fails, fall back to the next:

| Priority | Provider | Type | Cost | Korean Accuracy |
|:--------:|----------|------|------|:---------------:|
| 1 | Gemini CLI | Cloud API | Free tier | High |
| 2 | macOS Vision | Local | Free | Medium-High |
| 3 | Tesseract | Local | Free | Medium |

**Provider detection** (run once at agent startup):
```bash
# Check Gemini CLI
command -v gemini >/dev/null 2>&1 && echo "GEMINI_OK"
# Check macOS Vision (available on macOS 13+)
python3 -c "import Vision; print('VISION_OK')" 2>/dev/null || \
  sw_vers -productVersion | grep -q "^1[3-9]\|^[2-9]" && echo "VISION_OK"
# Check Tesseract
command -v tesseract >/dev/null 2>&1 && tesseract --list-langs 2>&1 | grep -q kor && echo "TESSERACT_OK"
```

**Fallback trigger conditions**:
- Gemini → Vision: authentication error, rate limit exhausted (4th hit), timeout
- Vision → Tesseract: Vision framework not available (non-macOS)
- All failed: DOM-only extraction, mark `ocr_source: false`

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

### 2. Image Preprocessing Pipeline

**CRITICAL**: Gemini CLI crashes with heap out of memory on PNG files. Always convert to JPEG first.

The full preprocessing pipeline runs in order. Each step is conditional:

**Step 2a: Format conversion (mandatory)**

macOS (sips):
```bash
sips -s format jpeg -s formatOptions 85 data/clinic-results/screenshots/hospital_{no}_doctors_{ts}.png --out data/clinic-results/screenshots/hospital_{no}_doctors_{ts}.jpg
```

Cross-platform fallback (if sips not available):
```bash
# Option 1: Python PIL/Pillow
python3 -c "from PIL import Image; Image.open('input.png').convert('RGB').save('output.jpg', quality=85)"
# Option 2: ImageMagick
convert input.png -quality 85 output.jpg
```

**Step 2b: Size normalization (if width > 1600px or file > 800KB)**
```bash
# Resize to 1200px width for optimal OCR accuracy vs speed
sips --resampleWidth 1200 -s format jpeg -s formatOptions 85 input.jpg --out output.jpg
```
Target: 1200px width, under 500KB.

**Step 2c: Quality analysis and enhancement**
```bash
python3 -c "
from PIL import Image, ImageStat, ImageEnhance, ImageFilter
img = Image.open('output.jpg')
gray = img.convert('L')
stat = ImageStat.Stat(gray)
variance = stat.var[0]
mean_brightness = stat.mean[0]
enhanced = img

# Low contrast: variance < 500
if variance < 500:
    enhanced = ImageEnhance.Contrast(enhanced).enhance(1.5)
    print('ENHANCED: contrast')

# Too dark: mean < 80
if mean_brightness < 80:
    enhanced = ImageEnhance.Brightness(enhanced).enhance(1.3)
    print('ENHANCED: brightness')

# Too bright/washed out: mean > 200
if mean_brightness > 200:
    enhanced = ImageEnhance.Brightness(enhanced).enhance(0.8)
    print('ENHANCED: brightness_reduce')

# Light noise reduction (preserves text edges)
enhanced = enhanced.filter(ImageFilter.MedianFilter(size=3))

enhanced.save('output_enhanced.jpg', quality=85)
print(f'STATS: variance={variance:.0f} brightness={mean_brightness:.0f}')
"
```

**Step 2d: Tesseract-specific binarization (only if Tesseract is the OCR provider)**
```bash
python3 -c "
from PIL import Image
img = Image.open('output_enhanced.jpg').convert('L')
# Otsu's threshold approximation
threshold = 128
img = img.point(lambda p: 255 if p > threshold else 0)
img.save('output_binary.jpg', quality=95)
"
```

### 2.5. OCR Cache Check

Before calling any OCR provider, check the cache for a previous result:

```bash
IMAGE_HASH=$(shasum -a 256 output.jpg | cut -d' ' -f1)
CACHED=$(python3 -c "
import sqlite3, json
conn = sqlite3.connect('data/clinic-results/hospitals.db')
row = conn.execute('SELECT result_json FROM ocr_cache WHERE image_hash=?', ('$IMAGE_HASH',)).fetchone()
if row: print(row[0])
else: print('CACHE_MISS')
conn.close()
")

if [ "$CACHED" != "CACHE_MISS" ]; then
    echo "$CACHED"  # Use cached result, skip OCR
    exit 0
fi
```

After successful OCR, save to cache:
```bash
python3 -c "
import sqlite3, json
conn = sqlite3.connect('data/clinic-results/hospitals.db')
conn.execute('CREATE TABLE IF NOT EXISTS ocr_cache (image_hash TEXT PRIMARY KEY, result_json TEXT NOT NULL, created_at TEXT DEFAULT (datetime(\"now\")))')
conn.execute('INSERT OR REPLACE INTO ocr_cache (image_hash, result_json) VALUES (?, ?)', ('$IMAGE_HASH', '''$OCR_RESULT'''))
conn.commit()
conn.close()
"
```

Cache TTL: 30 days. Purge old entries periodically:
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('data/clinic-results/hospitals.db')
conn.execute(\"DELETE FROM ocr_cache WHERE created_at < datetime('now', '-30 days')\")
conn.commit()
conn.close()
"
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
- 4th rate limit: **fall back to next OCR provider**

**API key expiration**: If authentication error detected, **switch to fallback provider** for remaining hospitals in batch.

### 3b. Fallback: macOS Vision Framework (Priority 2)

Available on macOS 13+. Uses Apple's built-in Korean text recognition.

```bash
python3 -c "
import Vision, Quartz, json
from Foundation import NSURL

image_url = NSURL.fileURLWithPath_('output_enhanced.jpg')
request = Vision.VNRecognizeTextRequest.alloc().init()
request.setRecognitionLanguages_(['ko', 'en'])
request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)

handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(image_url, {})
handler.performRequests_error_([request], None)

results = []
for obs in request.results():
    text = obs.topCandidates_(1)[0].string()
    confidence = obs.confidence()
    results.append({'text': text, 'confidence': float(confidence)})

print(json.dumps(results, ensure_ascii=False))
"
```

Post-processing: Parse raw text lines into doctor JSON structure using pattern matching:
- Lines with 2-5 Korean chars followed by role keyword → doctor name + role
- Lines with 대학/학위/졸업 → education
- Lines with 병원/클리닉/근무 → career
- Lines with 정회원/학회/자격 → credentials

### 3c. Fallback: Tesseract (Priority 3)

Requires: `brew install tesseract tesseract-lang`

```bash
# Use binarized image for best Tesseract accuracy
tesseract output_binary.jpg stdout -l kor+eng --psm 6 --oem 3 2>/dev/null
```

PSM modes for clinic pages:
- `--psm 6`: Uniform block of text (default, good for most pages)
- `--psm 4`: Single column (good for vertical card layouts)
- `--psm 3`: Fully automatic (fallback if 6 fails)

Post-processing: Same pattern matching as Vision fallback above.

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

**Calculate OCR confidence score** (`ocr_confidence: 0.0-1.0`):
For each doctor extracted via OCR, calculate confidence based on data quality:

| Criterion | Score |
|-----------|-------|
| Korean name 2-5 chars | +0.30 |
| Role matches known keyword (원장/전문의/의사) | +0.20 |
| 3+ credential items | +0.20 |
| Education info present | +0.15 |
| Photo URL found (DOM cross-reference) | +0.15 |

```python
def calc_ocr_confidence(doc):
    score = 0.0
    name = doc.get("name", "")
    if 2 <= len(name) <= 5 and all('\uac00' <= c <= '\ud7a3' for c in name):
        score += 0.30
    if doc.get("role") in ("원장", "대표원장", "부원장", "전문의", "의사"):
        score += 0.20
    if len(doc.get("credentials") or []) >= 3:
        score += 0.20
    if doc.get("education"):
        score += 0.15
    if doc.get("photo_url"):
        score += 0.15
    return round(min(score, 1.0), 2)
```

- Attach `ocr_confidence` to each doctor result
- Flag doctors with `ocr_confidence < 0.4` as low-confidence in warnings

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

- **No OCR provider available**: Skip OCR, log warning, proceed with DOM-only results. This is the ONLY case where skipping OCR is acceptable. When any OCR provider is available, OCR is MANDATORY for image-based pages.
- **Gemini timeout (>60s)**: Kill process via `timeout` command, fall back to next provider
- **Invalid JSON response**: Retry once with simplified prompt (plain text extraction), then skip
- **Response format variation**: Use multi-strategy JSON extraction (code block → raw JSON → regex). See Step 4.
- **PNG heap crash**: Always convert to JPEG first (see Step 2). This is a known Gemini CLI bug.
- **Image too large (>1MB JPEG)**: Resize to max 1024px width before sending
- **Project scan slow**: Use `--include-directories` flag to limit file scan scope (see Step 3)
- **Rate limit exceeded**: Exponential backoff with 3 retries (60s, 120s, 240s), then fall back to next OCR provider
- **API key expiration mid-batch**: Detect auth error in stderr, switch to fallback provider for remaining hospitals
- **sips not available (non-macOS)**: Fallback to PIL/Pillow or ImageMagick for PNG→JPEG conversion
- **Low contrast screenshot**: Detect via PIL variance check (<500), enhance contrast 1.5x before OCR
- **Long page (exceeds viewport)**: Take multiple viewport screenshots, OCR each separately, merge results
- **Partial/garbled OCR result**: Validate name >= 2 Korean characters, no truncation markers (digits, jamo)
- **Screenshot filename collision**: Use timestamp + hospital_no in filename to prevent batch collisions
- **Corrupted screenshot (<1KB)**: Re-take screenshot once, skip OCR if still corrupt
