---
name: research-shared
description: |
  콘텐츠 제작을 위한 리서치 공통 방법론.
  Presentation, Social Media, Tech Blog 에이전트가 공유하는 리서치 프로세스.
metadata:
  category: "📝 콘텐츠"
  type: shared
  version: "1.0.0"
  consumers:
    - presentation-agent-skills/1-research
    - social-media-agent-skills/1-research
    - tech-blog-agent-skills/1-research
---
# Research Skill (Shared)

콘텐츠 유형에 관계없이 적용되는 리서치 공통 방법론입니다.

## Triggers

- "리서치", "자료 조사", "트렌드 분석", "경쟁사 분석", "research"

---

## 공통 리서치 프로세스

### 1. 주제 분석 (Topic Analysis)

핵심 주제를 분석하고 하위 주제로 확장합니다:

1. 핵심 키워드 추출 및 확장
2. 관련 개념/용어 맵핑
3. 주제 범위 정의
4. 타깃 오디언스 식별

### 2. 웹 리서치 (Web Research)

최신 트렌드, 통계, 사례를 수집합니다:

**출처 우선순위:**

| 순위 | 출처 유형 | 예시 |
|------|----------|------|
| 1 | 공식 문서/기관 보고서 | 정부 통계, 학술 논문 |
| 2 | 산업 리서치 기관 | Gartner, McKinsey, IDC |
| 3 | 주요 언론사/전문 미디어 | TechCrunch, 한경 |
| 4 | 전문가 블로그/컨퍼런스 | 공식 블로그, 컨퍼런스 발표 |
| 5 | 커뮤니티/일반 블로그 | Reddit, 개인 블로그 |

### 3. 경쟁사/벤치마킹 분석

동일 주제의 기존 콘텐츠를 분석합니다:

- 구조/포맷 분석
- 메시지 전략 분석
- 차별화 포인트 식별

### 4. 출처 관리 (Source Tracking)

모든 수집 데이터에 출처를 기록합니다:

```yaml
source:
  url: "https://..."
  title: "출처 제목"
  date: "2025-01-15"
  type: "article|study|statistics|report"
  credibility: "high|medium|low"
```

### 5. 데이터 추출 (Data Extraction)

문서에서 핵심 데이터를 추출합니다:

- 통계/수치 데이터
- 핵심 인용문
- 사례 연구

---

## 신뢰도 평가 기준

| 출처 유형 | 초기 신뢰도 | 설명 |
|----------|------------|------|
| 정부기관/학술논문 | 0.9+ | 공신력 있는 기관 |
| 주요 언론사 | 0.8+ | 검증된 미디어 |
| 산업 리서치 기관 | 0.8+ | 전문 리서치 |
| 기업 공식 자료 | 0.7+ | 공식 발표 자료 |
| 전문 블로그 | 0.6+ | 전문가 의견 |
| 일반 블로그/커뮤니티 | 0.4+ | 추가 검증 필요 |
| 출처 불명 | 0.2 | 사용 비권장 |

---

## 리서치 결과 공통 구조

```yaml
research_output:
  date: "YYYY-MM-DD"
  topic: "[리서치 주제]"

  items:
    - id: "R001"
      content: "수집된 정보"
      source:
        url: "https://..."
        title: "출처 제목"
        date: "YYYY-MM-DD"
        type: "article"
      credibility_score: 0.85
      tags: ["키워드1", "키워드2"]

  sources:
    - url: "[출처 URL]"
      title: "[출처 제목]"
      credibility: "high"
```

---

## 공통 주의사항

- 모든 수집 데이터에 반드시 출처를 기록할 것
- 통계 데이터는 발행일 확인 필수
- 저작권 준수 (직접 인용 시 출처 명시)
- 초기 신뢰도 점수는 참고용이며 Validation에서 최종 검증

---

## 다음 단계

리서치 완료 후 → Validation Skill로 수집 데이터 검증

---

## 콘텐츠 유형별 오버라이드

각 에이전트별 스킬에서 다음 항목을 콘텐츠 유형에 맞게 구체화합니다:

| 항목 | Presentation | Social Media | Tech Blog |
|------|-------------|--------------|-----------|
| 추가 분석 | story_criticality, visual_suggestion | viral_pattern, topic_clustering | keyword_research, code_research |
| 결과 구조 | research_item + content_ready | research_output + content_ideas | web_research + code_research |
| 출처 현지화 | citation_config (ko/en) | - | - |
| 경쟁사 분석 | 발표자료 구조 분석 | 콘텐츠 퍼포먼스 분석 | SEO/검색량 분석 |
| 시각화 제안 | visual_suggestion 포함 | 플랫폼별 포맷 제안 | 코드 예제 포함 |
| 계절 연동 | - | seasonal_hooks, content_calendar | - |
