# Output Structure

> **Version**: 1.0.0 | **Type**: Shared Reference

---

## Directory Structure

**중요: 모든 산출물은 프로젝트별 폴더에 저장**

```
workspace/work-plan/
│
└── {project-name}/                 # 프로젝트별 폴더 (필수!)
    │
    ├── 01-discovery/
    │   ├── idea-intake.md          # 아이디어 정의
    │   ├── value-proposition.md    # 가치 제안
    │   └── target-user.md          # 타겟 사용자
    │
    ├── 02-research/
    │   ├── market-research.md      # 시장 조사
    │   ├── competitor-analysis.md  # 경쟁사 분석
    │   └── user-research.md        # 사용자 리서치 가이드
    │
    ├── 03-validation/
    │   ├── lean-canvas.md          # 린 캔버스
    │   ├── business-model.md       # 비즈니스 모델
    │   ├── pricing-strategy.md     # 가격 정책
    │   ├── mvp-definition.md       # MVP 정의
    │   └── legal-checklist.md      # 법적 체크리스트
    │
    ├── 04-specification/
    │   ├── prd.md                  # PRD
    │   ├── feature-spec.md         # 기능 명세
    │   ├── information-architecture.md # IA
    │   ├── user-flow.md            # 사용자 플로우
    │   ├── wireframe-guide.md      # 와이어프레임 가이드
    │   └── data-strategy.md        # 데이터 전략
    │
    ├── 05-estimation/
    │   ├── tech-stack.md           # 기술 스택
    │   ├── effort-estimation.md    # 공수 산정
    │   └── team-structure.md       # 팀 구성
    │
    ├── 06-design/
    │   ├── ux-strategy.md          # UX 전략
    │   └── brand-direction.md      # 브랜드 방향
    │
    ├── 07-execution/
    │   ├── roadmap.md              # 로드맵
    │   ├── risk-management.md      # 리스크 관리
    │   ├── kpi-okr.md              # KPI/OKR
    │   └── operation-plan.md       # 운영 계획
    │
    ├── 08-launch/
    │   ├── growth-strategy.md      # 그로스 전략
    │   ├── pitch-deck-outline.md   # 피치덱 구조
    │   └── gtm-strategy.md         # GTM 전략
    │
    ├── _synthesis/                   # Phase별 종합 문서
    │   ├── discovery-synthesis.md    # Discovery 종합
    │   ├── research-synthesis.md     # Research 종합
    │   ├── validation-synthesis.md   # Validation 종합
    │   ├── specification-synthesis.md # Specification 종합
    │   ├── estimation-synthesis.md   # Estimation 종합
    │   ├── design-synthesis.md       # Design 종합
    │   ├── execution-synthesis.md    # Execution 종합
    │   └── launch-synthesis.md       # Launch 종합
    │
    └── _exports/
        └── notion-export.md        # 노션 붙여넣기용 통합본
```

---

## Phase Outputs

### Discovery Phase

```yaml
outputs:
  - 아이디어 정의서
  - 가치 제안 캔버스
  - 페르소나 초안
```

### Research Phase

```yaml
outputs:
  - 시장 분석 리포트 (TAM/SAM/SOM)
  - 경쟁사 분석표
  - 사용자 리서치 가이드
```

### Validation Phase

```yaml
outputs:
  - 린 캔버스
  - 비즈니스 모델 문서
  - 가격 정책 설계
  - MVP 정의서
  - 법적 체크리스트
```

### Specification Phase

```yaml
outputs:
  - PRD (제품 요구사항 문서)
  - 기능 명세서
  - 정보 구조 (IA)
  - 사용자 플로우
  - 와이어프레임 가이드
  - 데이터 전략
```

### Estimation Phase

```yaml
outputs:
  - 기술 스택 추천
  - 개발 공수 산정표
  - 팀 구성 제안
```

### Design Phase

```yaml
outputs:
  - UX 전략 문서
  - 브랜드 방향 가이드
```

### Execution Phase

```yaml
outputs:
  - 로드맵 & 마일스톤
  - 리스크 관리 계획
  - KPI/OKR 정의
  - 운영 계획
```

### Launch Phase

```yaml
outputs:
  - 그로스 전략
  - 피치덱 구조
  - GTM 체크리스트
  - 노션 Export 통합본
```
