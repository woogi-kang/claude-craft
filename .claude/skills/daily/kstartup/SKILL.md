---
name: daily-kstartup
description: >
  K-Startup (k-startup.go.kr) announcement crawler skill.
  Fetches business announcements via curl + Python HTML parsing.
  Supports multi-page crawling, date filtering, and category grouping.
  Server-side rendered pages, no browser automation needed.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Bash Read
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-02-13"
  modularized: "false"
  tags: "kstartup, crawler, announcement, startup, government"
  aliases: "k-startup, kstartup-crawler"
  briefing_category: "biz"

# MoAI Extension: Triggers
triggers:
  keywords: ["k-startup", "kstartup", "사업공고", "창업지원", "창업공고"]
---

# K-Startup Announcement Crawler

## Overview

Crawl K-Startup (https://www.k-startup.go.kr) business announcements using curl + Python.
No Playwright or browser automation required - pages are server-side rendered.

## URL Pattern

```
https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=&page={PAGE_NUMBER}
```

- Pagination: `?page=1`, `?page=2`, etc.
- Default sort: 공고등록순 (newest registration first)
- Each page contains ~15 items

## Execution Steps

### Step 1: Fetch Pages via curl

```bash
curl -s 'https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=&page=1' \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/kstartup_p1.html

curl -s 'https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=&page=2' \
  -H 'User-Agent: Mozilla/5.0' -o /tmp/kstartup_p2.html
```

Default: Fetch pages 1 and 2 (about 30 items).
User can request more pages if needed.

### Step 2: Parse HTML with Python

Run the following Python parser. It extracts structured data from `<li class="notice">` elements.

```python
python3 << 'PYEOF'
from html.parser import HTMLParser
import json, re, sys

class KStartupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.in_notice_li = False
        self.in_flag = False
        self.in_flag_day = False
        self.in_tit = False
        self.in_bottom_list = False
        self.in_flag_agency = False
        self.current = {}
        self.current_text = ''

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        cls = attrs_dict.get('class', '')

        if tag == 'li' and 'notice' in cls:
            self.in_notice_li = True
            self.current = {
                'category':'','dDay':'','title':'','org':'',
                'regDate':'','startDate':'','endDate':'',
                'views':'','type':'','program':'','pbancSn':''
            }

        if self.in_notice_li:
            if 'flag ' in f' {cls} ' and 'day' not in cls and 'flag_agency' not in cls:
                self.in_flag = True; self.current_text = ''
            elif 'flag' in cls and 'day' in cls:
                self.in_flag_day = True; self.current_text = ''
            elif tag == 'p' and 'tit' in cls:
                self.in_tit = True; self.current_text = ''
            elif tag == 'span' and cls == 'list':
                self.in_bottom_list = True; self.current_text = ''
            elif 'flag_agency' in cls:
                self.in_flag_agency = True; self.current_text = ''
            elif tag == 'a' and 'go_view' in attrs_dict.get('href', ''):
                m = re.search(r'go_view\((\d+)\)', attrs_dict.get('href',''))
                if m and not self.current.get('pbancSn'):
                    self.current['pbancSn'] = m.group(1)

    def handle_data(self, data):
        if self.in_flag: self.current_text += data
        elif self.in_flag_day: self.current_text += data
        elif self.in_tit: self.current_text += data
        elif self.in_bottom_list: self.current_text += data
        elif self.in_flag_agency: self.current_text += data

    def handle_endtag(self, tag):
        if self.in_flag and tag == 'span':
            self.current['category'] = self.current_text.strip()
            self.in_flag = False
        elif self.in_flag_day and tag == 'span':
            self.current['dDay'] = self.current_text.strip()
            self.in_flag_day = False
        elif self.in_tit and tag == 'p':
            self.current['title'] = self.current_text.strip()
            self.in_tit = False
        elif self.in_bottom_list and tag == 'span':
            t = self.current_text.strip()
            if '등록일자' in t: self.current['regDate'] = t.replace('등록일자','').strip()
            elif '시작일자' in t: self.current['startDate'] = t.replace('시작일자','').strip()
            elif '마감일자' in t: self.current['endDate'] = t.replace('마감일자','').strip()
            elif '조회' in t: self.current['views'] = t.replace('조회','').strip()
            elif not self.current['program']: self.current['program'] = t
            elif not self.current['org']: self.current['org'] = t
            self.in_bottom_list = False
        elif self.in_flag_agency and tag == 'span':
            self.current['type'] = self.current_text.strip()
            self.in_flag_agency = False
        elif tag == 'li' and self.in_notice_li and self.current.get('title'):
            self.items.append(self.current)
            self.in_notice_li = False

# Parse specified pages
pages = [1, 2]  # Adjust as needed
all_items = []
for p in pages:
    try:
        with open(f'/tmp/kstartup_p{p}.html', 'r') as f:
            html = f.read()
        parser = KStartupParser()
        parser.feed(html)
        for item in parser.items:
            item['page'] = p
        all_items.extend(parser.items)
    except FileNotFoundError:
        pass

print(json.dumps(all_items, ensure_ascii=False, indent=2))
PYEOF
```

### Step 3: Filter and Group

After parsing, filter by the requested date (typically today) and group by category.

Date filtering logic:
- If user says "today" or "오늘": filter where `regDate == today's date`
- If no items match today: show all items with note about latest registration date
- User can specify a date range: "이번주", "최근 3일" etc.

### Step 4: Format Output

Present results grouped by category in markdown table format:

```markdown
## K-Startup 사업공고 (등록일: {DATE})

총 {N}건 | {PAGE_RANGE}

### {CATEGORY} ({COUNT}건)

| # | 공고명 | 기관 | 등록일 | 마감일 | D-Day | 구분 |
|---|--------|------|--------|--------|-------|------|
| 1 | {title} | {org} | {regDate} | {endDate} | {dDay} | {type} |
```

## HTML Structure Reference

Each announcement is a `<li class="notice">`:

```html
<li class="notice">
  <div class="inner">
    <div class="right">
      <div class="top">
        <span class="flag type04">카테고리</span>
        <span class="flag day">D-14</span>
      </div>
      <div class="middle">
        <a href="javascript:go_view(176300);">
          <div class="tit_wrap">
            <p class="tit">공고 제목</p>
            <span class="new">새로운게시글</span>
          </div>
        </a>
      </div>
      <div class="bottom">
        <span class="list">프로그램명</span>
        <span class="list">기관명</span>
        <span class="list">등록일자 2026-02-12</span>
        <span class="list">시작일자 2026-02-12</span>
        <span class="list">마감일자 2026-02-27</span>
        <span class="list">조회 573</span>
      </div>
    </div>
    <div class="left">
      <span class="flag_agency">민간</span>
    </div>
  </div>
</li>
```

## Known Categories

- 사업화
- 멘토링ㆍ컨설팅ㆍ교육
- 시설ㆍ공간ㆍ보육
- 행사ㆍ네트워크
- 판로ㆍ해외진출
- 인력
- 기술개발(R&D)

## Detail Page URL

```
https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do?schM=view&pbancSn={ID}
```
