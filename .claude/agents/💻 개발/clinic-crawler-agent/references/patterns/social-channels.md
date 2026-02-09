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

### Naver Booking
| Pattern | Example |
|---------|---------|
| `booking.naver.com/` | https://booking.naver.com/booking/6/bizes/12345 |

### Instagram
| Pattern | Example |
|---------|---------|
| `instagram.com/` | https://www.instagram.com/clinic_name |
| `instagram.com/direct` | https://instagram.com/direct/t/inbox/ |

### YouTube
| Pattern | Example |
|---------|---------|
| `youtube.com/@` | https://youtube.com/@clinic_name |
| `youtube.com/c/` | https://youtube.com/c/clinic_channel |

### Naver Blog
| Pattern | Example |
|---------|---------|
| `blog.naver.com/` | https://blog.naver.com/clinic_name |

### Facebook
| Pattern | Example |
|---------|---------|
| `facebook.com/` | https://www.facebook.com/clinic.name |

### Phone (Korean consultation)
| Pattern | Example |
|---------|---------|
| `tel:` links | `<a href="tel:+821012345678">` |
| Korean format in text | 010-1234-5678, 02-1234-5678 |
| International format | +82-10-1234-5678 |

Korean phone regex: `(?:0\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}|\+82[-.\s]?\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4})`

### SMS
| Pattern | Example |
|---------|---------|
| `sms:` links | `<a href="sms:+821012345678?body=상담">` |

### Deep Links (App-specific URIs)
| Scheme | Platform |
|--------|----------|
| `kakao://` | KakaoTalk |
| `line://` | Line |
| `weixin://` | WeChat |
| `instagram://` | Instagram |

## Extraction Locations (Priority Order)

1. `href` attributes in `<a>` tags (including `tel:`, `sms:`)
2. `onclick` handlers (`href='#none'` pattern)
3. `position:fixed` floating elements
4. Footer sections
5. `meta` tags (`og:url`, `description`)
6. `iframe src` attributes (including sandboxed)
7. JavaScript variables and SDK initialization
8. QR code images (especially WeChat)
9. JSON-LD structured data (`sameAs[]`, `contactPoint`)
10. CSS pseudo-elements (`::before`, `::after` content property)

## Six-Pass Extraction Strategy

### Pass 1: Static DOM (`extraction_method: "dom_static"`)
- Scan all `<a href>` attributes for platform URL patterns
- **Include `tel:` and `sms:` links** as Phone/SMS channels (`extraction_method: "phone_text"`)
- Check footer, sidebar, header sections
- Look for floating elements (`position:fixed`, `position:sticky`) → `extraction_method: "floating_element"`

### Pass 1.5: iframe Detection (`extraction_method: "iframe"`)
- Use `browser_evaluate` to find all `<iframe>` elements:
  ```javascript
  Array.from(document.querySelectorAll('iframe')).map(f => ({src: f.src, id: f.id, class: f.className, sandbox: f.sandbox?.value || ''}))
  ```
- Check iframe `src` for social platform domains (kakao, naver, line)
- Check for chat widget iframes (channel.io, zendesk, tawk.to, crisp)
- **Sandboxed iframes**: Read src from parent DOM attribute, not iframe content
- If iframe contains a social channel, record with `extraction_method: "iframe"`

### Pass 1.75: Structured Data (`extraction_method: "structured_data"`)
- Parse `<script type="application/ld+json">` blocks:
  ```javascript
  Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => {
    try { return JSON.parse(s.textContent); } catch(e) { return null; }
  }).filter(Boolean)
  ```
- Extract: `sameAs[]` arrays (social profiles), `contactPoint.telephone`
- Also check: `<meta property="og:see_also">`, `<meta name="contact">`
- Record with `extraction_method: "structured_data"`

### Pass 2: Dynamic JavaScript (`extraction_method: "dom_dynamic"`)
- Check `onclick` handlers (common pattern: `href="#none"` with `onclick="window.open('...')"`)
- **Decode obfuscated links**: Look for `atob()`, `decodeURIComponent()`, `unescape()` in handlers
- **Async handlers**: Extract URLs from `setTimeout(() => window.open(...))` patterns
- Detect chat widget SDKs (`extraction_method: "widget_sdk"`):
  - Kakao Channel: `window.Kakao?.Channel`
  - channel.io: `window.ChannelIO`
  - tawk.to: `window.tawk_chat`
  - Crisp: `window.Crisp?.chat`
  - Zendesk: `window.zE`
- Extract SDK initialization parameters for actual social links
- Use `browser_evaluate` to extract hidden social links from JS variables
- Record with `extraction_method: "dom_dynamic"` or `"widget_sdk"`

### Pass 2.5: Scroll-triggered Elements (`extraction_method: "scroll_triggered"`)
- Simulate scroll to reveal lazy-loaded floating chat buttons:
  ```javascript
  window.scrollTo(0, document.body.scrollHeight / 2);
  window.dispatchEvent(new Event('scroll'));
  ```
- Wait 2000ms for scroll-triggered widgets to appear
- Re-scan for `position:fixed` elements not found in Pass 1
- Record with `extraction_method: "scroll_triggered"`

### Pass 3: QR Codes (`extraction_method: "qr_decode"`)
- Find `<img>` tags with QR-related attributes (`qr`, `wechat`, `weixin`, `kakao`)
- Download and decode using image analysis
- Convert decoded URLs to social links

### Pass 4: URL Validation
For each extracted URL:
1. **Format check**: Verify URL has valid scheme
   - Accept: `http://`, `https://`, `tel:`, `sms:`, `kakao://`, `line://`, `weixin://`
2. **Honeypot filter**: Skip CSS-hidden links
   ```javascript
   const style = getComputedStyle(el);
   if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0' || el.offsetHeight === 0) continue;
   ```
3. **De-duplicate**: Normalize URLs (strip trailing slash, remove tracking params)
   - Remove: `?utm_*`, `?ref=*`, `?fbclid=*`, `?gclid=*`
4. **Platform classify**: Match normalized URL to platform patterns above
5. **Dead link detection**: If URL returns immediate redirect to error page or generic domain, mark as `"status": "dead"`
6. **Korean phone extraction**: Scan page text for phone patterns not in `<a>` tags
