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

## 다음 스킬 연결

- **A/B Testing Skill**: 테스트 결과 분석
- **Campaign Skill**: 캠페인 성과 기반 조정
- **Review Skill**: 전체 마케팅 리뷰

---

*측정하지 않으면 개선할 수 없습니다.*
*하지만 너무 많은 지표는 집중을 흐립니다. 핵심에 집중하세요.*
