# future-slide-skill tightened-slide 품질 검토

검토일: 2026-05-18

## 생성 산출물

- HTML 덱: `docs/260518-seo-aeo-search-era/future-tightened/index.html`
- QA 리포트: `docs/260518-seo-aeo-search-era/future-tightened/qa/qa-report.md`
- 전체 슬라이드 미리보기: `docs/260518-seo-aeo-search-era/future-tightened/qa/contact-sheet.png`
- 생성 스크립트: `docs/260518-seo-aeo-search-era/future-tightened-generate.cjs`
- 브라우저 QA 스크립트: `docs/260518-seo-aeo-search-era/future-tightened-qa.cjs`

## 사용한 future-slide-skill 경로

이번 테스트는 `future-slide-skill` 중 `tightened-slide` workflow를 사용했다.

- `skills/tightened-slide/SKILL.md`
- `skills/tightened-slide/assets/template.html`
- `skills/tightened-slide/references/layout-lock.md`
- `skills/tightened-slide/references/layouts.md`
- `skills/tightened-slide/references/themes.md`
- `skills/tightened-slide/scripts/validate-deck.mjs`

## 덱 구성

| Slide | Layout | 목적 |
|---|---|---|
| 01 | S01 | 커버와 핵심 전환 메시지 |
| 02 | S03 | SEO/AEO 관계에 대한 thesis |
| 03 | S07 | Pew 클릭 데이터 바 차트 |
| 04 | S08 | SEO vs AEO 역할 비교 |
| 05 | S17 | AEO-ready page 시스템 구조 |
| 06 | S20 | AEO 추가 KPI ledger |
| 07 | S11 | 90일 전환 로드맵 |
| 08 | S10 | 결론과 next actions |

8장 덱에서 8개의 서로 다른 등록 레이아웃을 사용했다. `tightened-slide`의 "7-8 page decks should use at least six different Sxx layouts" 기준은 충족한다.

## 검증 결과

### future validator

```text
Deck validation passed: 8 slide(s).
```

통과 항목:

- 모든 slide에 `data-layout` 존재
- 등록 레이아웃만 사용
- SVG visible `<text>` 없음
- local image가 없으므로 `data-image-slot` 위반 없음
- unregistered experimental image structure 없음

### 브라우저 QA

Playwright로 1366x768 viewport에서 8장 전체를 캡처했다.

- Offscreen elements: 0
- 1차 QA에서 6번 S20 ledger가 화면 아래로 밀렸고 수정 완료
- 남은 overflow warning은 대부분 large display heading의 line-height/scrollHeight false positive로 보인다
- 수치 라벨은 `t-meta` 자간 때문에 `2 6%`처럼 보이던 문제를 수정 완료

## 품질 평가

| 항목 | 점수 | 판단 |
|---|---:|---|
| 시각 일관성 | 9/10 | IKB 테마와 locked layout이 강하게 유지됨 |
| 발표용 임팩트 | 8/10 | 큰 타이포와 여백이 좋음. 컨퍼런스/키노트 톤에 강함 |
| 정보 밀도 | 6/10 | 전략 보고서나 컨설팅 PPT보다 정보량이 낮음 |
| 검증 가능성 | 8/10 | validator가 유용하지만 실제 overflow는 별도 브라우저 QA가 필요 |
| 편집 가능성 | 5/10 | HTML 편집은 가능하나 PowerPoint 객체 편집성과는 다름 |
| 기존 PPTX 파이프라인 대체성 | 4/10 | PPTX/PDF/리서치/팩트체크/리뷰/이미지 생성 전체를 대체하지 못함 |

## 대체 판정

현재 결과만 기준으로는 전체 대체는 권장하지 않는다.

이유:

- `tightened-slide` 결과물은 훌륭한 HTML 발표 덱이지만, 기존 `presentation-agent`의 PPTX/PDF 출력, 리서치, 검증, 리뷰, refinement, 이미지 생성 단계를 전부 대체하지 않는다.
- future validator는 layout contract 검증에는 좋지만, 실제 브라우저 렌더링 overflow를 완전히 잡지는 못했다. 이번에도 6번 슬라이드 overflow는 별도 QA에서 발견했다.
- 디자인 스타일이 강하게 고정되어 있어 모든 도메인 PPT에 적용하면 다양성과 정보 밀도 면에서 손해가 있다.
- `gpt-image-slide` 이미지 생성 workflow는 이번 테스트에서 별도 검증하지 않았다. 이 branch는 편집 가능한 PPT가 아니라 `page_N.png` 중심 산출물이다.

## 권장 도입안

1. 기존 PPT agent 삭제 금지
2. `future-tightened-slide`를 HTML 발표 덱 전용 보조 스킬로 추가
3. 라우팅을 다음처럼 제한
   - "HTML 덱", "swipe deck", "keynote-style web deck", "tightened" -> future tightened
   - "PPTX", "편집 가능한 PPT", "고객 제출용 문서", "PDF handout" -> 기존 presentation-agent
4. future validator 뒤에 Playwright QA를 필수 단계로 추가
5. 최소 3개 샘플을 더 돌린 뒤 대체 범위 재판정
   - 데이터 밀도 높은 경영 보고서
   - 이미지 중심 제품/브랜드 덱
   - 실제 PPTX 제출이 필요한 고객 제안서

## 결론

`future-slide-skill`의 tightened-slide는 채택 가치가 있다. 다만 "대체재"가 아니라 "HTML 발표 덱 생성 엔진"으로 도입해야 한다. 현재 기준에서 기존 PPT agent와 skills를 전부 제거하면 PPTX/PDF 산출, 리서치·검증·리뷰 체계, 편집 가능한 PowerPoint 객체 생성 능력을 잃는다.
