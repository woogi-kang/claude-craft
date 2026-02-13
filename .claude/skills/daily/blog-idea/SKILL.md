---
name: daily-blog-idea
description: >
  Blog topic idea generator using trending data from multiple sources.
  Combines HN top stories, dev.to trending articles, and Reddit r/programming.
  Suggests topics with context, angle, and keywords for blog posts.
  Pure Python with urllib, no dependencies required.
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
  tags: "blog, idea, trending, content, writing, daily"
  aliases: "blog-topic, content-idea"
  briefing_category: "content"

# MoAI Extension: Triggers
triggers:
  keywords: ["blog idea", "블로그 주제", "블로그 아이디어", "blog topic", "글감", "포스트 주제"]
---

# Blog Idea Generator

## Overview

Generate blog post ideas by analyzing trending topics across 3 sources:
1. Hacker News (tech community engagement, high-signal discussions)
2. dev.to (developer community trends, tag-based topic clustering)
3. Reddit r/programming (developer opinions, controversial takes)

No authentication required. Pure Python stdlib (urllib + json).

## Data Sources

```
HN Firebase API:     https://hacker-news.firebaseio.com/v0/topstories.json
dev.to API:          https://dev.to/api/articles?top=1&per_page=20
Reddit JSON API:     https://www.reddit.com/r/programming/hot.json?limit=15
```

All sources: No auth, JSON format, stdlib compatible.

Note: Google Trends was tested but returns sports/entertainment topics (not tech).
Reddit r/programming provides much better tech-focused trending data.

### API Details

HN Firebase API:
- No rate limit, no auth
- `/topstories.json` returns 500 story IDs sorted by rank
- `/item/{id}.json` returns story details (title, score, descendants, url)

dev.to API:
- No auth required (optional API key for higher limits)
- `?top=1` = trending in last 1 day
- Returns: title, tag_list, public_reactions_count, comments_count, url

Reddit JSON API:
- No auth required, but MUST set User-Agent header
- Append `.json` to any Reddit URL
- `?limit=15` controls result count
- Returns: title, score, num_comments, url, created_utc

## Execution Steps

### Step 1: Fetch Data from All Sources

```bash
python3 << 'PYEOF'
import json, urllib.request

headers = {"User-Agent": "Mozilla/5.0 (compatible; BlogBot/1.0)"}

# --- Source 1: HN Top Stories ---
hn_ids = json.loads(urllib.request.urlopen(
    "https://hacker-news.firebaseio.com/v0/topstories.json"
).read())[:20]

hn_stories = []
for sid in hn_ids:
    item = json.loads(urllib.request.urlopen(
        f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
    ).read())
    hn_stories.append({
        "title": item.get("title", ""),
        "score": item.get("score", 0),
        "comments": item.get("descendants", 0),
        "url": item.get("url", ""),
    })

# --- Source 2: dev.to Trending ---
req = urllib.request.Request(
    "https://dev.to/api/articles?top=1&per_page=20",
    headers=headers
)
devto_data = json.loads(urllib.request.urlopen(req, timeout=15).read())
devto_articles = [{
    "title": a.get("title", ""),
    "tags": a.get("tag_list", []),
    "reactions": a.get("public_reactions_count", 0),
    "comments": a.get("comments_count", 0),
    "url": a.get("url", ""),
} for a in devto_data]

# --- Source 3: Reddit r/programming ---
req = urllib.request.Request(
    "https://www.reddit.com/r/programming/hot.json?limit=15",
    headers={"User-Agent": "BlogBot/1.0 (compatible)"}
)
reddit_data = json.loads(urllib.request.urlopen(req, timeout=15).read())
reddit_posts = [{
    "title": p['data']['title'],
    "score": p['data']['score'],
    "comments": p['data']['num_comments'],
    "url": p['data'].get('url', ''),
} for p in reddit_data['data']['children'] if not p['data'].get('stickied')]

# --- Output raw data ---
result = {
    "hn": sorted(hn_stories, key=lambda x: x['score'], reverse=True),
    "devto": sorted(devto_articles, key=lambda x: x['reactions'], reverse=True),
    "reddit": sorted(reddit_posts, key=lambda x: x['score'], reverse=True),
}
print(json.dumps(result, ensure_ascii=False, indent=2))
PYEOF
```

### Step 2: Analyze and Generate Ideas

After fetching raw data, analyze patterns across sources to identify blog topics.

Analysis criteria:
1. **Cross-source overlap**: Topic appears in 2+ sources = high relevance
2. **High engagement**: HN score 200+ or Reddit score 500+ = proven interest
3. **High discussion**: Comment count 50+ = controversial or deep topic (good for opinion pieces)
4. **Tag clustering**: Common dev.to tags = trending technology areas
5. **Contrarian takes**: Reddit posts with high comments but moderate score = divisive topic (good for "hot take" posts)

Topic extraction strategy:
- Extract key themes from HN titles (AI, programming languages, tools, industry)
- Cross-reference with dev.to tags for technology-specific angles
- Use Reddit discussions for developer sentiment and opinion-based angles

### Step 3: Format Output

Present 5-7 blog post ideas with context and suggested angles.

```markdown
## Blog Post Ideas ({DATE})

### 1. {Topic Title}

- **Trending on**: HN (450 pts, 200 comments), Reddit (1.2k pts)
- **Keywords**: keyword1, keyword2, keyword3
- **Suggested angle**: {One sentence describing the unique angle}
- **Why now**: {Brief context on why this is timely}
- **Target audience**: {Who would read this}

---

### 2. {Topic Title}
...
```

### Idea Quality Guidelines

Each idea should have:
- A specific, non-generic title (not "Introduction to X")
- A unique angle that differentiates from existing content
- Timeliness factor (why write about it today)
- Clear target audience

Avoid suggesting:
- Overly broad topics ("What is AI?")
- Tutorial-only ideas without unique perspective
- Topics with no current engagement signal

### Customization Options

User can request:
- "AI focused" / specific domain - filter to domain-specific topics
- "beginner" / "advanced" - adjust suggested depth level
- "Korean audience" - tailor for Korean tech blog readers
- "controversial" - prioritize high-comment/divisive topics
