---
name: plan-discovery-synthesis
description: |
  Phase 1 Discovery 단계의 결과를 종합하는 스킬.
  아이디어 캡처와 시장 발견 결과를 통합 분석합니다.
triggers:
  - "discovery 종합"
  - "phase 1 종합"
  - "아이디어 종합"
input:
  - 01-discovery/idea-capture.md
  - 01-discovery/market-discovery.md
output:
  - 01-discovery/SYNTHESIS.md
phase: 1
sequence: S1
---

# Discovery Synthesis Skill

Phase 1 Discovery 단계의 모든 산출물을 종합하여 다음 단계 진행 여부를 결정합니다.

## 종합 대상 스킬

```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 1: Discovery                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. Idea Capture        →  아이디어 정의 및 초기 가설        │
│   2. Market Discovery    →  시장 기회 탐색                   │
│                                                              │
│   ════════════════════════════════════════════════════════   │
│                                                              │
│   S1. Discovery Synthesis →  종합 분석 및 Go/No-Go 결정      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 종합 분석 프레임워크

### 1. 핵심 질문 검증

| 질문 | 충족 여부 | 근거 |
|------|----------|------|
| 해결할 문제가 명확한가? | ✅/❌ | {evidence} |
| 타겟 고객이 정의되었는가? | ✅/❌ | {evidence} |
| 시장 기회가 존재하는가? | ✅/❌ | {evidence} |
| 초기 가설이 수립되었는가? | ✅/❌ | {evidence} |

### 2. Go/No-Go 결정 매트릭스

```
                    시장 기회
                 Low       High
              ┌─────────┬─────────┐
      High    │  PIVOT  │   GO    │
문제          │  방향 수정 │  진행   │
명확성        ├─────────┼─────────┤
      Low     │  STOP   │ REFINE  │
              │  중단    │ 문제 재정의│
              └─────────┴─────────┘
```

## 출력 템플릿

```markdown
# {Project Name} - Discovery 종합 리포트

## Phase 1 Summary | Date: {date}

---

## 1. Executive Summary

### 한 줄 요약
> {one_line_summary}

### 핵심 발견
1. {key_finding_1}
2. {key_finding_2}
3. {key_finding_3}

---

## 2. 아이디어 분석 결과

### 아이디어 개요
| 항목 | 내용 |
|------|------|
| 아이디어 명 | {idea_name} |
| 카테고리 | {category} |
| 핵심 가치 | {core_value} |

### 초기 가설
| # | 가설 | 검증 필요성 | 우선순위 |
|---|------|------------|----------|
| 1 | {hypothesis_1} | 🔴 High | P0 |
| 2 | {hypothesis_2} | 🟡 Medium | P1 |
| 3 | {hypothesis_3} | 🟢 Low | P2 |

---

## 3. 시장 기회 분석 결과

### 시장 규모 (초기 추정)
| 구분 | 규모 | 신뢰도 |
|------|------|--------|
| TAM | {tam} | 🟡 Medium |
| SAM | {sam} | 🟡 Medium |
| SOM | {som} | 🔴 Low |

### 시장 트렌드
- **성장 트렌드**: {growth_trend}
- **기술 트렌드**: {tech_trend}
- **소비자 트렌드**: {consumer_trend}

---

## 4. 종합 평가

### 평가 매트릭스

| 평가 항목 | 점수 (1-5) | 코멘트 |
|----------|-----------|--------|
| 문제 명확성 | {score}/5 | {comment} |
| 시장 기회 | {score}/5 | {comment} |
| 차별화 가능성 | {score}/5 | {comment} |
| 실현 가능성 | {score}/5 | {comment} |
| **종합 점수** | **{total}/20** | |

### 점수 해석
```
16-20점: GO - 다음 단계 진행
11-15점: CONDITIONAL - 보완 후 진행
6-10점:  PIVOT - 방향 수정 필요
1-5점:   STOP - 재검토 필요
```

---

## 5. Go/No-Go 결정

### 결정: {GO / CONDITIONAL / PIVOT / STOP}

**결정 근거**
{decision_rationale}

### 다음 단계 권장사항

**진행 시 (GO/CONDITIONAL)**
- [ ] Phase 2 Research 진행
- [ ] 우선 검증할 가설: {priority_hypothesis}
- [ ] 추가 조사 필요 영역: {research_area}

**수정 시 (PIVOT)**
- [ ] 수정 방향: {pivot_direction}
- [ ] 재검토 항목: {review_items}

**중단 시 (STOP)**
- [ ] 중단 사유: {stop_reason}
- [ ] 학습 포인트: {lessons_learned}

---

## 6. 미해결 질문

| # | 질문 | 답변 필요 시점 | 담당 |
|---|------|--------------|------|
| 1 | {question_1} | Phase 2 | - |
| 2 | {question_2} | Phase 3 | - |

---

## 7. 다음 Phase 준비사항

### Phase 2: Research 진입 조건
- [ ] Discovery 종합 점수 11점 이상
- [ ] 핵심 가설 3개 이상 정의
- [ ] 타겟 고객 세그먼트 정의

### 예상 소요 기간
- Phase 2 예상: {estimated_duration}

---

*Phase 1 Discovery 완료 | 다음: Phase 2 Research*
```

## 🎯 인터랙티브 가이드

### 종합 전 확인 질문

스킬 실행 시 다음 질문들을 순차적으로 확인합니다:

**Q1. 모든 Discovery 문서가 작성되었나요?**
- [ ] idea-capture.md 완료
- [ ] market-discovery.md 완료

**Q2. 각 문서의 핵심 섹션이 채워졌나요?**
- 아이디어 캡처: 문제 정의, 솔루션 가설, 타겟 고객
- 시장 발견: 시장 규모, 트렌드, 기회 영역

**Q3. Go/No-Go 결정에 필요한 정보가 충분한가요?**
- 충분함 → 종합 리포트 작성
- 부족함 → 추가 조사 필요 영역 식별

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| 시작 전 | 문서 완성도 | "Discovery 문서들이 모두 작성되었나요?" |
| 평가 시 | 점수 기준 | "각 항목별 점수를 어떻게 평가하시겠어요?" |
| 결정 시 | Go/No-Go | "종합 점수 기반으로 어떤 결정을 내리시겠어요?" |
| 완료 후 | 다음 단계 | "Phase 2로 진행하시겠어요?" |

---

## 퀄리티 체크리스트

```
□ 모든 Discovery 산출물이 검토되었는가?
□ 핵심 가설이 명확히 정리되었는가?
□ 시장 기회가 객관적으로 평가되었는가?
□ Go/No-Go 결정 근거가 명확한가?
□ 다음 단계 권장사항이 구체적인가?
□ 미해결 질문이 식별되었는가?
```

## 다음 스킬 연결

Discovery Synthesis 완료 후:

1. **GO 결정 시** → Phase 2 Research 스킬들 진행
2. **PIVOT 결정 시** → Idea Capture 재실행
3. **STOP 결정 시** → 새로운 아이디어로 Phase 1 재시작

---

*종합 리포트는 의사결정의 근거가 됩니다. 객관적으로 평가하세요.*
