# Text To Lottie Harness Integration

Date: 2026-06-13
Status: applied
Source: <https://github.com/diffusionstudio/lottie>

## Why

`diffusionstudio/lottie` is an open-source text-to-Lottie harness for generating production-ready Lottie animations with coding agents. Its useful part for Claude Craft is not just the prompt guidance; it standardizes a local preview and verification loop around a Vite React player using CanvasKit's Skottie renderer.

## Source Read

The upstream repository provides:

| Area | Finding | Integration decision |
|---|---|---|
| Skill trigger | `text-to-lottie` should be used for Lottie generation, editing, and repair | Add a local `text-to-lottie` skill with Korean/English trigger terms |
| Player harness | Use the official `diffusionstudio/lottie` project, scaffolded by `degit` | Require official player for preview instead of a hand-rolled HTML viewer |
| Runtime | CanvasKit/Skottie, not `lottie-web` | Validate against Skottie-specific failure modes such as blank canvases from ungrouped shapes |
| File contract | Edit `public/lottie.json`; optional `public/controls.json` describes slots | Preserve the contract in the local skill |
| Browser QA | Use `?frame=N&paused=1` and canvas screenshot hooks for deterministic inspection | Add pinned-frame verification to the workflow |
| Authoring rules | Top-level Lottie shape, grouped primitives, normalized RGBA, array keyframe values, slots | Add explicit mechanical rules and a local validator |

## Local Changes

- Added `.claude/skills/text-to-lottie/SKILL.md`.
- Added `.claude/skills/text-to-lottie/scripts/validate-lottie.mjs`.
- Linked `design-harness` animate/motion guidance to `text-to-lottie` when the deliverable is Lottie JSON.
- Added routing entries in `.claude/skills/design/ROUTING.md` and `.claude/rules/common/agent-orchestration.md`.
- Updated the UI design agent reference loading section.

## Boundary

`design-harness` still owns the design read, register, motion intent, timing judgment, and anti-slop review. `text-to-lottie` owns Bodymovin JSON mechanics, Skottie slot controls, official player setup, and frame-level verification.

Do not route normal CSS/Framer Motion UI transitions to `text-to-lottie`. Do not route Remotion video timelines to it. Use it when the final asset is a Lottie/Bodymovin JSON animation.

## Verification

The local validator checks:

- required top-level Lottie fields
- shape-layer group wrapping
- group transform placement
- keyframe scalar array shape
- normalized RGBA colors
- background color slot and matching `controls.json` entry
- background layer placement

Future improvement: add a generated sample fixture and a browser screenshot regression once a real project starts producing Lottie assets.
