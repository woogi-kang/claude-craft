# Clinic Crawler Agent Usage Guide

## Quick Start

### Crawl a single hospital
```
Use the clinic-crawler-agent to crawl hospital #6 (고은미인의원) at http://www.goeunmiin.co.kr/
Extract social consultation channels and doctor information.
Save results to data/clinic-results/hospitals.db
```

### Crawl multiple hospitals sequentially
```
Use the clinic-crawler-agent to crawl the following hospitals one by one:
1. Hospital #6 (고은미인의원) at http://www.goeunmiin.co.kr/
2. Hospital #15 (톡스앤필의원) at http://www.toxnfill10.com/
3. Hospital #28 (서울미의원) at http://www.seoulmi.kr
Save each result to data/clinic-results/hospitals.db
```

IMPORTANT: Run hospitals sequentially (one at a time), not in parallel.
Playwright MCP uses a single browser instance that cannot handle concurrent navigations.

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
Run hospitals sequentially. Parallel Playwright MCP calls share the same browser.

### Popup blocking the page
The agent tries up to 3 dismissal strategies automatically.
If still blocked, it proceeds with whatever content is accessible.

### Image-based pages with no OCR
If Gemini CLI is not installed, the agent skips OCR and returns partial results.
Install with: `brew install gemini-cli`
