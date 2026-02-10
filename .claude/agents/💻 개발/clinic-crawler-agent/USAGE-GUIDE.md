# Clinic Crawler Agent Usage Guide

## Quick Start

### Mode 1: Single Hospital (LLM Agent via Playwright MCP)

Best for: edge cases, complex sites, manual review of failures.

```
Use the clinic-crawler-agent to crawl hospital #6 (고은미인의원) at http://www.goeunmiin.co.kr/
Extract social consultation channels and doctor information.
Save results to data/clinic-results/hospitals.db
```

IMPORTANT: Playwright MCP shares a single browser. Run hospitals sequentially (one at a time) in this mode.

### Mode 2: Parallel Batch (Python Playwright - Isolated Browsers)

Best for: bulk crawling 10+ hospitals with true parallel execution.

```bash
# 10 random Seoul clinics, 5 parallel browsers:
python3 scripts/clinic-storage/crawl_batch.py \
  --csv data/clinic-results/skin_clinics.csv \
  --filter-city 서울 --sample 10 --parallel 5

# Specific hospitals, 3 parallel:
python3 scripts/clinic-storage/crawl_batch.py \
  --csv data/clinic-results/skin_clinics.csv \
  --numbers 6,15,28 --parallel 3

# All Seoul clinics (skip already-crawled):
python3 scripts/clinic-storage/crawl_batch.py \
  --csv data/clinic-results/skin_clinics.csv \
  --filter-city 서울 --parallel 5

# Dry run (preview without crawling):
python3 scripts/clinic-storage/crawl_batch.py \
  --csv data/clinic-results/skin_clinics.csv \
  --filter-city 서울 --sample 10 --dry-run
```

Each hospital gets its own headless Chromium browser. No shared state, no conflicts.

### Single Hospital with Isolated Browser

```bash
python3 scripts/clinic-storage/crawl_single.py \
  --no 6 --name "고은미인의원" --url "http://www.goeunmiin.co.kr/"
```

Options: `--timeout 60`, `--headed` (show browser for debugging), `--db path/to/db`

## What Gets Extracted

### Social Consultation Channels
- KakaoTalk (Channel, Open Chat)
- Naver Talk
- Line
- WeChat (including QR codes)
- WhatsApp
- Telegram
- Facebook Messenger
- Also captures: Instagram, YouTube, Naver Blog, Facebook (as bonus social links)

### Doctor/Medical Staff Information
- Name (Korean + English if available)
- Role (director, specialist, etc.)
- Photo URL
- Education history
- Career history
- Credentials and certifications
- OCR source flag (true if extracted via Gemini image analysis)

## Storage

### SQLite Database
Location: `data/clinic-results/hospitals.db`

### CSV Export
```bash
python3 scripts/clinic-storage/storage_manager.py export \
  --db data/clinic-results/hospitals.db \
  --output data/clinic-results/exports/
```

Generates: `hospitals.csv`, `social_channels.csv`, `doctors.csv`

### Statistics
```bash
python3 scripts/clinic-storage/storage_manager.py stats \
  --db data/clinic-results/hospitals.db
```

## Gemini OCR

For image-based doctor pages where text extraction fails, the agent automatically:
1. Takes a screenshot of the doctor section
2. Sends it to Gemini CLI for analysis
3. Parses the Korean text and credentials
4. Marks results with `ocr_source: true`

Requires: Gemini CLI installed (`brew install gemini-cli`)

## Troubleshooting

### Browser conflicts with parallel execution
Use Mode 2 (crawl_batch.py) for parallel crawling. Each process gets its own browser.
Mode 1 (Playwright MCP) shares a single browser and must be run sequentially.

### Popup blocking the page
The agent tries up to 3 dismissal strategies automatically.
If still blocked, it proceeds with whatever content is accessible.

### Image-based pages with no OCR
If Gemini CLI is not installed, the agent skips OCR and returns partial results.
Install with: `brew install gemini-cli`

### Installing Python Playwright (for Mode 2)
```bash
pip install playwright
python -m playwright install chromium
```

### Debugging a failed crawl
```bash
# Run single hospital with visible browser:
python3 scripts/clinic-storage/crawl_single.py \
  --no 123 --name "Test" --url "https://example.com" --headed
```
