# future-slide-skill 도입 검토

검토일: 2026-05-18

## 요약 판단

`bytonylee/future-slide-skill`은 현재 PPT Agent를 대체하기보다는 보조 워크플로우로 제한 도입하는 것이 맞다.

- 기존 `presentation-agent`는 리서치 -> 검증 -> 구조 -> 콘텐츠 -> 디자인 -> 시각화 -> 리뷰 -> PPTX/PDF 출력까지 담당하는 종합 PPT 제작 체계다.
- `future-slide-skill`은 1) 참고 이미지 기반 디자인 추출 후 페이지 이미지 생성, 2) locked-layout HTML swipe deck 생성에 강하다.
- 편집 가능한 `.pptx`를 직접 만드는 기능은 핵심 범위가 아니다.
- 전역 설치하면 `tightened-slide`의 트리거가 넓어 기존 `presentation-agent`와 라우팅이 겹칠 수 있다.

권장: `future-*` 접두사를 붙여 project-local skill로 벤더링하고, 라우팅을 명확히 좁힌다.

## 외부 저장소 구성

확인한 저장소: `https://github.com/bytonylee/future-slide-skill`

주요 파일:

- `skills/slide-design/SKILL.md`
- `skills/gpt-image-slide/SKILL.md`
- `skills/gpt-image-slide-plan/SKILL.md`
- `skills/gpt-image-slide-prompt/SKILL.md`
- `skills/gpt-image-slide-render/SKILL.md`
- `skills/tightened-slide/SKILL.md`
- `skills/tightened-slide/assets/template.html`
- `skills/tightened-slide/scripts/validate-deck.mjs`
- `templates/DESIGN_TEMPLATE.md`

저장소 README 기준 산출물:

- 이미지 생성형: `DESIGN.md`, `slide_plan.json`, `slide_prompts.json`, `page_1.png ... page_N.png`
- HTML 덱형: `index.html`, `images/`, `validate-deck.mjs` 통과 결과

## 현재 환경의 PPT 관련 자산

현재 워크스페이스에는 이미 다음 체계가 있다.

- `.claude/agents/📝 콘텐츠/presentation-agent.md`
  - `ppt-research`, `ppt-validation`, `ppt-structure`, `ppt-content`, `ppt-design-system`, `ppt-visual`, `ppt-image-gen`, `ppt-review`, `ppt-refinement`, `export-pptx`, `export-pdf`
- `.claude/skills/slides/SKILL.md`
  - `ckm:slides`: 전략적 HTML 프레젠테이션, Chart.js, 디자인 토큰, 반응형 레이아웃
- `.claude/skills/📝 콘텐츠/presentation-agent-skills/10-export-pptx/SKILL.md`
  - HTML -> 브라우저 렌더링 -> DOM 분석 -> PptxGenJS 변환 -> PPTX 검증

## 중복 및 충돌 가능성

| 영역 | 기존 환경 | future-slide-skill | 판단 |
|---|---|---|---|
| PPT 전체 제작 | `presentation-agent`가 전체 파이프라인 관리 | `gpt-image-slide`가 이미지 덱 4단계 관리 | 역할 중복 있음. 기존 agent를 기본값으로 유지 |
| 구조 설계 | `ppt-structure` | `gpt-image-slide-plan` | 개념 중복. future는 이미지 생성용 JSON plan에 특화 |
| 콘텐츠/프롬프트 | `ppt-content`, `ppt-visual` | `gpt-image-slide-prompt` | 일부 중복. future는 page-level image prompt 전용 |
| 이미지 생성 | `ppt-image-gen` | `gpt-image-slide-render` | 중복. future는 page PNG 순차 생성 규칙이 더 강함 |
| HTML 덱 | `ckm:slides` | `tightened-slide` | 직접 충돌 가능. 둘 다 HTML deck 요청을 받을 수 있음 |
| PPTX 출력 | `export-pptx` | 직접 제공 없음 | 보완 관계. future 산출물을 PPTX로 만들려면 기존 export 파이프라인이 필요 |
| 검증 | `ppt-review`, export 검증 | `validate-deck.mjs` | 보완 가능. 단 검증 기준이 HTML locked layout에 한정 |
| 스킬 이름 | `slides`, `ppt-*`, `export-*` | `slide-design`, `gpt-image-slide-*`, `tightened-slide` | 이름 직접 충돌은 낮음. 라우팅 설명은 충돌 위험 있음 |

## 주의할 점

1. `tightened-slide` 설명이 넓다.
   - "launch deck, analysis deck, framework deck, product deck, data-driven talk" 요청에 반응하도록 되어 있어 기존 `presentation-agent`와 경쟁할 수 있다.

2. `gpt-image-slide`는 editable PPTX가 아니다.
   - 최종물이 `page_N.png` 이미지라 텍스트 편집성이 떨어진다.
   - 고객 제출용 PPTX가 필요하면 기존 `export-pptx`를 우선해야 한다.

3. README와 저장소명이 일부 어긋난다.
   - README 설치 예시는 `jyoung105/future-slide-skill`을 언급하지만 사용자가 준 저장소는 `bytonylee/future-slide-skill`이다.
   - 도입 시 실제 upstream URL을 고정해야 한다.

4. `slide-design`의 일반명은 장기적으로 충돌 여지가 있다.
   - 현재 직접 충돌은 없지만, project-local skill로 넣을 때 `future-slide-design`처럼 prefix를 권장한다.

5. `tightened-slide`의 디자인 규칙은 엄격하고 취향이 분명하다.
   - no gradients, no shadows, no rounded cards 등 기존 디자인 시스템의 일부 테마와 맞지 않을 수 있다.
   - 그래서 일반 PPT 요청에 기본 적용하면 디자인 자유도가 줄어든다.

## 권장 도입 방식

전역 설치보다 프로젝트 로컬 벤더링을 권장한다.

```text
.claude/skills/future-slide/
├── future-slide-design/SKILL.md
├── future-gpt-image-slide/SKILL.md
├── future-gpt-image-slide-plan/SKILL.md
├── future-gpt-image-slide-prompt/SKILL.md
├── future-gpt-image-slide-render/SKILL.md
└── future-tightened-slide/SKILL.md
```

라우팅 원칙:

- "PPTX", "PowerPoint", "편집 가능한 발표자료" -> 기존 `presentation-agent` + `export-pptx`
- "참고 이미지와 같은 톤으로 페이지 이미지 생성" -> `future-gpt-image-slide`
- "가로 swipe HTML 덱", "locked layout HTML deck" -> `future-tightened-slide`
- "디자인 레퍼런스 분석", "`DESIGN.md` 추출" -> `future-slide-design`

## 결론

도입 가능하되 기본 PPT 제작 경로로 넣으면 안 된다. 현재 환경의 PPT Agent가 더 넓고 산출물도 `.pptx/.pdf`에 맞다. `future-slide-skill`은 레퍼런스 이미지 기반 visual system 추출, 이미지 덱 생성, locked-layout HTML deck 검증용으로 좁혀 넣으면 충돌 없이 가치가 있다.
