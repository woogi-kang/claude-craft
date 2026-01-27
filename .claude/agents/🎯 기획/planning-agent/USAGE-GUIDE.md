---
name: "Planning Agent Usage Guide"
description: "Unified orchestrator with phase selection (8 phases, 37 skills)"
---

# Planning Agent Usage Guide

> **v3.2.0** - Progressive Disclosure + Phase Selection

---

## Phase 비교

| Phase | Skills | 주요 산출물 | 소요 시간 |
|-------|--------|------------|----------|
| 1. Discovery | 3 | 아이디어/가치제안/타겟 | 30분 |
| 2. Research | 3 | 시장/경쟁/사용자 리서치 | 45분 |
| 3. Validation | 5 | 린캔버스/MVP/법적체크 | 60분 |
| 4. Specification | 6 | PRD/기능명세/플로우 | 90분 |
| 5. Estimation | 3 | 기술스택/공수/팀구성 | 30분 |
| 6. Design | 2 | UX전략/브랜드방향 | 20분 |
| 7. Execution | 4 | 로드맵/리스크/KPI | 45분 |
| 8. Launch | 3 | 그로스/피치덱/GTM | 30분 |

---

## Quick Start

### 전체 기획 (모든 Phase)

```bash
@planning-agent "[아이디어] 서비스 기획해줘"
@planning-agent "[아이디어] 전체 기획 문서 만들어줘"
```

### 특정 Phase만 실행

```bash
# Phase 지정
@planning-agent "[아이디어]" --phase discovery
@planning-agent "[아이디어]" --phase validation
@planning-agent "[아이디어]" --phase specification

# 특정 Phase부터 시작
@planning-agent "[아이디어]" --from specification
```

### Phase 미지정 (선택 프롬프트)

```bash
# Phase를 지정하지 않으면 선택 옵션 제공
@planning-agent "[아이디어]"

# → "어떤 범위로 기획할까요?"
#   [전체 (8 Phases)] [Discovery~Validation] [Specification만] [특정 Phase 선택]
```

---

## 시나리오별 권장 Phase

### 새 아이디어 검증
```bash
# Discovery + Research + Validation만
@planning-agent "[아이디어]" --phases discovery,research,validation
```

### MVP 개발 준비
```bash
# Validation + Specification + Estimation
@planning-agent "[아이디어]" --phases validation,specification,estimation
```

### 투자 유치 준비
```bash
# Research + Validation + Launch
@planning-agent "[아이디어]" --phases research,validation,launch
```

### 기존 서비스 신규 기능
```bash
# Specification만
@planning-agent "[기능 설명]" --phase specification
```

---

## 디렉토리 구조 (v3.2.0)

```
planning-agent/
├── planning-agent-unified.md   # 통합 오케스트레이터 (메인)
├── USAGE-GUIDE.md              # 이 가이드
│
└── references/                  # Progressive Disclosure
    ├── phases/                  # Phase별 참조
    │   ├── phase-1-discovery.md
    │   ├── phase-2-research.md
    │   ├── phase-3-validation.md
    │   ├── phase-4-specification.md
    │   ├── phase-5-estimation.md
    │   ├── phase-6-design.md
    │   ├── phase-7-execution.md
    │   └── phase-8-launch.md
    │
    └── shared/                  # 공통 참조
        └── framework-summary.md
```

---

## 출력물 구조

```
workspace/work-plan/{project-name}/
├── 01-discovery/
├── 02-research/
├── 03-validation/
├── 04-specification/
├── 05-estimation/
├── 06-design/
├── 07-execution/
├── 08-launch/
├── _synthesis/           # Phase별 종합 문서
└── _exports/
    └── notion-export.md
```

---

## 특정 Skill 직접 호출

```bash
/plan-idea          # 아이디어 정의
/plan-value         # 가치 제안
/plan-target        # 타겟 사용자
/plan-market        # 시장 조사
/plan-competitor    # 경쟁사 분석
/plan-lean          # 린 캔버스
/plan-prd           # PRD
/plan-feature       # 기능 명세
/plan-roadmap       # 로드맵
/plan-pitch         # 피치덱
```

---

## 마이그레이션 가이드

```bash
# Before (기존)
"서비스 기획해줘"  # → 전체 889줄 로드

# After (v3.2.0)
"서비스 기획해줘"  # → 200줄 오케스트레이터 + 필요한 Phase만 로드
```

---

## 문제 해결

| 문제 | 해결 방법 |
|-----|----------|
| 결과물이 generic | Idea Intake에서 상세 정보 제공 |
| 시장 데이터 부정확 | 외부 리서치로 보완 |
| 기술 스택 안 맞음 | 팀 역량/제약 조건 공유 |
| 공수 추정 안 맞음 | 버퍼 추가, 스프린트 단위로 쪼개기 |
