---
name: plan-research-synthesis
description: |
  Phase 2 Research 단계의 결과를 종합하는 스킬.
  시장, 경쟁사, 사용자 리서치 결과를 통합 분석합니다.
triggers:
  - "research 종합"
  - "phase 2 종합"
  - "리서치 종합"
input:
  - 02-research/tam-sam-som.md
  - 02-research/trend-analysis.md
  - 02-research/competitor-analysis.md
  - 02-research/user-research.md
output:
  - 02-research/SYNTHESIS.md
phase: 2
sequence: S2
---

# Research Synthesis Skill

Phase 2 Research 단계의 모든 산출물을 종합하여 시장 진입 가능성을 평가합니다.

## 종합 대상 스킬

```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 2: Research                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   3. TAM-SAM-SOM       →  시장 규모 정량화                   │
│   4. Trend Analysis    →  트렌드 분석                        │
│   5. Competitor        →  경쟁 환경 분석                     │
│   6. User Research     →  사용자 니즈 파악                   │
│                                                              │
│   ════════════════════════════════════════════════════════   │
│                                                              │
│   S2. Research Synthesis →  시장 진입 가능성 종합 평가        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 종합 분석 프레임워크

### Market Attractiveness Matrix

```
                    시장 성장률
                 Low       High
              ┌─────────┬─────────┐
      High    │ HARVEST │  INVEST │
경쟁          │ 수확형   │  투자형  │
강도          ├─────────┼─────────┤
      Low     │ DIVEST  │  GROW   │
              │ 철수형   │  성장형  │
              └─────────┴─────────┘
```

## 출력 템플릿

```markdown
# {Project Name} - Research 종합 리포트

## Phase 2 Summary | Date: {date}

---

## 1. Executive Summary

### 한 줄 요약
> {one_line_summary}

### 핵심 인사이트 Top 3
1. 📊 **시장**: {market_insight}
2. 🎯 **경쟁**: {competition_insight}
3. 👤 **고객**: {customer_insight}

---

## 2. 시장 규모 종합 (TAM-SAM-SOM)

### 시장 규모 요약

| 구분 | 규모 | 성장률 | 신뢰도 |
|------|------|--------|--------|
| TAM | {tam} | {growth}% | {confidence} |
| SAM | {sam} | {growth}% | {confidence} |
| SOM (Year 1) | {som} | - | {confidence} |

### 시장 규모 시각화

```
TAM ████████████████████████████████ {tam}
SAM ████████████████████░░░░░░░░░░░░ {sam}
SOM ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░ {som}
```

### 시장 평가
- **매력도**: {high/medium/low}
- **진입 시점**: {timing_assessment}
- **성장 잠재력**: {growth_potential}

---

## 3. 트렌드 분석 종합

### 주요 트렌드 영향도

| 트렌드 | 유형 | 영향도 | 시기 |
|--------|------|--------|------|
| {trend_1} | 기회 | 🔴 High | 단기 |
| {trend_2} | 기회 | 🟡 Medium | 중기 |
| {trend_3} | 위협 | 🟡 Medium | 장기 |

### 트렌드 활용 전략
- **활용할 트렌드**: {leverage_trend}
- **대비할 트렌드**: {prepare_trend}

---

## 4. 경쟁 분석 종합

### 경쟁 구도 요약

| 경쟁사 유형 | 수 | 위협 수준 | 대표 기업 |
|------------|---|----------|----------|
| 직접 경쟁 | {n} | 🔴 High | {companies} |
| 간접 경쟁 | {n} | 🟡 Medium | {companies} |
| 잠재 경쟁 | {n} | 🟢 Low | {companies} |

### 경쟁 우위 기회

| 영역 | 경쟁사 약점 | 우리의 기회 |
|------|-----------|------------|
| {area_1} | {weakness} | {opportunity} |
| {area_2} | {weakness} | {opportunity} |

### 포지셔닝 방향
> {positioning_statement}

---

## 5. 사용자 리서치 종합

### 타겟 사용자 프로필

| 세그먼트 | 크기 | 니즈 강도 | 우선순위 |
|---------|------|----------|----------|
| {segment_1} | {size} | 🔴 High | P0 |
| {segment_2} | {size} | 🟡 Medium | P1 |

### 검증된 사용자 니즈 Top 5

| # | 니즈 | 검증 방법 | 확신도 |
|---|------|----------|--------|
| 1 | {need_1} | {method} | ⭐⭐⭐⭐⭐ |
| 2 | {need_2} | {method} | ⭐⭐⭐⭐ |
| 3 | {need_3} | {method} | ⭐⭐⭐⭐ |
| 4 | {need_4} | {method} | ⭐⭐⭐ |
| 5 | {need_5} | {method} | ⭐⭐⭐ |

### 페르소나 요약
- **Primary**: {primary_persona}
- **Secondary**: {secondary_persona}

---

## 6. 종합 평가

### Research 평가 매트릭스

| 평가 항목 | 점수 (1-5) | 가중치 | 가중 점수 |
|----------|-----------|--------|----------|
| 시장 규모 | {score} | 25% | {weighted} |
| 시장 성장성 | {score} | 20% | {weighted} |
| 경쟁 강도 (역) | {score} | 20% | {weighted} |
| 사용자 니즈 강도 | {score} | 20% | {weighted} |
| 트렌드 부합성 | {score} | 15% | {weighted} |
| **총점** | | 100% | **{total}/5.0** |

### 점수 해석
```
4.0-5.0: 매우 유망 - 적극 진행
3.0-3.9: 유망 - 진행 권장
2.0-2.9: 보통 - 선택적 진행
1.0-1.9: 비유망 - 재검토 필요
```

---

## 7. 전략적 시사점

### SWOT 종합

| 강점 (S) | 약점 (W) |
|----------|----------|
| {strength_1} | {weakness_1} |
| {strength_2} | {weakness_2} |

| 기회 (O) | 위협 (T) |
|----------|----------|
| {opportunity_1} | {threat_1} |
| {opportunity_2} | {threat_2} |

### 핵심 전략 방향
1. **SO 전략**: {so_strategy}
2. **WO 전략**: {wo_strategy}
3. **ST 전략**: {st_strategy}

---

## 8. Phase 3 진행 권장사항

### 진행 결정: {PROCEED / PIVOT / HOLD}

**결정 근거**
{decision_rationale}

### Validation 단계 우선순위

| 우선순위 | 검증 항목 | 검증 방법 |
|---------|----------|----------|
| P0 | {item_1} | {method} |
| P1 | {item_2} | {method} |
| P2 | {item_3} | {method} |

### 위험 요소 모니터링
- {risk_1}: {mitigation}
- {risk_2}: {mitigation}

---

## 9. 미해결 질문

| # | 질문 | 중요도 | 답변 예정 |
|---|------|--------|----------|
| 1 | {question_1} | 🔴 | Phase 3 |
| 2 | {question_2} | 🟡 | Phase 4 |

---

*Phase 2 Research 완료 | 다음: Phase 3 Validation*
```

## 🎯 인터랙티브 가이드

### 종합 전 확인 질문

**Q1. 모든 Research 문서가 작성되었나요?**
- [ ] tam-sam-som.md 완료
- [ ] trend-analysis.md 완료
- [ ] competitor-analysis.md 완료
- [ ] user-research.md 완료

**Q2. 시장 규모 데이터의 신뢰도는?**
- 높음: 공신력 있는 리서치 기관 데이터
- 중간: 다수의 2차 자료 교차 검증
- 낮음: 추정 기반

**Q3. 사용자 리서치 샘플 수는 충분한가요?**
- 정량 조사: 최소 100명 이상
- 정성 조사: 최소 10명 이상

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| 시장 평가 | 규모/성장성 판단 | "시장 매력도를 어떻게 평가하시겠어요?" |
| 경쟁 평가 | 진입 장벽 | "경쟁 강도를 어떻게 보시나요?" |
| 종합 평가 | 가중치 조정 | "평가 항목별 가중치를 조정하시겠어요?" |
| 최종 결정 | 진행 여부 | "Phase 3로 진행하시겠어요?" |

---

## 퀄리티 체크리스트

```
□ 4개 Research 산출물이 모두 검토되었는가?
□ 시장 규모가 정량화되었는가?
□ 경쟁 구도가 명확히 파악되었는가?
□ 사용자 니즈가 검증되었는가?
□ 전략적 시사점이 도출되었는가?
□ Phase 3 우선순위가 정해졌는가?
```

## 다음 스킬 연결

Research Synthesis 완료 후:

1. **PROCEED** → Phase 3 Validation 스킬들 진행
2. **PIVOT** → 타겟 시장/고객 재정의 후 Research 재실행
3. **HOLD** → 추가 리서치 수행 후 재평가

---

*Research는 의사결정의 기반입니다. 데이터에 기반한 판단을 하세요.*
