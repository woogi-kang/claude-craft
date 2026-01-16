---
name: plan-kpi-okr
description: |
  KPI와 OKR을 설정하는 스킬.
  측정 가능한 목표와 핵심 결과를 정의합니다.
triggers:
  - "KPI 설정"
  - "OKR 설정"
  - "목표 설정"
  - "성과 지표"
input:
  - roadmap.md 결과
  - mvp-definition.md 결과
  - business-model.md 결과
output:
  - 07-execution/kpi-okr.md
---

# KPI/OKR Skill

측정 가능한 목표와 핵심 성과 지표를 설정합니다.

## 출력 템플릿

```markdown
# {Project Name} - KPI & OKR

## 1. North Star Metric

### 핵심 지표

> **"{north_star_metric}"**

| 항목 | 내용 |
|------|------|
| 지표명 | {metric_name} |
| 정의 | {definition} |
| 측정 방식 | {measurement} |
| 현재 값 | {current} |
| 목표 값 | {target} |

### North Star 선정 이유

```
왜 이 지표인가?
─────────────────────────────────────
1. 고객 가치와 직접 연결됨
2. 비즈니스 성장을 반영함
3. 팀 전체가 영향을 줄 수 있음
4. 측정이 가능하고 실행 가능함
```

### 지표 계층

```
                    North Star
                        │
         ┌──────────────┼──────────────┐
         │              │              │
    Acquisition    Activation     Revenue
         │              │              │
    ┌────┴────┐    ┌────┴────┐   ┌────┴────┐
  Visits    Signup  Onboard  Usage  Conv  ARPU
```

---

## 2. AARRR Metrics (Pirate Metrics)

### 퍼널 지표

| Stage | 지표 | 현재 | 목표 | 측정 |
|-------|------|------|------|------|
| **Acquisition** | {metric} | {current} | {target} | {how} |
| **Activation** | {metric} | {current} | {target} | {how} |
| **Retention** | {metric} | {current} | {target} | {how} |
| **Revenue** | {metric} | {current} | {target} | {how} |
| **Referral** | {metric} | {current} | {target} | {how} |

### 상세 지표

#### Acquisition (획득)

| 지표 | 정의 | 목표 | 측정 |
|------|------|------|------|
| 방문자 수 | Unique Visitors / 월 | {target} | GA |
| 가입 전환율 | 가입 / 방문 | {target}% | GA |
| CAC | 마케팅비 / 신규고객 | {target} | 계산 |
| 채널별 유입 | 채널별 비율 | {target} | UTM |

#### Activation (활성화)

| 지표 | 정의 | 목표 | 측정 |
|------|------|------|------|
| 온보딩 완료율 | 완료 / 가입 | {target}% | Event |
| Aha Moment 도달 | {aha_action} 완료 | {target}% | Event |
| 첫 핵심 액션 | {core_action} | {target}% | Event |
| Time to Value | 가입~핵심액션 시간 | < {target} | Event |

#### Retention (유지)

| 지표 | 정의 | 목표 | 측정 |
|------|------|------|------|
| D1 Retention | 1일 후 재방문 | {target}% | Cohort |
| D7 Retention | 7일 후 재방문 | {target}% | Cohort |
| D30 Retention | 30일 후 재방문 | {target}% | Cohort |
| WAU/MAU | 주간/월간 비율 | {target}% | Analytics |

#### Revenue (수익)

| 지표 | 정의 | 목표 | 측정 |
|------|------|------|------|
| MRR | 월간 반복 매출 | {target} | Billing |
| ARPU | 사용자당 매출 | {target} | 계산 |
| LTV | 고객 생애 가치 | {target} | 계산 |
| LTV/CAC | 획득 효율 | > 3 | 계산 |

#### Referral (추천)

| 지표 | 정의 | 목표 | 측정 |
|------|------|------|------|
| NPS | 추천 의향 | > 50 | Survey |
| Viral Coefficient | 추천당 신규 | > 1 | 계산 |
| 추천 전환율 | 추천 가입 / 추천 발송 | {target}% | Event |

---

## 3. OKR (Objectives & Key Results)

### OKR 프레임워크

```
Objective: 영감을 주는 정성적 목표
   │
   ├── KR1: 측정 가능한 결과 (70% 달성이 Good)
   ├── KR2: 측정 가능한 결과
   └── KR3: 측정 가능한 결과
```

### Q{N} OKR

#### Objective 1: {Objective Title}

> **"{objective_statement}"**

| KR | Key Result | 목표 | 현재 | 진행 |
|----|-----------|------|------|------|
| KR1 | {key_result_1} | {target} | {current} | ░░░░░ 0% |
| KR2 | {key_result_2} | {target} | {current} | ░░░░░ 0% |
| KR3 | {key_result_3} | {target} | {current} | ░░░░░ 0% |

**Initiative (핵심 활동)**
- {initiative_1}
- {initiative_2}
- {initiative_3}

#### Objective 2: {Objective Title}

> **"{objective_statement}"**

| KR | Key Result | 목표 | 현재 | 진행 |
|----|-----------|------|------|------|
| KR1 | {key_result_1} | {target} | {current} | ░░░░░ 0% |
| KR2 | {key_result_2} | {target} | {current} | ░░░░░ 0% |
| KR3 | {key_result_3} | {target} | {current} | ░░░░░ 0% |

#### Objective 3: {Objective Title}

(동일 구조)

### Team OKR

#### Product Team

| Objective | KR | 목표 |
|-----------|-----|------|
| {obj} | {kr_1} | {target} |
| | {kr_2} | {target} |

#### Engineering Team

| Objective | KR | 목표 |
|-----------|-----|------|
| {obj} | {kr_1} | {target} |
| | {kr_2} | {target} |

---

## 4. Phase별 목표

### MVP Phase

| 영역 | 지표 | 목표 | 기간 |
|------|------|------|------|
| Product | MVP 완성 | 100% | Week 8 |
| Users | 베타 사용자 | {target}명 | Week 8 |
| Activation | Aha Moment | {target}% | Week 8 |
| Feedback | NPS | > 30 | Week 8 |

### Growth Phase

| 영역 | 지표 | 목표 | 기간 |
|------|------|------|------|
| Users | MAU | {target} | Month 6 |
| Retention | D30 | {target}% | Month 6 |
| Revenue | MRR | {target} | Month 6 |

### Scale Phase

| 영역 | 지표 | 목표 | 기간 |
|------|------|------|------|
| Users | MAU | {target} | Month 12 |
| Revenue | ARR | {target} | Month 12 |
| Efficiency | LTV/CAC | > 3 | Month 12 |

---

## 5. KPI 대시보드

### 일간 모니터링

| 지표 | 어제 | 오늘 | WoW | 상태 |
|------|------|------|-----|------|
| DAU | {n} | {n} | {%} | 🟢 |
| 신규 가입 | {n} | {n} | {%} | 🟡 |
| 핵심 액션 | {n} | {n} | {%} | 🟢 |
| 매출 | {n} | {n} | {%} | 🟢 |

### 주간 모니터링

| 지표 | 이번주 | 지난주 | MoM | 상태 |
|------|--------|--------|-----|------|
| WAU | {n} | {n} | {%} | 🟢 |
| Retention | {%} | {%} | {%} | 🟡 |
| 전환율 | {%} | {%} | {%} | 🟢 |

### 월간 모니터링

| 지표 | 이번달 | 지난달 | 목표 | 달성률 |
|------|--------|--------|------|--------|
| MAU | {n} | {n} | {target} | {%} |
| MRR | {n} | {n} | {target} | {%} |
| NPS | {n} | {n} | {target} | {%} |

---

## 6. 지표 정의서

### 핵심 지표 정의

#### {Metric Name}

| 항목 | 내용 |
|------|------|
| 정의 | {exact_definition} |
| 공식 | {formula} |
| 데이터 소스 | {source} |
| 측정 주기 | {frequency} |
| 담당자 | {owner} |

**계산 예시**
```
{metric} = {numerator} / {denominator}
         = {example_value} / {example_value}
         = {result}
```

**주의사항**
- {caveat_1}
- {caveat_2}

---

## 7. 목표 달성 전략

### Input → Output → Outcome

```
Input (투입)          Output (산출)         Outcome (결과)
─────────────────────────────────────────────────────────
마케팅 예산           캠페인 수              신규 가입
개발 시간             기능 개수              사용률
CS 인력               응답 수                만족도
```

### Leading vs Lagging Indicators

| Lagging (결과) | Leading (선행) |
|---------------|----------------|
| 매출 | 데모 신청 수 |
| 이탈률 | 기능 사용 빈도 |
| NPS | 지원 티켓 수 |
| LTV | 첫 주 사용 패턴 |

### 집중 지표

```
This Quarter Focus:
─────────────────────────────────────
1순위: {metric_1} ← 현재 {current}, 목표 {target}
2순위: {metric_2}
3순위: {metric_3}
```

---

## 8. 측정 인프라

### Analytics Stack

| 용도 | 도구 | 설정 |
|------|------|------|
| 웹 분석 | Google Analytics 4 | ⬜ |
| 제품 분석 | Amplitude / Mixpanel | ⬜ |
| 사용자 피드백 | Hotjar | ⬜ |
| A/B 테스트 | {tool} | ⬜ |
| 대시보드 | {tool} | ⬜ |

### Event Tracking

| 이벤트 | 설명 | 속성 |
|--------|------|------|
| sign_up | 회원가입 완료 | source, plan |
| {aha_event} | Aha Moment | - |
| {core_event} | 핵심 액션 | type |
| purchase | 결제 | amount, plan |

### Data Pipeline

```
Event → Analytics → Warehouse → Dashboard
  │         │           │           │
 SDK       GA4       BigQuery    Looker
```

---

## 9. 리뷰 & 커뮤니케이션

### OKR 리뷰 주기

| 리뷰 | 주기 | 참석 | 목적 |
|------|------|------|------|
| OKR Check-in | 주간 | 팀 | 진행 점검 |
| OKR Review | 월간 | 전체 | 조정 필요성 |
| OKR Retro | 분기 | 전체 | 다음 분기 설정 |

### 진행 상황 공유

| 채널 | 내용 | 주기 |
|------|------|------|
| Slack #metrics | 일간 지표 | 매일 |
| Weekly Report | 주간 대시보드 | 주간 |
| All-hands | OKR 진행 | 월간 |

---

## 10. 결론

### OKR 요약

```
┌─────────────────────────────────────────────────────────────────┐
│                    Q{N} OKR Summary                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ⭐ North Star: {north_star_metric}                             │
│     Target: {target}                                            │
│                                                                  │
│  O1: {objective_1}                                              │
│      KR1: {kr} ({progress}%)                                    │
│      KR2: {kr} ({progress}%)                                    │
│                                                                  │
│  O2: {objective_2}                                              │
│      KR1: {kr} ({progress}%)                                    │
│      KR2: {kr} ({progress}%)                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 다음 액션

1. **{action_1}** ← Analytics 설정
2. **{action_2}** ← 대시보드 구축
3. **{action_3}** ← 팀 OKR 정렬

---

*다음 단계: Operation Plan → Growth Strategy*
```

## 퀄리티 체크리스트

```
□ North Star Metric이 정의되었는가?
□ AARRR 각 단계 지표가 있는가?
□ OKR이 SMART 기준을 충족하는가?
□ 측정 방법이 명확한가?
□ Analytics 설정 계획이 있는가?
□ 리뷰 주기가 정해졌는가?
```

## 좋은 OKR 기준

```
✅ Objective
- 영감을 주는 정성적 목표
- 팀이 공감하고 동기부여되는 목표
- 분기 내 달성 가능한 범위

✅ Key Result
- 측정 가능한 정량적 결과
- 70% 달성이 Good (stretch goal)
- 3-5개 이내
```

## 🎯 인터랙티브 가이드

### 작성 전 확인 질문

**Q1. North Star Metric이 정해졌나요?**
- 정해짐 → North Star 기반 OKR 설계
- 미정 → "서비스 성공을 대표하는 하나의 지표는?"

**Q2. 분석 도구가 설치되었나요?**
- 설치됨 → 지표 측정 가능
- 미설치 → "Data Strategy 스킬을 먼저 완료해주세요"

**Q3. OKR 주기를 정했나요?**
- 정함 → 주기에 맞는 목표 설정
- 안 정함 → "분기별 OKR을 권장합니다. 동의하시나요?"

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| Objective | 영감 | "이 목표가 팀에 영감을 주나요?" |
| Key Result | 측정 | "이 결과를 어떻게 측정하나요?" |
| 난이도 | Stretch | "70% 달성이 Good인 수준인가요?" |
| 정렬 | 연결 | "이 OKR이 회사 목표와 연결되나요?" |

---

## 다음 스킬 연결

KPI/OKR 완료 후:

1. **운영 계획** → Operation Plan Skill
2. **성장 전략** → Growth Strategy Skill
3. **실행 시작** → Sprint Planning

---

*측정하지 않으면 관리할 수 없습니다. 단, 모든 것을 측정할 필요는 없습니다.*
