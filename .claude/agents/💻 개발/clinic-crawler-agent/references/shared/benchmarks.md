# Performance Benchmarks

Reference performance data for clinic crawl operations.

## Single Hospital Crawl Time

| Site Type | Expected Time | Notes |
|-----------|:------------:|-------|
| Static HTML (simple clinic) | 10-20s | Direct DOM extraction, no SPA wait |
| WordPress/Cafe24 | 15-25s | Standard CMS, predictable selectors |
| SPA (React/Next.js) | 25-40s | MutationObserver wait + hydration |
| imweb/modoo builder | 20-35s | Builder platforms, consistent structure |
| Image-based (OCR needed) | 40-90s | Screenshot + JPEG conversion + Gemini CLI |
| Chain sibling (cached selectors) | 8-15s | Selector reuse, skip discovery phase |
| Complex multi-branch | 30-50s | Branch matching + per-branch extraction |

## OCR Provider Performance

| Provider | Avg Time | Korean Accuracy | Cost |
|----------|:--------:|:---------------:|------|
| Gemini CLI | 15-30s | 90-95% | Free tier (rate limited) |
| macOS Vision | 3-8s | 80-88% | Free (local) |
| Tesseract (kor) | 2-5s | 65-78% | Free (local) |

Notes:
- Gemini accuracy is highest but subject to rate limits and network latency
- macOS Vision is fastest with good accuracy, macOS 13+ only
- Tesseract benefits most from image preprocessing (binarization)

## Batch Throughput

| Configuration | Hospitals/Hour | Notes |
|---------------|:--------------:|-------|
| Single agent, sequential | 60-100 | Default mode |
| Single agent, chain-optimized | 80-130 | Selector reuse for chains |
| 3 parallel agents | 180-300 | Requires range partitioning |
| 3 agents + chain optimization | 240-400 | Optimal configuration |

## Target Success Rates by CMS

| CMS Platform | Target Success Rate | Known Challenges |
|-------------|:-------------------:|------------------|
| Custom domain (general) | 75%+ | Highly variable structure |
| WordPress | 90%+ | Predictable selectors |
| imweb | 85%+ | Consistent builder structure |
| modoo (Naver) | 80%+ | Heavy JavaScript, occasional popups |
| Cafe24 | 85%+ | Standard e-commerce CMS |
| Wix | 70%+ | Complex DOM, shadow components |

## Platform Discovery Rates (Expected)

Among successfully crawled hospitals:

| Platform | Expected Discovery Rate | Notes |
|----------|:-----------------------:|-------|
| Phone | 90-95% | Most sites have phone numbers |
| KakaoTalk | 60-75% | Primary Korean consultation channel |
| NaverTalk | 30-45% | Common for Naver-integrated clinics |
| NaverBooking | 25-40% | Naver reservation integration |
| Instagram | 40-55% | Social media presence |
| NaverBlog | 20-35% | Blog link on homepage |
| YouTube | 15-25% | Video content clinics |
| Line | 5-10% | Primarily international clinics |
| WhatsApp | 3-8% | International patient focus |
| WeChat | 2-5% | Chinese patient focus, often QR only |

## Resource Usage

| Metric | Threshold | Action |
|--------|:---------:|--------|
| Browser memory | 500MB | Restart browser |
| Screenshots folder | 100MB | Warn user, suggest cleanup |
| SQLite DB size | 50MB | Consider archiving old data |
| OCR cache entries | 1000+ | Purge entries older than 30 days |
| Consecutive failures | 5 | Halt batch, alert user |
| Failure rate (per 10) | 30%+ | Pause and alert user |

## Estimated Full Dataset Completion

For 4,256 hospitals:
- **Optimistic** (3 agents, chain-optimized): ~12-15 hours
- **Standard** (1 agent, sequential): ~45-60 hours
- **Conservative** (with retries, manual review): ~70-90 hours

Factors that increase time:
- High OCR ratio (image-heavy sites)
- Many chain hospitals needing individual crawl (selector mismatch)
- Rate limiting from target sites or OCR API
- Network instability requiring retries
