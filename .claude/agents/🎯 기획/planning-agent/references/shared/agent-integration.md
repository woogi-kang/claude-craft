# Agent Integration

> **Version**: 1.0.0 | **Type**: Shared Reference

---

## Integration Overview

```
planning-agent (기획)
    │
    ├─► frontend-design-agent (UI 디자인)
    │       └─ wireframe-guide에서 연계
    │
    ├─► nextjs-expert-agent / flutter-expert-agent (개발)
    │       └─ tech-stack에서 연계
    │
    ├─► ppt-agent (피치덱)
    │       └─ pitch-deck에서 연계
    │
    ├─► marketing-agent (GTM 실행)
    │       └─ gtm-strategy에서 연계
    │
    └─► legal-contract-agent (법무 검토)
            └─ legal-checklist에서 연계
```

---

## Handoff Points

### frontend-design-agent

**Trigger**: wireframe-guide.md 완성 후
**Input**: 와이어프레임 가이드, IA 문서
**Output**: 실제 UI 디자인

```yaml
handoff:
  from: planning-agent
  to: frontend-design-agent
  artifact: wireframe-guide.md
  context:
    - information-architecture.md
    - user-flow.md
    - ux-strategy.md
```

### nextjs-expert-agent / flutter-expert-agent

**Trigger**: tech-stack.md 완성 후
**Input**: 기술 스택, PRD, 기능 명세
**Output**: 실제 코드 구현

```yaml
handoff:
  from: planning-agent
  to: nextjs-expert-agent | flutter-expert-agent
  artifact: tech-stack.md
  context:
    - prd.md
    - feature-spec.md
    - data-strategy.md
```

### ppt-agent

**Trigger**: pitch-deck-outline.md 완성 후
**Input**: 피치덱 구조, 비즈니스 모델
**Output**: PPT 슬라이드

```yaml
handoff:
  from: planning-agent
  to: ppt-agent
  artifact: pitch-deck-outline.md
  context:
    - lean-canvas.md
    - business-model.md
    - market-research.md
```

### marketing-agent

**Trigger**: gtm-strategy.md 완성 후
**Input**: GTM 전략, 그로스 전략
**Output**: 상세 마케팅 실행 계획

```yaml
handoff:
  from: planning-agent
  to: marketing-agent
  artifact: gtm-strategy.md
  context:
    - growth-strategy.md
    - target-user.md
```

### legal-contract-agent

**Trigger**: legal-checklist.md 완성 후
**Input**: 법적 체크리스트
**Output**: 상세 법무 검토, 약관 초안

```yaml
handoff:
  from: planning-agent
  to: legal-contract-agent
  artifact: legal-checklist.md
  context:
    - business-model.md
    - pricing-strategy.md
```

---

## Execution Example

```
사용자: "서비스 기획부터 개발까지 해줘"

1. planning-agent 실행
   └─ 8개 Phase 완료

2. 자동 연계 제안
   ├─ "UI 디자인을 진행할까요?" → frontend-design-agent
   ├─ "개발을 시작할까요?" → nextjs-expert-agent
   └─ "피치덱을 만들까요?" → ppt-agent

3. 사용자 선택에 따라 해당 에이전트 호출
```
