---
name: plan-prd
description: |
  제품 요구사항 문서(PRD)를 작성하는 스킬.
  개발팀과 소통할 수 있는 명확한 기획서를 생성합니다.
triggers:
  - "PRD"
  - "제품 요구사항"
  - "기획서"
  - "요구사항 문서"
input:
  - mvp-definition.md 결과
  - target-user.md 결과
output:
  - 04-specification/prd.md
---

# PRD Skill

개발팀, 디자인팀과 소통할 수 있는 제품 요구사항 문서를 작성합니다.

## PRD 원칙

```
좋은 PRD는:
✅ 왜(Why)를 먼저 설명한다
✅ 무엇(What)을 명확히 정의한다
✅ 어떻게(How)는 팀에게 맡긴다
✅ 성공 기준이 측정 가능하다
```

## 출력 템플릿

```markdown
# {Project Name} - PRD

**Version**: {version}
**Author**: {author}
**Date**: {date}
**Status**: Draft / Review / Approved

---

## 1. Overview

### 1.1 Problem Statement

> **{problem_statement}**

**현재 상황**
{current_situation}

**문제의 영향**
- {impact_1}
- {impact_2}
- {impact_3}

### 1.2 Solution Summary

> **{solution_summary}**

### 1.3 Target Users

**Primary**
- {primary_user_description}

**Secondary**
- {secondary_user_description}

### 1.4 Goals & Success Metrics

| 목표 | 지표 | 목표값 | 측정 방법 |
|------|------|--------|----------|
| {goal_1} | {metric_1} | {target_1} | {how_1} |
| {goal_2} | {metric_2} | {target_2} | {how_2} |
| {goal_3} | {metric_3} | {target_3} | {how_3} |

---

## 2. User Stories

### 2.1 Epic: {Epic Name}

**US-001: {User Story Title}**

```
As a {user_type}
I want to {action}
So that {benefit}
```

**Acceptance Criteria**
- [ ] Given {precondition}, When {action}, Then {result}
- [ ] Given {precondition}, When {action}, Then {result}
- [ ] Given {precondition}, When {action}, Then {result}

**Priority**: Must Have / Should Have / Could Have
**Estimate**: S / M / L / XL

---

**US-002: {User Story Title}**

(동일 구조 반복)

---

### 2.2 Epic: {Epic Name}

(동일 구조)

---

## 3. Functional Requirements

### 3.1 {Feature Area 1}

#### FR-001: {Feature Name}

| 항목 | 내용 |
|------|------|
| 설명 | {description} |
| 우선순위 | {priority} |
| 관련 US | US-001, US-002 |

**상세 요구사항**
1. {requirement_1}
2. {requirement_2}
3. {requirement_3}

**비즈니스 규칙**
- {rule_1}
- {rule_2}

**엣지 케이스**
| 케이스 | 처리 방법 |
|--------|----------|
| {edge_case_1} | {handling_1} |
| {edge_case_2} | {handling_2} |

---

#### FR-002: {Feature Name}

(동일 구조)

---

### 3.2 {Feature Area 2}

(동일 구조)

---

## 4. Non-Functional Requirements

### 4.1 Performance

| 항목 | 요구사항 | 우선순위 |
|------|----------|----------|
| 페이지 로딩 | < {n}초 | 🔴 |
| API 응답 | < {n}ms | 🔴 |
| 동시 사용자 | {n}명 | 🟡 |

### 4.2 Security

| 항목 | 요구사항 | 우선순위 |
|------|----------|----------|
| 인증 | {auth_method} | 🔴 |
| 데이터 암호화 | {encryption} | 🔴 |
| 접근 제어 | {access_control} | 🔴 |

### 4.3 Scalability

| 항목 | 요구사항 |
|------|----------|
| 예상 사용자 (Y1) | {users} |
| 예상 데이터 | {data} |
| 확장 전략 | {strategy} |

### 4.4 Accessibility

| 항목 | 요구사항 |
|------|----------|
| WCAG 레벨 | {level} |
| 스크린 리더 | {support} |
| 키보드 네비게이션 | {support} |

---

## 5. UI/UX Requirements

### 5.1 Design Principles

1. **{principle_1}**: {description}
2. **{principle_2}**: {description}
3. **{principle_3}**: {description}

### 5.2 Key Screens

| 화면 | 목적 | 우선순위 |
|------|------|----------|
| {screen_1} | {purpose_1} | 🔴 |
| {screen_2} | {purpose_2} | 🔴 |
| {screen_3} | {purpose_3} | 🟡 |

### 5.3 User Flows

**Flow 1: {Flow Name}**
```
{step_1} → {step_2} → {step_3} → {step_4}
```

(상세는 user-flow.md 참조)

---

## 6. Technical Considerations

### 6.1 Dependencies

| 의존성 | 유형 | 상태 |
|--------|------|------|
| {dependency_1} | External API | {status} |
| {dependency_2} | Third Party | {status} |
| {dependency_3} | Internal | {status} |

### 6.2 Integration Points

| 시스템 | 연동 방식 | 용도 |
|--------|----------|------|
| {system_1} | {method} | {purpose} |
| {system_2} | {method} | {purpose} |

### 6.3 Known Constraints

- {constraint_1}
- {constraint_2}
- {constraint_3}

---

## 7. Release Plan

### 7.1 Phases

| Phase | 범위 | 목표 시점 |
|-------|------|----------|
| MVP | US-001 ~ US-005 | {date} |
| v1.1 | US-006 ~ US-010 | {date} |
| v1.2 | US-011 ~ US-015 | {date} |

### 7.2 MVP Scope

**포함**
- {included_1}
- {included_2}
- {included_3}

**제외 (이후 버전)**
- {excluded_1}
- {excluded_2}

---

## 8. Risks & Assumptions

### 8.1 Assumptions

| # | 가정 | 영향 (가정 틀릴 시) |
|---|------|-------------------|
| 1 | {assumption_1} | {impact_1} |
| 2 | {assumption_2} | {impact_2} |

### 8.2 Risks

| 리스크 | 확률 | 영향 | 대응 |
|--------|------|------|------|
| {risk_1} | 🟡 | 🔴 | {mitigation_1} |
| {risk_2} | 🟢 | 🟡 | {mitigation_2} |

### 8.3 Open Questions

| # | 질문 | 담당 | 기한 |
|---|------|------|------|
| 1 | {question_1} | {owner} | {date} |
| 2 | {question_2} | {owner} | {date} |

---

## 9. Appendix

### 9.1 Glossary

| 용어 | 정의 |
|------|------|
| {term_1} | {definition_1} |
| {term_2} | {definition_2} |

### 9.2 Related Documents

| 문서 | 링크 |
|------|------|
| Lean Canvas | ./03-validation/lean-canvas.md |
| MVP Definition | ./03-validation/mvp-definition.md |
| Feature Spec | ./04-specification/feature-spec.md |
| User Flow | ./04-specification/user-flow.md |

---

## Revision History

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 0.1 | {date} | {author} | 초안 작성 |
| 0.2 | {date} | {author} | {changes} |

---

*이 문서는 기획 문서입니다. 기술적 구현 방법은 개발팀에서 결정합니다.*
```

## 퀄리티 체크리스트

```
□ 문제 정의가 명확한가?
□ 목표가 측정 가능한가?
□ User Story가 INVEST 원칙을 따르는가?
□ Acceptance Criteria가 구체적인가?
□ 우선순위가 명확한가?
□ 비기능 요구사항이 정의되었는가?
□ 리스크가 식별되었는가?
□ Open Questions가 정리되었는가?
```

## 🎯 인터랙티브 가이드

### 작성 전 확인 질문

**Q1. MVP 범위가 확정되었나요?**
- 확정됨 → PRD 상세 작성 진행
- 미확정 → "MVP Definition 스킬을 먼저 완료해주세요"

**Q2. 이해관계자가 누구인가요?**
- 명확함 → PRD 공유 대상 정의
- 불명확 → "이 문서를 읽을 사람은 누구인가요? (개발자, 디자이너, 경영진)"

**Q3. 성공 지표가 정의되었나요?**
- 정의됨 → Goals 섹션 작성
- 미정의 → "이 제품이 성공했다는 걸 어떻게 알 수 있나요?"

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| 문제 정의 | 명확성 | "해결하려는 문제를 한 문장으로 말할 수 있나요?" |
| 범위 설정 | Out of Scope | "명확히 제외할 것은 무엇인가요?" |
| 우선순위 | 기준 | "우선순위를 어떤 기준으로 정했나요?" |
| 리스크 | 대응 | "가장 큰 기술적 리스크는 무엇인가요?" |

---

## 다음 스킬 연결

PRD 완료 후:

1. **기능 상세화** → Feature Spec Skill
2. **정보 구조** → Information Architecture Skill
3. **사용자 플로우** → User Flow Skill

---

*PRD는 팀의 북극성입니다. 명확하게, 그러나 유연하게.*
