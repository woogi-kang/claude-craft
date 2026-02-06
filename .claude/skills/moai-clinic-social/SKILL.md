---
name: moai-clinic-social
description: >
  Social consultation channel extraction patterns for Korean skin clinic
  websites. Covers 7 platforms (KakaoTalk, Naver Talk, Line, WeChat,
  WhatsApp, Telegram, Facebook Messenger), three-pass extraction strategy,
  floating element detection, QR code identification, and chat widget
  detection. Use when extracting social links from clinic websites.
license: Apache-2.0
compatibility: Designed for Claude Code
allowed-tools: Read Grep Glob Bash
user-invocable: false
metadata:
  version: "1.0.0"
  category: "domain"
  status: "active"
  updated: "2026-02-06"
  modularized: "false"
  tags: "clinic, social, kakao, naver-talk, line, wechat, whatsapp, qr, chat-widget"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 5000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "social channel"
    - "kakao"
    - "naver talk"
    - "line"
    - "wechat"
    - "whatsapp"
    - "consultation link"
    - "chat widget"
    - "qr code"
  agents:
    - "clinic-crawler-agent"
  phases:
    - "run"
---

# Social Channel Extraction

## Three-Pass Strategy

### Pass 1: Prescan (HTTP Regex)
Fast regex extraction from raw HTML without browser rendering.
Catches ~60% of social links. High confidence (0.8).

Patterns: See clinic-crawl/patterns/social_urls.json

### Pass 2: Static DOM
Browser-rendered DOM analysis via Playwright snapshot.
Catches links in rendered HTML that regex might miss.

Key locations:
1. **Footer** - Most common social link location
2. **Floating buttons** - position:fixed elements with social icons
3. **Header/nav** - Sometimes in top navigation bar
4. **Sidebar** - Occasionally in side panels

### Pass 3: Dynamic JavaScript
For sites using href="#none" with onclick handlers.
Use browser_evaluate to extract hidden social URLs.

```javascript
// Example: Extract Kakao channel from onclick
document.querySelectorAll('a[href="#none"], a[href="javascript:void(0)"]')
```

Also check for:
- Chat widget SDK initialization (Kakao Channel plugin)
- Meta tags with social URLs
- iframe src attributes pointing to social platforms

## Platform URL Patterns

| Platform | URL Patterns |
|----------|-------------|
| KakaoTalk | pf.kakao.com/*, open.kakao.com/o/*, talk.kakao.com/* |
| Naver Talk | talk.naver.com/*, naver.me/* |
| Line | line.me/*, lin.ee/* |
| WeChat | u.wechat.com/*, weixin.qq.com/* |
| WhatsApp | wa.me/*, api.whatsapp.com/* |
| Telegram | t.me/* |
| FB Messenger | m.me/* |

## Chat Widget Detection

Some clinics embed Kakao Channel SDK instead of linking:
- Look for `kakaocdn.net/js_plugins` script tag
- Look for `Kakao.Channel.createChatButton` calls
- Also check: channel.io, tawk.to

## QR Code Handling

WeChat links are often QR-only (no clickable URL):
1. Find img tags with qr/wechat/위챗 in alt, class, or nearby text
2. Download image
3. Decode with pyzbar
4. Extract social URL from decoded text

## Confidence Scoring

| Method | Confidence |
|--------|-----------|
| prescan_regex | 0.80 |
| dom_static | 0.90 |
| dom_dynamic | 0.85 |
| floating_element | 0.85 |
| qr_decode | 0.95 |
| meta_tag | 0.70 |
| iframe_widget | 0.75 |

## Reference

See: clinic-crawl/clinic_crawl/scripts/extract_social.py
See: clinic-crawl/patterns/social_urls.json
