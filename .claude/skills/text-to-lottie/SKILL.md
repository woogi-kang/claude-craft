---
name: text-to-lottie
description: "Lottie/Bodymovin JSON 애니메이션을 생성, 수정, 검증하는 스킬. 사용자가 Lottie, 로티, Bodymovin, Skottie, animated JSON, lottie.json, controls.json, SVG/path를 움직이는 Lottie로 만들기, 로딩/아이콘/마케팅 모션 에셋을 요청하면 반드시 사용한다. 공식 diffusionstudio/lottie CanvasKit 플레이어 하네스로 preview와 validation까지 끝낸다."
license: MIT
metadata:
  category: "🎨 디자인"
  version: "0.1.0"
  tags: "lottie, bodymovin, skottie, animation, motion, design-harness"
  source: "diffusionstudio/lottie skills/text-to-lottie, adapted 2026-06-13"
---

# Text To Lottie

Lottie/Bodymovin JSON을 직접 작성하고, Skia Skottie 기반 플레이어에서 실제 렌더링까지 확인하는 제작 하네스다. 원본 분석 기준은 `diffusionstudio/lottie`의 `skills/text-to-lottie`와 공식 Vite/CanvasKit 플레이어다.

이 스킬은 모션의 미감보다 **렌더 가능한 Lottie 파일의 기계적 정확성**을 책임진다. 모션 의도, 타이밍, 제품/브랜드 적합성은 먼저 `design-harness`의 `animate` 흐름과 `.claude/skills/design-harness/references/motion-interaction.md`로 정한다.

## When To Use

Use this skill when the user asks for:

- Lottie, 로티, Bodymovin, Skottie, `lottie.json`, `controls.json`
- SVG path, 로고, 아이콘, loader, empty state, onboarding illustration을 움직이는 JSON으로 만들기
- 기존 Lottie가 blank canvas, parse error, 색상/크기/프레임 문제를 내는 경우
- 웹/모바일 앱에 넣을 작은 모션 에셋을 코드로 생성해야 하는 경우

Do not use it for Remotion videos, CSS micro-interactions, or general UI transitions unless the deliverable is a Lottie JSON file.

## Core Flow

1. **Ground the animation**
   - Prefer concrete input: SVG path, existing icon geometry, screenshots, brand colors, timing, duration, target size.
   - If the user only asks for "nice animation", make one small assumption about role and context, then proceed.

2. **Use the official player harness**
   - If no player project exists, scaffold it with:

     ```bash
     npx degit diffusionstudio/lottie my-lottie-animation
     cd my-lottie-animation
     npm install
     npm run dev
     ```

   - If the project already exists, run `npm install` if dependencies are missing, then `npm run dev`.
   - Do not hand-roll a custom HTML viewer or swap in `lottie-web` for verification. The harness behavior depends on CanvasKit/Skottie, slot support, `controls.json`, and frame-pinned URLs.

3. **Write the animation**
   - Put the generated file at `public/lottie.json`.
   - Put optional presentation metadata at `public/controls.json`.
   - The player fetches `/lottie.json` at startup and watches `public/lottie.json` plus `public/controls.json` for full reloads.

4. **Validate before browser inspection**
   - Run JSON parsing and the local validator:

     ```bash
     node -e "JSON.parse(require('fs').readFileSync('public/lottie.json','utf8'))"
     node /Users/woogi/Development/claude-craft/.claude/skills/text-to-lottie/scripts/validate-lottie.mjs public/lottie.json public/controls.json
     ```

5. **Verify rendered frames**
   - Open the local Vite URL.
   - Inspect deterministic frames with query params instead of dragging controls:

     ```text
     http://localhost:5173/?frame=60&paused=1
     ```

   - When a browser tool is available, screenshot the canvas at key frames and confirm it is nonblank, positioned correctly, and not clipped.

## Required Lottie Shape

Every generated document is one JSON object with:

```json
{
  "v": "5.7.0",
  "fr": 60,
  "ip": 0,
  "op": 120,
  "w": 512,
  "h": 512,
  "assets": [],
  "layers": []
}
```

- `fr` is frames per second.
- `ip` and `op` define the timeline. Duration is `(op - ip) / fr` seconds.
- Use a square or intentionally chosen aspect ratio. The player letterboxes the composition into the canvas.
- Layer order follows After Effects semantics: earlier array entries render above later entries.

## Layer Rules

Prefer shape layers (`"ty": 4`) for generated assets because they do not need external files.

Each visible shape layer needs:

```json
{
  "ty": 4,
  "nm": "layer-name",
  "ip": 0,
  "op": 120,
  "st": 0,
  "ks": {
    "o": { "a": 0, "k": 100 },
    "r": { "a": 0, "k": 0 },
    "p": { "a": 0, "k": [256, 256, 0] },
    "a": { "a": 0, "k": [0, 0, 0] },
    "s": { "a": 0, "k": [100, 100, 100] }
  },
  "shapes": []
}
```

Anchor points matter: rotation and scale pivot around `ks.a`, in the layer's local coordinate space. Put geometry around the anchor when a shape should rotate around its own center.

## Shape Group Rule

Skottie commonly renders blank when primitives sit directly in `shapes`. Wrap geometry, fill/stroke, and group transform inside a group:

```json
"shapes": [
  {
    "ty": "gr",
    "nm": "icon-group",
    "it": [
      { "ty": "el", "p": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [120, 120] } },
      { "ty": "fl", "c": { "a": 0, "k": [0.2, 0.6, 1, 1] }, "o": { "a": 0, "k": 100 } },
      { "ty": "tr", "p": { "a": 0, "k": [0, 0] }, "a": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [100, 100] }, "r": { "a": 0, "k": 0 }, "o": { "a": 0, "k": 100 } }
    ]
  }
]
```

Common shape primitives:

- `el`: ellipse, with `p` center and `s` size
- `rc`: rectangle, with `p`, `s`, and `r` corner radius
- `sh`: custom bezier path, with `ks.k` containing `c`, `v`, `i`, `o`
- `fl`: fill, with RGBA color values normalized from `0` to `1`
- `st`: stroke, with color, width, and opacity
- `tr`: group transform; include it last in every group

## Keyframes

Set a property to animated with `"a": 1` and use keyframe objects:

```json
"p": {
  "a": 1,
  "k": [
    { "t": 0, "s": [256, 120, 0], "i": { "x": [0.5], "y": [1] }, "o": { "x": [0.5], "y": [0] } },
    { "t": 60, "s": [256, 400, 0], "i": { "x": [0.5], "y": [1] }, "o": { "x": [0.5], "y": [0] } },
    { "t": 120, "s": [256, 120, 0] }
  ]
}
```

- `t` is the frame number.
- `s` is always an array, including scalar values like rotation: `"s": [360]`.
- For seamless loops, repeat the first value at the final keyframe.
- Keep keyframes inside the document `ip`/`op`, and layer `ip`/`op`.

## Slots And Controls

Use Skottie slots when the animation should expose editable values in the player. Declare a top-level `slots` object, then reference values by `sid`.

```json
"slots": {
  "accentColor": { "p": { "a": 0, "k": [0.2, 0.6, 1, 1] } },
  "markSize": { "p": { "a": 0, "k": [120, 120] } }
}
```

Example usage:

```json
{ "ty": "fl", "c": { "sid": "accentColor" }, "o": { "a": 0, "k": 100 } }
```

Describe labels and slider ranges in `public/controls.json`:

```json
{
  "controls": [
    { "sid": "accentColor", "label": "Accent color" },
    { "sid": "markSize", "label": "Mark size", "min": 40, "max": 240, "step": 1 }
  ]
}
```

Every generated animation must expose a background color control:

- Add a full-composition background rectangle as the last layer, so it renders underneath everything.
- Fill it with a color slot named `bgColor` or another clearly background-named slot.
- Add a matching `controls.json` entry with a readable label such as `Background color`.

## Verification Checklist

Before finishing:

- `public/lottie.json` parses as strict JSON.
- `validate-lottie.mjs` passes with no errors.
- Shape primitives are inside `"ty": "gr"` groups and every group includes a final `"tr"` transform.
- Colors are normalized RGBA values, not `0-255`.
- `op` covers every animated frame and each layer's visibility range.
- Keyframe `s` values are arrays.
- The background layer is last, fills the full composition, uses a background color slot, and has a `controls.json` label.
- The official player runs and at least one pinned frame renders nonblank.

## Result Format

When reporting back, include:

- Player URL or local path.
- Files changed: `public/lottie.json`, `public/controls.json`, and any source SVG/assets.
- Validation commands run.
- Frames inspected, for example `0`, midpoint, final loop frame.
