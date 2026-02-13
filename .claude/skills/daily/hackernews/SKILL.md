---
name: daily-hackernews
description: >
  Hacker News top stories crawler using Firebase API.
  Fetches top/best/new stories with scores, comments, and links.
  Pure Python with urllib, no dependencies required.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Bash
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-02-13"
  modularized: "false"
  tags: "hackernews, news, tech, trends, daily"
  aliases: "hn, hacker-news"
  briefing_category: "dev"

# MoAI Extension: Triggers
triggers:
  keywords: ["hackernews", "hacker news", "hn", "tech news", "뉴스", "트렌드"]
---

# Hacker News Daily Crawler

## Overview

Fetch top stories from Hacker News using the official Firebase API.
Pure Python stdlib, no external dependencies.

## API Reference

```
Base URL: https://hacker-news.firebaseio.com/v0

Top stories:  /topstories.json   (500 IDs, sorted by ranking)
Best stories: /beststories.json   (500 IDs, sorted by score)
New stories:  /newstories.json    (500 IDs, sorted by time)
Item detail:  /item/{id}.json
```

## Execution Steps

### Step 1: Fetch and Parse

Run the following Python script. Adjust `count` and `endpoint` as needed.

```bash
python3 << 'PYEOF'
import json, urllib.request, sys
from datetime import datetime, timezone

endpoint = "topstories"  # topstories | beststories | newstories
count = 20  # number of stories to fetch

# Fetch story IDs
url = f"https://hacker-news.firebaseio.com/v0/{endpoint}.json"
ids = json.loads(urllib.request.urlopen(url).read())[:count]

# Fetch each story
stories = []
for sid in ids:
    item = json.loads(urllib.request.urlopen(
        f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
    ).read())
    stories.append({
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "score": item.get("score", 0),
        "by": item.get("by", ""),
        "comments": item.get("descendants", 0),
        "id": item.get("id", ""),
        "time": item.get("time", 0),
    })

print(json.dumps(stories, ensure_ascii=False, indent=2))
PYEOF
```

### Step 2: Format Output

Present results grouped by score tiers:

```markdown
## Hacker News Top Stories ({DATE})

### Hot (500+ points)
| # | Score | Comments | Title |
|---|-------|----------|-------|
| 1 | 1344 | 581 | [Title](url) |

### Trending (100-499 points)
| # | Score | Comments | Title |
|---|-------|----------|-------|

### Rising (< 100 points)
| # | Score | Comments | Title |
|---|-------|----------|-------|
```

Each title should link to the original URL.
Add HN discussion link: `https://news.ycombinator.com/item?id={ID}`

### Customization Options

User can request:
- "top 10" / "top 30" → adjust `count`
- "best" → change endpoint to `beststories`
- "new" / "latest" → change endpoint to `newstories`
- "AI only" / "specific topic" → filter titles after fetching

## Output Fields

| Field | Description |
|-------|-------------|
| title | Story headline |
| url | Original article URL (may be empty for Ask HN / Show HN) |
| score | Upvote count |
| comments | Comment count (descendants) |
| by | Submitter username |
| id | HN item ID (for discussion link) |
| time | Unix timestamp of submission |
