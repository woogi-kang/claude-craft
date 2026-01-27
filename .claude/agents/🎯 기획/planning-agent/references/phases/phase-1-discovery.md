# Phase 1: Discovery (발견)

> **Version**: 3.2.0 | **Type**: Phase Reference
> 아이디어/가치제안/타겟 사용자 정의

---

## Overview

| Property | Value |
|----------|-------|
| Phase Number | 1 |
| Skills | 3 (idea-intake, value-proposition, target-user) |
| Synthesis | synthesis-discovery |
| Output Folder | `01-discovery/` |

---

## Skills

### 1. Idea Intake
- **역할**: 아이디어 정의, 문제/솔루션 가설
- **프레임워크**: Problem-Solution Fit
- **출력**: `idea-intake.md`

### 2. Value Proposition
- **역할**: 가치 제안, 차별점, Why Now
- **프레임워크**: UVP Canvas
- **출력**: `value-proposition.md`

### 3. Target User
- **역할**: 타겟 사용자 정의
- **프레임워크**: Persona, JTBD
- **출력**: `target-user.md`

---

## Execution Flow

```mermaid
flowchart TD
    s1["1. Idea Intake<br/>아이디어 정의, 문제 정의, 솔루션 가설"]
    s1 --> check1{정보 부족?}
    check1 -->|예| q1[추가 질문]
    q1 --> s1
    check1 -->|아니오| s2

    s2["2. Value Proposition<br/>UVP, 차별점, Why Now"]
    s2 --> s3

    s3["3. Target User<br/>페르소나, JTBD"]
    s3 --> syn1

    syn1[/"Synthesis-Discovery<br/>품질 검증 & 통합"/]
    syn1 --> check2{누락/불일치?}
    check2 -->|예| retry1[해당 Skill 재실행]
    retry1 --> s1
    check2 -->|아니오| done1([Discovery 문서 완성])
```

---

## Frameworks

| Framework | Purpose | Skill |
|-----------|---------|-------|
| **Problem-Solution Fit** | 문제/솔루션 정합성 | Idea Intake |
| **UVP Canvas** | 가치 제안 정의 | Value Proposition |
| **JTBD** | 고객 니즈 분석 | Target User |
| **Persona** | 타겟 사용자 구체화 | Target User |

---

## Quality Checklist

- [ ] 문제 정의가 명확한가?
- [ ] 솔루션이 문제를 해결하는가?
- [ ] 타겟 사용자가 구체적인가?
- [ ] Why Now (왜 지금인가)가 설득력 있는가?
