---
name: plan-launch-synthesis
description: |
  Phase 8 Launch Prep 단계의 결과를 종합하는 스킬.
  전체 기획 과정의 최종 리포트와 Executive Summary를 생성합니다.
triggers:
  - "launch 종합"
  - "phase 8 종합"
  - "런칭 종합"
  - "최종 종합"
  - "executive summary"
input:
  - 08-launch/growth-strategy.md
  - 08-launch/pitch-deck.md
  - 08-launch/gtm-strategy.md
  - 모든 Phase SYNTHESIS.md
output:
  - 08-launch/SYNTHESIS.md
  - EXECUTIVE-SUMMARY.md
phase: 8
sequence: S8
---

# Launch Synthesis Skill

Phase 8 Launch Prep 단계의 모든 산출물을 종합하고, 전체 기획 과정의 Executive Summary를 생성합니다.

## 종합 대상 스킬

```
┌─────────────────────────────────────────────────────────────┐
│                   Phase 8: Launch Prep                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  27. Growth Strategy    →  성장 전략 수립                    │
│  28. Pitch Deck         →  투자/발표 자료 기획               │
│  29. GTM Strategy       →  시장 진입 전략                    │
│                                                              │
│   ════════════════════════════════════════════════════════   │
│                                                              │
│   S8. Launch Synthesis  →  최종 종합 & Executive Summary     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 최종 대시보드

```
┌─────────────────────────────────────────────────────────────┐
│              🚀 LAUNCH READINESS FINAL CHECK                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Phase 1: Discovery        ████████████████████  ✅ 100%   │
│   Phase 2: Research         ████████████████████  ✅ 100%   │
│   Phase 3: Validation       ████████████████████  ✅ 100%   │
│   Phase 4: Specification    ████████████████████  ✅ 100%   │
│   Phase 5: Estimation       ████████████████████  ✅ 100%   │
│   Phase 6: Design           ████████████████████  ✅ 100%   │
│   Phase 7: Execution        ████████████████████  ✅ 100%   │
│   Phase 8: Launch Prep      ████████████████████  ✅ 100%   │
│   ─────────────────────────────────────────────────────────  │
│                                                              │
│   📊 Overall Completion: 100%                                │
│   🎯 Launch Status: READY                                    │
│   📅 Target Date: {launch_date}                              │
│                                                              │
│              🚀 ALL SYSTEMS GO! 🚀                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 출력 템플릿 1: Launch Synthesis

```markdown
# {Project Name} - Launch Prep 종합 리포트

## Phase 8 Summary | Date: {date}

---

## 1. Executive Summary

### 런칭 준비 완료
> **🚀 READY FOR LAUNCH**

### 핵심 준비 현황
| 영역 | 상태 | 완료일 |
|------|------|--------|
| 성장 전략 | ✅ 완료 | {date} |
| 피치덱 | ✅ 완료 | {date} |
| GTM 전략 | ✅ 완료 | {date} |

---

## 2. 성장 전략 요약

### AARRR 전략 요약

| 단계 | 전략 | 핵심 액션 | 목표 |
|------|------|----------|------|
| Acquisition | {strategy} | {action} | {target} |
| Activation | {strategy} | {action} | {target} |
| Retention | {strategy} | {action} | {target} |
| Revenue | {strategy} | {action} | {target} |
| Referral | {strategy} | {action} | {target} |

### Growth Loop

```
         ┌──────────────────────────────────────┐
         │                                      │
         ▼                                      │
    [신규 가입] → [Aha Moment] → [습관화] → [추천]
         │              │            │          │
         └──────────────┴────────────┴──────────┘
                   Growth Flywheel
```

### Month 1-3 성장 목표

| 지표 | Month 1 | Month 2 | Month 3 |
|------|---------|---------|---------|
| 사용자 수 | {target} | {target} | {target} |
| MAU | {target} | {target} | {target} |
| MRR | {target} | {target} | {target} |

---

## 3. 피치덱 요약

### 12장 구조 완성도

| # | 슬라이드 | 상태 | 핵심 메시지 |
|---|---------|------|------------|
| 1 | Cover | ✅ | {message} |
| 2 | Problem | ✅ | {message} |
| 3 | Solution | ✅ | {message} |
| 4 | Why Now | ✅ | {message} |
| 5 | Market | ✅ | {message} |
| 6 | Product | ✅ | {message} |
| 7 | Traction | ✅ | {message} |
| 8 | Business Model | ✅ | {message} |
| 9 | Competition | ✅ | {message} |
| 10 | Team | ✅ | {message} |
| 11 | Financials | ✅ | {message} |
| 12 | Ask | ✅ | {message} |

### 피치 핵심 스토리

> **One-liner**: {one_liner}
>
> **Problem**: {problem}
>
> **Solution**: {solution}
>
> **Ask**: {ask}

---

## 4. GTM 전략 요약

### 런칭 타임라인

```
      Pre-Launch          Launch Day         Post-Launch
    (D-30 ~ D-1)            (D-Day)          (D+1 ~ D+30)
────────────────────────────────────────────────────────────
[Waitlist 구축]  →  [공식 런칭]  →  [초기 성장 가속]
[커뮤니티 빌딩]      [PR/발표]      [피드백 수집]
[베타 테스트]        [프로모션]      [빠른 개선]
```

### 채널별 런칭 전략

| 채널 | 액션 | 타이밍 | KPI |
|------|------|--------|-----|
| Product Hunt | 런칭 | D-Day | {kpi} |
| Social Media | 캠페인 | D-7 ~ D+7 | {kpi} |
| PR/Media | 보도자료 | D-Day | {kpi} |
| Community | 이벤트 | D-Day ~ D+14 | {kpi} |

### ICP (Ideal Customer Profile)

| 속성 | 정의 |
|------|------|
| 산업 | {industry} |
| 규모 | {size} |
| 역할 | {role} |
| Pain Point | {pain_point} |
| 구매 동기 | {motivation} |

---

## 5. 런칭 체크리스트 최종 확인

### 제품 준비 ✅

- [x] MVP 기능 완료
- [x] QA 완료
- [x] 성능 최적화
- [x] 보안 점검

### 마케팅 준비 ✅

- [x] 랜딩 페이지
- [x] 소셜 미디어 계정
- [x] 보도자료
- [x] 콘텐츠 준비

### 운영 준비 ✅

- [x] 고객 지원 체계
- [x] 모니터링 대시보드
- [x] 온콜 스케줄
- [x] 에스컬레이션 절차

### 비즈니스 준비 ✅

- [x] 결제 시스템
- [x] 약관/정책
- [x] 파트너십

---

## 6. 런칭 D-Day 플랜

### 런칭일 스케줄

| 시간 | 액션 | 담당 | 채널 |
|------|------|------|------|
| 00:00 | 서비스 오픈 | DevOps | - |
| 09:00 | 공식 발표 | Marketing | All |
| 10:00 | Product Hunt 런칭 | PM | PH |
| 12:00 | 소셜 미디어 포스팅 | Marketing | SNS |
| 14:00 | 보도자료 배포 | PR | Media |
| 18:00 | 성과 1차 리뷰 | All | - |

### 비상 대응 체계

| 상황 | 대응 | 담당 | 연락처 |
|------|------|------|--------|
| 서버 장애 | 즉시 롤백 | DevOps | {contact} |
| 결제 오류 | 수동 처리 | Ops | {contact} |
| 보안 이슈 | 서비스 중단 | Security | {contact} |

---

## 7. Phase 8 완료 평가

### 런칭 준비도 최종 점수

| 영역 | 점수 | 상태 |
|------|------|------|
| 성장 전략 | {score}/100 | ✅ |
| 피치덱 | {score}/100 | ✅ |
| GTM 전략 | {score}/100 | ✅ |
| 런칭 체크리스트 | {score}/100 | ✅ |
| **총점** | **{total}/100** | **✅ READY** |

---

*Phase 8 Launch Prep 완료 | 🚀 READY FOR LAUNCH*
```

---

## 출력 템플릿 2: Executive Summary (전체 기획 종합)

```markdown
# {Project Name} - Executive Summary

## 전체 기획 종합 리포트 | {date}

---

## 1. 프로젝트 개요

### One-Liner
> **{one_liner}**

### 핵심 정보

| 항목 | 내용 |
|------|------|
| 프로젝트명 | {project_name} |
| 카테고리 | {category} |
| 타겟 고객 | {target_customer} |
| 핵심 가치 | {core_value} |
| 목표 출시일 | {launch_date} |

---

## 2. 8개 Phase 종합

### Phase 완료 현황

```
Phase 1: Discovery      ✅ 완료  │ 아이디어 검증
Phase 2: Research       ✅ 완료  │ 시장 분석
Phase 3: Validation     ✅ 완료  │ 비즈니스 모델 검증
Phase 4: Specification  ✅ 완료  │ 제품 명세
Phase 5: Estimation     ✅ 완료  │ 비용/일정 추정
Phase 6: Design         ✅ 완료  │ 팀/UX/브랜드
Phase 7: Execution      ✅ 완료  │ 개발/운영 준비
Phase 8: Launch Prep    ✅ 완료  │ 런칭 준비
────────────────────────────────────────────
Total Documents: {n}개  │  기획 기간: {weeks}주
```

### Phase별 핵심 산출물

| Phase | 핵심 산출물 | 주요 결정 |
|-------|-----------|----------|
| 1. Discovery | 아이디어 정의 | {decision} |
| 2. Research | 시장 분석 | TAM: {tam} |
| 3. Validation | 린 캔버스 | BM: {business_model} |
| 4. Specification | PRD | MVP: {mvp_scope} |
| 5. Estimation | 비용/일정 | {budget} / {duration} |
| 6. Design | 팀/UX/브랜드 | {team_size}명 |
| 7. Execution | 로드맵 | {milestones} |
| 8. Launch | GTM 전략 | {launch_date} |

---

## 3. 비즈니스 모델 요약

### 린 캔버스 요약

```
┌─────────────────────────────────────────────────────────────┐
│  PROBLEM       │  SOLUTION     │  UVP           │ CUSTOMER │
│  {p1}          │  {s1}         │                │ {c1}     │
│  {p2}          │  {s2}         │  {uvp}         │ {c2}     │
├────────────────┴───────────────┴────────────────┴──────────┤
│  KEY METRICS: {metrics}    │  CHANNELS: {channels}         │
├────────────────────────────┴───────────────────────────────┤
│  COST: {cost}              │  REVENUE: {revenue}           │
└────────────────────────────┴───────────────────────────────┘
```

### 수익 모델

| 수익원 | 비중 | Year 1 목표 |
|--------|------|------------|
| {revenue_1} | {%}% | {amount} |
| {revenue_2} | {%}% | {amount} |

### 단위 경제학

| 지표 | 값 | 상태 |
|------|-----|------|
| ARPU | {arpu} | - |
| CAC | {cac} | - |
| LTV | {ltv} | - |
| LTV:CAC | {ratio}:1 | ✅ 건전 |

---

## 4. 시장 기회

### 시장 규모

```
TAM ████████████████████████████████ {tam}
SAM ████████████████░░░░░░░░░░░░░░░░ {sam}
SOM █████░░░░░░░░░░░░░░░░░░░░░░░░░░░ {som}
```

### 경쟁 포지셔닝

> **"{positioning_statement}"**

### 차별화 요소
1. {differentiator_1}
2. {differentiator_2}
3. {differentiator_3}

---

## 5. 제품 개요

### MVP 범위

| 기능 | 우선순위 | 상태 |
|------|---------|------|
| {feature_1} | P0 | ✅ |
| {feature_2} | P0 | ✅ |
| {feature_3} | P1 | ✅ |

### 기술 스택

| 레이어 | 기술 |
|--------|------|
| Frontend | {tech} |
| Backend | {tech} |
| Database | {tech} |
| Infra | {tech} |

---

## 6. 실행 계획

### 예산 및 일정

| 항목 | 값 |
|------|-----|
| 총 예산 | {total_budget} |
| 개발 기간 | {duration} |
| 팀 규모 | {team_size}명 |
| 런칭 목표 | {launch_date} |

### 마일스톤

```
{start}                                              {launch}
   │                                                     │
   ▼                                                     ▼
   [설계] → [개발] → [테스트] → [베타] → [런칭]
```

---

## 7. 성장 전략

### Year 1 목표

| 지표 | Q1 | Q2 | Q3 | Q4 |
|------|-----|-----|-----|-----|
| Users | {n} | {n} | {n} | {n} |
| MRR | {n} | {n} | {n} | {n} |

### GTM 전략
- **Primary Channel**: {channel}
- **Launch Strategy**: {strategy}
- **Growth Loop**: {loop}

---

## 8. 팀 구성

### 핵심 팀

| 역할 | 이름 | 강점 |
|------|------|------|
| CEO/PM | {name} | {strength} |
| CTO | {name} | {strength} |
| Designer | {name} | {strength} |

---

## 9. 투자 요청 (선택)

### Funding Ask
- **단계**: {stage}
- **금액**: {amount}
- **용도**: {use_of_funds}

### 사용 계획

| 항목 | 비중 | 금액 |
|------|------|------|
| 인건비 | {%}% | {amount} |
| 마케팅 | {%}% | {amount} |
| 인프라 | {%}% | {amount} |
| 기타 | {%}% | {amount} |

---

## 10. 핵심 리스크 & 대응

| 리스크 | 영향 | 대응 |
|--------|------|------|
| {risk_1} | 🔴 | {mitigation} |
| {risk_2} | 🟡 | {mitigation} |
| {risk_3} | 🟢 | {mitigation} |

---

## 11. 다음 단계

### 즉시 실행
1. {action_1}
2. {action_2}
3. {action_3}

### 30일 내
1. {action_1}
2. {action_2}

### 90일 내
1. {action_1}
2. {action_2}

---

## 12. 부록: 전체 문서 목록

### Phase별 산출물

| Phase | 문서 | 경로 |
|-------|------|------|
| 1 | Idea Capture | 01-discovery/ |
| 1 | Market Discovery | 01-discovery/ |
| 1 | **SYNTHESIS** | 01-discovery/ |
| 2 | TAM-SAM-SOM | 02-research/ |
| ... | ... | ... |
| 8 | **SYNTHESIS** | 08-launch/ |
| - | **EXECUTIVE SUMMARY** | / |

---

*🚀 {Project Name} - Ready for Launch*

*Generated by Planning Agent | {date}*
```

## 🎯 인터랙티브 가이드

### 종합 전 확인 질문

**Q1. 모든 Phase가 완료되었나요?**
- 8개 Phase 모두 SYNTHESIS 완료 확인

**Q2. Executive Summary가 필요한가요?**
- 필요 (투자 유치, 내부 보고용)
- 불필요 (Phase 8 종합만)

**Q3. 런칭 일정이 확정되었나요?**
- 확정됨: {date}
- 미확정: "목표 일정을 정해주세요"

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| 성장 전략 | 목표 검토 | "성장 목표가 현실적인가요?" |
| 피치덱 | 스토리 | "피치 스토리가 설득력 있나요?" |
| GTM | 채널 전략 | "런칭 채널 전략이 적절한가요?" |
| 최종 | 런칭 결정 | "최종 런칭을 진행하시겠어요?" |

---

## 퀄리티 체크리스트

```
□ 8개 Phase SYNTHESIS가 모두 완료되었는가?
□ 성장 전략이 구체적인가?
□ 피치덱 12장이 완성되었는가?
□ GTM 전략이 실행 가능한가?
□ 런칭 체크리스트가 100%인가?
□ Executive Summary가 작성되었는가?
```

---

*S8 Launch Synthesis는 전체 기획의 완결입니다. 모든 것을 종합하여 성공적인 런칭을 준비하세요.*
