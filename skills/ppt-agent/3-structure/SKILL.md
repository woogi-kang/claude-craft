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

### 4. outline_generate (아웃라인 생성)
슬라이드별 아웃라인을 생성합니다.

**출력 구조:**
```json
{
  "outline": {
    "total_slides": 16,
    "estimated_duration": "15min",
    "framework": "SCQA",
    "slides": [
      {
        "number": 1,
        "type": "title",
        "headline": "3가지 전략으로 시장 점유율 10% 회복",
        "key_points": [],
        "data_sources": [],
        "notes": "임팩트 있는 오프닝"
      }
    ]
  }
}
```

### 5. flow_validate (흐름 검증)
스토리라인의 논리적 흐름을 검증합니다.

**검증 항목:**
- 프레임워크 일관성
- 논리적 연결성
- 시간 배분 적절성
- 메시지 명확성

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
