# Social Channel Patterns

Reference data for extracting social consultation channels from Korean skin clinic websites.

## Platform URL Patterns

### KakaoTalk
| Pattern | Example |
|---------|---------|
| `pf.kakao.com/` | https://pf.kakao.com/_abc123 |
| `open.kakao.com/o/` | https://open.kakao.com/o/xyz789 |
| `talk.kakao.com/` | https://talk.kakao.com/... |
| `kakao.com/channel/` | https://kakao.com/channel/... |

Widget signatures:
- `kakao.channel.chat`
- `Kakao.Channel`
- `kakaocdn.net/js_plugins`

### Naver Talk
| Pattern | Example |
|---------|---------|
| `talk.naver.com/` | https://talk.naver.com/ct/... |
| `naver.me/` | https://naver.me/abc123 |

### Line
| Pattern | Example |
|---------|---------|
| `line.me/` | https://line.me/ti/p/... |
| `lin.ee/` | https://lin.ee/abc123 |

### WeChat
| Pattern | Example |
|---------|---------|
| `u.wechat.com/` | https://u.wechat.com/... |
| `weixin.qq.com/` | https://weixin.qq.com/... |

Note: WeChat links are often available only as QR code images. Check `<img>` tags with qr/wechat keywords.

### WhatsApp
| Pattern | Example |
|---------|---------|
| `wa.me/` | https://wa.me/821012345678 |
| `api.whatsapp.com/` | https://api.whatsapp.com/send?phone=... |

### Telegram
| Pattern | Example |
|---------|---------|
| `t.me/` | https://t.me/clinicname |

### Facebook Messenger
| Pattern | Example |
|---------|---------|
| `m.me/` | https://m.me/clinicname |

## Extraction Locations (Priority Order)

1. `href` attributes in `<a>` tags
2. `onclick` handlers (`href='#none'` pattern)
3. `position:fixed` floating elements
4. Footer sections
5. `meta` tags (`og:url`, `description`)
6. `iframe src` attributes
7. JavaScript variables and SDK initialization
8. QR code images (especially WeChat)

## Four-Pass Extraction Strategy

### Pass 1: Static DOM
- Scan all `<a href>` attributes for platform URL patterns
- Check footer, sidebar, header sections
- Look for floating elements (`position:fixed`, `position:sticky`)

### Pass 1.5: iframe Detection
- Use `browser_evaluate` to find all `<iframe>` elements:
  ```javascript
  Array.from(document.querySelectorAll('iframe')).map(f => ({src: f.src, id: f.id, class: f.className}))
  ```
- Check iframe `src` for social platform domains (kakao, naver, line)
- Check for chat widget iframes (channel.io, zendesk, tawk.to, crisp)
- If iframe contains a social channel, record with `extraction_method: "iframe"`

### Pass 2: Dynamic JavaScript
- Check `onclick` handlers (common pattern: `href="#none"` with `onclick="window.open('...')"`)
- Detect chat widget SDKs (Kakao Channel, channel.io, tawk.to)
- Use `browser_evaluate` to extract hidden social links from JS variables

### Pass 3: QR Codes
- Find `<img>` tags with QR-related attributes (`qr`, `wechat`, `weixin`, `kakao`)
- Download and decode using image analysis
- Convert decoded URLs to social links

### Pass 4: URL Validation
For each extracted URL:
1. **Format check**: Verify URL has valid scheme (http/https)
2. **De-duplicate**: Normalize URLs (strip trailing slash, remove tracking params)
   - Remove: `?utm_*`, `?ref=*`, `?fbclid=*`, `?gclid=*`
3. **Platform classify**: Match normalized URL to platform patterns above
4. **Dead link detection**: If URL returns immediate redirect to error page or generic domain, mark as `"status": "dead"`
