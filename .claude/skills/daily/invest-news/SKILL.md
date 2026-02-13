---
name: daily-invest-news
description: >
  Korean startup investment news crawler.
  Fetches latest funding rounds from Platum (primary) and VentureSquare (supplementary).
  Platum investment category is the best source for Korean startup funding news.
  Pure Python with urllib + regex, no dependencies required.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Bash
user-invocable: false
metadata:
  version: "1.1.0"
  category: "domain"
  status: "active"
  updated: "2026-02-13"
  modularized: "false"
  tags: "investment, startup, funding, platum, venturesquare, daily, korea"
  aliases: "invest, funding-news, startup-news"
  briefing_category: "biz"

# MoAI Extension: Triggers
triggers:
  keywords: ["투자", "펀딩", "investment", "funding", "투자뉴스", "스타트업투자", "시리즈", "라운드"]
---

# Korean Startup Investment News Crawler

## Overview

Crawl latest startup investment/funding news from Korean tech media.
No API available - uses curl + Python regex parsing (stdlib only).

## Data Sources

### Source 1: Platum (platum.kr) - PRIMARY

```
Investment category: https://platum.kr/archives/category/investment
Format: HTML (server-side rendered, GenerateBlocks theme)
Auth: None
```

Platum is the best source for Korean startup investment news since 2012.
The investment category page lists ~24 articles per page, all investment-specific.

#### HTML Structure (GenerateBlocks layout)

Each article is a `gb-grid-column` with class `is-loop-template-item`:

```
gb-grid-column.is-loop-template-item
  gb-container
    gb-container.rounded.bordered.hover-box-shadow
      a.gb-container-link[href=ARTICLE_URL]     ← URL (empty tag, overlay link)
      gb-container
        gb-container
          p.gb-headline.category-terms           ← Category tag ("투자")
          h3.gb-headline.gb-headline-text        ← TITLE (plain text, no <a>)
          p.gb-headline.excerpt                  ← EXCERPT
        gb-container.author-date
          time[datetime=YYYY-MM-DDTHH:MM:SS]     ← DATE
```

Key selectors:
- Article wrapper: split by `is-loop-template-item">`
- URL: `<a class="gb-container-link" href="https://platum.kr/archives/NNNNN">`
- Title: `<h3 ...gb-headline-text...>TITLE TEXT</h3>` (NOT inside an <a> tag)
- Excerpt: `<p ...excerpt...>TEXT</p>`
- Date: `<time datetime="YYYY-MM-DD...">`

### Source 2: VentureSquare (venturesquare.net) - SUPPLEMENTARY

```
News page: https://www.venturesquare.net/category/news
Format: HTML (server-side rendered, Bootstrap layout)
Auth: None
```

VentureSquare is a general startup news site. Requires keyword filtering for investment articles.

#### HTML Structure

Each article is an `<article>` tag:

```
article#post-NNNNNN
  div.row
    div.row.g-0
      div.col
        h5.mb-0.bold
          a.black[href=ARTICLE_URL]              ← TITLE + URL
```

Dates are in separate `<time>` tags outside article blocks (in sidebar/meta sections).
Strategy: extract articles and dates separately, then zip by order.

Key selectors:
- Article wrapper: `<article ...>`
- Title + URL: `<h5 ...><a class="black" href="URL">TITLE</a></h5>`
- Dates: `<time datetime="YYYY-MM-DD ...">` (extracted separately and zipped)

## Execution Steps

### Step 1: Fetch Pages via curl

```bash
curl -s 'https://platum.kr/archives/category/investment' \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/platum_invest.html

curl -s 'https://www.venturesquare.net/category/news' \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/vs_news.html
```

### Step 2: Parse Platum (Primary Source)

```bash
python3 << 'PYEOF'
import re, json

with open('/tmp/platum_invest.html', 'r') as f:
    html = f.read()

blocks = html.split('is-loop-template-item">')
items = []

for block in blocks[1:]:
    # URL from gb-container-link (empty <a> tag used as clickable overlay)
    url_m = re.search(r'gb-container-link"\s*href="(https://platum\.kr/archives/\d+)"', block)
    if not url_m:
        continue
    url = url_m.group(1)

    # Title from <h3 class="gb-headline...gb-headline-text">TEXT</h3>
    title_m = re.search(r'<h3[^>]*gb-headline-text[^>]*>(.*?)</h3>', block, re.DOTALL)
    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip() if title_m else ''

    # Excerpt from <p ...excerpt...>TEXT</p>
    excerpt_m = re.search(r'excerpt[^>]*>(.*?)</p>', block, re.DOTALL)
    excerpt = re.sub(r'<[^>]+>', '', excerpt_m.group(1)).strip()[:200] if excerpt_m else ''

    # Date from <time datetime="YYYY-MM-DD...">
    date_m = re.search(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})', block)
    date = date_m.group(1) if date_m else ''

    if title:
        # Clean HTML entities
        for old, new in [('&#8216;', "'"), ('&#8217;', "'"), ('&#8220;', '"'),
                         ('&#8221;', '"'), ('&#038;', '&'), ('&amp;', '&')]:
            title = title.replace(old, new)
            excerpt = excerpt.replace(old, new)
        items.append({
            'title': title, 'url': url, 'date': date,
            'excerpt': excerpt, 'source': 'Platum'
        })

print(json.dumps(items, ensure_ascii=False, indent=2))
PYEOF
```

### Step 3: Parse VentureSquare (Supplementary)

```bash
python3 << 'PYEOF'
import re, json

with open('/tmp/vs_news.html', 'r') as f:
    html = f.read()

# Extract articles: title + URL from <h5><a class="black" href="URL">TITLE</a></h5>
articles = []
for m in re.finditer(
    r'<h5[^>]*>\s*<a[^>]*href="(https://www\.venturesquare\.net/\d+/)"[^>]*>(.*?)</a>',
    html, re.DOTALL
):
    title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    for old, new in [('&#038;', '&'), ('&#8217;', "'"), ('&#8220;', '"'), ('&#8221;', '"')]:
        title = title.replace(old, new)
    articles.append({'title': title, 'url': m.group(1)})

# Extract dates separately (same order as articles)
dates = [m.group(1) for m in re.finditer(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})', html)]

# Zip articles with dates
items = []
for i, art in enumerate(articles):
    art['date'] = dates[i] if i < len(dates) else ''
    art['source'] = 'VentureSquare'
    items.append(art)

# Filter investment-related articles only
invest_kw = ['투자', '펀딩', '시리즈', '라운드', '인수', '억원', '억 원',
             '유치', 'VC', '벤처캐피탈', 'Pre-IPO', 'IPO', '시드', 'M&A']
invest_items = [item for item in items if any(kw in item['title'] for kw in invest_kw)]

print(json.dumps(invest_items, ensure_ascii=False, indent=2))
PYEOF
```

### Step 4: Format Output

Combine Platum (all articles) + VentureSquare (investment-filtered).
Group by date, newest first. Platum is primary, VS is supplementary.

```markdown
## Startup Investment News ({DATE})

Platum 투자 카테고리 기준 | 최근 1주일

### {DATE} (오늘)

| # | 스타트업 | 내용 | 링크 |
|---|---------|------|------|
| 1 | **{company}** | {summary} | [Platum]({url}) |

### {DATE-1}

| # | 스타트업 | 내용 | 링크 |
|---|---------|------|------|

---

### 주요 트렌드
- {trend_1}
- {trend_2}
- {trend_3}
```

Highlight key details in titles:
- Investment amounts: **320억 원**, **50억 원**
- Round types: 시리즈A, 시리즈E, 시드, Pre-IPO
- Notable investors in excerpt

### Customization Options

User can request:
- "오늘만" - filter strictly by today's date
- "이번주" - show this week's articles
- "AI 관련" / specific keyword - filter by keyword
- "VS도 포함" - include all VentureSquare articles (not just investment-filtered)
