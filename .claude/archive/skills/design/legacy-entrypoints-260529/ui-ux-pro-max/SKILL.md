---
name: ui-ux-pro-max
description: "LEGACY 디자인 데이터베이스. 일반 UI/UX 디자인, 리디자인, 스타일/컬러/타이포그래피/UX 의사결정은 design-harness를 사용한다. 이 스킬은 사용자가 명시적으로 과거 CSV 검색/--design-system 스크립트 실행을 요청할 때만 사용한다."
metadata:
  category: "🎨 디자인"
  version: "legacy-2026-05"
  replacement: "design-harness"
---

# UI/UX Pro Max (Legacy)

This skill is no longer the primary design entrypoint.

Use `design-harness` for:

- New UI/UX design.
- Landing pages, dashboards, admin UI, product UI, mobile web, portfolios.
- Redesigns and visual QA.
- Style, color, typography, layout, motion, and accessibility decisions.
- Anti-slop preflight and production polish.

Use this legacy skill only when the user explicitly asks for the old searchable database or scripts.

## Legacy Scripts

The CSV database and search scripts are still available:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system -p "Project Name"
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --domain <product|style|color|typography|chart|ux|landing>
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<query>" --stack <react|nextjs|react-native|flutter|swiftui|html-tailwind>
```

Treat the output as raw reference material, not final direction. Pass any useful findings through `design-harness` before implementation.

## Migration Note

The old file mixed planning, UX rules, app/mobile rules, Korean locale guidance, stack guidance, and anti-slop snippets in one large context payload. That made the skill expensive to load and encouraged template-like outputs. The replacement architecture is:

```text
design-harness  -> primary UI/UX design, audit, polish, redesign
ui-styling      -> shadcn/Tailwind/component implementation
design-system   -> tokens/CSS variables/component specs
design          -> asset/CIP/social/slides orchestration
logo-creator    -> logos and app icons
banner-design   -> banners and cover images
```
