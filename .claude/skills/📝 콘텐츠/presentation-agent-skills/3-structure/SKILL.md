---
name: ppt-structure
description: |
  검증된 데이터를 바탕으로 PPT의 스토리라인과 논리 구조를 설계하는 Skill.
  청중 분석, 핵심 메시지 도출, 슬라이드 아웃라인 구성 시 활성화.
  "구조 잡아줘", "스토리라인 만들어줘", "아웃라인 설계해줘" 등의 요청에 반응.
---

# PPT Structure Skill

검증된 데이터를 바탕으로 PPT의 스토리라인과 논리 구조를 설계하는 Skill입니다.

## 스토리텔링 프레임워크

### 1. SCQA Framework (McKinsey/BCG 컨설팅 표준)
> 출처: The Analyst Academy - PowerPoint Storytelling

비즈니스 발표에 가장 효과적인 프레임워크입니다.

```
S - Situation (상황): 현재 상태 설명
C - Complication (문제): 직면한 과제/위기
Q - Question (질문): 해결해야 할 핵심 질문 (암묵적)
A - Answer (해답): 제안하는 솔루션
```

**적용 예시:**
```
[S] "우리 회사는 지난 5년간 연평균 15% 성장을 달성했습니다."
[C] "그러나 올해 신규 경쟁사 진입으로 시장 점유율이 5% 하락했습니다."
[Q] (암묵적: 어떻게 시장 점유율을 회복할 것인가?)
[A] "3가지 전략적 이니셔티브를 제안합니다..."
```

**적합한 상황:** 투자 피치, 전략 제안, 문제 해결 발표

### 2. SCR Framework (McKinsey 3-Step)
> 출처: SlidesPilot - McKinsey's 3-Step SCR Framework

SCQA의 간소화 버전으로 빠른 의사결정에 적합합니다.

```
S - Situation: 컨텍스트와 배경 설정
C - Complication: 긴장감과 문제 제기
R - Resolution: 명확한 해결책과 액션 플랜
```

**적합한 상황:** 경영진 보고, 빠른 의사결정이 필요한 미팅

### 3. Pyramid Principle (Minto/McKinsey)
> 출처: Product Mindset - McKinsey's Pyramid Framework

결론부터 말하고 근거로 뒷받침하는 구조입니다.

```
           [핵심 메시지]
          /      |      \
    [근거 1]  [근거 2]  [근거 3]
     /  \      /  \      /  \
  [세부] [세부] [세부] [세부] [세부] [세부]
```

**원칙:**
- 답부터 제시 (Answer First)
- 그룹화된 근거 제시
- 논리적 순서 (시간순, 구조순, 중요도순)

**적합한 상황:** 경영진 보고, 복잡한 분석 결과 발표

### 4. Hero's Journey (영웅의 여정)
> 출처: Storydoc - Presentation Storytelling Examples

감정적 연결이 필요한 스토리텔링에 적합합니다.

```
1. 일상 세계 (현재 상태)
2. 모험의 소명 (기회/도전)
3. 소명의 거부 (장애물)
4. 멘토와의 만남 (솔루션 제안자)
5. 첫 관문 통과 (초기 성공)
6. 시험과 동맹 (과정)
7. 가장 깊은 동굴 (핵심 도전)
8. 시련 (클라이맥스)
9. 보상 (성과)
10. 귀환의 길 (구현)
11. 부활 (변화)
12. 영약과 함께 귀환 (새로운 상태)
```

**간소화 버전 (발표용):**
```
현재 상태 → 도전/기회 → 여정 → 변화 → 새로운 미래
```

**적합한 상황:** 브랜드 스토리, 창업 피치, 변화 관리

### 5. Sparklines (Nancy Duarte)
> 출처: Videoscribe - 8 Classic Storytelling Techniques

현실과 이상을 반복적으로 대조하여 변화 욕구를 자극합니다.

```
현실(What is) ←→ 이상(What could be)의 반복적 대조
      ↓
   변화에 대한 열망 생성
      ↓
   행동으로의 동기 부여
```

**구조:**
```
[현실] "지금 우리는 이런 상태입니다..."
[이상] "하지만 이렇게 될 수 있습니다!"
[현실] "아직 이런 문제가 있습니다..."
[이상] "해결하면 이런 미래가 열립니다!"
[행동] "지금 바로 시작합시다!"
```

**적합한 상황:** 비전 발표, 동기 부여, 변화 촉구

## 청중 분석 매트릭스

발표 대상에 따른 구조 선택 가이드:

| 청중 유형 | 주요 관심사 | 추천 프레임워크 | 슬라이드 특성 |
|----------|------------|----------------|--------------|
| **경영진** | ROI, 전략적 영향 | SCQA, Pyramid | 핵심 먼저, 상세는 Appendix |
| **투자자** | 성장성, 시장규모, 팀 역량 | Hero's Journey, SCQA | 비전 중심, 숫자로 증명 |
| **기술팀** | How-to, 구현 방법, 기술 스택 | 순차적 구조 | 다이어그램, 코드 예시 |
| **일반 대중** | 이해하기 쉬운 설명 | Sparklines | 비유, 시각화 강조 |
| **고객사** | 문제 해결, 비용 절감, 가치 | SCR, SCQA | 사례 중심, ROI 강조 |
| **내부 팀** | 실행 계획, 역할 분담 | 순차적/Pyramid | 액션 아이템 명확화 |

## 슬라이드 맵핑

### 기본 슬라이드 맵 템플릿

```yaml
slide_map:
  - slide: 1
    type: "title"
    purpose: "핵심 가치 제안 한 줄"
    framework_role: "Hook"
    duration: 30sec

  - slide: 2
    type: "agenda"
    purpose: "발표 흐름 안내"
    framework_role: "Overview"
    duration: 30sec

  - slide: 3-5
    type: "situation"
    purpose: "현재 상황/배경 설명"
    framework_role: "S (Situation)"
    duration: 2min
    key_data: ["시장 현황", "현재 성과", "배경 정보"]

  - slide: 6-8
    type: "complication"
    purpose: "문제점/기회 제시"
    framework_role: "C (Complication)"
    duration: 2min
    key_data: ["문제 정의", "영향 분석", "긴급성"]

  - slide: 9-15
    type: "solution"
    purpose: "핵심 제안 상세"
    framework_role: "A (Answer)"
    duration: 5min
    key_data: ["솔루션 개요", "세부 전략", "실행 계획"]

  - slide: 16
    type: "cta"
    purpose: "명확한 Call-to-Action"
    framework_role: "Next Steps"
    duration: 1min
```

### 발표 유형별 슬라이드 구성

#### 투자 피치덱 (15-20장)
```
1. 타이틀 + Hook
2. 문제 정의
3-4. 솔루션
5. 시장 규모
6. 비즈니스 모델
7-8. 트랙션/성과
9. 경쟁 우위
10. 팀 소개
11. 재무 계획
12. 투자 요청
13. Q&A/Contact
+ Appendix
```

#### 기술 세미나 (20-30장)
```
1. 타이틀
2. Agenda
3. 배경/맥락
4-6. 기술 개요
7-15. 상세 설명 (코드/다이어그램)
16-18. 데모/예시
19. 결론
20. Q&A
+ 참고 자료
```

#### 경영 보고 (10-15장)
```
1. Executive Summary
2. 핵심 성과 지표
3-5. 상세 분석
6-7. 이슈/리스크
8-9. 대응 방안
10. Next Steps
+ Appendix (상세 데이터)
```

## 핵심 기능

### 1. audience_analysis (청중 분석)
청중 특성을 분석하여 최적의 구조를 추천합니다.

**입력:**
- 청중 유형 (경영진, 투자자, 기술팀 등)
- 발표 목적
- 시간 제약

**출력:**
- 추천 프레임워크
- 슬라이드 수 권장
- 주요 관심사 리스트

### 2. framework_select (프레임워크 선택)
발표 목적에 맞는 스토리텔링 프레임워크를 선택합니다.

**수행 작업:**
- 청중 분석 결과 반영
- 콘텐츠 유형 분석
- 최적 프레임워크 추천 (1순위, 2순위)

### 3. message_extract (핵심 메시지 도출)
검증된 데이터에서 핵심 메시지를 추출합니다.

**수행 작업:**
- 주요 논점 추출
- 메시지 우선순위 설정
- 한 줄 요약 생성

### 4. outline_generate (아웃라인 생성) ⭐ ENHANCED
슬라이드별 아웃라인과 **Research 매핑**을 생성합니다.

**추가 수행 작업:**
- Research Item을 슬라이드에 명시적 배정
- must_use 항목 우선 배치
- 데이터 밀도 균형 분석
- 미사용 핵심 데이터 경고

**출력 구조:**
```json
{
  "outline": {
    "total_slides": 16,
    "estimated_duration": "15min",
    "framework": "SCQA",

    "research_utilization": {
      "total_research_items": 15,
      "utilized_items": 12,
      "utilization_rate": 0.8,
      "by_priority": {
        "must_use": { "total": 5, "utilized": 5, "rate": 1.0 },
        "should_use": { "total": 7, "utilized": 6, "rate": 0.86 },
        "nice_to_have": { "total": 3, "utilized": 1, "rate": 0.33 }
      },
      "distribution_by_section": {
        "situation": { "slides": "1-4", "items": 3, "coverage": "adequate" },
        "complication": { "slides": "5-7", "items": 5, "coverage": "strong" },
        "answer": { "slides": "8-14", "items": 4, "coverage": "adequate" },
        "cta": { "slides": "15-16", "items": 0, "coverage": "weak", "warning": "데이터 부족" }
      },
      "unused_must_use": [],
      "recommendations": [
        "CTA 섹션에 성과 데이터(R008) 추가 권장"
      ]
    },

    "slides": [
      {
        "number": 5,
        "type": "problem",
        "framework_role": "Complication",
        "headline": "수작업 오류로 연간 $2M 손실",
        "key_points": [
          "수작업 데이터 입력 오류율 15%",
          "오류 수정 비용 연간 $2M",
          "직원 40% 업무시간 수동 작업에 소비"
        ],
        "notes": "임팩트 있는 문제 제기",
        "duration": "1min",

        "research_mapping": [
          {
            "research_id": "R003",
            "usage": "headline",
            "claim": "연간 $2M 손실",
            "data_type": "statistic",
            "priority": "must_use",
            "citation_short": "(내부 감사 2024)",
            "content_ready": {
              "text": "수작업 오류로 인한 연간 손실 $2M",
              "source": "내부 감사 보고서 2024, n=500 거래 분석"
            },
            "visual_suggestion": {
              "type": "metric_box",
              "highlight": true
            }
          },
          {
            "research_id": "R005",
            "usage": "bullet",
            "claim": "오류율 15%",
            "data_type": "statistic",
            "priority": "should_use",
            "citation_short": "(운영팀 조사)",
            "content_ready": {
              "text": "수작업 데이터 입력 오류율 15%",
              "source": "운영팀 품질 조사 2024 Q3"
            }
          },
          {
            "research_id": "R007",
            "usage": "visual",
            "claim": "40% 시간 수동 작업",
            "data_type": "statistic",
            "priority": "should_use",
            "visual_suggestion": {
              "type": "pie_chart",
              "spec": {
                "segments": [
                  { "label": "수동 작업", "value": 40, "highlight": true },
                  { "label": "자동화 작업", "value": 35 },
                  { "label": "기타", "value": 25 }
                ]
              }
            }
          }
        ],

        "data_density": {
          "total_items": 3,
          "by_priority": { "must_use": 1, "should_use": 2, "nice_to_have": 0 },
          "coverage_score": 0.85,
          "evidence_strength": "strong"
        }
      }
    ]
  }
}
```

**Research 매핑 규칙:**

| 규칙 | 설명 |
|-----|------|
| must_use 100% 활용 | 모든 must_use 항목은 반드시 슬라이드에 배정 |
| story_role 매칭 | hook→오프닝, evidence→본론, closing→CTA |
| 슬라이드당 3-5개 | 너무 많은 데이터는 분산 배치 |
| visual 연계 | visual_suggestion이 있으면 Visual Skill에 전달 |

**Usage 옵션:**

| 값 | 설명 | 표시 위치 |
|---|------|----------|
| `headline` | 슬라이드 제목에 사용 | 최상단 |
| `bullet` | 불릿 포인트에 사용 | 본문 |
| `visual` | 차트/그래프로 시각화 | 시각 영역 |
| `speaker_note` | 발표자 노트에만 | 숨김 |
| `appendix` | 부록으로 이동 | Appendix |

### 5. flow_validate (흐름 검증)
스토리라인의 논리적 흐름을 검증합니다.

**검증 항목:**
- 프레임워크 일관성
- 논리적 연결성
- 시간 배분 적절성
- 메시지 명확성

### 6. evidence_balance (증거 균형 분석) ⭐ NEW
전체 PPT에서 Research 데이터가 균등하게 분포되어 있는지 분석합니다.

**수행 작업:**
- 섹션별 데이터 분포 분석
- 데이터 공백 섹션 식별
- must_use 미사용 항목 경고
- 재배치 제안

**분석 기준:**

| Coverage 등급 | 조건 | 권장 조치 |
|--------------|------|----------|
| `strong` | 섹션당 research_item >= 3개 | 유지 |
| `adequate` | 섹션당 research_item 1-2개 | 선택적 보강 |
| `weak` | 섹션당 research_item 0개 | 필수 보강 |

**출력물:**
```json
{
  "evidence_balance": {
    "overall_score": 0.78,
    "section_analysis": [
      {
        "section": "complication",
        "slides": "5-7",
        "research_count": 5,
        "coverage": "strong",
        "dominant_data_type": "statistic"
      },
      {
        "section": "cta",
        "slides": "15-16",
        "research_count": 0,
        "coverage": "weak",
        "recommendation": "R008(성과 데이터) 추가 권장"
      }
    ],
    "unused_must_use": [
      {
        "research_id": "R012",
        "content": "고객 만족도 92% 달성",
        "suggested_placement": "closing 섹션"
      }
    ],
    "rebalance_suggestions": [
      "Complication 섹션의 R005를 CTA로 이동 고려",
      "Answer 섹션에 case_study 타입 데이터 추가 권장"
    ]
  }
}
```

### 7. auto_redistribute (자동 재배치) ⭐ NEW

weak 섹션이 감지되면 다른 섹션에서 재활용 가능한 Research Item을 자동으로 제안하고 배치합니다.

**트리거 조건:**
- evidence_balance에서 coverage="weak" 섹션 발견
- 해당 섹션이 CTA, Closing 등 핵심 마무리 섹션

**수행 작업:**
1. weak 섹션의 목적 분석 (CTA → 행동 촉구, Closing → 요약/강화)
2. 다른 섹션에서 재활용 가능한 데이터 탐색
3. 재활용 우선순위 결정
4. 자동 배치 또는 사용자 확인 요청

**재활용 우선순위 매트릭스:**

| 대상 섹션 | 재활용 적합 data_type | 재활용 방식 |
|----------|---------------------|------------|
| CTA | statistic (ROI, 성과) | 핵심 수치 요약 재사용 |
| CTA | quote (고객 증언) | 신뢰 강화용 재사용 |
| Closing | statistic (핵심 KPI) | 3대 성과 요약 |
| Closing | comparison (차별점) | 경쟁 우위 재강조 |

**Reuse Type 정의:**

| 타입 | 설명 | 변환 예시 |
|-----|------|----------|
| `summary` | 핵심 수치만 추출 | "90% 감소, 3개월 ROI" → "$1.8M 절감 효과" |
| `reinforcement` | 신뢰 강화 요소로 변환 | "삼성전자 증언" → "삼성전자 도입 사례" |
| `callback` | 앞서 언급한 내용 상기 | "앞서 말씀드린 $2M 손실을 해결합니다" |
| `projection` | 미래 예측으로 변환 | "90% 오류 감소" → "연간 $1.8M 절감 예상" |

**출력 구조:**
```json
{
  "auto_redistribute": {
    "triggered_by": "weak_section_detected",
    "weak_sections": ["cta"],
    "redistribution_plan": [
      {
        "target_section": "cta",
        "target_slide": 11,
        "source_research_id": "R003",
        "original_section": "answer",
        "original_slide": 7,
        "reuse_type": "summary",
        "reuse_content": {
          "original": "90% 오류 감소, 3개월 ROI 달성",
          "reused_as": "투자 시 3개월 내 ROI 달성 보장",
          "visual": "metric_box",
          "placement": "CTA 버튼 상단"
        },
        "confidence": 0.9,
        "auto_apply": true
      },
      {
        "target_section": "cta",
        "target_slide": 11,
        "source_research_id": "R004",
        "original_section": "answer",
        "original_slide": 9,
        "reuse_type": "reinforcement",
        "reuse_content": {
          "original": "팀 생산성 40% 향상 - 삼성전자",
          "reused_as": "삼성전자도 선택한 솔루션",
          "visual": "source_badge",
          "placement": "신뢰 배지"
        },
        "confidence": 0.85,
        "auto_apply": false,
        "requires_confirmation": true
      }
    ],
    "post_redistribution_coverage": {
      "cta": { "coverage": "adequate", "research_count": 2 }
    }
  }
}
```

**설정 옵션:**

```yaml
auto_redistribute:
  enabled: true
  auto_apply_threshold: 0.9  # confidence 이상이면 자동 적용
  require_confirmation_below: 0.9
  max_reuse_per_section: 3

  # 섹션별 재활용 규칙
  section_rules:
    cta:
      preferred_data_types: ["statistic", "quote"]
      reuse_types: ["summary", "reinforcement"]
      min_items: 1
      max_items: 2
    closing:
      preferred_data_types: ["statistic", "comparison"]
      reuse_types: ["summary", "callback"]
      min_items: 2
      max_items: 3
```

**워크플로우 변경:**

```
기존:
outline_generate → evidence_balance → [경고만 표시] → Content Skill

개선:
outline_generate → evidence_balance → weak 감지?
                                         │
                                         ├─ Yes → auto_redistribute
                                         │           │
                                         │           ├─ confidence >= 0.9 → 자동 배치
                                         │           │
                                         │           └─ confidence < 0.9
                                         │                  → 사용자 확인 요청
                                         │
                                         └─ No → Content Skill로 전달
```

## 구조 설계 워크플로우

```
검증된 데이터 수신 (Validation Skill)
         │
         ▼
   청중 분석 (audience_analysis)
         │
         ▼
   프레임워크 선택 (framework_select)
         │
         ▼
   핵심 메시지 도출 (message_extract)
         │
         ▼
   아웃라인 생성 (outline_generate)
         │
         ▼
   흐름 검증 (flow_validate)
         │
         ├─ 검증 실패 → 아웃라인 수정
         │
         ▼
   Content Skill로 전달
```

## 사용 예시

### 예시 1: 구조 설계 요청
```
사용자: "투자자 대상 피치덱 구조 잡아줘"

수행:
1. audience_analysis: 청중=투자자 분석
2. framework_select: SCQA 또는 Hero's Journey 추천
3. message_extract: 핵심 가치 제안 도출
4. outline_generate: 15장 피치덱 아웃라인 생성
5. flow_validate: 논리 흐름 검증
```

### 예시 2: 스토리라인 개선
```
사용자: "기존 PPT 스토리라인 개선해줘"

수행:
1. 기존 구조 분석
2. 청중 재분석
3. 프레임워크 적합성 평가
4. 개선된 아웃라인 제안
5. 변경 사항 비교표 제공
```

## 아웃라인 출력 템플릿

```markdown
# PPT 구조 설계서

## 개요
- **발표 제목:** [제목]
- **청중:** [청중 유형]
- **프레임워크:** SCQA
- **총 슬라이드:** 16장
- **예상 발표 시간:** 15분

## 슬라이드 아웃라인

### Part 1: Situation (슬라이드 1-5)
| # | 유형 | 헤드라인 | 핵심 내용 | 데이터 출처 |
|---|------|---------|----------|------------|
| 1 | Title | [헤드라인] | - | - |
| 2 | Agenda | 오늘 다룰 내용 | 3가지 주제 | - |
| ... | ... | ... | ... | ... |

### Part 2: Complication (슬라이드 6-8)
...

### Part 3: Answer (슬라이드 9-15)
...

### Part 4: CTA (슬라이드 16)
...

## 핵심 메시지
1. [첫 번째 핵심 메시지]
2. [두 번째 핵심 메시지]
3. [세 번째 핵심 메시지]

## 시간 배분
- Situation: 3분 (20%)
- Complication: 2분 (13%)
- Answer: 8분 (54%)
- CTA: 2분 (13%)
```

## 다음 단계 연결

구조 설계 완료 후:
1. 아웃라인은 **Content Skill**로 전달하여 슬라이드별 콘텐츠 작성
2. 프레임워크 정보는 **Design System Skill**에서 시각적 흐름 설계에 활용

## 주의사항

- 청중 분석 없이 구조를 설계하지 말 것
- 프레임워크는 혼합 사용 가능하나, 주 프레임워크 하나를 일관되게 유지
- 슬라이드 수는 1분당 1-2장 기준 (복잡도에 따라 조정)
- 핵심 메시지는 3개 이내로 유지 (기억 용이성)
- Appendix 활용으로 본문 슬라이드 간결하게 유지
