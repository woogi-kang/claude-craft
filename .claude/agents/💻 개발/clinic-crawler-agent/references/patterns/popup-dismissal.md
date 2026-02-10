# Popup Dismissal Strategies

Reference data for dismissing popups on Korean clinic websites before crawling.

## Detection

Container selectors (check visibility via display, opacity, z-index):
- `.popup`, `.modal`, `.layer-popup`, `.pop-layer`
- `#popup`, `[class*='popup']`, `[class*='modal']`, `[role='dialog']`

Rules:
- Max 3 dismissal attempts per page
- Wait 500ms after each close action
- Re-check for new popups after dismissal

## Strategy 1: X Button (Priority 1)

Click close button with X icon or close class.

Selectors:
- `button.close`, `.popup-close`, `.modal-close`, `.btn-close`
- `[aria-label='닫기']`, `[aria-label='Close']`
- `.popup .close`, `.modal .close`
- `.layer-close`, `.pop-close`, `.closeBtn`, `.close-btn`

## Strategy 2: Text Button (Priority 2)

Click button containing close text.

Korean text: `닫기`, `확인`, `창닫기`, `팝업닫기`
English text: `CLOSE`, `Close`, `OK`

## Strategy 3: Checkbox Then Close (Priority 3)

First check "don't show again" checkbox, then click close.

Checkbox selectors:
- `input[type='checkbox']`
- `.today-close input`, `.popup-today input`

Checkbox labels to match:
- `오늘 하루동안 열지않기`, `오늘 하루 열지 않기`
- `오늘 그만 보기`, `다시 보지 않기`
- `하루동안 보지않기`, `Don't show today`

Important: Must check checkbox BEFORE clicking close button.

## Strategy 4: Overlay Click (Priority 4)

Click background overlay to dismiss.

Selectors:
- `.modal-backdrop`, `.popup-overlay`, `.popup-bg`
- `.dim`, `.dimmed`, `.overlay`

## Strategy 5: Age Verification Gate (Priority 5)

Classify age verification popups into two types before acting:

**Type A - Informational confirmation** (auto-accept):
- Simple "예/아니오" or "네, 19세 이상입니다" button without input fields
- Detection: No `input[type="text"]`, no `input[type="tel"]`, no authentication module
- Action: Click the affirmative button ("예", "네", "19세 이상", "확인")
- Selectors:
  - `button:has-text("예")`, `button:has-text("네")`
  - `button:has-text("19세 이상")`, `a:has-text("성인입니다")`

**Type B - Real identity verification** (skip):
- Requires phone number, resident registration number, or 3rd-party auth module
- Detection: `input[type="text"]`, `input[type="tel"]`, iframe with auth provider
- Action: Mark as `age_restricted`, do not bypass
- Auth provider markers: `nice.checkplus`, `dreamsecurity`, `inicis.com/auth`

Classification logic:
```javascript
const hasInputField = document.querySelector('input[type="text"], input[type="tel"], input[type="number"]');
const hasAuthIframe = document.querySelector('iframe[src*="nice"], iframe[src*="dreamsecurity"], iframe[src*="inicis"]');
if (hasInputField || hasAuthIframe) return 'TYPE_B_REAL_AUTH';
else return 'TYPE_A_INFORMATIONAL';
```

## Strategy 6: Google Maps Embedded Info (Priority 6)

Extract contact info from embedded Google Maps iframes:

Detection: `iframe[src*="google.com/maps"]`
Action:
- Parse iframe `src` URL for `!1s` place identifier
- Check surrounding DOM elements for phone/address text
- Look for `<a href="tel:">` links near the maps iframe
- Record phone numbers with `extraction_method: "maps_embed"`

## Cookie Suppression

Set cookies before page load to prevent popups:
- `popup_close`, `todayClose`, `popup_today`, `layer_close`

Use `browser_evaluate` to set:
```javascript
document.cookie = "popup_close=done; path=/; max-age=86400";
```
