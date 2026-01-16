---
name: plan-validation-synthesis
description: |
  Phase 3 Validation 단계의 결과를 종합하는 스킬.
  비즈니스 모델, 가격, MVP 검증 결과를 통합 분석합니다.
triggers:
  - "validation 종합"
  - "phase 3 종합"
  - "검증 종합"
input:
  - 03-validation/lean-canvas.md
  - 03-validation/business-model.md
  - 03-validation/pricing-strategy.md
  - 03-validation/mvp-definition.md
  - 03-validation/legal-checklist.md
output:
  - 03-validation/SYNTHESIS.md
phase: 3
sequence: S3
---

# Validation Synthesis Skill

Phase 3 Validation 단계의 모든 산출물을 종합하여 비즈니스 실행 가능성을 최종 검증합니다.

## 종합 대상 스킬

```
┌─────────────────────────────────────────────────────────────┐
│                   Phase 3: Validation                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   7. Lean Canvas       →  비즈니스 모델 요약                 │
│   8. Business Model    →  수익 구조 상세화                   │
│   9. Pricing Strategy  →  가격 정책 설계                     │
│  10. MVP Definition    →  최소 기능 제품 정의                │
│  11. Legal Checklist   →  법적 요건 확인                     │
│                                                              │
│   ════════════════════════════════════════════════════════   │
│                                                              │
│   S3. Validation Synthesis →  비즈니스 실행 가능성 최종 검증  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 종합 분석 프레임워크

### Business Viability Score

```
┌─────────────────────────────────────────────────────────────┐
│                  Business Viability Assessment               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Desirability (고객 관점)     ████████░░  80%               │
│   └─ 고객이 원하는가?                                        │
│                                                              │
│   Feasibility (기술 관점)      ██████████  100%              │
│   └─ 만들 수 있는가?                                         │
│                                                              │
│   Viability (비즈니스 관점)    ███████░░░  70%               │
│   └─ 수익이 나는가?                                          │
│                                                              │
│   ─────────────────────────────────────────────────────────  │
│   Overall Score: 83% → VALIDATED ✅                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 출력 템플릿

```markdown
# {Project Name} - Validation 종합 리포트

## Phase 3 Summary | Date: {date}

---

## 1. Executive Summary

### 검증 결과 한 줄 요약
> {validation_summary}

### 핵심 검증 결과
| 영역 | 결과 | 신뢰도 |
|------|------|--------|
| 비즈니스 모델 | ✅ 검증됨 | High |
| 수익 모델 | ✅ 검증됨 | Medium |
| 가격 정책 | 🟡 부분 검증 | Medium |
| MVP 범위 | ✅ 확정됨 | High |
| 법적 요건 | ✅ 확인됨 | High |

---

## 2. 린 캔버스 검증 결과

### 9블록 검증 상태

| 블록 | 상태 | 변경 사항 |
|------|------|----------|
| 1. 고객 세그먼트 | ✅ | {change} |
| 2. 문제 | ✅ | {change} |
| 3. 고유 가치 제안 | ✅ | {change} |
| 4. 솔루션 | ✅ | {change} |
| 5. 채널 | 🟡 | {change} |
| 6. 수익원 | ✅ | {change} |
| 7. 비용 구조 | ✅ | {change} |
| 8. 핵심 지표 | ✅ | {change} |
| 9. 경쟁 우위 | 🟡 | {change} |

### 핵심 가설 검증 현황

| 가설 | 검증 방법 | 결과 | 학습 |
|------|----------|------|------|
| {hypothesis_1} | {method} | ✅/❌ | {learning} |
| {hypothesis_2} | {method} | ✅/❌ | {learning} |
| {hypothesis_3} | {method} | ✅/❌ | {learning} |

---

## 3. 비즈니스 모델 검증 결과

### 수익 모델 요약

| 수익원 | 비중 | Year 1 예상 | 검증 상태 |
|--------|------|------------|----------|
| {revenue_1} | {%} | {amount} | ✅ |
| {revenue_2} | {%} | {amount} | 🟡 |

### 단위 경제학 (Unit Economics)

```
┌─────────────────────────────────────────┐
│           Unit Economics                 │
├─────────────────────────────────────────┤
│  ARPU (객단가)        : {arpu}          │
│  CAC (획득 비용)      : {cac}           │
│  LTV (고객 생애 가치) : {ltv}           │
│  ─────────────────────────────────────  │
│  LTV:CAC Ratio       : {ratio}:1        │
│  Payback Period      : {months}개월     │
│  ─────────────────────────────────────  │
│  평가: {healthy/warning/critical}       │
└─────────────────────────────────────────┘
```

### 손익분기점
- **월 고정비**: {fixed_cost}
- **객단가**: {price}
- **BEP 고객 수**: {bep_customers}명
- **BEP 달성 예상**: {bep_timeline}

---

## 4. 가격 정책 검증 결과

### 가격 구조 확정

| 플랜 | 가격 | 타겟 | 예상 비중 |
|------|------|------|----------|
| Free | ₩0 | {target} | {%} |
| Basic | ₩{price}/월 | {target} | {%} |
| Pro | ₩{price}/월 | {target} | {%} |
| Enterprise | 문의 | {target} | {%} |

### 가격 검증 결과
- **경쟁 대비 포지션**: {position}
- **고객 WTP 부합**: {fit_level}
- **마진 확보**: {margin_status}

---

## 5. MVP 범위 확정

### MVP 기능 목록

| 우선순위 | 기능 | 필수/선택 | 예상 공수 |
|---------|------|----------|----------|
| P0 | {feature_1} | Must | {effort} |
| P0 | {feature_2} | Must | {effort} |
| P1 | {feature_3} | Should | {effort} |
| P2 | {feature_4} | Could | {effort} |

### MVP 범위 요약
- **총 기능 수**: {total} (Must: {must}, Should: {should}, Could: {could})
- **예상 개발 기간**: {duration}
- **예상 비용**: {cost}

---

## 6. 법적 요건 확인

### 체크리스트 결과

| 영역 | 상태 | 조치 필요 |
|------|------|----------|
| 개인정보보호 | ✅ | {action} |
| 이용약관 | ✅ | {action} |
| 사업자 등록 | ✅ | {action} |
| 지적재산권 | 🟡 | {action} |
| 산업 규제 | ✅ | {action} |

### 필수 조치 사항
1. {legal_action_1}
2. {legal_action_2}

---

## 7. Business Viability Score

### 종합 점수

| 영역 | 점수 | 가중치 | 가중 점수 |
|------|------|--------|----------|
| Desirability (고객 원함) | {score}/100 | 35% | {weighted} |
| Feasibility (구현 가능) | {score}/100 | 30% | {weighted} |
| Viability (수익 가능) | {score}/100 | 35% | {weighted} |
| **총점** | | 100% | **{total}/100** |

### 점수 해석
```
80-100: VALIDATED - 실행 단계 진입
60-79:  CONDITIONAL - 보완 후 진행
40-59:  PIVOT NEEDED - 모델 수정 필요
0-39:   NOT VIABLE - 재검토 필요
```

---

## 8. 리스크 & 가정

### 핵심 리스크

| 리스크 | 영향 | 확률 | 대응 방안 |
|--------|------|------|----------|
| {risk_1} | 🔴 | High | {mitigation} |
| {risk_2} | 🟡 | Medium | {mitigation} |
| {risk_3} | 🟢 | Low | {mitigation} |

### 검증이 필요한 가정
1. {assumption_1} → Phase 4에서 검증
2. {assumption_2} → 런칭 후 검증

---

## 9. Phase 4 진행 권장사항

### 진행 결정: {VALIDATED / CONDITIONAL / PIVOT / NOT VIABLE}

**결정 근거**
{decision_rationale}

### Specification 단계 우선순위

| 우선순위 | 산출물 | 이유 |
|---------|--------|------|
| 1 | PRD | {reason} |
| 2 | User Stories | {reason} |
| 3 | Technical Spec | {reason} |

### 다음 단계 준비 체크리스트
- [ ] 비즈니스 모델 최종 확정
- [ ] MVP 범위 팀 합의
- [ ] 법적 조치 사항 완료
- [ ] 개발 리소스 확보

---

*Phase 3 Validation 완료 | 다음: Phase 4 Specification*
```

## 🎯 인터랙티브 가이드

### 종합 전 확인 질문

**Q1. 비즈니스 모델이 확정되었나요?**
- 확정됨 → 다음 질문으로
- 미확정 → "어떤 부분이 불확실한가요?"

**Q2. MVP 범위에 팀 합의가 되었나요?**
- 합의됨 → 다음 질문으로
- 미합의 → "의견 차이가 있는 기능은?"

**Q3. 단위 경제학이 건전한가요?**
- LTV:CAC > 3:1 → 건전
- LTV:CAC 1-3:1 → 주의 필요
- LTV:CAC < 1:1 → 모델 수정 필요

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| 가격 검증 | 최종 가격 | "이 가격 구조로 확정하시겠어요?" |
| MVP 범위 | 기능 목록 | "MVP에 포함할 기능이 맞나요?" |
| 종합 점수 | Viability | "점수 평가에 동의하시나요?" |
| 최종 결정 | 진행 여부 | "Phase 4로 진행하시겠어요?" |

---

## 퀄리티 체크리스트

```
□ 린 캔버스 9블록이 모두 검증되었는가?
□ 단위 경제학이 계산되었는가?
□ 가격 정책이 확정되었는가?
□ MVP 범위가 명확한가?
□ 법적 요건이 확인되었는가?
□ 핵심 리스크가 식별되었는가?
```

---

*Validation은 실행 전 마지막 검증입니다. 확신이 생길 때까지 검증하세요.*
