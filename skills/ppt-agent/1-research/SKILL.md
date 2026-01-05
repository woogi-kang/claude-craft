---
name: ppt-research
description: |
  PPT 제작을 위한 리서치 및 자료 수집 Skill.
  웹 검색, 문서 분석, 경쟁사 조사, 통계 데이터 수집 시 활성화.
  "자료 조사해줘", "트렌드 분석해줘", "경쟁사 PPT 분석" 등의 요청에 반응.
---

# PPT Research Skill

PPT 제작을 위한 리서치 및 자료 수집을 담당하는 Skill입니다.

## 핵심 기능

### 1. topic_deep_dive (주제 심층 분석)
주제 키워드를 확장하고 관련 개념을 맵핑합니다.

**수행 작업:**
- 핵심 키워드 추출 및 확장
- 관련 개념/용어 맵핑
- 주제 범위 정의

**출력물:**
- 개념 맵 (Concept Map)
- 확장 키워드 목록
- 주제 범위 문서

### 2. web_research (웹 리서치)
최신 트렌드, 통계, 사례를 웹에서 수집합니다.

**수행 작업:**
- 최신 기사 및 보고서 검색
- 통계 데이터 수집
- 사례 연구 수집

**출력물:**
- 출처 포함 리서치 노트
- 수집된 통계 데이터
- 사례 목록

### 3. competitor_analysis (경쟁사 분석)
경쟁사 또는 유사 발표자료를 분석합니다.

**수행 작업:**
- 경쟁사 발표자료 구조 분석
- 메시지 전략 분석
- 디자인 트렌드 파악

**출력물:**
- 벤치마킹 리포트
- 구조 비교표
- 디자인 레퍼런스

### 4. data_extraction (데이터 추출)
PDF, 문서에서 핵심 데이터를 추출합니다.

**수행 작업:**
- 문서 텍스트 추출
- 표/차트 데이터 추출
- 핵심 인용문 추출

**출력물:**
- 정형화된 데이터셋
- 핵심 인용문 목록

### 5. source_tracking (출처 관리)
모든 출처를 관리하고 신뢰도를 태깅합니다.

**수행 작업:**
- 출처 URL/제목/날짜 기록
- 출처 유형 분류
- 초기 신뢰도 점수 부여

**출력물:**
- 출처 메타데이터 목록
- 신뢰도 태그

### 6. criticality_analyze (스토리 중요도 분석) ⭐ NEW
수집된 Research Item의 스토리 중요도를 분석하고 태깅합니다.

**수행 작업:**
- 핵심 스토리 기여도 평가 (priority 결정)
- 스토리 역할 분류 (story_role 결정)
- 데이터 유형 분류 (data_type 결정)
- 청중 임팩트 평가
- 시각화 방식 제안 (visual_suggestion 생성)
- 콘텐츠 형식 사전 가공 (content_ready 생성)

**판단 기준 매트릭스:**

| 평가 항목 | 가중치 | 측정 방법 |
|----------|-------|----------|
| 신뢰도 | 30% | credibility_score 기반 |
| 차별성 | 25% | 경쟁 자료와 중복도 분석 |
| 증명력 | 25% | 주장-근거 연결 강도 |
| 최신성 | 20% | 발행일 기준 (1년 이내 높음) |

**Priority 자동 결정 로직:**
```
총점 계산 = (신뢰도×0.3) + (차별성×0.25) + (증명력×0.25) + (최신성×0.2)

총점 >= 0.8 → must_use
총점 >= 0.6 → should_use
총점 < 0.6  → nice_to_have
```

**출력물:**
- story_criticality 객체
- visual_suggestion 객체
- content_ready 객체 (사전 가공된 콘텐츠)

## 수집 데이터 구조

리서치 결과는 다음 JSON 구조로 저장합니다:

```json
{
  "research_item": {
    "id": "R001",
    "content": "AI 시장 연평균 40% 성장, 2025년 $150B 예상",
    "source": {
      "url": "https://gartner.com/ai-report-2024",
      "title": "Gartner AI Market Report 2024",
      "date": "2024-11-15",
      "type": "article|study|statistics|report"
    },
    "credibility_score": 0.92,
    "tags": ["AI", "시장규모", "통계"],
    "validation_status": "verified",

    "story_criticality": {
      "priority": "must_use",
      "story_role": "hook",
      "data_type": "statistic",
      "audience_impact": "high",
      "uniqueness": "high"
    },
    "visual_suggestion": {
      "recommended_type": "bar_chart",
      "data_format": {
        "value": 150,
        "unit": "billion_usd",
        "comparison_base": "2024년 $100B 대비",
        "trend": "growth"
      }
    },
    "content_ready": {
      "headline_format": "AI 시장 2025년 $150B 도달, 연 40% 성장",
      "bullet_format": "시장 규모: $100B → $150B (40% YoY)",
      "metric_format": {
        "value": "$150B",
        "label": "2025 예상 시장",
        "delta": "+40%"
      },
      "citation_short": "(Gartner, 2024)",
      "citation_full": "Source: Gartner AI Market Report, Nov 2024",
      "speaker_note": "가트너의 최신 보고서에 따르면, AI 시장은 2025년 1,500억 달러에 도달할 것으로 예상됩니다."
    }
  }
}
```

### Story Criticality 필드 정의

#### `priority` (스토리 우선순위)

| 값 | 의미 | 사용 가이드 |
|---|------|-----------|
| `must_use` | 핵심 스토리에 필수 | 반드시 슬라이드에 포함 |
| `should_use` | 스토리 강화에 권장 | 공간 있으면 포함 |
| `nice_to_have` | 보조 자료 | Appendix 또는 생략 가능 |

**판단 기준:**
```
must_use 조건 (하나 이상 충족):
├─ 핵심 주장의 유일한 근거
├─ credibility_score >= 0.85
├─ 경영진/투자자가 반드시 알아야 할 정보
└─ 경쟁사 대비 차별화 핵심 포인트

should_use 조건:
├─ 핵심 주장 보강 자료
├─ credibility_score >= 0.7
└─ 추가 맥락 제공

nice_to_have 조건:
├─ 참고용 배경 정보
├─ credibility_score < 0.7
└─ 핵심 스토리와 간접적 연관
```

#### `story_role` (스토리 역할)

| 값 | 의미 | 배치 위치 |
|---|------|----------|
| `hook` | 청중 주의 집중용 강렬한 데이터 | 타이틀, 오프닝 슬라이드 |
| `evidence` | 주장 입증 핵심 근거 | 본론 슬라이드 |
| `support` | 보조 설명/맥락 | 상세 설명 슬라이드 |
| `closing` | 마무리/CTA 강화 | 결론, CTA 슬라이드 |

#### `data_type` (데이터 유형)

| 값 | 설명 | 시각화 권장 |
|---|------|-----------|
| `statistic` | 정량적 수치 | 차트, 메트릭 박스 |
| `quote` | 인용문 | Quote 슬라이드 |
| `case_study` | 사례 연구 | 카드 레이아웃 |
| `comparison` | 비교 데이터 | 테이블, 비교 차트 |
| `trend` | 추세/변화 | 라인 차트, 타임라인 |

### Visual Suggestion 필드 정의

```json
{
  "visual_suggestion": {
    "recommended_type": "bar_chart",
    "data_format": {
      "value": 40,
      "unit": "percent",
      "comparison_base": "전년 대비",
      "trend": "growth",
      "time_range": "YoY"
    },
    "chart_spec": {
      "x_axis": "연도",
      "y_axis": "시장 규모 ($B)",
      "highlight": "2025"
    }
  }
}
```

**Visual Type 옵션:**

| 타입 | 용도 | 적합한 data_type |
|-----|------|-----------------|
| `bar_chart` | 비교, 순위 | statistic, comparison |
| `line_chart` | 추세, 변화 | trend, statistic |
| `pie_chart` | 구성비 | statistic |
| `metric_box` | 핵심 KPI 강조 | statistic |
| `quote_slide` | 인용문 | quote |
| `comparison_table` | 상세 비교 | comparison |
| `timeline` | 시간순 진행 | trend |
| `process_flow` | 프로세스/흐름 | case_study |
| `case_card` | 사례 요약 카드 | case_study |
| `none` | 텍스트만 | support |

### Trend 타입 상세 스펙 ⭐ NEW

시간에 따른 변화나 성장 추이를 표현할 때 사용합니다.

```json
{
  "research_item": {
    "id": "R010",
    "content": "AutoFlow 성장 추이: 2023 출시 → 2024 100개 고객 → 2025 500개 목표",
    "story_criticality": {
      "priority": "must_use",
      "story_role": "evidence",
      "data_type": "trend"
    },
    "visual_suggestion": {
      "recommended_type": "timeline_h",
      "data_format": {
        "time_range": "2023-2025",
        "milestones": [
          {
            "date": "2023 Q1",
            "label": "제품 출시",
            "status": "completed",
            "metric": null
          },
          {
            "date": "2024 Q4",
            "label": "100개 고객 확보",
            "status": "completed",
            "metric": { "value": 100, "unit": "customers" }
          },
          {
            "date": "2025 Q4",
            "label": "500개 고객 목표",
            "status": "planned",
            "metric": { "value": 500, "unit": "customers" }
          }
        ],
        "highlight_current": true,
        "show_growth_rate": true
      }
    },
    "content_ready": {
      "headline_format": "2년 만에 100개 → 500개 고객 성장 목표",
      "bullet_format": "성장 추이: 2023 출시 → 2024 100개 → 2025 500개 목표",
      "timeline_format": {
        "items": [
          { "year": "2023", "event": "제품 출시" },
          { "year": "2024", "event": "100개 고객" },
          { "year": "2025", "event": "500개 목표" }
        ]
      },
      "citation_short": "(내부 자료)",
      "citation_full": "AutoFlow 성장 로드맵, 2024"
    }
  }
}
```

**Milestone Status 옵션:**

| 값 | 설명 | 시각적 표현 |
|---|------|-----------|
| `completed` | 완료됨 | 채워진 원, 강조 색상 |
| `in_progress` | 진행 중 | 테두리 원, 펄스 효과 |
| `planned` | 계획됨 | 빈 원, 점선 연결 |

### Case Study 타입 상세 스펙 ⭐ NEW

고객 사례나 성공 스토리를 표현할 때 사용합니다.

```json
{
  "research_item": {
    "id": "R011",
    "content": "삼성전자 도입 사례: 문제(수작업 오류) → 솔루션(AutoFlow) → 결과(40% 생산성↑)",
    "source": {
      "type": "case_study",
      "company": "삼성전자",
      "industry": "전자/IT",
      "date": "2024-12"
    },
    "story_criticality": {
      "priority": "should_use",
      "story_role": "evidence",
      "data_type": "case_study"
    },
    "visual_suggestion": {
      "recommended_type": "process_flow",
      "alternative_type": "case_card",
      "data_format": {
        "company": "삼성전자",
        "company_logo": "samsung",
        "industry": "전자/IT",
        "steps": [
          {
            "phase": "problem",
            "icon": "⚠️",
            "title": "문제 상황",
            "description": "수작업 데이터 입력으로 오류율 15%"
          },
          {
            "phase": "solution",
            "icon": "🔧",
            "title": "AutoFlow 도입",
            "description": "AI 기반 자동화 시스템 구축"
          },
          {
            "phase": "result",
            "icon": "🎯",
            "title": "성과",
            "description": "생산성 40% 향상, 오류 90% 감소"
          }
        ],
        "outcome_metrics": [
          { "label": "생산성", "value": "+40%", "direction": "up" },
          { "label": "오류율", "value": "-90%", "direction": "down" }
        ],
        "testimonial": {
          "quote": "AutoFlow 도입 후 팀 생산성이 40% 향상되었습니다.",
          "author": "김철수",
          "role": "IT팀장"
        }
      }
    },
    "content_ready": {
      "headline_format": "삼성전자: AutoFlow로 생산성 40% 향상",
      "bullet_format": "삼성전자 사례: 오류 90% 감소, 생산성 40% 향상",
      "card_format": {
        "company_logo": "samsung",
        "headline": "생산성 40% 향상",
        "summary": "수작업 오류 문제를 AI 자동화로 해결"
      },
      "citation_short": "(삼성전자 사례)",
      "citation_full": "삼성전자 고객 사례 연구, 2024년 12월"
    }
  }
}
```

**Case Study Phase 옵션:**

| 값 | 설명 | 권장 아이콘 |
|---|------|-----------|
| `problem` | 도입 전 문제 상황 | ⚠️ 🔴 ❌ |
| `solution` | 도입한 솔루션 | 🔧 💡 🚀 |
| `result` | 도입 후 성과 | 🎯 ✅ 📈 |
| `future` | 향후 계획 | 🔮 📅 |

**Visual Type 선택 가이드:**

| 조건 | 권장 컴포넌트 |
|-----|-------------|
| steps 배열 존재 (3단계 이상) | process_flow |
| steps 없음 + outcome_metrics 존재 | case_card |
| testimonial 중심 | quote_block + source_badge |

### Content Ready 필드 정의

Content Skill에서 바로 사용 가능한 사전 가공 형식:

```json
{
  "content_ready": {
    "headline_format": "AI 시장 2025년 $150B, 40% 성장 전망",
    "bullet_format": "시장 규모: $100B → $150B (YoY 40%)",
    "metric_format": {
      "value": "$150B",
      "label": "2025 예상 시장",
      "delta": "+40%",
      "delta_direction": "up"
    },
    "citation_short": "(Gartner, 2024)",
    "citation_full": "Source: Gartner AI Market Report, November 2024",
    "speaker_note": "가트너의 최신 보고서에 따르면..."
  }
}
```

## Citation Localization (출처 현지화) ⭐ NEW

모든 citation을 일관된 언어와 형식으로 통일합니다.

### Citation Config 설정

```yaml
citation_config:
  language: "ko"  # ko | en | auto (발표 언어에 맞춤)

  format:
    short: "{source}, {year}"
    full: "{title}, {source}, {date}"

  # 언어별 템플릿
  templates:
    ko:
      short: "({source}, {year})"
      full: "출처: {source} {title}, {year}년 {month}월"
      source_label: "출처"
      internal_label: "내부 자료"

    en:
      short: "({source}, {year})"
      full: "Source: {source} {title}, {month} {year}"
      source_label: "Source"
      internal_label: "Internal"

  # 출처명 번역 매핑
  source_translation:
    ko:
      "Gartner": "가트너"
      "McKinsey": "맥킨지"
      "Forrester": "포레스터"
      "Deloitte": "딜로이트"
      "BCG": "BCG"
      "Accenture": "액센추어"
      "IDC": "IDC"
      "Internal": "내부 자료"
      "Customer Interview": "고객 인터뷰"
      "Internal Audit": "내부 감사"
      "Operations Survey": "운영팀 조사"
      "Employee Survey": "직원 설문"

    en:
      "내부 감사": "Internal Audit"
      "운영팀 조사": "Operations Survey"
      "직원 설문": "Employee Survey"
      "고객 인터뷰": "Customer Interview"
      "내부 자료": "Internal"
```

### Citation 생성 규칙

**언어 설정에 따른 변환:**

| 원본 출처 | language=ko | language=en |
|----------|------------|------------|
| `Gartner, 2024` | `(가트너, 2024)` | `(Gartner, 2024)` |
| `내부 감사 2024` | `(내부 자료, 2024)` | `(Internal Audit, 2024)` |
| `McKinsey Study` | `(맥킨지, 2024)` | `(McKinsey, 2024)` |
| `Forrester TEI` | `(포레스터, 2024)` | `(Forrester, 2024)` |

**content_ready 생성 시 자동 적용:**

```json
{
  "content_ready": {
    "citation_short": "(가트너, 2024)",
    "citation_full": "출처: 가트너 AI 시장 보고서, 2024년 11월",
    "citation_raw": {
      "source": "Gartner",
      "title": "AI Market Report",
      "date": "2024-11",
      "original_language": "en"
    }
  }
}
```

## 신뢰도 초기 평가 기준

| 출처 유형 | 초기 신뢰도 | 설명 |
|----------|------------|------|
| 정부기관/학술논문 | 0.9+ | 공신력 있는 기관 |
| 주요 언론사 | 0.8+ | 검증된 미디어 |
| 산업 리서치 기관 | 0.8+ | 전문 리서치 |
| 기업 공식 자료 | 0.7+ | 공식 발표 자료 |
| 전문 블로그 | 0.6+ | 전문가 의견 |
| 일반 블로그/커뮤니티 | 0.4+ | 추가 검증 필요 |
| 출처 불명 | 0.2 | 사용 비권장 |

## 사용 예시

### 예시 1: 주제 리서치 요청
```
사용자: "AI 트렌드에 대해 자료 조사해줘"

수행:
1. "AI 트렌드" 키워드로 topic_deep_dive 실행
2. 관련 키워드 확장: 생성형 AI, LLM, AI Agent 등
3. web_research로 최신 기사/보고서 수집
4. source_tracking으로 출처 정리
5. 리서치 노트 생성
```

### 예시 2: 경쟁사 분석 요청
```
사용자: "경쟁사 A사의 투자 피치덱 분석해줘"

수행:
1. competitor_analysis로 구조 분석
2. 핵심 메시지 전략 추출
3. 디자인 요소 분석
4. 벤치마킹 리포트 작성
```

## 다음 단계 연결

리서치 완료 후:
1. 수집된 데이터는 **Validation Skill**로 전달하여 신뢰성 검증
2. 검증 통과 시 **Structure Skill**에서 스토리라인 구성에 활용

## 주의사항

- 모든 수집 데이터에 반드시 출처를 기록할 것
- 통계 데이터는 발행일 확인 필수
- 초기 신뢰도 점수는 참고용이며, Validation Skill에서 최종 검증
- 저작권 준수 (직접 인용 시 출처 명시)
