# Workflows

Use this file to choose the right operating mode.

## Shape

Use before code when direction or scope is unclear.

Output:

- Design read.
- Reference stance when a brand, product, site, or proven design direction is relevant.
- Register and dial values.
- Surface map: sections/screens/components.
- Visual stance and anti-goals.
- Key assets needed.
- Open questions limited to blockers.
- Validation method.

Do not create a long generic design brief when a compact plan is enough.

## Craft

Use when building a page/screen/component.

Steps:

1. Inspect existing stack, tokens, components, and package dependencies.
2. Decide register, reference stance, and dials.
3. Translate borrowed reference grammar into local tokens, components, and layout rules.
4. Identify the one visual idea or product usability goal.
5. Implement with existing primitives where they fit.
6. Add necessary states and responsive behavior.
7. Run mechanical preflight.
8. Run browser/screenshot QA when possible.

## Measure

Use when a concrete URL, screenshot, or product reference should inform local tokens or styling.

Steps:

1. Read `references/reference-style-extraction.md`.
2. Capture source evidence: CSS, computed styles, screenshots, or clearly marked visual estimates.
3. Produce a compact `design.md` with token roles, provenance, transfer rules, and do-not-borrow guardrails.
4. Choose apply level:
   - `L1 tokens`: typography scale, spacing, color roles, radius, shadows.
   - `L2 style`: tokens plus component treatment and state styling.
   - `L3 redesign`: layout/IA changes only with explicit approval.
5. Map reference grammar into the current project's tokens/components.
6. Verify the result does not copy brand identity, proprietary art, exact layout, or trademarked chrome.

## Audit

Use for review without immediately rewriting.

Lead with:

| Before | After | Why |
|---|---|---|

Prioritize:

1. Broken usability or accessibility.
2. Layout/responsive failures.
3. Missing states.
4. AI slop signatures.
5. Visual polish.

## Polish

Use after a surface exists and mostly works.

Order of operations:

1. Fix readability and contrast.
2. Fix spacing rhythm and hierarchy.
3. Remove generic filler elements.
4. Add or correct interaction states.
5. Apply interface polish: text wrapping, dynamic numerals, optical alignment, radius math, image edges, hit areas, and transition specificity.
6. Improve assets and copy.
7. Tune motion only where it communicates.

## Redesign

Use for existing projects.

1. Detect mode: preserve, evolve, or overhaul.
2. Inventory current font, palette, radius, shadows, spacing, icon set, section patterns.
3. Pick primary, secondary, and anti-reference if the redesign needs outside direction.
4. List top 5 slop signatures and top 5 trust/usability issues.
5. Fix in low-risk order: typography, color tokens, interaction states, spacing, layout, assets, motion.
6. Preserve URL structure, form field names, legal copy, analytics hooks, and product behavior unless requested.

## Harden

Use before ship.

- Text overflow and longest words.
- Empty/loading/error/disabled/focus states.
- Keyboard and screen-reader access.
- Reduced motion.
- Mobile nav and touch targets.
- Image dimensions and CLS.
- Transition hygiene and `will-change` usage.
- Dynamic numeric alignment.
- i18n and Korean line breaking where relevant.
