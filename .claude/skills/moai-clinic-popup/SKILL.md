---
name: moai-clinic-popup
description: >
  Popup and dialog dismissal patterns for Korean skin clinic websites.
  Covers 4 close mechanisms (X button, text button, checkbox-first,
  overlay click), cookie suppression, and multi-popup handling.
  Use when encountering popups, modals, or dialogs on clinic websites.
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
  tags: "clinic, popup, modal, dialog, close, dismiss, overlay"

# MoAI Extension: Progressive Disclosure
progressive_disclosure:
  enabled: true
  level1_tokens: 100
  level2_tokens: 3000

# MoAI Extension: Triggers
triggers:
  keywords:
    - "popup"
    - "modal"
    - "dialog"
    - "overlay"
    - "banner"
    - "팝업"
    - "dismiss"
  agents:
    - "clinic-crawler-agent"
  phases:
    - "run"
---

# Popup Dismissal

## Detection

After navigating to a clinic website, check for visible popups:

Container selectors (check display/visibility/opacity):
- .popup, .modal, .layer-popup, .pop-layer
- #popup, [class*='popup'], [class*='modal']
- [role='dialog']

## Close Strategy (Priority Order)

### Strategy 1: X Button (Most Common)
```
Selectors:
  button.close, .popup-close, .modal-close, .btn-close
  [aria-label='닫기'], [aria-label='Close']
  .popup .close, .layer-close, .pop-close
  .closeBtn, .close-btn
```

### Strategy 2: Text Button
```
Look for buttons/links containing:
  "닫기", "CLOSE", "Close", "확인", "OK"
  "창닫기", "팝업닫기"
```

### Strategy 3: Checkbox + Close (Korean Specialty)
Many Korean sites require checking a checkbox BEFORE the close button works:
```
Step 1: Check the checkbox
  Labels: "오늘 하루동안 열지않기", "오늘 하루 열지 않기"
          "오늘 그만 보기", "다시 보지 않기"
Step 2: Then click the close button
```
WARNING: Must check checkbox FIRST, then close. Reverse order won't work.

### Strategy 4: Overlay Click
Click the dimmed background area:
```
  .modal-backdrop, .popup-overlay, .popup-bg
  .dim, .dimmed, .overlay
```

## Multi-Popup Handling

Some sites show 2-3 popups simultaneously or sequentially.

Algorithm:
1. Take snapshot, count visible popups
2. Close the topmost popup (highest z-index)
3. Wait 500ms
4. Take snapshot again
5. Repeat until no popups or max 3 attempts

## Cookie Suppression

Some popups can be prevented by setting cookies before navigation:
```javascript
document.cookie = "popup_close=Y; path=/";
document.cookie = "todayClose=Y; path=/";
```

Use browser_evaluate to set these cookies after initial navigation.

## Reference

See: .claude/agents/💻 개발/clinic-crawler-agent/references/patterns/popup-dismissal.md
