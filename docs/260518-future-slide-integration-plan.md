# Future Slide Integration Plan

Date: 2026-05-18
Status: Phase 1 setup

## 결론

`future-slide-skill`은 기존 PPT agent를 즉시 대체하지 않고, HTML visual deck 전용 경로로 먼저 편입한다.

이유:
- Future Slide는 locked HTML layout과 visual QA에 강하다.
- 기존 `presentation-agent`는 리서치, 검증, 구조화, PPTX/PDF export까지 포함한다.
- `.claude/skills`가 Codex/Gemini/OpenCode의 Single Source of Truth라서 외부 스킬을 직접 덮으면 충돌 범위가 크다.

## 설치 방식

원본 repo는 vendor로 보존하고, 실제 호출은 wrapper skill을 통한다.

```text
.claude/skills/📝 콘텐츠/future-slide-skills/
├── _vendor/future-slide-skill/
├── future-tightened-slide/
├── future-slide-design/
├── future-slide-asset-gen/
└── future-slide-qa/
```

`_vendor` 내부 원본 스킬 파일은 자동 스킬 스캔 충돌을 피하기 위해 `SKILL.md`가 아니라 `VENDOR_SKILL.md`로 보존한다. Codex가 직접 트리거하는 스킬은 `future-*` wrapper만이다.

## Routing

| 요청 유형 | 기본 경로 |
|---|---|
| PPTX, PowerPoint, 편집 가능한 발표자료 | `presentation-agent` |
| HTML 덱, Tightened Slide, Future Slide | `future-tightened-slide` |
| Chart.js/data-driven HTML 프레젠테이션 | `slides` |
| 이미지 기반 visual asset이 필요한 Future Slide | `future-slide-asset-gen` 후 `future-tightened-slide` |
| 제출용 PDF/PPTX까지 필요한 Future Slide | `future-tightened-slide` 후 기존 `export-pdf`/`export-pptx` 검토 |

## 이미지 생성 정책

이미지 생성은 Codex native image generation/CLI workflow로 진행한다.

원칙:
- vendor의 `gpt-image-slide-render/VENDOR_SKILL.md`처럼 한 장 또는 한 asset씩 순차 생성한다.
- 생성 직후 육안 검수하고, 선택한 결과만 workspace의 `images/` 또는 `page_<n>.png`로 복사한다.
- `asset_manifest.json`에는 `generator: "codex-native-image-cli"`와 생성 상태를 기록한다.
- CLI/native generation을 실행하지 못한 local fallback/placeholder는 production visual로 인정하지 않는다.

덱에서는 전체 슬라이드 이미지를 만들지 않는다. 텍스트는 HTML/PPT 레이어에 유지하고, 이미지는 hero visual, diagram base, icon, texture, object illustration만 생성한다.

## QA Gate

Future Slide 덱은 아래 순서를 통과해야 한다.

```bash
node ".claude/skills/📝 콘텐츠/future-slide-skills/_vendor/future-slide-skill/skills/tightened-slide/scripts/validate-deck.mjs" path/to/index.html
node ".claude/skills/📝 콘텐츠/future-slide-skills/future-slide-qa/scripts/check-tightened-deck.cjs" path/to/index.html --out path/to/qa
```

검사 항목:
- layout registry 위반
- offscreen
- overflow
- padding/safe area
- bottom navigation collision
- Korean word breaking
- image load/alt/data-image-slot
- S15/S16/S22 image slot consistency

## Replacement Criteria Review

현재 판정: Shadow Mode

| 기준 | 현재 상태 | 판정 |
|---|---|---|
| HTML visual deck 품질 | SEO -> AEO 3개 variant에서 자동 QA 통과 | 통과 |
| 한국어 layout/word break | 샘플 기준 PASS, 더 많은 주제 필요 | 부분 통과 |
| 이미지 asset 생성 | Product/brand visual deck에서 CLI/native image asset, slot/manifest/QA, semantic review 통과 | 부분 통과 |
| PPTX/PDF export parity | 기존 export 스킬과 연동 검토 필요 | 미통과 |
| 리서치/검증/구조화 parity | 기존 PPT agent가 우위 | 미통과 |
| 자동 QA 재현성 | Playwright QA 스크립트 편입 | 부분 통과 |

## 대체 전 필수 Archetype

1. Executive KPI report
2. Workshop/framework deck
3. Product/brand visual deck
4. Dense data/chart deck
5. PPTX/PDF handoff deck

각 archetype은 validator error 0건, visual QA FAIL 0건, screenshot/contact sheet 생성, 이미지 텍스트 오류 0건, export 필요 시 PPTX/PDF 육안 검수를 통과해야 한다.

## Retire 정책

기존 `presentation-agent`와 PPT skills는 아직 제거하지 않는다.

Retire/Merge는 다음 조건을 모두 만족할 때만 진행한다.
- 5개 archetype 통과
- 이미지 asset workflow 통과
- PPTX/PDF export parity 통과
- `/skill-audit`에서 Retire/Merge 후보로 판정
- 사용자 확인 완료

## Validation Notes

Phase 1 smoke test:
- vendor `validate-deck.mjs` on SEO -> AEO sample: pass, 8 slides
- `future-slide-qa` on SEO -> AEO sample: desktop 1366x768, 8 PASS / 0 WARN / 0 FAIL
- new `future-*` SKILL.md frontmatter: pass

Product/brand visual archetype:
- deck: `docs/260518-future-slide-product-brand-visual/index.html`
- vendor `validate-deck.mjs`: pass, 8 slides
- `future-slide-qa`: desktop 1366x768, 8 PASS / 0 WARN / 0 FAIL
- image asset manifest: present, 1 hero image asset with slot/prompt/alt/status/visual contract
- hero image: generated via Codex native image generation/CLI, 1911x819 exact 21:9
- QA now fails local preview/fallback images unless the manifest records `generator: "codex-native-image-cli"`
- slide 4 changed from sparse comparison cards to dense S20 ledger
- slide 6 moved module meaning from generated thumbnails to HTML semantic cards
- QA now detects rendered Korean orphan endings such as `다.` on a line by itself

전체 `scripts/validate-skills.sh`는 통과한다.

```text
Total SKILL.md files: 392
With frontmatter:     392
Without frontmatter:  0
```
