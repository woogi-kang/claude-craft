---
name: plan-gtm-strategy
description: |
  Go-to-Market 전략을 수립하는 스킬.
  시장 진입과 런칭 전략을 정의합니다.
triggers:
  - "GTM 전략"
  - "Go-to-Market"
  - "런칭 전략"
  - "시장 진입"
input:
  - growth-strategy.md 결과
  - target-user.md 결과
  - market-research.md 결과
output:
  - 08-launch/gtm-strategy.md
---

# GTM Strategy Skill

시장 진입 전략과 런칭 실행 계획을 수립합니다.

## 출력 템플릿

```markdown
# {Project Name} - Go-to-Market 전략

## 1. GTM Overview

### 런칭 목표

> **"{launch_goal}"**

| 항목 | 내용 |
|------|------|
| 런칭일 | {date} |
| 타겟 | {target} |
| 목표 | {objective} |
| 성공 지표 | {metric} |

### GTM 전략 유형

| 전략 | 특징 | 우리 선택 |
|------|------|----------|
| Product-Led | 제품 중심, 셀프서비스 | ⬜ |
| Sales-Led | 영업 중심, 직접 판매 | ⬜ |
| Community-Led | 커뮤니티 중심 | ⬜ |
| Partner-Led | 파트너십 중심 | ⬜ |

**선택: {chosen_strategy}**

이유: {rationale}

---

## 2. 타겟 시장

### 시장 세분화

| 세그먼트 | 규모 | 특징 | 우선순위 |
|----------|------|------|----------|
| {segment_1} | {size} | {characteristic} | 🔴 |
| {segment_2} | {size} | {characteristic} | 🟡 |
| {segment_3} | {size} | {characteristic} | 🟢 |

### ICP (Ideal Customer Profile)

```
Primary ICP:
─────────────────────────────────────
산업:        {industry}
규모:        {company_size}
역할:        {buyer_role}
예산:        {budget_range}
Pain Point:  {main_pain}
```

### 초기 타겟

| 구분 | 내용 |
|------|------|
| Beachhead Market | {beachhead} |
| 초기 고객 수 | {target_customers} |
| 초기 매출 목표 | {revenue_target} |
| 성공 기준 | {success_criteria} |

---

## 3. 가치 제안 메시지

### 핵심 메시지

> **"{core_message}"**

### 청중별 메시지

| 청중 | 메시지 | 증거 |
|------|--------|------|
| 의사결정자 | {message_decision_maker} | {proof} |
| 실사용자 | {message_end_user} | {proof} |
| 영향력자 | {message_influencer} | {proof} |

### 메시지 프레임워크

**Problem Agitation Solution (PAS)**
```
Problem:   {problem_statement}
Agitation: {why_it_matters}
Solution:  {our_solution}
```

**Before → After → Bridge**
```
Before:  {current_state}
After:   {desired_state}
Bridge:  {how_we_help}
```

### 차별화 포인트

| 경쟁사 | 그들의 메시지 | 우리의 차별점 |
|--------|-------------|-------------|
| {comp_1} | {their_msg} | {our_diff} |
| {comp_2} | {their_msg} | {our_diff} |

---

## 4. 채널 전략

### 채널 믹스

| 채널 | 유형 | 역할 | 우선순위 |
|------|------|------|----------|
| {channel_1} | Owned | Awareness | 🔴 |
| {channel_2} | Earned | Trust | 🔴 |
| {channel_3} | Paid | Scale | 🟡 |
| {channel_4} | Partner | Access | 🟡 |

### 채널별 전략

#### Owned Media (자체 채널)

| 채널 | 콘텐츠 | 빈도 | KPI |
|------|--------|------|-----|
| 웹사이트 | 랜딩 페이지, 블로그 | 상시 | 트래픽, 전환 |
| 이메일 | 뉴스레터, 드립 | 주 {n}회 | Open, CTR |
| SNS | {platforms} | 일 {n}회 | Engagement |

#### Earned Media (획득 채널)

| 채널 | 전략 | 목표 |
|------|------|------|
| PR | {pr_strategy} | {goal} |
| 리뷰 | {review_strategy} | {goal} |
| 추천 | {referral_strategy} | {goal} |
| SEO | {seo_strategy} | {goal} |

#### Paid Media (유료 채널)

| 채널 | 예산 | 타겟 | 목표 CAC |
|------|------|------|----------|
| Google Ads | {budget} | {target} | ${cac} |
| Meta Ads | {budget} | {target} | ${cac} |
| {other} | {budget} | {target} | ${cac} |

---

## 5. 런칭 단계

### 런칭 타임라인

```
Pre-Launch        Launch          Post-Launch
(D-30 ~ D-1)      (D-Day)         (D+1 ~ D+30)
    │                │                 │
    ▼                ▼                 ▼
준비/빌드업       공식 런칭         모니터링/최적화
```

### Phase 1: Pre-Launch (D-30 ~ D-1)

#### 빌드업 활동

| Week | 활동 | 목표 |
|------|------|------|
| W-4 | 티저 콘텐츠 | 호기심 유발 |
| W-3 | 대기자 명단 | {n}명 확보 |
| W-2 | 베타 접근 | 얼리어답터 확보 |
| W-1 | 최종 준비 | 모든 채널 ready |

#### Pre-Launch 체크리스트

```
Marketing
─────────────────────────────────────
□ 랜딩 페이지 라이브
□ 대기자 명단 페이지
□ 이메일 시퀀스 설정
□ SNS 계정 준비
□ 보도자료 초안
□ 인플루언서 섭외

Product
─────────────────────────────────────
□ 베타 테스트 완료
□ 온보딩 플로우 검증
□ 결제 시스템 테스트
□ 고객 지원 준비
□ FAQ 문서화
□ 버그 수정 완료
```

### Phase 2: Launch (D-Day)

#### 런칭 일정

| 시간 | 활동 | 담당 |
|------|------|------|
| 06:00 | 최종 점검 | Tech |
| 09:00 | 공식 오픈 | PM |
| 09:00 | 이메일 발송 | Marketing |
| 09:30 | SNS 포스팅 | Marketing |
| 10:00 | PR 배포 | Marketing |
| 12:00 | 중간 점검 | 전원 |
| 18:00 | 성과 리뷰 | PM |

#### 런칭 체크리스트

```
□ 제품 정상 작동 확인
□ 이메일 일괄 발송
□ 모든 SNS 채널 포스팅
□ 보도자료 배포
□ 모니터링 대시보드 확인
□ 고객 지원 채널 오픈
□ 실시간 피드백 대응
```

### Phase 3: Post-Launch (D+1 ~ D+30)

| Week | 활동 | 목표 |
|------|------|------|
| D+1~7 | 모니터링, 버그 수정 | 안정화 |
| D+8~14 | 피드백 수집 | 개선점 파악 |
| D+15~21 | 최적화 | 전환율 개선 |
| D+22~30 | 회고, 다음 계획 | 학습 |

---

## 6. 콘텐츠 전략

### 런칭 콘텐츠 맵

| 단계 | 콘텐츠 | 채널 | 목적 |
|------|--------|------|------|
| Awareness | {content_1} | {channel} | 인지 |
| Interest | {content_2} | {channel} | 관심 |
| Decision | {content_3} | {channel} | 결정 |
| Action | {content_4} | {channel} | 전환 |

### 핵심 콘텐츠

#### 1. 랜딩 페이지

| 섹션 | 내용 |
|------|------|
| Hero | {headline} + CTA |
| Problem | {pain_points} |
| Solution | {features} |
| Social Proof | {testimonials} |
| Pricing | {plans} |
| FAQ | {questions} |

#### 2. 런칭 이메일

| 이메일 | 제목 | 목적 |
|--------|------|------|
| 런칭 안내 | {subject} | 가입 유도 |
| 24시간 후 | {subject} | 리마인더 |
| 7일 후 | {subject} | 미가입자 전환 |

#### 3. SNS 콘텐츠

| 플랫폼 | 콘텐츠 유형 | 빈도 |
|--------|-----------|------|
| {platform_1} | {content_type} | {frequency} |
| {platform_2} | {content_type} | {frequency} |

---

## 7. 파트너십 전략

### 파트너 유형

| 유형 | 역할 | 예시 |
|------|------|------|
| 기술 파트너 | 통합, 연동 | {example} |
| 채널 파트너 | 판매, 리셀러 | {example} |
| 마케팅 파트너 | 공동 프로모션 | {example} |
| 전략 파트너 | 번들, 협업 | {example} |

### 타겟 파트너

| 파트너 | 협업 내용 | 우선순위 | 상태 |
|--------|----------|----------|------|
| {partner_1} | {collaboration} | 🔴 | {status} |
| {partner_2} | {collaboration} | 🟡 | {status} |

### 파트너 가치 제안

| 파트너 혜택 | 우리 혜택 |
|------------|----------|
| {benefit_for_partner_1} | {benefit_for_us_1} |
| {benefit_for_partner_2} | {benefit_for_us_2} |

---

## 8. 가격 & 프로모션

### 런칭 프로모션

| 프로모션 | 내용 | 기간 | 조건 |
|----------|------|------|------|
| 얼리버드 | {discount}% 할인 | {period} | 첫 {n}명 |
| 런칭 특가 | {offer} | {period} | 모든 가입자 |
| 추천 보너스 | {reward} | 상시 | 추천 시 |

### 가격 전략

| 전략 | 설명 | 적용 |
|------|------|------|
| Penetration | 낮은 가격으로 시장 진입 | ⬜ |
| Skimming | 높은 가격에서 시작 | ⬜ |
| Freemium | 무료 + 유료 | ⬜ |
| Trial | 무료 체험 후 유료 | ⬜ |

**선택: {chosen_strategy}**

---

## 9. 측정 & KPI

### 런칭 KPI

| 지표 | D-Day | Week 1 | Month 1 |
|------|-------|--------|---------|
| 방문자 | {n} | {n} | {n} |
| 가입자 | {n} | {n} | {n} |
| 활성 사용자 | {n} | {n} | {n} |
| 유료 전환 | {n} | {n} | {n} |
| 매출 | ${n} | ${n} | ${n} |

### 채널별 KPI

| 채널 | 지표 | 목표 |
|------|------|------|
| 웹사이트 | 전환율 | {%} |
| 이메일 | Open Rate | {%} |
| SNS | Engagement | {%} |
| Paid | ROAS | {x} |

### 모니터링 대시보드

```
┌─────────────────────────────────────────────────────────────────┐
│                    Launch Dashboard                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  📊 Today's Performance                                         │
│  ─────────────────────                                          │
│  Visitors:     {n}     (+{%} vs goal)                          │
│  Sign-ups:     {n}     (+{%} vs goal)                          │
│  Conversions:  {n}     (+{%} vs goal)                          │
│  Revenue:      ${n}    (+{%} vs goal)                          │
│                                                                  │
│  📈 Channel Performance                                         │
│  ─────────────────────                                          │
│  Organic:      {%}                                              │
│  Email:        {%}                                              │
│  Social:       {%}                                              │
│  Paid:         {%}                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. 위험 관리

### 런칭 리스크

| 리스크 | 확률 | 영향 | 대응 |
|--------|------|------|------|
| 서버 과부하 | 🟡 | 🔴 | Auto-scaling |
| 낮은 관심 | 🟡 | 🟠 | 추가 마케팅 |
| 버그 발생 | 🟠 | 🟠 | Hotfix 준비 |
| 부정적 피드백 | 🟢 | 🟡 | 빠른 대응 |

### 비상 계획

| 시나리오 | 트리거 | 액션 |
|----------|--------|------|
| 서버 장애 | 응답 > 10s | 캐시 활성화, 스케일업 |
| 전환율 < 1% | D+3 | 랜딩 페이지 A/B 테스트 |
| 부정 리뷰 | 3건 이상 | 개별 대응, 개선 약속 |

---

## 11. 팀 & 역할

### 런칭 팀

| 역할 | 담당자 | 책임 |
|------|--------|------|
| Launch Lead | {name} | 전체 조율 |
| Marketing | {name} | 콘텐츠, 채널 |
| Product | {name} | 제품 준비 |
| Engineering | {name} | 기술 안정화 |
| CS | {name} | 고객 대응 |

### 커뮤니케이션

| 용도 | 채널 | 빈도 |
|------|------|------|
| 실시간 현황 | Slack #launch | 실시간 |
| 일간 리포트 | 이메일 | 매일 |
| 이슈 에스컬레이션 | 전화/긴급 채널 | 즉시 |

---

## 12. 결론

### GTM 체크리스트

```
Pre-Launch
─────────────────────────────────────
□ 타겟 시장 정의
□ 메시지 개발
□ 콘텐츠 제작
□ 채널 설정
□ 대기자 명단 구축

Launch
─────────────────────────────────────
□ 모든 채널 활성화
□ 모니터링 체계 가동
□ 고객 지원 준비

Post-Launch
─────────────────────────────────────
□ 데이터 수집
□ 피드백 분석
□ 최적화 실행
```

### 핵심 성공 요인

```
1. 명확한 ICP와 메시지
2. 채널 집중 (분산 금지)
3. 빠른 실행과 학습
4. 데이터 기반 최적화
```

### 다음 액션

1. **{action_1}** ← 랜딩 페이지 완성
2. **{action_2}** ← 대기자 명단 구축
3. **{action_3}** ← 콘텐츠 제작
4. **{action_4}** ← 파트너십 접촉

---

*마케팅 Agent 연계로 실제 콘텐츠 제작 가능*
```

## 퀄리티 체크리스트

```
□ 타겟 시장이 명확한가?
□ 메시지가 차별화되었는가?
□ 채널 전략이 구체적인가?
□ 런칭 타임라인이 있는가?
□ KPI가 정의되었는가?
□ 리스크 대응이 있는가?
□ 팀 역할이 명확한가?
```

## 다음 스킬 연결

GTM Strategy 완료 후:

1. **콘텐츠 제작** → Marketing Agent 연계
2. **디자인** → Frontend Design Agent 연계
3. **개발** → Development Agent 연계

---

*GTM은 계획보다 실행입니다. 작게 시작하고, 빠르게 학습하세요.*
