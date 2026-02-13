---
name: daily-producthunt
description: >
  Product Hunt daily launches crawler using Atom feed.
  Fetches recent featured products with names, taglines, authors, and links.
  Pure Python with urllib + xml.etree, no dependencies required.
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
  tags: "producthunt, product, launch, startup, daily"
  aliases: "ph, product-hunt"
  briefing_category: "dev"

# MoAI Extension: Triggers
triggers:
  keywords: ["producthunt", "product hunt", "ph", "런칭", "신제품", "launch"]
---

# Product Hunt Daily Launches

## Overview

Fetch recent featured products from Product Hunt via Atom feed.
No authentication required. Pure Python stdlib (urllib + xml.etree.ElementTree).

## Data Source

```
Atom Feed: https://www.producthunt.com/feed
Format: XML (Atom 1.0, NOT RSS 2.0)
Namespace: http://www.w3.org/2005/Atom
Auth: None
Items: ~50 recent products
```

Note: The feed URL redirects to `?category=bank` but returns all recent products.

### Atom Entry Structure

```xml
<entry>
  <id>tag:www.producthunt.com,2005:Post/NNNNNNN</id>
  <published>2026-02-11T08:57:59-08:00</published>
  <updated>2026-02-12T17:18:41-08:00</updated>
  <link rel="alternate" type="text/html" href="https://www.producthunt.com/products/SLUG"/>
  <title>Product Name</title>
  <content type="html">
    &lt;p&gt;Tagline description&lt;/p&gt;
    &lt;p&gt;&lt;a href="..."&gt;Discussion&lt;/a&gt; | &lt;a href="..."&gt;Link&lt;/a&gt;&lt;/p&gt;
  </content>
  <author><name>Author Name</name></author>
</entry>
```

Key selectors (with Atom namespace `atom:`):
- Entries: `atom:entry`
- Title: `atom:title`
- URL: `atom:link[@rel="alternate"]` -> `href` attribute (NOT text content)
- Tagline: `atom:content` -> first `<p>` text (HTML-encoded, strip tags)
- Date: `atom:published` -> `YYYY-MM-DD` prefix
- Author: `atom:author/atom:name`

## Execution Steps

### Step 1: Fetch and Parse

```bash
curl -s 'https://www.producthunt.com/feed' \
  -H 'User-Agent: Mozilla/5.0 (compatible; DailyBot/1.0)' \
  -o /tmp/ph_feed.xml
```

```bash
python3 << 'PYEOF'
import xml.etree.ElementTree as ET
import json, re

with open('/tmp/ph_feed.xml', 'r') as f:
    feed_data = f.read()

root = ET.fromstring(feed_data)
ns = {'atom': 'http://www.w3.org/2005/Atom'}

entries = root.findall('atom:entry', ns)

products = []
for entry in entries:
    title_el = entry.find('atom:title', ns)
    link_el = entry.find('atom:link[@rel="alternate"]', ns)
    content_el = entry.find('atom:content', ns)
    pub_el = entry.find('atom:published', ns)
    author_el = entry.find('atom:author/atom:name', ns)

    title = title_el.text.strip() if title_el is not None else ''
    link = link_el.get('href', '') if link_el is not None else ''
    content = content_el.text if content_el is not None else ''
    pub = pub_el.text if pub_el is not None else ''
    author = author_el.text if author_el is not None else ''

    # Extract tagline from first <p> in content
    tagline_m = re.search(r'<p>\s*(.*?)\s*</p>', content, re.DOTALL)
    tagline = re.sub(r'<[^>]+>', '', tagline_m.group(1)).strip() if tagline_m else ''

    # Clean entities
    for old, new in [('&#8216;', "'"), ('&#8217;', "'"), ('&#038;', '&'),
                     ('&amp;', '&'), ('&amp;amp;', '&')]:
        title = title.replace(old, new)
        tagline = tagline.replace(old, new)

    date = pub[:10] if pub else ''

    products.append({
        'name': title,
        'url': link,
        'tagline': tagline,
        'date': date,
        'author': author,
    })

print(json.dumps(products, ensure_ascii=False, indent=2))
PYEOF
```

### Step 2: Format Output

Group by date, newest first. Show up to 15 products.

```markdown
## Product Hunt - Recent Launches ({DATE})

### {DATE} (Today)

| # | Product | Tagline | Author |
|---|---------|---------|--------|
| 1 | [{name}]({url}) | {tagline} | {author} |

### {DATE-1}

| # | Product | Tagline | Author |
|---|---------|---------|--------|
```

### Customization Options

User can request:
- "top 5" / "top 20" - adjust display count
- "AI only" / specific keyword - filter by title/tagline keyword match
- "today only" - show only today's launches
