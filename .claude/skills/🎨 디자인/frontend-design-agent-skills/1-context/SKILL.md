---
name: fd-context-intake
description: |
  프론트엔드 디자인 프로젝트의 기초를 다지는 핵심 스킬.
  목적, 타겟 사용자, 브랜드 톤, 제약 조건, 경쟁사 정보를 체계적으로 수집합니다.
triggers:
  - "컨텍스트"
  - "프로젝트 파악"
  - "요구사항"
  - "디자인 시작"
  - "브리핑"
input:
  - 프로젝트 설명
  - 브랜드 자료 (선택)
  - 기존 디자인 (선택)
output:
  - workspace/work-design/{project}/context/project-context.md
---

# Context Intake Skill

프론트엔드 디자인의 성공은 **명확한 컨텍스트 파악**에서 시작됩니다.
이 스킬은 프로젝트의 목적, 사용자, 브랜드, 제약 조건을 체계적으로 수집합니다.

## 왜 중요한가?

```
컨텍스트 없이 디자인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"예쁘게 만들어주세요" → 방향 없는 디자인

컨텍스트 기반 디자인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Context Intake → 목적에 맞는 전략적 디자인
```

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| 프로젝트 설명 | Y | 무엇을 만드는지 (랜딩페이지, 대시보드, 앱 등) |
| 목적/목표 | Y | 왜 만드는지 (전환율, 브랜딩, 정보 전달 등) |
| 타겟 사용자 | Y | 누구를 위한 것인지 |
| 브랜드 가이드 | N | 기존 브랜드 자료, 로고, 컬러 |
| 경쟁사 | N | 참고할 경쟁사나 벤치마크 |
| 제약 조건 | N | 기술 스택, 예산, 일정, 접근성 요구사항 |

## 수집 항목

### 1. 필수 정보 (Must Have)

```yaml
project:
  name: ""                      # 프로젝트/제품 이름
  type: ""                      # 유형: 랜딩페이지 | 대시보드 | SaaS | 이커머스 | 포트폴리오 | 블로그
  one_liner: ""                 # 한 줄 설명
  industry: ""                  # 산업군: 핀테크 | 헬스케어 | 에듀테크 | AI/ML | 이커머스 | B2B

goal:
  primary: ""                   # 주요 목표: 리드 수집 | 전환율 | 브랜드 인지도 | 정보 전달
  success_metrics:              # 성공 지표
    - ""
  priority: ""                  # 우선순위: 전환 | 미적 임팩트 | 사용성 | 정보 전달

target_users:
  primary: ""                   # 주 사용자 그룹
  secondary: ""                 # 부 사용자 그룹 (선택)
  demographics:                 # 인구통계
    age_range: ""               # 예: "25-40"
    occupation: ""              # 예: "스타트업 창업자, 개발자"
    tech_savviness: ""          # 높음 | 중간 | 낮음
```

### 2. 브랜드 정보 (Should Have)

```yaml
brand:
  existing_guidelines: false    # 기존 브랜드 가이드 유무
  logo_url: ""                  # 로고 파일 경로/URL

  tone:                         # 브랜드 톤 (3가지 선택)
    - ""                        # 예: "전문적인", "친근한", "혁신적인"
    - ""                        # 예: "신뢰감 있는", "젊은", "럭셔리한"
    - ""

  personality:                  # 브랜드가 사람이라면?
    is_like: ""                 # 예: "믿음직한 친구", "혁신적인 리더"
    not_like: ""                # 예: "딱딱한 관공서", "너무 가벼운 캐주얼"

  colors:
    primary: ""                 # 메인 컬러 (HEX)
    secondary: ""               # 보조 컬러 (HEX)
    has_flexibility: true       # 컬러 조정 가능 여부

  fonts:
    preferred: ""               # 선호 폰트
    avoid: ""                   # 피해야 할 폰트 스타일
```

### 3. 경쟁 환경 (Should Have)

```yaml
competitors:
  direct:                       # 직접 경쟁사
    - name: ""
      url: ""
      like: ""                  # 좋은 점
      dislike: ""               # 개선할 점

  aspirational:                 # 닮고 싶은 브랜드 (다른 산업도 가능)
    - name: ""
      url: ""
      why: ""                   # 이유

differentiation:
  unique_value: ""              # 차별화 포인트
  avoid_similarity: ""          # 닮으면 안 되는 것
```

### 4. 제약 조건 (Nice to Have)

```yaml
constraints:
  tech_stack:                   # 기술 스택
    framework: ""               # React | Next.js | Vue | Svelte
    ui_library: ""              # Tailwind | shadcn | Chakra | 순수 CSS
    animation: ""               # Framer Motion | GSAP | CSS only

  timeline:
    deadline: ""                # 마감일
    milestones: []              # 중간 마일스톤

  accessibility:
    wcag_level: ""              # AA | AAA | 없음
    special_needs: []           # 시각장애, 고령자 등

  devices:
    primary: ""                 # 데스크톱 | 모바일 | 태블릿
    support: []                 # 지원 기기 목록

  performance:
    target_lcp: ""              # 목표 LCP (초)
    bundle_budget: ""           # JS 번들 크기 제한
```

## 인터뷰 질문 템플릿

### Quick Start (5분)

```
1. 무엇을 만드시나요? (프로젝트 유형)
2. 이 프로젝트의 목표는 무엇인가요? (목적)
3. 누가 사용하나요? (타겟 사용자)
4. 브랜드 톤을 3단어로 표현한다면? (톤앤매너)
5. 참고하고 싶은 사이트가 있나요? (레퍼런스)
```

### Deep Dive (15분)

```
프로젝트 개요
─────────────────────────────────
1. 프로젝트를 한 문장으로 설명해주세요.
2. 어떤 산업/분야인가요?
3. 경쟁사 대비 차별점은 무엇인가요?
4. 이 프로젝트의 가장 중요한 성공 지표는?
5. 가장 우선시하는 것은? (전환 vs 미적 임팩트 vs 사용성)

타겟 사용자
─────────────────────────────────
6. 주요 타겟 사용자는 누구인가요?
7. 그들의 연령대와 기술 친숙도는?
8. 어떤 문제를 해결해주나요?
9. 사용자가 이 사이트에서 가장 먼저 해야 할 행동은?
10. 모바일 vs 데스크톱, 어디서 더 많이 접속하나요?

브랜드 & 톤
─────────────────────────────────
11. 기존 브랜드 가이드가 있나요?
12. 브랜드가 사람이라면 어떤 성격인가요?
13. 절대 하고 싶지 않은 디자인 스타일은?
14. 닮고 싶은 브랜드/사이트 3개를 꼽는다면?
15. 기존 로고나 컬러 사용이 필수인가요?

제약 조건
─────────────────────────────────
16. 사용해야 하는 기술 스택이 있나요?
17. 접근성 요구사항이 있나요? (WCAG 레벨)
18. 마감 기한이 언제인가요?
19. 다크모드 지원이 필요한가요?
20. 다국어 지원이 필요한가요?
```

### Design-Specific 질문 (10분)

```
미적 선호도
─────────────────────────────────
1. 미니멀 vs 맥시멀리즘?
2. 기하학적 vs 유기적 형태?
3. 플랫 vs 글래스모피즘 vs 뉴모피즘?
4. 정적 vs 인터랙티브 (모션 많음)?
5. 모노톤 vs 비비드 컬러?

콘텐츠 유형
─────────────────────────────────
6. 주요 콘텐츠는? (텍스트 | 이미지 | 비디오 | 데이터)
7. 일러스트레이션 스타일 선호? (2D | 3D | 없음)
8. 아이콘 스타일? (라인 | 솔리드 | 없음)
9. 사진 톤? (밝은 | 어두운 | 자연스러운)
```

## Workflow

```
1. 사용자 요청 수신
      │
      ▼
2. 프로젝트 유형 파악
   ├── 랜딩페이지/마케팅
   ├── 대시보드/SaaS
   ├── 이커머스
   ├── 포트폴리오
   └── 기타
      │
      ▼
3. Quick Start 질문 (필수 정보 수집)
      │
      ├─ 부족 → 추가 질문
      │
      ▼
4. Deep Dive 질문 (권장 정보 수집)
      │
      ▼
5. Design-Specific 질문 (선택)
      │
      ▼
6. 컨텍스트 문서 생성
      │
      ▼
7. 사용자 확인 & 보완
      │
      ▼
8. 최종 저장
   → workspace/work-design/{project}/context/project-context.md
```

## Output

### 출력 디렉토리 구조

```
workspace/work-design/{project}/
├── context/
│   └── project-context.md      # 프로젝트 컨텍스트
├── inspiration/                 # 2-inspiration 스킬에서 사용
├── direction/                   # 3-direction 스킬에서 사용
└── design-system/               # Phase 2 스킬에서 사용
```

### 컨텍스트 문서 템플릿

```markdown
# {Project Name} Design Context

> 생성일: {date}
> 마지막 수정: {date}

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 프로젝트명 | {name} |
| 유형 | {type} |
| 산업군 | {industry} |
| 한 줄 설명 | {one_liner} |

## 2. 목표 & 성공 지표

### 주요 목표
{primary_goal}

### 성공 지표
- {metric_1}
- {metric_2}

### 우선순위
1순위: {priority}

## 3. 타겟 사용자

### 주요 사용자
- **그룹**: {primary_users}
- **연령대**: {age_range}
- **직업**: {occupation}
- **기술 친숙도**: {tech_savviness}

### 사용자 니즈
- {need_1}
- {need_2}

### 핵심 사용자 행동 (Primary Action)
{primary_action}

## 4. 브랜드 가이드

### 톤앤매너
| 키워드 | 설명 |
|--------|------|
| {tone_1} | {explanation} |
| {tone_2} | {explanation} |
| {tone_3} | {explanation} |

### 브랜드 성격
- **닮은 것**: {is_like}
- **피할 것**: {not_like}

### 컬러 & 폰트
| 항목 | 값 | 조정 가능 |
|------|-----|----------|
| Primary Color | {primary_color} | {yes/no} |
| Secondary Color | {secondary_color} | {yes/no} |
| 선호 폰트 | {preferred_font} | - |

## 5. 경쟁 & 벤치마크

### 직접 경쟁사
| 경쟁사 | URL | 좋은 점 | 개선할 점 |
|--------|-----|---------|----------|
| {competitor_1} | {url} | {like} | {dislike} |
| {competitor_2} | {url} | {like} | {dislike} |

### 롤모델 브랜드
| 브랜드 | 이유 |
|--------|------|
| {aspirational_1} | {why} |
| {aspirational_2} | {why} |

### 차별화 포인트
{differentiation}

## 6. 제약 조건

### 기술 스택
| 항목 | 값 |
|------|-----|
| Framework | {framework} |
| UI Library | {ui_library} |
| Animation | {animation_library} |

### 일정
| 마일스톤 | 일자 |
|----------|------|
| 디자인 시스템 | {date} |
| 첫 번째 페이지 | {date} |
| 전체 완료 | {deadline} |

### 접근성
- WCAG 레벨: {wcag_level}
- 특수 요구사항: {special_needs}

### 디바이스
- 주요 디바이스: {primary_device}
- 지원 디바이스: {supported_devices}

### 성능
- 목표 LCP: {target_lcp}
- 번들 예산: {bundle_budget}

## 7. 미적 선호도 요약

| 축 | 선호도 |
|----|--------|
| 복잡도 | {미니멀 ←――――→ 맥시멀} |
| 형태 | {기하학 ←――――→ 유기적} |
| 질감 | {플랫 ←――――→ 글래스/뉴모} |
| 모션 | {정적 ←――――→ 인터랙티브} |
| 컬러 | {모노톤 ←――――→ 비비드} |

## 8. 다음 단계

- [ ] 인스피레이션 수집 (2-inspiration)
- [ ] 미적 방향 결정 (3-direction)
- [ ] 타이포그래피 시스템 (4-typography)

---

*이 문서는 모든 디자인 스킬에서 참조됩니다. 정보가 변경되면 업데이트하세요.*
```

## 퀄리티 체크리스트

```
□ 프로젝트 유형 명확
□ 주요 목표 정의됨
□ 타겟 사용자 구체적
□ 브랜드 톤 3가지 이상
□ 경쟁사/벤치마크 1개 이상
□ 우선순위 명확 (전환 vs 미적 vs 사용성)
□ 기술 제약 파악
□ 접근성 요구사항 확인
```

## 정보 부족 시 대응

### 최소 정보로 시작

```yaml
minimum_viable_context:
  type: "프로젝트 유형"
  goal: "주요 목표"
  target_hint: "대략적인 타겟"
  tone_hint: "원하는 느낌 1-2가지"
```

최소 정보만으로도 시작 가능하지만, 결과물이 generic할 수 있음을 안내합니다.

### 점진적 수집

```
1차 컨텍스트 → Direction 제안 → 피드백 → 컨텍스트 보완 → 최종 Direction
```

## 다음 스킬 연결

컨텍스트 수집 완료 후:

| 상황 | 다음 스킬 |
|------|-----------|
| 레퍼런스 필요 | → 2-inspiration |
| 방향 결정 필요 | → 3-direction |
| 브랜드 컬러 있음 | → 5-color (바로 진행 가능) |

---

*Context Intake는 디자인 품질의 80%를 결정합니다. 충분한 시간을 투자하세요.*
