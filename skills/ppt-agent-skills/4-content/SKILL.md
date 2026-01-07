---
name: ppt-content
description: |
  슬라이드별 텍스트 콘텐츠를 최적화하는 Skill.
  헤드라인 작성, 불릿 포인트 압축, 발표 스크립트 생성 시 활성화.
  "내용 작성해줘", "헤드라인 만들어줘", "스크립트 써줘" 등의 요청에 반응.
---

# PPT Content Skill

슬라이드별 텍스트 콘텐츠를 최적화하는 Skill입니다.

## 콘텐츠 작성 원칙

### 1. 헤드라인 공식

효과적인 헤드라인은 다음 공식을 따릅니다:

```
[숫자/수치] + [혜택/결과] + [기간/방법]
```

**예시:**
| 유형 | 헤드라인 예시 |
|-----|-------------|
| 성과 강조 | "3가지 전략으로 매출 40% 성장 달성" |
| 문제 해결 | "6개월 만에 고객 이탈률 50% 감소" |
| 학습/교육 | "1시간 안에 마스터하는 AI 프롬프팅" |
| 기회 제시 | "2025년 $50B 시장, 3가지 진입 전략" |
| 비교 | "기존 대비 5배 빠른 처리 속도" |

**헤드라인 체크리스트:**
- [ ] 구체적인 숫자가 포함되어 있는가?
- [ ] 독자에게 주는 혜택이 명확한가?
- [ ] 10단어 이내인가?
- [ ] 행동을 유도하는가?

### 2. 슬라이드 텍스트 규칙

#### 텍스트 분량 가이드

| 요소 | 권장 기준 | 최대 기준 |
|-----|---------|---------|
| **헤드라인** | 7단어 | 10단어 |
| **불릿 포인트 수** | 3개 | 5개 |
| **불릿당 줄 수** | 1줄 | 2줄 |
| **슬라이드당 총 단어** | 30단어 | 50단어 |

#### 폰트 크기 가이드

| 요소 | 최소 크기 | 권장 크기 |
|-----|---------|---------|
| **제목** | 36pt | 44pt+ |
| **부제목** | 28pt | 32pt |
| **본문** | 24pt | 28pt |
| **캡션/주석** | 18pt | 20pt |

### 3. 불릿 포인트 작성법

**원칙:**
1. **병렬 구조 유지** - 모든 불릿이 동일한 문법 구조
2. **동사로 시작** - 행동 지향적 표현
3. **구체적 수치 포함** - 모호한 표현 지양
4. **한 가지 아이디어** - 불릿당 하나의 핵심만

**Before & After:**

| Before (나쁜 예) | After (좋은 예) |
|-----------------|----------------|
| 매출이 증가했습니다 | 매출 40% 증가 (YoY) |
| 고객 만족도 향상 | 고객 만족도 4.2 → 4.8 |
| 효율성이 좋아짐 | 처리 시간 50% 단축 |
| 다양한 기능 | 핵심 기능 5가지 탑재 |

### 4. 발표자 노트 구조

각 슬라이드의 발표자 노트는 다음 구조를 따릅니다:

```
[오프닝 훅] - 청중 주의 집중 (10초)
"여러분, 지난 분기 우리 팀이 달성한 놀라운 성과를 공유하려 합니다."

[핵심 메시지] - 슬라이드의 요점 (20초)
"이 슬라이드의 핵심은 3가지 전략이 40% 매출 성장을 이끌었다는 것입니다."

[부연 설명] - 예시, 사례, 데이터 (30초)
"구체적으로 살펴보면, 첫 번째 전략인 신규 시장 진출이 전체 성장의 60%를 차지했습니다..."

[전환 문구] - 다음 슬라이드로 연결 (10초)
"이제 각 전략의 상세 내용을 살펴보겠습니다."
```

**발표자 노트 시간 배분:**
- 일반 슬라이드: 1분
- 데이터 슬라이드: 1분 30초
- 타이틀/전환 슬라이드: 30초

## 핵심 기능

### 1. headline_generate (헤드라인 생성)
슬라이드별 임팩트 있는 헤드라인을 생성합니다.

**입력:**
- 슬라이드 유형 (title, data, solution 등)
- 핵심 메시지
- 관련 데이터

**출력:**
- 주 헤드라인 (1안)
- 대안 헤드라인 (2-3안)
- 헤드라인 품질 점수

**헤드라인 유형별 템플릿:**

| 슬라이드 유형 | 템플릿 | 예시 |
|-------------|-------|------|
| Title | [핵심 가치] [청중 혜택] | "AI 자동화로 업무 시간 50% 절감" |
| Problem | [문제] [영향/비용] | "수작업 오류로 연간 $2M 손실" |
| Solution | [방법] [결과] | "3단계 자동화로 오류율 90% 감소" |
| Data | [수치] [의미] | "DAU 100만 돌파, 전년 대비 3배 성장" |
| CTA | [행동] [기대 결과] | "지금 시작하면 3개월 내 ROI 달성" |

### 2. bullet_optimize (불릿 최적화) ⭐ ENHANCED
긴 텍스트를 효과적인 불릿 포인트로 압축하고 **Research 출처를 연결**합니다.

**수행 작업:**
- 핵심 정보 추출
- 병렬 구조로 재구성
- 숫자/수치 강조
- 불필요한 단어 제거
- **research_mapping 기반 content_ready 활용**
- **출처 정보 자동 연결**

**입력:** Structure Skill의 research_mapping 포함 아웃라인

**개선된 압축 규칙:**
```
입력:
- research_mapping: {
    research_id: "R003",
    content_ready: {
      bullet_format: "수작업 오류 비용 연간 $2M",
      citation_short: "(내부 감사 2024)"
    }
  }
- 원문: "내부 감사에서 수작업 오류 비용이 높다고 분석됨"

출력:
{
  "text": "수작업 오류 비용 연간 $2M",
  "attribution": {
    "research_id": "R003",
    "citation_short": "(내부 감사 2024)",
    "citation_full": "내부 감사 보고서 2024, n=500 거래 분석",
    "confidence": 0.92
  }
}
```

**기존 압축 예시:**
```
원문: "우리 회사는 지난 6개월 동안 새로운 마케팅 전략을 도입하여
      신규 고객 수가 크게 증가하는 성과를 거두었습니다."

압축: "신규 고객 45% 증가 (6개월)"
```

### 3. script_generate (발표 스크립트 생성)
각 슬라이드에 대한 발표자 스크립트를 생성합니다.

**출력 구조:**
```json
{
  "slide_script": {
    "slide_number": 5,
    "duration": "60sec",
    "opening_hook": "...",
    "key_message": "...",
    "supporting_details": "...",
    "transition": "...",
    "full_script": "...",
    "keywords_to_emphasize": ["성장", "40%", "전략"]
  }
}
```

### 4. tone_adjust (톤 조정)
청중에 맞게 콘텐츠의 톤과 난이도를 조정합니다.

**톤 매트릭스:**

| 청중 | 톤 | 전문 용어 | 예시 표현 |
|-----|---|---------|---------|
| 경영진 | 간결, 전략적 | 최소화 | "ROI 3배 달성" |
| 기술팀 | 상세, 기술적 | 적극 사용 | "API 레이턴시 50ms 이하" |
| 투자자 | 비전, 확신 | 설명 포함 | "TAM $50B 시장 진출" |
| 일반 대중 | 친근, 비유 | 회피 | "스마트폰처럼 쉬운 사용" |

### 5. consistency_check (일관성 검사)
전체 PPT의 용어, 표현, 숫자 일관성을 검사합니다.

**검사 항목:**
- 숫자 표기 통일 (%, 퍼센트 혼용 금지)
- 용어 통일 (같은 개념, 같은 단어)
- 시제 일관성
- 띄어쓰기/맞춤법

### 6. attribution_attach (출처 부착) ⭐ NEW
콘텐츠의 모든 정량적 주장에 Research 출처를 자동으로 부착합니다.

**입력:**
- Structure Skill의 research_mapping
- 생성된 headline/bullet 텍스트

**수행 작업:**
- 텍스트 내 정량적 주장 식별 (숫자, %, 금액 등)
- research_mapping에서 해당 주장의 출처 매칭
- citation_short/citation_full 생성
- display_mode에 따른 렌더링

**출력 구조:**
```json
{
  "slide": {
    "number": 5,
    "type": "problem",
    "headline": {
      "text": "수작업 오류로 연간 $2M 손실",
      "attribution": {
        "research_id": "R003",
        "citation_short": "(내부 감사 2024)",
        "citation_full": "내부 감사 보고서 2024, n=500 거래 분석",
        "confidence": 0.92
      }
    },
    "bullets": [
      {
        "text": "수작업 데이터 입력 오류율 15%",
        "attribution": {
          "research_id": "R005",
          "citation_short": "(운영팀 조사)",
          "citation_full": "운영팀 품질 조사 2024 Q3",
          "confidence": 0.85
        }
      },
      {
        "text": "직원 40% 업무시간이 수동 작업에 소비",
        "attribution": {
          "research_id": "R007",
          "citation_short": "(직원 설문)",
          "citation_full": "2024 직원 업무 효율성 설문, n=200",
          "confidence": 0.78
        }
      }
    ],

    "attribution_config": {
      "display_mode": "footnote",
      "include_confidence": false,
      "footnote_style": "short"
    },

    "rendered_content": {
      "headline": "수작업 오류로 연간 $2M 손실",
      "bullets_with_citations": [
        "수작업 데이터 입력 오류율 15% ¹",
        "직원 40% 업무시간이 수동 작업에 소비 ²"
      ],
      "footnotes": [
        "¹ 운영팀 조사 2024",
        "² 직원 설문 2024"
      ]
    },

    "speaker_note_sources": {
      "opening": "이 슬라이드의 데이터는 2024년 내부 감사 및 직원 설문에서 가져왔습니다.",
      "detail_by_claim": [
        "📊 '$2M 손실' - 내부 감사팀이 500건의 거래를 분석한 결과입니다.",
        "📊 '15% 오류율' - 운영팀이 Q3에 측정한 품질 지표입니다.",
        "📊 '40% 시간' - 200명 직원 대상 설문 결과입니다."
      ]
    }
  }
}
```

**Display Mode 옵션:**

| 모드 | 설명 | 적용 예시 |
|-----|------|----------|
| `inline` | 텍스트 내 삽입 | "연간 $2M 손실 (내부 감사 2024)" |
| `footnote` | 각주 번호 | "연간 $2M 손실 ¹" + 하단 각주 |
| `speaker_note` | 발표자 노트에만 | 슬라이드에는 미표시 |
| `hidden` | 메타데이터만 | 표시 없음, 추적용 |

**Footnote Style 옵션:**

| 스타일 | 형식 | 예시 |
|-------|------|------|
| `short` | 출처명 + 연도 | "Gartner, 2024" |
| `full` | 전체 출처 정보 | "Gartner AI Market Report, Nov 2024" |
| `numbered` | 번호만 | "¹" (하단에 상세) |

### 7. citation_normalize (출처 정규화) ⭐ NEW

모든 citation을 설정된 언어와 형식으로 통일합니다.

**입력:**
- Research Skill의 citation_config 설정
- 원본 citation_short, citation_full

**수행 작업:**
1. 출처명 언어 감지
2. 설정된 언어로 번역/변환
3. 형식 템플릿 적용
4. 일관성 검증

**출력 구조:**
```json
{
  "citation_normalize": {
    "config": {
      "language": "ko",
      "format": "short"
    },
    "normalized_citations": [
      {
        "research_id": "R001",
        "original": {
          "short": "(Gartner, 2024)",
          "full": "Gartner AI Market Report, Nov 2024"
        },
        "normalized": {
          "short": "(가트너, 2024)",
          "full": "출처: 가트너 AI 시장 보고서, 2024년 11월"
        },
        "changes_made": ["source_translated", "format_applied"]
      },
      {
        "research_id": "R002",
        "original": {
          "short": "(McKinsey, 2024)",
          "full": "McKinsey Automation ROI Study"
        },
        "normalized": {
          "short": "(맥킨지, 2024)",
          "full": "출처: 맥킨지 자동화 ROI 연구, 2024년 9월"
        },
        "changes_made": ["source_translated", "title_translated", "format_applied"]
      },
      {
        "research_id": "R003",
        "original": {
          "short": "(내부 감사)",
          "full": "내부 감사 보고서 2024"
        },
        "normalized": {
          "short": "(내부 자료, 2024)",
          "full": "출처: 내부 감사 보고서, 2024년"
        },
        "changes_made": ["label_standardized", "format_applied"]
      }
    ],
    "consistency_score": 1.0,
    "warnings": []
  }
}
```

**정규화 규칙:**

| 규칙 | 설명 | 예시 |
|-----|------|------|
| 출처명 번역 | citation_config.source_translation 적용 | Gartner → 가트너 |
| 연도 통일 | 4자리 연도 표기 | 24 → 2024 |
| 형식 통일 | 괄호 형식 일관화 | [출처] → (출처) |
| 라벨 표준화 | 내부 출처 통일 | 자체 조사 → 내부 자료 |

**워크플로우:**

```
attribution_attach
       │
       ▼
citation_normalize (language 설정 적용)
       │
       ▼
rendered_content (통일된 출처 형식)
```

**슬라이드 하단 출처 표기 (정규화 후):**

```html
<footer class="slide__footer">
  <div class="citation-list">
    <span class="citation-list__label">출처:</span>
    <span class="citation-list__item">¹ 가트너 AI 시장 보고서, 2024</span>
    <span class="citation-list__item">² 맥킨지 자동화 ROI 연구, 2024</span>
    <span class="citation-list__item">³ 내부 자료</span>
  </div>
</footer>
```

## 콘텐츠 템플릿

### 타이틀 슬라이드
```yaml
slide_type: title
headline: "[핵심 가치 제안]"
subtitle: "[발표 제목 또는 부연]"
presenter: "[발표자 이름]"
date: "[발표 날짜]"
logo: "[회사 로고]"
```

### 문제 정의 슬라이드
```yaml
slide_type: problem
headline: "[문제] [영향/비용]"
bullets:
  - "현황: [구체적 수치]"
  - "문제점: [핵심 이슈]"
  - "영향: [비용/손실]"
visual: "[관련 차트 또는 이미지]"
```

### 솔루션 슬라이드
```yaml
slide_type: solution
headline: "[방법] [결과]"
bullets:
  - "전략 1: [내용] → [결과]"
  - "전략 2: [내용] → [결과]"
  - "전략 3: [내용] → [결과]"
visual: "[프로세스 다이어그램]"
```

### 데이터 슬라이드
```yaml
slide_type: data
headline: "[핵심 인사이트] [수치]"
chart_type: "[bar/line/pie]"
key_insight: "[차트에서 주목할 점]"
annotation: "[추가 설명]"
source: "[데이터 출처]"
```

### CTA 슬라이드
```yaml
slide_type: cta
headline: "[행동 촉구]"
next_steps:
  - "Step 1: [구체적 행동]"
  - "Step 2: [구체적 행동]"
  - "Step 3: [구체적 행동]"
contact: "[연락처 정보]"
```

## 콘텐츠 작성 워크플로우

```
아웃라인 수신 (Structure Skill)
         │
         ▼
   슬라이드별 헤드라인 생성
         │
         ▼
   불릿 포인트 작성/최적화
         │
         ▼
   발표자 노트 생성
         │
         ▼
   톤 조정 (청중 맞춤)
         │
         ▼
   일관성 검사
         │
         ├─ 검사 실패 → 수정
         │
         ▼
   Design System Skill로 전달
```

## 사용 예시

### 예시 1: 콘텐츠 작성 요청
```
사용자: "슬라이드 5-8 내용 작성해줘"

수행:
1. 각 슬라이드 유형 확인
2. headline_generate로 헤드라인 생성
3. bullet_optimize로 불릿 작성
4. script_generate로 발표자 노트 생성
5. consistency_check로 일관성 검증
```

### 예시 2: 헤드라인 개선 요청
```
사용자: "이 헤드라인 더 임팩트있게 만들어줘"

수행:
1. 현재 헤드라인 분석
2. 헤드라인 공식 적용
3. 3가지 대안 제시
4. 각 대안의 장단점 설명
```

## 콘텐츠 품질 체크리스트

### 헤드라인 체크
- [ ] 10단어 이내
- [ ] 구체적 숫자/수치 포함
- [ ] 청중 혜택 명시
- [ ] 액션 지향적

### 불릿 포인트 체크
- [ ] 3-5개 이내
- [ ] 병렬 구조
- [ ] 각 불릿 2줄 이내
- [ ] 모호한 표현 없음

### 발표자 노트 체크
- [ ] 1분 분량
- [ ] 4파트 구조 (훅-메시지-상세-전환)
- [ ] 강조할 키워드 표시
- [ ] 자연스러운 연결

### 전체 일관성 체크
- [ ] 용어 통일
- [ ] 숫자 표기 통일
- [ ] 시제 일관성
- [ ] 맞춤법/띄어쓰기

## 다음 단계 연결

콘텐츠 작성 완료 후:
1. 완성된 콘텐츠는 **Design System Skill**로 전달하여 시각적 스타일 적용
2. 데이터 관련 슬라이드는 **Visual Skill**에서 차트/그래프 생성

## 주의사항

- 슬라이드당 한 가지 핵심 메시지만 전달
- 텍스트보다 시각 자료를 우선 고려
- 발표자 노트 없이 슬라이드만으로 이해 불가능해야 효과적
- 청중 수준에 맞는 용어와 톤 사용
- 모든 숫자는 출처와 함께 기록
