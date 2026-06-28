# Reference Style Extraction

Use this workflow when the user names a URL, product, or site as a design reference and wants the local UI to borrow its design grammar.

The goal is measured inspiration, not cloning. Extract reusable choices such as type scale, spacing rhythm, component density, interaction tone, and color roles. Do not copy logos, proprietary artwork, exact layouts, trademarked chrome, or a recognizable brand identity.

## Inputs

- Reference URL or local screenshot
- Target surface in the current project
- Desired apply level:
  - `L1 tokens`: palette, font scale, radius, shadows, spacing only
  - `L2 style`: tokens plus component styling and state treatment
  - `L3 redesign`: layout and IA changes, only with explicit user approval

## Extraction Steps

1. Capture evidence.
   - Prefer actual CSS, design tokens, computed styles, screenshots, and browser inspection.
   - Use `web-access-ladder` if the public reference page is hard to fetch.
   - If only screenshots are available, mark all measurements as visual estimates.

2. Build `design.md`.
   - Source URL and retrieval date
   - Fonts and type scale
   - Color roles with hex values and provenance
   - Spacing rhythm
   - Radius and border treatment
   - Elevation/shadow treatment
   - Component patterns
   - Motion and interaction tone
   - What to borrow
   - What not to borrow

3. Apply locally.
   - Map reference grammar to existing tokens and components.
   - Preserve current product behavior, legal copy, analytics hooks, and data contracts.
   - For Korean products, run `korean-typography` before finalizing font choices.

4. Verify.
   - Run design-harness mechanical preflight.
   - Run browser/screenshot QA when the project is runnable.
   - Confirm the result is not a copy of the reference identity.

## Report Template

```markdown
# Reference Extraction: {name}

## Source
- URL:
- Retrieved:
- Evidence: CSS|computed styles|screenshot|estimate

## Measured Tokens
| Role | Value | Evidence |
|---|---|---|

## Transfer Rules
| Borrow | Local Mapping | Guardrail |
|---|---|---|

## Do Not Borrow
-

## Verification
-
```
