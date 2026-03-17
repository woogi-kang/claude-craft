---
name: mkt-analytics-kpi
description: |
  마케팅 KPI 정의 및 대시보드 설계.
  채널별, 단계별 핵심 지표를 설정합니다.
triggers:
  - "KPI 설정"
  - "대시보드"
  - "마케팅 분석"
  - "성과 지표"
input:
  - strategy/marketing-strategy.md
  - campaigns/*.md
output:
  - reports/kpi-dashboard.md
---

# Analytics KPI Skill

마케팅 성과 측정을 위한 KPI와 대시보드를 설계합니다.

## 마케팅 KPI 체계

### 퍼널별 KPI

```
┌─────────────────────────────────────────────────────────────┐
│                    Marketing KPI Funnel                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   TOFU (Top of Funnel) - 인지                               │
│   ├─ 웹사이트 방문자                                         │
│   ├─ 노출수 (Impressions)                                   │
│   ├─ 소셜 도달률                                             │
│   └─ 브랜드 검색량                                           │
│                                                              │
│   MOFU (Middle of Funnel) - 고려                            │
│   ├─ 리드 수                                                 │
│   ├─ 콘텐츠 다운로드                                         │
│   ├─ 이메일 오픈율/클릭률                                    │
│   └─ 제품 페이지 방문                                        │
│                                                              │
│   BOFU (Bottom of Funnel) - 전환                            │
│   ├─ 전환율                                                  │
│   ├─ 가입/구매 수                                            │
│   ├─ CAC (고객획득비용)                                      │
│   └─ 매출                                                    │
│                                                              │
│   POST-FUNNEL - 충성                                        │
│   ├─ LTV (고객생애가치)                                      │
│   ├─ 유지율                                                  │
│   ├─ NPS                                                    │
│   └─ 추천율                                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 채널별 KPI

```yaml
channel_kpis:
  paid_search:
    - impressions
    - clicks
    - ctr
    - cpc
    - conversions
    - conversion_rate
    - cpa
    - roas

  paid_social:
    - reach
    - impressions
    - engagement_rate
    - clicks
    - ctr
    - cpc
    - conversions
    - cpa

  organic_search:
    - organic_traffic
    - keyword_rankings
    - organic_conversions
    - pages_per_session
    - bounce_rate

  email:
    - list_size
    - open_rate
    - click_rate
    - unsubscribe_rate
    - conversion_rate

  content:
    - page_views
    - time_on_page
    - social_shares
    - backlinks
    - lead_magnet_downloads

  social_organic:
    - followers
    - engagement_rate
    - reach
    - shares
    - mentions
```

## 핵심 계산식

### 고객 관련

```yaml
calculations:
  cac:
    formula: "총 마케팅 비용 ÷ 신규 고객 수"
    example: "₩10,000,000 ÷ 100 = ₩100,000"

  ltv:
    formula: "평균 구매 금액 × 구매 빈도 × 고객 수명"
    example: "₩50,000 × 12회 × 3년 = ₩1,800,000"

  ltv_cac_ratio:
    formula: "LTV ÷ CAC"
    benchmark: "> 3:1 권장"
    example: "₩1,800,000 ÷ ₩100,000 = 18:1"

  payback_period:
    formula: "CAC ÷ 월간 매출"
    benchmark: "< 12개월 권장"
```

### 마케팅 효율

```yaml
efficiency_metrics:
  roas:
    formula: "광고 매출 ÷ 광고 비용"
    example: "₩50,000,000 ÷ ₩10,000,000 = 5x"

  roi:
    formula: "(매출 - 비용) ÷ 비용 × 100"
    example: "(₩50M - ₩10M) ÷ ₩10M × 100 = 400%"

  conversion_rate:
    formula: "전환 수 ÷ 방문자 수 × 100"
    example: "500 ÷ 10,000 × 100 = 5%"
```

## 워크플로우

```
1. 비즈니스 목표 확인
      │
      ▼
2. North Star Metric 정의
      │
      ▼
3. 퍼널별 KPI 선정
      │
      ▼
4. 채널별 KPI 선정
      │
      ▼
5. 목표치 설정
      │
      ▼
6. 대시보드 설계
      │
      ▼
7. KPI 문서 저장
   → workspace/work-marketing/reports/kpi-dashboard.md
```

## 출력 템플릿

```markdown
# {Project Name} Marketing KPI Dashboard

## North Star Metric

| 지표 | 현재 | 목표 | 기간 |
|------|------|------|------|
| **{north_star_metric}** | {current} | {target} | {period} |

**정의**: {definition}

**선정 이유**: {rationale}

---

## Executive Summary

### 이번 기간 성과 요약

| 지표 | 목표 | 실적 | 달성률 | 추이 |
|------|------|------|--------|------|
| {metric_1} | {target} | {actual} | {%} | ↑/↓ |
| {metric_2} | {target} | {actual} | {%} | ↑/↓ |
| {metric_3} | {target} | {actual} | {%} | ↑/↓ |

### 주요 인사이트

1. **{insight_1}**
2. **{insight_2}**
3. **{insight_3}**

---

## Funnel Metrics

### TOFU (인지)

| 지표 | 현재 | 목표 | Gap | 추이 |
|------|------|------|-----|------|
| 웹사이트 방문자 | {current} | {target} | {gap} | {trend} |
| 노출수 | {current} | {target} | {gap} | {trend} |
| 소셜 도달 | {current} | {target} | {gap} | {trend} |

### MOFU (고려)

| 지표 | 현재 | 목표 | Gap | 추이 |
|------|------|------|-----|------|
| 리드 수 | {current} | {target} | {gap} | {trend} |
| 이메일 구독자 | {current} | {target} | {gap} | {trend} |
| 콘텐츠 다운로드 | {current} | {target} | {gap} | {trend} |

### BOFU (전환)

| 지표 | 현재 | 목표 | Gap | 추이 |
|------|------|------|-----|------|
| 전환율 | {current}% | {target}% | {gap} | {trend} |
| 신규 고객 | {current} | {target} | {gap} | {trend} |
| 매출 | {current} | {target} | {gap} | {trend} |
| CAC | {current} | {target} | {gap} | {trend} |

### POST-FUNNEL (충성)

| 지표 | 현재 | 목표 | Gap | 추이 |
|------|------|------|-----|------|
| LTV | {current} | {target} | {gap} | {trend} |
| LTV:CAC | {current} | {target} | {gap} | {trend} |
| 유지율 | {current}% | {target}% | {gap} | {trend} |
| NPS | {current} | {target} | {gap} | {trend} |

---

## Channel Performance

### Paid Search (Google Ads)

| 지표 | 이번 기간 | 이전 기간 | 변화 |
|------|----------|----------|------|
| 광고비 | {spend} | {prev} | {change} |
| 클릭 | {clicks} | {prev} | {change} |
| CTR | {ctr}% | {prev}% | {change} |
| CPC | {cpc} | {prev} | {change} |
| 전환 | {conv} | {prev} | {change} |
| CPA | {cpa} | {prev} | {change} |
| ROAS | {roas}x | {prev}x | {change} |

### Paid Social (Meta)

| 지표 | 이번 기간 | 이전 기간 | 변화 |
|------|----------|----------|------|
| 광고비 | {spend} | {prev} | {change} |
| 도달 | {reach} | {prev} | {change} |
| 참여율 | {engagement}% | {prev}% | {change} |
| 클릭 | {clicks} | {prev} | {change} |
| 전환 | {conv} | {prev} | {change} |
| CPA | {cpa} | {prev} | {change} |

### Organic Search (SEO)

| 지표 | 이번 기간 | 이전 기간 | 변화 |
|------|----------|----------|------|
| 유기 트래픽 | {traffic} | {prev} | {change} |
| 키워드 순위 (평균) | {rank} | {prev} | {change} |
| 유기 전환 | {conv} | {prev} | {change} |
| 이탈률 | {bounce}% | {prev}% | {change} |

### Email

| 지표 | 이번 기간 | 이전 기간 | 변화 |
|------|----------|----------|------|
| 리스트 크기 | {size} | {prev} | {change} |
| 발송 수 | {sent} | {prev} | {change} |
| 오픈율 | {open}% | {prev}% | {change} |
| 클릭률 | {click}% | {prev}% | {change} |
| 전환 | {conv} | {prev} | {change} |

---

## Campaign Performance

| 캠페인 | 예산 | 지출 | 전환 | CPA | ROAS | 상태 |
|--------|------|------|------|-----|------|------|
| {campaign_1} | {budget} | {spend} | {conv} | {cpa} | {roas} | {status} |
| {campaign_2} | {budget} | {spend} | {conv} | {cpa} | {roas} | {status} |

---

## Trend Charts (시각화 가이드)

### 주요 지표 추이

```
트래픽 추이 (주간)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  10k ┼                              ●
      │                         ●   ╱
   8k ┼                    ●   ╱   ╱
      │               ●   ╱   ╱
   6k ┼          ●   ╱   ╱
      │     ●   ╱   ╱
   4k ┼    ╱   ╱
      │   ╱
   2k ┼──╱
      └────┬────┬────┬────┬────┬────┬────
          W1   W2   W3   W4   W5   W6   W7
```

---

## Budget Tracking

### 월간 예산 vs 실제

| 채널 | 예산 | 실제 | 잔여 | 예산 대비 |
|------|------|------|------|----------|
| Paid Search | {budget} | {actual} | {remaining} | {%} |
| Paid Social | {budget} | {actual} | {remaining} | {%} |
| Content | {budget} | {actual} | {remaining} | {%} |
| **Total** | **{total_budget}** | **{total_actual}** | **{total_remaining}** | **{%}** |

---

## Action Items

### 이번 주

- [ ] {action_1}
- [ ] {action_2}
- [ ] {action_3}

### 다음 주

- [ ] {action_1}
- [ ] {action_2}

---

## Definitions

| 지표 | 정의 | 계산식 |
|------|------|--------|
| CAC | 고객 획득 비용 | 총 마케팅 비용 ÷ 신규 고객 |
| LTV | 고객 생애 가치 | 평균 매출 × 구매 빈도 × 고객 수명 |
| ROAS | 광고 수익률 | 광고 매출 ÷ 광고 비용 |
| CTR | 클릭률 | 클릭 ÷ 노출 × 100 |
| CPA | 전환당 비용 | 광고 비용 ÷ 전환 수 |

---

## Reporting Schedule

| 리포트 | 빈도 | 담당 | 배포 |
|--------|------|------|------|
| Daily Check | 매일 | {owner} | 슬랙 |
| Weekly Report | 매주 월요일 | {owner} | 이메일 |
| Monthly Review | 매월 첫째 주 | {owner} | 미팅 |
| Quarterly Review | 분기 말 | {owner} | 미팅 |

---

*Report Period: {start_date} - {end_date}*
*Generated: {generation_date}*
*Owner: {owner}*
```

## 벤치마크 참고

### 산업별 평균

| 지표 | SaaS | E-commerce | B2B |
|------|------|------------|-----|
| 전환율 | 3-5% | 2-3% | 2-5% |
| CAC | $200-500 | $50-100 | $500-1000 |
| LTV:CAC | 3:1+ | 3:1+ | 3:1+ |
| 이메일 오픈율 | 20-25% | 15-20% | 20-25% |
| 이메일 클릭률 | 2-3% | 2-3% | 3-5% |

<!-- Merged from coreyhaines31/marketingskills -->

## GA4 Implementation Guide

### Quick Setup

```yaml
ga4_setup:
  step_1: "GA4 property 및 data stream 생성"
  step_2: "gtag.js 또는 GTM 설치"
  step_3: "Enhanced Measurement 활성화"
  step_4: "Custom events 설정"
  step_5: "Admin에서 Conversions 마킹"
```

### Custom Event 예시

```javascript
// 가입 완료 이벤트
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});

// CTA 클릭 이벤트
gtag('event', 'cta_clicked', {
  'button_text': 'Start Free Trial',
  'location': 'hero_section'
});

// 구매 완료 이벤트
gtag('event', 'purchase', {
  'transaction_id': 'T12345',
  'value': 49000,
  'currency': 'KRW',
  'items': [{
    'item_name': 'Pro Plan',
    'price': 49000
  }]
});
```

### GA4 핵심 이벤트 목록

| 이벤트 | 카테고리 | 속성(Properties) |
|--------|---------|-----------------|
| `page_view` | 자동 | page_title, page_location, page_referrer |
| `cta_clicked` | 커스텀 | button_text, location |
| `form_submitted` | 커스텀 | form_type |
| `signup_completed` | 커스텀 | method, source |
| `demo_requested` | 커스텀 | - |
| `purchase` | 커스텀 | transaction_id, value, currency, items |
| `feature_used` | 커스텀 | feature_name |

### Custom Dimensions 설정

```yaml
custom_dimensions:
  user_scope:
    - name: "user_type"
      parameter: "user_type"
      description: "사용자 유형 (free, paid, enterprise)"
    - name: "plan_type"
      parameter: "plan_type"
      description: "구독 플랜"

  event_scope:
    - name: "button_location"
      parameter: "location"
      description: "CTA 위치"
    - name: "content_type"
      parameter: "content_type"
      description: "콘텐츠 유형"
```

### Conversions 설정

```yaml
conversions:
  - event: "signup_completed"
    counting: "Once per session"
  - event: "purchase"
    counting: "Once per event"
  - event: "demo_requested"
    counting: "Once per session"
```

---

## Data Layer Specifications (GTM)

Google Tag Manager와 함께 사용할 Data Layer 명세입니다.

### Data Layer 기본 구조

```javascript
// 페이지 로드 시 기본 데이터
window.dataLayer = window.dataLayer || [];
dataLayer.push({
  'event': 'page_data_ready',
  'page_type': 'landing_page',
  'user_logged_in': false,
  'user_plan': null
});
```

### 이벤트별 Data Layer Push

```javascript
// 폼 제출
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});

// 제품 조회
dataLayer.push({
  'event': 'product_viewed',
  'product_name': 'Pro Plan',
  'product_price': 49000,
  'product_category': 'subscription'
});

// 전환 완료
dataLayer.push({
  'event': 'conversion_completed',
  'conversion_type': 'signup',
  'conversion_value': 0,
  'conversion_source': 'organic'
});
```

### GTM Container 구조

| 컴포넌트 | 용도 | 예시 |
|---------|------|------|
| **Tags** | 실행할 코드 | GA4 이벤트, Meta Pixel, LinkedIn Insight |
| **Triggers** | 태그 실행 시점 | 페이지뷰, 클릭, 폼 제출, Data Layer 이벤트 |
| **Variables** | 동적 값 | 클릭 텍스트, Data Layer 변수, URL 파라미터 |

### 네이밍 컨벤션

```yaml
naming_conventions:
  events:
    format: "object_action"
    examples:
      - "signup_completed"
      - "button_clicked"
      - "form_submitted"
      - "article_read"
      - "checkout_payment_completed"
  rules:
    - "소문자 + 언더스코어"
    - "구체적으로: cta_hero_clicked (O) vs button_clicked (X)"
    - "컨텍스트는 속성에, 이벤트명에는 넣지 않기"
    - "공백/특수문자 금지"
```

---

## Attribution Model Selection (기여도 모델 선택)

### 모델 비교

| 모델 | 방식 | 장점 | 단점 | 적합 |
|------|------|------|------|------|
| **Last-Click** | 마지막 클릭에 100% | 단순, 명확 | 상위 퍼널 과소평가 | 짧은 구매 사이클 |
| **First-Click** | 첫 클릭에 100% | 인지도 평가에 유용 | 전환 기여 무시 | 인지도 캠페인 |
| **Linear** | 균등 배분 | 모든 터치포인트 인정 | 핵심 포인트 구분 불가 | 멀티채널 균형 |
| **Time-Decay** | 최근에 가중치 | 전환 직전 활동 중시 | 초기 인지 과소평가 | 긴 세일즈 사이클 |
| **Data-Driven** | ML 기반 실제 기여도 | 가장 정확 | 데이터 300건+ 필요 | 충분한 데이터 |

### 선택 가이드

```yaml
model_selection:
  짧은_구매_사이클:
    recommended: "Last-Click"
    reason: "구매 결정이 빠르므로 마지막 터치포인트가 중요"

  긴_B2B_사이클:
    recommended: "Time-Decay 또는 Data-Driven"
    reason: "여러 터치포인트를 거치므로 종합 평가 필요"

  인지도_중심_캠페인:
    recommended: "First-Click"
    reason: "최초 접점의 가치를 정확히 평가"

  충분한_전환_데이터:
    recommended: "Data-Driven"
    reason: "실제 패턴 기반으로 가장 정확한 기여도 산정"
```

---

## Tracking Debugging / Troubleshooting Guide

### 디버깅 도구

| 도구 | 용도 | 접근 방법 |
|------|------|----------|
| **GA4 DebugView** | 실시간 이벤트 모니터링 | GA4 Admin → DebugView |
| **GTM Preview Mode** | 태그 트리거 테스트 | GTM → Preview 버튼 |
| **Tag Assistant** | 크롬 확장 프로그램 | Chrome Web Store |
| **dataLayer Inspector** | Data Layer 디버깅 | 브라우저 콘솔 |
| **Network Tab** | 요청 확인 | 브라우저 개발자 도구 → Network |

### 일반적인 문제와 해결

| 문제 | 확인 사항 | 해결 방법 |
|------|----------|----------|
| 이벤트 미발화 | 트리거 설정, GTM 로드 여부 | 트리거 조건 확인, GTM 스니펫 점검 |
| 잘못된 값 | 변수 경로, Data Layer 구조 | 변수 매핑 확인, 콘솔에서 dataLayer 확인 |
| 중복 이벤트 | 복수 컨테이너, 트리거 중복 | 한 컨테이너만 사용, 트리거 조건 정밀화 |
| 전환 미기록 | 전환 마킹, 이벤트 파라미터 | GA4에서 해당 이벤트가 Conversion으로 마킹됐는지 확인 |
| PII 유출 | 이벤트 속성에 개인정보 | 이메일, 전화번호 등 속성에서 제거 |

### Validation Checklist

```
□ 올바른 트리거에서 이벤트가 발화하는가?
□ 속성 값이 올바르게 채워지는가?
□ 중복 이벤트가 없는가?
□ 크로스 브라우저 및 모바일에서 동작하는가?
□ 전환이 올바르게 기록되는가?
□ PII(개인정보)가 유출되지 않는가?
□ 쿠키 동의 연동이 되어 있는가?
```

---

## UTM Parameter Strategy

### 표준 파라미터

| 파라미터 | 용도 | 예시 |
|---------|------|------|
| `utm_source` | 트래픽 소스 | google, newsletter, linkedin |
| `utm_medium` | 마케팅 매체 | cpc, email, social, referral |
| `utm_campaign` | 캠페인 이름 | spring_sale, product_launch_q1 |
| `utm_content` | 버전 구분 | hero_cta, sidebar_banner, email_footer |
| `utm_term` | 유료 검색 키워드 | running+shoes, project+management |

### 네이밍 규칙

```yaml
utm_naming_rules:
  case: "소문자 통일"
  separator: "언더스코어(_) 또는 하이픈(-) 중 하나로 통일"
  specificity: "구체적이되 간결하게"
  documentation: "모든 UTM을 스프레드시트에 문서화"

  examples:
    good:
      - "?utm_source=google&utm_medium=cpc&utm_campaign=brand_2024q1&utm_content=headline_a"
      - "?utm_source=newsletter&utm_medium=email&utm_campaign=weekly_digest_240315"
    bad:
      - "?utm_source=Google (대문자)"
      - "?utm_campaign=campaign1 (의미 불명)"
      - "?utm_content=cta (어떤 CTA?)"
```

### UTM 빌더 템플릿

```
기본 URL:        https://example.com/landing
utm_source:      {플랫폼 or 소스}
utm_medium:      {채널 유형}
utm_campaign:    {캠페인명_YYMMDD or YYQ#}
utm_content:     {변형 구분}
utm_term:        {키워드} (유료 검색만)

결과: https://example.com/landing?utm_source=linkedin&utm_medium=social&utm_campaign=product_launch_2403&utm_content=carousel_v2
```

### 자주 쓰는 utm_medium 값

```yaml
standard_mediums:
  - cpc: "유료 검색 (CPC)"
  - cpm: "유료 디스플레이 (CPM)"
  - email: "이메일"
  - social: "소셜 미디어 (유기적)"
  - paid_social: "소셜 미디어 (유료)"
  - referral: "레퍼럴/제휴"
  - affiliate: "어필리에이트"
  - organic: "오가닉 검색"
  - direct: "다이렉트 트래픽"
```

<!-- End of merged content from coreyhaines31/marketingskills -->

---

## 다음 스킬 연결

- **A/B Testing Skill**: 테스트 결과 분석
- **Campaign Skill**: 캠페인 성과 기반 조정
- **Review Skill**: 전체 마케팅 리뷰

---

*측정하지 않으면 개선할 수 없습니다.*
*하지만 너무 많은 지표는 집중을 흐립니다. 핵심에 집중하세요.*
