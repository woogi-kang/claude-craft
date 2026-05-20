# Product/Brand Visual Deck Review

Date: 2026-05-18
Archetype: Product/brand visual deck
Deck: `index.html`

## Result

Status: Product/brand visual archetype pass

Passed:
- Future Slide vendor validator: pass, 8 slides
- Future Slide QA: desktop 1366x768, 8 PASS / 0 WARN / 0 FAIL
- Layout QA checks: offscreen/overflow/padding/word-breaking issues are 0
- Image slots: S22 hero image only; module meaning moved into HTML cards
- Image metadata: `asset_manifest.json` includes slot, file, prompt, alt, generator status, and visual contract
- CLI/native image asset: generated via `codex-native-image-cli`, 1911x819, exact 21:9
- Semantic graphic review: left evidence repository, middle citation paths, and right answer surface are visually legible
- Manual visual review: fixed Korean word-breaking issues on slides 2, 5, and 8
- Slide 4: changed from sparse S08 compare cards to denser S20 ledger
- Slide 6: removed low-meaning generated thumbnails and replaced them with semantic HTML module cards

Still not a replacement approval:
- This only clears the product/brand visual archetype.
- PPTX/PDF export parity and the remaining archetypes still need separate validation.

## Files

```text
docs/260518-future-slide-product-brand-visual/
├── index.html
├── asset_manifest.json
├── generate-answerlayer-brand-deck.cjs
├── images/
└── qa/
    ├── qa-report.md
    └── contact-sheet.png
```

## QA Commands

```bash
node ".claude/skills/📝 콘텐츠/future-slide-skills/_vendor/future-slide-skill/skills/tightened-slide/scripts/validate-deck.mjs" docs/260518-future-slide-product-brand-visual/index.html
node ".claude/skills/📝 콘텐츠/future-slide-skills/future-slide-qa/scripts/check-tightened-deck.cjs" docs/260518-future-slide-product-brand-visual/index.html --out docs/260518-future-slide-product-brand-visual/qa --allow-warnings
```

## Replacement Criteria Impact

| Criteria | Status | Note |
|---|---|---|
| Product/brand visual deck layout | Pass | 8 slides, 7 layout families |
| Overflow/padding/word-breaking QA | Pass | automated QA + manual visual review |
| Asset manifest workflow | Pass | prompt/slot/alt/status/visual contract recorded |
| Semantic graphic quality | Pass | evidence repository -> citation paths -> answer surface |
| CLI/native image asset quality | Pass | `generator: codex-native-image-cli` |
| Existing PPT agent replacement | Not approved | still needs remaining archetypes and export parity |

## QA Improvement

`future-slide-qa` now inspects rendered text lines and flags Korean orphan particles/sentence endings such as `다.` rendered alone. A synthetic regression with `다.` on its own line exits non-zero and reports:

```text
Korean orphan particle or sentence ending rendered as its own line.
```
