---
name: plan-risk-management
description: |
  리스크를 식별하고 관리하는 스킬.
  잠재적 위험 요소와 대응 계획을 수립합니다.
triggers:
  - "리스크 관리"
  - "Risk Management"
  - "위험 분석"
  - "리스크 분석"
input:
  - roadmap.md 결과
  - tech-stack.md 결과
  - team-structure.md 결과
output:
  - 07-execution/risk-management.md
---

# Risk Management Skill

프로젝트 리스크를 식별하고 대응 계획을 수립합니다.

## 출력 템플릿

```markdown
# {Project Name} - 리스크 관리

## 1. 리스크 Overview

### 리스크 매트릭스

```
              높음 ┃          ┃          ┃
                   ┃  MEDIUM  ┃   HIGH   ┃ CRITICAL
                   ┃          ┃          ┃
      영 ──────────╋──────────╋──────────╋──────────
      향           ┃          ┃          ┃
                   ┃   LOW    ┃  MEDIUM  ┃   HIGH
              중간 ┃          ┃          ┃
                   ┃          ┃          ┃
         ──────────╋──────────╋──────────╋──────────
                   ┃          ┃          ┃
                   ┃   LOW    ┃   LOW    ┃  MEDIUM
              낮음 ┃          ┃          ┃
                   ┃──────────┃──────────┃──────────
                      낮음       중간       높음
                              발생 확률
```

### 리스크 현황

| 등급 | 개수 | 주요 리스크 |
|------|------|------------|
| 🔴 Critical | {n} | {risk_summary} |
| 🟠 High | {n} | {risk_summary} |
| 🟡 Medium | {n} | {risk_summary} |
| 🟢 Low | {n} | {risk_summary} |

---

## 2. 제품 리스크

### 시장 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| MR-001 | 시장 수요 부족 | {prob} | {impact} | 🔴 | {response} |
| MR-002 | 경쟁사 대응 | {prob} | {impact} | 🟠 | {response} |
| MR-003 | 시장 타이밍 | {prob} | {impact} | 🟡 | {response} |

**대응 전략**

| 리스크 | 예방 | 완화 | 전가 | 수용 |
|--------|------|------|------|------|
| MR-001 | MVP 검증 | 피봇 플랜 | - | - |
| MR-002 | 차별화 | 빠른 실행 | - | - |

### 제품 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| PR-001 | PMF 미달성 | {prob} | {impact} | 🔴 | {response} |
| PR-002 | 사용성 문제 | {prob} | {impact} | 🟠 | {response} |
| PR-003 | 기능 범위 과다 | {prob} | {impact} | 🟡 | {response} |

---

## 3. 기술 리스크

### 개발 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| TR-001 | 기술 난이도 | {prob} | {impact} | 🟠 | {response} |
| TR-002 | 일정 지연 | {prob} | {impact} | 🟠 | {response} |
| TR-003 | 기술 부채 | {prob} | {impact} | 🟡 | {response} |
| TR-004 | 외부 API 의존성 | {prob} | {impact} | 🟡 | {response} |

**기술 부채 관리**

| 영역 | 현재 상태 | 허용 수준 | 해소 계획 |
|------|----------|----------|----------|
| 코드 품질 | {status} | {threshold} | {plan} |
| 테스트 커버리지 | {status} | {threshold} | {plan} |
| 문서화 | {status} | {threshold} | {plan} |

### 인프라 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| IR-001 | 서버 장애 | {prob} | {impact} | 🟠 | {response} |
| IR-002 | 데이터 유실 | {prob} | {impact} | 🔴 | {response} |
| IR-003 | 보안 사고 | {prob} | {impact} | 🔴 | {response} |

---

## 4. 비즈니스 리스크

### 재무 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| FR-001 | 자금 소진 | {prob} | {impact} | 🔴 | {response} |
| FR-002 | 수익화 실패 | {prob} | {impact} | 🔴 | {response} |
| FR-003 | 비용 초과 | {prob} | {impact} | 🟠 | {response} |

**Runway 시나리오**

| 시나리오 | 월 Burn | Runway | 필요 조치 |
|----------|---------|--------|-----------|
| Best | {burn} | {months}개월 | - |
| Base | {burn} | {months}개월 | {action} |
| Worst | {burn} | {months}개월 | {action} |

### 법적 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| LR-001 | 규제 변경 | {prob} | {impact} | 🟡 | {response} |
| LR-002 | 개인정보 위반 | {prob} | {impact} | 🔴 | {response} |
| LR-003 | 지적재산권 | {prob} | {impact} | 🟡 | {response} |

---

## 5. 조직 리스크

### 팀 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| OR-001 | 핵심 인력 이탈 | {prob} | {impact} | 🔴 | {response} |
| OR-002 | 채용 실패 | {prob} | {impact} | 🟠 | {response} |
| OR-003 | 팀 갈등 | {prob} | {impact} | 🟡 | {response} |
| OR-004 | 번아웃 | {prob} | {impact} | 🟠 | {response} |

**Key Person Risk**

| 역할 | 현재 | 백업 | 지식 문서화 |
|------|------|------|------------|
| {role_1} | {name} | {backup} | {status} |
| {role_2} | {name} | {backup} | {status} |

### 커뮤니케이션 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| CR-001 | 정보 단절 | {prob} | {impact} | 🟡 | {response} |
| CR-002 | 의사결정 지연 | {prob} | {impact} | 🟡 | {response} |

---

## 6. 외부 리스크

### 시장 환경 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| ER-001 | 경기 침체 | {prob} | {impact} | 🟡 | {response} |
| ER-002 | 기술 변화 | {prob} | {impact} | 🟡 | {response} |
| ER-003 | 플랫폼 정책 변경 | {prob} | {impact} | 🟠 | {response} |

### 경쟁 리스크

| ID | 리스크 | 확률 | 영향 | 등급 | 대응 |
|----|--------|------|------|------|------|
| CR-001 | 대기업 진입 | {prob} | {impact} | 🟠 | {response} |
| CR-002 | 가격 경쟁 | {prob} | {impact} | 🟡 | {response} |
| CR-003 | 카피캣 | {prob} | {impact} | 🟢 | {response} |

---

## 7. 리스크 대응 계획

### 대응 전략 유형

| 전략 | 설명 | 적용 |
|------|------|------|
| 회피 (Avoid) | 리스크 원인 제거 | 고위험, 고영향 |
| 완화 (Mitigate) | 확률/영향 감소 | 중위험 |
| 전가 (Transfer) | 제3자에게 이전 | 보험, 계약 |
| 수용 (Accept) | 발생 시 대응 | 저위험, 저영향 |

### Critical 리스크 대응

#### 🔴 {Risk Name}

| 항목 | 내용 |
|------|------|
| 리스크 ID | {id} |
| 설명 | {description} |
| 영향 | {impact_detail} |

**대응 계획**

1. **예방 조치**
   - {prevention_1}
   - {prevention_2}

2. **완화 조치**
   - {mitigation_1}
   - {mitigation_2}

3. **비상 계획**
   - 트리거: {trigger}
   - 조치: {action}
   - 담당: {owner}

---

## 8. 모니터링 계획

### 리스크 지표

| 리스크 | 모니터링 지표 | 임계값 | 주기 |
|--------|-------------|--------|------|
| {risk_1} | {indicator} | {threshold} | 주간 |
| {risk_2} | {indicator} | {threshold} | 일간 |
| {risk_3} | {indicator} | {threshold} | 월간 |

### Early Warning Signs

| 리스크 | 경고 신호 | 조치 |
|--------|----------|------|
| {risk_1} | {warning_sign} | {action} |
| {risk_2} | {warning_sign} | {action} |

### 정기 리뷰

| 리뷰 | 주기 | 참석자 | 안건 |
|------|------|--------|------|
| 리스크 점검 | 주간 | PM, TL | 주요 리스크 현황 |
| 리스크 리뷰 | 월간 | 전원 | 신규 리스크, 대응 효과 |
| 리스크 감사 | 분기 | 경영진 | 전체 리스크 현황 |

---

## 9. 비상 대응 체계

### 에스컬레이션 매트릭스

| 등급 | 대응 시간 | 보고 대상 | 의사결정 |
|------|----------|----------|----------|
| 🔴 Critical | 즉시 | CEO/CTO | 경영진 |
| 🟠 High | 4시간 | PM/TL | PM |
| 🟡 Medium | 24시간 | PM | PM |
| 🟢 Low | 1주 | 담당자 | 담당자 |

### 비상 연락망

| 상황 | 1차 | 2차 | 3차 |
|------|-----|-----|-----|
| 서비스 장애 | {name} | {name} | {name} |
| 보안 사고 | {name} | {name} | {name} |
| 데이터 유실 | {name} | {name} | {name} |

### Incident Response

```
1. 탐지 (Detection)
   └─ 모니터링, 알림

2. 분석 (Analysis)
   └─ 영향 범위 파악

3. 격리 (Containment)
   └─ 확산 방지

4. 해결 (Resolution)
   └─ 원인 제거

5. 복구 (Recovery)
   └─ 정상화

6. 학습 (Lessons Learned)
   └─ 재발 방지
```

---

## 10. 결론

### 주요 리스크 요약

```
┌─────────────────────────────────────────────────────────────────┐
│                        리스크 현황                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🔴 Critical ({n}개)                                            │
│  ─────────────                                                  │
│  - {critical_risk_1}                                           │
│  - {critical_risk_2}                                           │
│                                                                  │
│  🟠 High ({n}개)                                                │
│  ─────────────                                                  │
│  - {high_risk_1}                                               │
│  - {high_risk_2}                                               │
│                                                                  │
│  📊 총 리스크: {total}개                                        │
│  📅 다음 리뷰: {date}                                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 즉시 조치 필요

1. **{action_1}** ← 담당: {owner}
2. **{action_2}** ← 담당: {owner}
3. **{action_3}** ← 담당: {owner}

---

*다음 단계: KPI/OKR → Operation Plan*
```

## 퀄리티 체크리스트

```
□ 모든 리스크 영역이 식별되었는가?
□ 확률과 영향이 평가되었는가?
□ 대응 전략이 수립되었는가?
□ 모니터링 계획이 있는가?
□ 비상 대응 체계가 있는가?
□ 담당자가 지정되었는가?
□ 정기 리뷰 계획이 있는가?
```

## 다음 스킬 연결

Risk Management 완료 후:

1. **KPI/OKR 설정** → KPI/OKR Skill
2. **운영 계획** → Operation Plan Skill
3. **실행 착수** → Sprint 시작

---

*리스크 관리는 예측이 아니라 준비입니다. 최악에 대비하세요.*
