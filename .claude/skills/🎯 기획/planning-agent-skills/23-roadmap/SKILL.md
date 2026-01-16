---
name: plan-roadmap
description: |
  로드맵과 마일스톤을 정의하는 스킬.
  단계별 계획과 우선순위를 설정합니다.
triggers:
  - "로드맵"
  - "Roadmap"
  - "마일스톤"
  - "일정 계획"
input:
  - mvp-definition.md 결과
  - effort-estimation.md 결과
output:
  - 07-execution/roadmap.md
---

# Roadmap Skill

제품 로드맵과 마일스톤을 정의합니다.

## 출력 템플릿

```markdown
# {Project Name} - 로드맵

## 1. 로드맵 Overview

### 비전 타임라인

```
NOW          +3M          +6M          +12M         VISION
 │            │            │             │            │
 │   MVP      │   Growth   │   Scale     │   Expand   │
 │  (검증)    │  (성장)    │   (확장)    │   (확대)   │
 │            │            │             │            │
 └────────────┴────────────┴─────────────┴────────────┘
```

### 단계별 목표

| Phase | 기간 | 목표 | 성공 지표 |
|-------|------|------|----------|
| MVP | {duration} | {goal} | {metric} |
| Growth | {duration} | {goal} | {metric} |
| Scale | {duration} | {goal} | {metric} |

---

## 2. Phase 1: MVP

### 목표

> **"{mvp_goal}"**

### 타임라인

```
Week 1-2:  █████████░░░░░░  환경 구축, 기초 작업
Week 3-4:  ███████████████  핵심 기능 개발
Week 5-6:  ██████████████░  부가 기능, 통합
Week 7-8:  █████████░░░░░░  QA, 버그 수정
Week 8:    Launch! 🚀
```

### 마일스톤

| # | 마일스톤 | 목표일 | 산출물 | 상태 |
|---|----------|--------|--------|------|
| M1 | 환경 구축 | Week 1 | 개발 환경, CI/CD | ⬜ |
| M2 | 핵심 기능 | Week 4 | {features} | ⬜ |
| M3 | MVP 완성 | Week 6 | 전체 기능 | ⬜ |
| M4 | QA 완료 | Week 7 | 테스트 통과 | ⬜ |
| M5 | 런칭 | Week 8 | Production | ⬜ |

### 기능 범위

| 기능 | 우선순위 | Phase | 담당 |
|------|----------|-------|------|
| {feature_1} | 🔴 Must | MVP | {owner} |
| {feature_2} | 🔴 Must | MVP | {owner} |
| {feature_3} | 🟡 Should | MVP | {owner} |

### MVP 완료 기준

- [ ] 핵심 기능 동작
- [ ] 주요 플로우 완성
- [ ] 치명적 버그 없음
- [ ] 기본 분석 설정
- [ ] 런칭 체크리스트 완료

---

## 3. Phase 2: Growth

### 목표

> **"{growth_goal}"**

### 타임라인

```
Month 3:   피드백 수집, 개선
Month 4:   핵심 기능 강화
Month 5:   성장 기능 추가
Month 6:   최적화, 스케일 준비
```

### 기능 범위

| 기능 | 트리거 | 목표 | 담당 |
|------|--------|------|------|
| {feature_1} | MVP 완료 후 | {goal} | {owner} |
| {feature_2} | 사용자 {n}명 | {goal} | {owner} |
| {feature_3} | 피드백 기반 | {goal} | {owner} |

### 성공 지표

| 지표 | 목표 | 측정 |
|------|------|------|
| MAU | {target} | Analytics |
| Retention | {target}% | Cohort |
| NPS | {target} | Survey |

---

## 4. Phase 3: Scale

### 목표

> **"{scale_goal}"**

### 주요 이니셔티브

| 이니셔티브 | 목표 | 투자 |
|-----------|------|------|
| {initiative_1} | {goal} | {investment} |
| {initiative_2} | {goal} | {investment} |
| {initiative_3} | {goal} | {investment} |

---

## 5. 기능 로드맵

### Feature Timeline

```
        Q1           Q2           Q3           Q4
         │            │            │            │
Auth     ████████
Core          ████████████████
Billing            ████████
Growth                  ████████████████
Scale                             ████████████████
         │            │            │            │
```

### 분기별 주요 기능

**Q1 (MVP)**
- {feature_1}
- {feature_2}
- {feature_3}

**Q2 (Growth)**
- {feature_4}
- {feature_5}
- {feature_6}

**Q3 (Scale)**
- {feature_7}
- {feature_8}

**Q4 (Expand)**
- {feature_9}
- {feature_10}

---

## 6. 의존성 & 블로커

### 의존성 맵

```
{Feature A}
    │
    └───► {Feature B}
              │
              └───► {Feature C}

{External API}
    │
    └───► {Feature D}
```

### 잠재적 블로커

| 블로커 | 영향 | 대응 | 담당 |
|--------|------|------|------|
| {blocker_1} | {impact} | {mitigation} | {owner} |
| {blocker_2} | {impact} | {mitigation} | {owner} |

---

## 7. 리소스 계획

### 단계별 팀 규모

| Phase | 팀 규모 | 구성 |
|-------|---------|------|
| MVP | {n}명 | {composition} |
| Growth | {n}명 | {composition} |
| Scale | {n}명 | {composition} |

### 예산 계획

| Phase | 인건비 | 인프라 | 기타 | 총액 |
|-------|--------|--------|------|------|
| MVP | {cost} | {cost} | {cost} | {total} |
| Growth | {cost} | {cost} | {cost} | {total} |
| Scale | {cost} | {cost} | {cost} | {total} |

---

## 8. Go/No-Go 기준

### Phase 전환 기준

**MVP → Growth**
| 기준 | 목표 | 실제 | Pass |
|------|------|------|------|
| 사용자 수 | {target} | - | ⬜ |
| Retention | {target}% | - | ⬜ |
| 치명 버그 | 0 | - | ⬜ |

**Growth → Scale**
| 기준 | 목표 | 실제 | Pass |
|------|------|------|------|
| MAU | {target} | - | ⬜ |
| MRR | {target} | - | ⬜ |
| Unit Economics | 양수 | - | ⬜ |

---

## 9. 커뮤니케이션 계획

### 정기 업데이트

| 대상 | 빈도 | 내용 |
|------|------|------|
| 팀 | 주간 | 진행 상황 |
| 이해관계자 | 격주 | 마일스톤 업데이트 |
| 투자자 | 월간 | 지표 리포트 |

### 마일스톤 리뷰

| 마일스톤 | 리뷰 일정 | 참석자 |
|----------|----------|--------|
| M1 | {date} | {attendees} |
| M2 | {date} | {attendees} |

---

## 10. 로드맵 요약

### 한 눈에 보기

```
┌─────────────────────────────────────────────────────────────────┐
│                    {PROJECT} 로드맵                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MVP ({duration})                                               │
│  ─────────────────                                              │
│  목표: {mvp_goal}                                               │
│  기능: {mvp_features}                                           │
│  지표: {mvp_metric}                                             │
│                                                                  │
│  Growth ({duration})                                            │
│  ─────────────────                                              │
│  목표: {growth_goal}                                            │
│  기능: {growth_features}                                        │
│  지표: {growth_metric}                                          │
│                                                                  │
│  Scale ({duration})                                             │
│  ─────────────────                                              │
│  목표: {scale_goal}                                             │
│  기능: {scale_features}                                         │
│  지표: {scale_metric}                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 다음 액션

1. **{action_1}**
2. **{action_2}**
3. **{action_3}**

---

*다음 단계: Risk Management → KPI/OKR*
```

## 퀄리티 체크리스트

```
□ 단계별 목표가 명확한가?
□ 마일스톤이 측정 가능한가?
□ 의존성이 파악되었는가?
□ Go/No-Go 기준이 있는가?
□ 리소스 계획이 현실적인가?
□ 커뮤니케이션 계획이 있는가?
```

## 🎯 인터랙티브 가이드

### 작성 전 확인 질문

**Q1. MVP 범위가 확정되었나요?**
- 확정됨 → MVP 기준 Phase 1 설정
- 미확정 → "MVP Definition 스킬을 먼저 완료해주세요"

**Q2. 공수 추정이 완료되었나요?**
- 완료됨 → 공수 기반 일정 수립
- 미완료 → "Effort Estimation 스킬을 먼저 완료해주세요"

**Q3. 팀 리소스가 확정되었나요?**
- 확정됨 → 리소스 기반 병렬 작업 계획
- 미확정 → "투입 가능한 개발자 수는?"

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| Phase 구분 | 기준 | "각 Phase의 목표는 무엇인가요?" |
| 마일스톤 | 검증 | "이 마일스톤에서 뭘 검증하나요?" |
| 의존성 | 순서 | "반드시 먼저 해야 할 것은?" |
| Go/No-Go | 기준 | "다음 Phase로 가는 조건은?" |

---

## 다음 스킬 연결

Roadmap 완료 후:

1. **리스크 관리** → Risk Management Skill
2. **KPI 설정** → KPI/OKR Skill
3. **실행 시작** → Sprint Planning

---

*로드맵은 나침반이지 지도가 아닙니다. 유연하게 조정하세요.*
