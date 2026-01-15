---
name: plan-idea-intake
description: |
  기획 퀄리티 향상의 핵심 스킬.
  아이디어, 문제 정의, 솔루션 가설을 체계적으로 수집합니다.
triggers:
  - "아이디어 정의"
  - "문제 정의"
  - "서비스 기획 시작"
  - "아이디어 정리"
input:
  - 아이디어 설명
  - 해결하려는 문제 (선택)
  - 솔루션 가설 (선택)
output:
  - 01-discovery/idea-intake.md
---

# Idea Intake Skill

기획 결과물 퀄리티를 결정하는 가장 중요한 스킬입니다.
명확한 문제 정의 = 높은 퀄리티 기획 산출물

## 왜 중요한가?

```
문제 정의 없이 시작
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"앱 기획해줘" → 방향 없는 결과물

문제 정의 충분히
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Idea Intake → 목적에 맞는 기획서
```

## Problem-Solution Fit 프레임워크

### 핵심 질문 3가지

```
1. 누가 (Who) - 이 문제를 겪는 사람은 누구인가?
2. 무엇 (What) - 그들이 겪는 문제는 무엇인가?
3. 어떻게 (How) - 우리 솔루션은 어떻게 해결하는가?
```

## 수집 항목

### 1. 필수 정보 (Must Have)

```yaml
idea:
  name: ""                      # 프로젝트/서비스 이름
  one_liner: ""                 # 한 줄 설명 (엘리베이터 피치)
  category: ""                  # 카테고리 (SaaS, 앱, 플랫폼, 이커머스)

problem:
  statement: ""                 # 문제 정의 (한 문장)
  who_has_it: ""                # 문제를 겪는 사람
  frequency: ""                 # 얼마나 자주 겪는지
  current_solution: ""          # 현재 어떻게 해결하고 있는지
  pain_level: ""                # 불편함 정도 (1-10)

solution:
  description: ""               # 솔루션 설명
  key_features:                 # 핵심 기능 3가지
    - ""
    - ""
    - ""
  how_it_solves: ""             # 어떻게 문제를 해결하는지
```

### 2. 권장 정보 (Should Have)

```yaml
context:
  why_now: ""                   # 왜 지금인가? (타이밍)
  why_you: ""                   # 왜 당신인가? (팀 역량)
  market_size_guess: ""         # 시장 규모 추정 (감으로)

inspiration:
  similar_services: []          # 유사 서비스 (참고할 것)
  different_from: ""            # 차별점 (간단히)

constraints:
  tech_limitations: []          # 기술적 제약
  budget_range: ""              # 예산 범위 (대략)
  timeline: ""                  # 희망 일정 (대략)
```

### 3. 선택 정보 (Nice to Have)

```yaml
validation:
  customer_interviews: false    # 고객 인터뷰 진행 여부
  existing_demand: ""           # 기존 수요 증거
  waitlist: 0                   # 대기자 명단

team:
  members: []                   # 팀 구성원
  expertise: []                 # 보유 역량
  missing_roles: []             # 부족한 역할

goal:
  short_term: ""                # 단기 목표 (3개월)
  long_term: ""                 # 장기 목표 (1년)
  success_metric: ""            # 성공 지표
```

## 인터뷰 질문 템플릿

### Quick Start (5분)

```
1. 어떤 서비스를 만들고 싶으세요?
2. 누구를 위한 서비스인가요?
3. 그 사람들이 겪는 문제는 뭔가요?
4. 현재 그 문제를 어떻게 해결하고 있나요?
5. 당신의 솔루션은 뭐가 다른가요?
```

### Deep Dive (15분)

```
문제 정의
─────────────────────────────────
1. 타겟 고객을 한 문장으로 설명해주세요.
2. 그들이 겪는 가장 큰 문제는?
3. 이 문제가 얼마나 심각한가요? (1-10)
4. 얼마나 자주 이 문제를 겪나요?
5. 현재 어떤 대안을 사용하고 있나요?
6. 현재 대안의 가장 큰 문제점은?

솔루션
─────────────────────────────────
7. 당신의 솔루션을 한 문장으로?
8. 핵심 기능 3가지를 꼽는다면?
9. 기존 대안보다 나은 점은?
10. 사용자가 "와!" 할 순간은?

타이밍 & 팀
─────────────────────────────────
11. 왜 지금 이 서비스가 필요한가요?
12. 당신/팀이 이걸 만들기에 적합한 이유는?
13. 부족한 부분은 뭔가요?

목표
─────────────────────────────────
14. 3개월 후 성공은 어떤 모습인가요?
15. 실패한다면 어떤 이유일까요?
```

## 워크플로우

```
1. 사용자 아이디어 수신
      │
      ▼
2. 필수 정보 확인
      │
      ├─ 부족 → 인터뷰 질문
      │
      ▼
3. Problem-Solution Fit 검토
      │
      ├─ Fit 불명확 → 추가 질문
      │
      ▼
4. 아이디어 정의서 생성
      │
      ▼
5. 사용자 확인 & 보완
      │
      ▼
6. 최종 문서 저장
   → workspace/work-plan/{project}/01-discovery/idea-intake.md
```

## 출력 템플릿

```markdown
# {Project Name} - 아이디어 정의서

## Executive Summary

> **{one_liner}**
>
> {problem_statement}을 겪는 {who_has_it}를 위한 솔루션입니다.

## 1. 문제 정의 (Problem)

### 타겟 고객
- **누구인가**: {who_has_it}
- **특징**: {demographics_hint}

### 문제 상황
| 항목 | 내용 |
|------|------|
| 문제 | {problem_statement} |
| 빈도 | {frequency} |
| 심각도 | {pain_level}/10 |

### 현재 대안과 한계
| 현재 대안 | 한계점 |
|----------|--------|
| {current_solution} | {limitation} |

## 2. 솔루션 (Solution)

### 핵심 가치
{how_it_solves}

### 핵심 기능
| # | 기능 | 해결하는 문제 |
|---|------|--------------|
| 1 | {feature_1} | {problem_solved_1} |
| 2 | {feature_2} | {problem_solved_2} |
| 3 | {feature_3} | {problem_solved_3} |

### 차별화 포인트
{different_from}

## 3. 타이밍 & 팀

### Why Now?
{why_now}

### Why Us?
{why_you}

### 팀 역량
| 영역 | 현재 | 필요 |
|------|------|------|
| 개발 | {dev_status} | {dev_need} |
| 디자인 | {design_status} | {design_need} |
| 비즈니스 | {biz_status} | {biz_need} |

## 4. 제약 조건

### 기술적 제약
{tech_limitations}

### 리소스 제약
- **예산**: {budget_range}
- **일정**: {timeline}

## 5. 가설 & 검증 필요 사항

### 핵심 가설
| # | 가설 | 검증 방법 |
|---|------|----------|
| 1 | {hypothesis_1} | {validation_1} |
| 2 | {hypothesis_2} | {validation_2} |

### 리스크
| 리스크 | 영향 | 대응 |
|--------|------|------|
| {risk_1} | {impact_1} | {mitigation_1} |

## 6. 초기 목표

### 3개월 목표
{short_term_goal}

### 성공 지표
{success_metric}

---

*다음 단계: Value Proposition → Target User 정의*
```

## 퀄리티 체크리스트

```
□ 한 줄 설명이 명확한가?
□ 문제가 구체적으로 정의되었는가?
□ 타겟 고객이 식별 가능한가?
□ 현재 대안과 한계가 파악되었는가?
□ 솔루션이 문제를 해결하는 방법이 명확한가?
□ 핵심 기능 3가지가 정리되었는가?
□ Why Now/Why Us가 설명되었는가?
□ 핵심 가설이 식별되었는가?
```

## Problem-Solution Fit 체크

### Fit이 강한 신호

```
✅ 문제가 구체적이고 빈번함
✅ 현재 대안이 불만족스러움
✅ 솔루션이 직접적으로 문제 해결
✅ 타겟 고객이 명확함
✅ 팀이 도메인 지식 보유
```

### Fit이 약한 신호

```
⚠️ "모든 사람"이 타겟
⚠️ 문제보다 기술이 먼저
⚠️ "있으면 좋겠다" 수준의 문제
⚠️ 경쟁사와 차별점 불명확
⚠️ Why Now가 약함
```

## 정보 부족 시 대응

### 최소 정보로 시작

```yaml
minimum_viable_idea:
  one_liner: "한 줄 설명"
  problem: "해결하려는 문제"
  target_hint: "타겟 힌트"
```

이 정도만 있어도 시작 가능. 단, 결과물이 generic할 수 있음을 안내.

### 점진적 수집

```
1차 기획 → 피드백 → 아이디어 보완 → 2차 기획 (개선)
```

## 다음 스킬 연결

아이디어 정의 완료 후:

1. **가치 제안 정리** → Value Proposition Skill
2. **타겟 구체화** → Target User Skill
3. **바로 검증** → MVP Definition Skill

---

*Idea Intake는 기획의 방향을 결정합니다. 충분한 시간을 투자하세요.*
