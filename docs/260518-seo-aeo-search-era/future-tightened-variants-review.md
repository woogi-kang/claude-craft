# Future Slide Skill 3-Variant Review

검토일: 2026-05-18

주제: SEO -> AEO 검색 시대

사용 스킬: `bytonylee/future-slide-skill`의 `tightened-slide`

## 산출물

| 버전 | 목적 | HTML 덱 | Contact sheet |
|---|---|---|---|
| V1 Balanced Analysis | 분석형 기본 덱 | `future-tightened-variants/v1-balanced-analysis/index.html` | `future-tightened-variants/v1-balanced-analysis/qa/contact-sheet.png` |
| V2 Executive Metrics | 숫자/KPI 중심 임원 보고형 | `future-tightened-variants/v2-executive-metrics/index.html` | `future-tightened-variants/v2-executive-metrics/qa/contact-sheet.png` |
| V3 Framework Workshop | 프레임워크/워크숍형 | `future-tightened-variants/v3-framework-workshop/index.html` | `future-tightened-variants/v3-framework-workshop/qa/contact-sheet.png` |

생성 스크립트:

- `future-tightened-variants-generate.cjs`
- `future-tightened-variants-qa.cjs`
- `future-tightened-variants/qa-summary.md`

## Layout 구성

### V1 Balanced Analysis

| Slide | Layout | 용도 |
|---|---|---|
| 01 | S01 | 커버 |
| 02 | S03 | 핵심 thesis |
| 03 | S07 | Pew 클릭 데이터 바 차트 |
| 04 | S08 | SEO vs AEO 비교 |
| 05 | S17 | AEO-ready content system |
| 06 | S20 | KPI ledger |
| 07 | S11 | 90일 로드맵 |
| 08 | S10 | 결론 |

평가:

- 가장 균형이 좋다.
- 정보 흐름이 자연스럽고, 기존 PPT Agent 산출물과 비교하기 가장 적합하다.
- AEO 설명/설득용 첫 버전으로 추천.

### V2 Executive Metrics

| Slide | Layout | 용도 |
|---|---|---|
| 01 | S01 | 커버 |
| 02 | S18 | Why now |
| 03 | S06 | KPI tower |
| 04 | S15 | Audit matrix + hero stat |
| 05 | S05 | Three layers |
| 06 | S21 | Program spec sheet |
| 07 | S11 | Decision timeline |
| 08 | S10 | 임원 의사결정 |

평가:

- 숫자와 의사결정 프레임이 가장 강하다.
- 경영진 보고나 내부 승인용으로 적합하다.
- S06/S15/S21 조합이 future tightened layout의 데이터형 표현력을 확인하기 좋다.

### V3 Framework Workshop

| Slide | Layout | 용도 |
|---|---|---|
| 01 | S01 | 커버 |
| 02 | S12 | Manifesto |
| 03 | S04 | 6-block anatomy |
| 04 | S13 | Three forces |
| 05 | S14 | Operating loop |
| 06 | S19 | Team responsibilities |
| 07 | S02 | Workshop agenda |
| 08 | S10 | 워크숍 산출물 |

평가:

- 워크숍/교육용으로 가장 좋다.
- 구조를 설명하고 팀 실행으로 연결하는 데 강하다.
- S14 loop와 S02 timeline은 검증 없이 쓰면 하단 safe area를 침범하기 쉬워 QA가 필수다.

## QA 결과

검사 viewport: 1366x768

자동 검사 항목:

- layout/offscreen
- overflow
- padding/safe area
- bottom navigation safe area
- 한글 heading의 의도치 않은 word breaking
- percent label letter-spacing

최종 결과:

| 버전 | Slides | PASS | WARN | FAIL |
|---|---:|---:|---:|---:|
| V1 Balanced Analysis | 8 | 8 | 0 | 0 |
| V2 Executive Metrics | 8 | 8 | 0 | 0 |
| V3 Framework Workshop | 8 | 8 | 0 | 0 |

`future-slide-skill` validator도 세 버전 모두 통과했다.

```text
Deck validation passed: 8 slide(s).
Deck validation passed: 8 slide(s).
Deck validation passed: 8 slide(s).
```

## 발견 및 수정한 문제

1. V2 S06 KPI tower가 처음에는 화면 아래로 밀렸다.
   - 원인: 큰 heading + tower card 높이가 결합되며 bottom safe area 초과.
   - 수정: heading 크기 축소, tower 높이 축소, card padding 축소.

2. V3 S14 loop slide에서 하단 `Measure` 라벨이 잘렸다.
   - 원인: absolute label 위치가 실제 viewport 기준으로 너무 낮음.
   - 수정: label 위치를 상단 기준으로 재배치하고 step card padding을 축소.

3. 수치 라벨이 `2 6%`처럼 벌어질 수 있었다.
   - 원인: `t-meta`/`t-cat`의 letter-spacing이 숫자 퍼센트에 적용됨.
   - 수정: 퍼센트 라벨은 `mono` + `letter-spacing:0` 사용.

4. 대형 숫자 계열은 CSS font metric 때문에 scrollHeight false positive가 발생했다.
   - 조치: 화면 안에 들어와 있고 시각적으로 잘리지 않는 display number는 QA에서 overflow fail로 보지 않도록 분리했다.

## 결론

세 버전 모두 현재 QA 기준으로 깨짐 없이 통과했다. 다만 이 결과는 HTML 발표 덱 기준이다. 기존 PPT Agent 전체를 대체할지 판단하려면 다음 두 케이스를 추가 검증해야 한다.

- PPTX/PDF 제출용 산출물 변환 품질
- 이미지 생성형 `gpt-image-slide` workflow의 텍스트 정확도와 편집성

현재 기준 추천:

- HTML 발표 덱: `future-tightened-slide` 도입 가능
- 기존 PPTX 중심 agent/skills 전체 삭제: 아직 보류
