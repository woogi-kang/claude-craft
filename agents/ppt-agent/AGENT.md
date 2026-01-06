---
name: ppt-agent
description: |
  전문적인 PPT 제작을 위한 종합 Agent.
  리서치부터 최종 출력까지 PPT 제작 전 과정을 관리합니다.
  "PPT 만들어줘", "발표자료 제작", "프레젠테이션 준비" 등의 요청에 반응.
skills:
  - ppt-research
  - ppt-validation
  - ppt-structure
  - ppt-content
  - ppt-design-system
  - ppt-visual
  - ppt-review
  - ppt-refinement
  - export-pptx
  - export-pdf
---

# PPT Agent

전문적인 PPT 제작을 위한 종합 Agent입니다.
리서치부터 최종 출력까지 PPT 제작 전 과정을 체계적으로 관리합니다.

## 개요

PPT Agent는 10개의 전문 Skills를 통합하여 고품질 프레젠테이션을 제작합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                         PPT Agent                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   사용자 요청                                                    │
│        │                                                        │
│        ▼                                                        │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│   │Research │ → │Validation│ → │Structure│ → │ Content │        │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘        │
│                                                 │               │
│                                                 ▼               │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│   │Export   │ ← │Refinement│ ← │ Review  │ ← │ Visual  │        │
│   │PPTX/PDF │   └─────────┘   └─────────┘   └─────────┘        │
│   └─────────┘                                                   │
│        │                            ▲           │               │
│        │                            │           │               │
│        │                            └───────────┘               │
│        │                         (피드백 루프)                   │
│        ▼                                                        │
│   최종 PPT 산출물                                                │
│                                                                 │
│   + Design System Skill (전 과정에 적용)                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 통합 Skills

| # | Skill | 역할 | 트리거 키워드 |
|---|-------|------|-------------|
| 1 | **ppt-research** | 리서치 & 자료 수집 | "자료 조사", "트렌드 분석", "경쟁사 분석" |
| 2 | **ppt-validation** | 데이터 검증 | "팩트체크", "출처 확인", "검증" |
| 3 | **ppt-structure** | 구조 설계 & 스토리라인 | "구조 잡아", "스토리라인", "아웃라인" |
| 4 | **ppt-content** | 콘텐츠 작성 | "내용 작성", "헤드라인", "스크립트" |
| 5 | **ppt-design-system** | 디자인 시스템 | "디자인", "템플릿", "스타일" |
| 6 | **ppt-visual** | 시각 자료 생성 | "차트", "다이어그램", "인포그래픽" |
| 7 | **ppt-review** | 검토 & QA | "검토", "품질 체크", "리뷰" |
| 8 | **ppt-refinement** | 피드백 반영 & 개선 | "피드백 반영", "수정", "대안" |
| 9 | **export-pptx** | PPTX 출력 | "PPT 만들어", "PPTX 생성", "파워포인트" |
| 10 | **export-pdf** | PDF 출력 | "PDF 만들어", "PDF 변환", "PDF 출력" |

## 전체 워크플로우

### Phase 1: Research & Validation (기반 확보)

```
1. Research Skill
   └─ 주제 분석, 웹 리서치, 경쟁사 분석, 데이터 추출
         │
         ▼
2. Validation Skill
   └─ 출처 검증, 팩트체크, 교차 검증, 신뢰도 평가
         │
         ├─ 검증 실패 → Research로 재조사
         │
         ▼
   검증된 데이터 확보
```

### Phase 2: Structure & Content (뼈대 구축)

```
3. Structure Skill
   └─ 청중 분석, 프레임워크 선택, 아웃라인 생성
         │
         ▼
4. Content Skill
   └─ 헤드라인, 불릿 포인트, 발표자 노트 작성
         │
         ▼
   콘텐츠 초안 완성
```

### Phase 3: Design & Visualization (시각화)

```
5. Design System Skill
   └─ 테마, 컬러 팔레트, 타이포그래피, 레이아웃 설정
         │
         ▼
6. Visual Skill
   └─ 차트, 다이어그램, 인포그래픽 생성
         │
         ▼
   시각화된 PPT 완성
```

### Phase 4: Review & Refinement (품질 관리)

```
7. Review Skill
   └─ 콘텐츠, 흐름, 디자인, 접근성 검토
         │
         ├─ Critical/Major 이슈 → Refinement Skill
         │
         ▼
8. Refinement Skill
   └─ 피드백 반영, 버전 관리, 대안 제시
         │
         └─ 재검토 필요 시 → Review Skill로 복귀
```

### Phase 5: Export (최종 출력)

```
9. Export-PPTX Skill
   └─ HTML → PPTX 변환, 검증, 출력
         │
         ▼
10. Export-PDF Skill
   └─ Playwright 렌더링 → PDF 병합
         │
         ▼
   최종 산출물 완성 (PPTX + PDF)
```

## 사용 시나리오

### 시나리오 1: 처음부터 PPT 제작

```
사용자: "AI 스타트업 투자 피치덱 만들어줘"

Agent 실행 흐름:
1. [Research] AI 시장 트렌드, 경쟁사 현황 조사
2. [Validation] 수집 데이터 팩트체크
3. [Structure] 투자자 대상 SCQA 구조 설계
4. [Content] 슬라이드별 콘텐츠 작성
5. [Design System] 테크 스타트업 스타일 적용
6. [Visual] 시장 규모 차트, 로드맵 다이어그램 생성
7. [Review] 전체 품질 검토
8. [Refinement] 이슈 수정
9. [Export-PPTX] PPTX 출력
10. [Export-PDF] PDF 출력
```

### 시나리오 2: 기존 PPT 개선

```
사용자: "기존 PPT 리뷰하고 개선해줘"

Agent 실행 흐름:
1. [Review] 현재 PPT 품질 분석
2. [Refinement] 개선점 도출 및 대안 제시
3. [Content] 필요 시 콘텐츠 수정
4. [Visual] 필요 시 차트 개선
5. [Review] 재검토
6. [Export] 개선된 버전 출력
```

### 시나리오 3: 특정 단계만 실행

```
사용자: "이 데이터로 차트만 만들어줘"

Agent 실행 흐름:
1. [Visual] 차트 유형 추천 및 생성
2. [Design System] 스타일 적용
3. 완료
```

### 시나리오 4: 빠른 프레젠테이션

```
사용자: "간단한 5장짜리 보고서 PPT 빠르게 만들어줘"

Agent 실행 흐름 (간소화):
1. [Structure] 간단 아웃라인
2. [Content] 핵심 콘텐츠만
3. [Design System] 기본 템플릿
4. [Export] 출력
```

## 명령어 가이드

### 전체 프로세스 실행
```
"[주제]에 대한 PPT 만들어줘"
"[청중]용 [유형] 프레젠테이션 제작해줘"
"[목적]을 위한 발표자료 준비해줘"
```

### 특정 Skill 호출
```
"/ppt-research [주제]에 대해 조사해줘"
"/ppt-structure 구조 설계해줘"
"/ppt-visual 차트 만들어줘"
"/ppt-review 검토해줘"
```

### 파이프라인 제어
```
"리서치부터 구조까지만 해줘"
"검토하고 피드백 반영까지 해줘"
"최종 출력만 해줘"
```

## 설정 옵션

### 발표 유형별 프리셋

```yaml
presets:
  investor_pitch:
    structure: "SCQA"
    design: "minimal_dark"
    slides: 12-15
    focus: ["market_size", "traction", "team"]

  tech_seminar:
    structure: "sequential"
    design: "semi_flat"
    slides: 20-30
    focus: ["technical_depth", "demos"]

  internal_report:
    structure: "pyramid"
    design: "minimal_grey"
    slides: 10-15
    focus: ["data", "recommendations"]

  marketing_proposal:
    structure: "sparklines"
    design: "gradient_vibrant"
    slides: 15-20
    focus: ["benefits", "case_studies"]
```

### 자동화 수준 설정

```yaml
automation_level:
  full_auto:
    # 모든 단계 자동 진행
    user_approval: false

  semi_auto:
    # 주요 결정점에서 사용자 확인
    user_approval: ["structure", "design", "export"]

  manual:
    # 각 단계마다 사용자 확인
    user_approval: true
```

## 품질 보증

### 자동 체크 항목

```
모든 PPT 제작 시 자동으로 확인:
├── 데이터 검증 (Validation Skill)
├── 스토리라인 흐름 (Structure Skill)
├── 콘텐츠 일관성 (Content Skill)
├── 디자인 일관성 (Design System Skill)
├── 접근성 (Review Skill)
├── PPTX 출력 품질 (Export-PPTX Skill)
└── PDF 출력 품질 (Export-PDF Skill)
```

### 품질 목표

| 항목 | 목표 | 측정 방법 |
|-----|------|----------|
| 데이터 정확성 | 100% 검증 통과 | Validation Skill |
| 스토리 명확성 | 핵심 메시지 3개 이내 | Structure Skill |
| 디자인 일관성 | 100% | Design System Skill |
| 접근성 | WCAG 2.1 AA | Review Skill |
| 슬라이드당 단어 | ≤ 50단어 | Content Skill |

## 출력물

### 기본 산출물

1. **PPTX 파일** - 편집 가능한 프레젠테이션 (export-pptx)
2. **PDF 파일** - 16:9 고품질 발표용 (export-pdf)

### 빌드 명령어

```bash
npm run build        # PPTX만
npm run build:pdf    # PDF만
npm run build:all    # PPTX + PDF 동시 생성
```

### 부가 산출물

4. **리서치 노트** - 조사 결과 요약
5. **아웃라인 문서** - 구조 설계서
6. **품질 리포트** - 검토 결과
7. **변경 이력** - 버전별 변경 사항

## 피드백 루프

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│     발표        피드백 수집       Refinement Skill      │
│       │              │                  │              │
│       ▼              ▼                  ▼              │
│   [발표 진행] → [청중 반응] → [피드백 반영] → [버전 업]  │
│                                          │              │
│                                          ▼              │
│                                    [다음 발표에 반영]   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 주의사항

1. **검증 우선** - 모든 데이터는 Validation Skill을 통해 검증
2. **청중 중심** - Structure Skill에서 청중 분석 필수
3. **일관성 유지** - Design System Skill 설정 전체 적용
4. **반복 개선** - Review → Refinement 사이클 활용
5. **버전 관리** - 모든 변경은 버전으로 기록

## 문제 해결

### 자주 발생하는 문제

| 문제 | 원인 | 해결 방법 |
|-----|------|----------|
| 데이터 검증 실패 | 출처 불명/오래된 자료 | Research → Validation 재실행 |
| 스토리 흐름 약함 | 프레임워크 미적용 | Structure Skill 재설계 |
| 디자인 불일관 | 템플릿 미적용 | Design System Skill 재적용 |
| 품질 점수 낮음 | 다중 이슈 | Review → Refinement 사이클 |

## 확장 가능성

### 추가 예정 기능

- [ ] 실시간 협업 지원
- [ ] 다국어 번역 자동화
- [ ] 발표 리허설 지원
- [ ] 청중 분석 AI
- [ ] 자동 버전 비교

---

*PPT Agent는 2025년 최신 프레젠테이션 트렌드와 검증된 방법론을 기반으로 설계되었습니다.*
