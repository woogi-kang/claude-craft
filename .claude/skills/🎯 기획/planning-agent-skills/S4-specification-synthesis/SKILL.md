---
name: plan-specification-synthesis
description: |
  Phase 4 Specification 단계의 결과를 종합하는 스킬.
  PRD, 사용자 스토리, 기술 명세를 통합 검토합니다.
triggers:
  - "specification 종합"
  - "phase 4 종합"
  - "명세 종합"
input:
  - 04-specification/prd.md
  - 04-specification/user-stories.md
  - 04-specification/technical-requirements.md
  - 04-specification/api-specification.md
  - 04-specification/data-model.md
  - 04-specification/data-strategy.md
output:
  - 04-specification/SYNTHESIS.md
phase: 4
sequence: S4
---

# Specification Synthesis Skill

Phase 4 Specification 단계의 모든 산출물을 종합하여 개발 준비 완료 상태를 확인합니다.

## 종합 대상 스킬

```
┌─────────────────────────────────────────────────────────────┐
│                  Phase 4: Specification                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  12. PRD                  →  제품 요구사항 정의              │
│  13. User Stories         →  사용자 스토리 작성              │
│  14. Technical Req        →  기술 요구사항 정의              │
│  15. API Specification    →  API 명세 작성                  │
│  16. Data Model           →  데이터 모델 설계                │
│  17. Data Strategy        →  데이터 전략 수립                │
│                                                              │
│   ════════════════════════════════════════════════════════   │
│                                                              │
│   S4. Specification Synthesis →  개발 준비 완료 검증         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Development Readiness Checklist

```
┌─────────────────────────────────────────────────────────────┐
│              Development Readiness Score                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ✅ PRD 완성도              ████████████████████  100%      │
│   ✅ User Stories 커버리지   ████████████████░░░░   80%      │
│   ✅ 기술 스펙 명확성        ████████████████████  100%      │
│   ✅ API 설계 완료           ████████████████████  100%      │
│   ✅ 데이터 모델 완료        ████████████████░░░░   80%      │
│   ✅ 추정 가능성             ████████████████████  100%      │
│   ─────────────────────────────────────────────────────────  │
│   Overall Readiness: 93% → READY TO DEVELOP ✅               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 출력 템플릿

```markdown
# {Project Name} - Specification 종합 리포트

## Phase 4 Summary | Date: {date}

---

## 1. Executive Summary

### 개발 준비 상태
> **{READY / ALMOST READY / NOT READY}**

### 핵심 산출물 현황
| 산출물 | 완성도 | 리뷰 상태 |
|--------|--------|----------|
| PRD | {%} | ✅ Approved |
| User Stories | {%} | ✅ Approved |
| Technical Spec | {%} | 🟡 In Review |
| API Spec | {%} | ✅ Approved |
| Data Model | {%} | ✅ Approved |
| Data Strategy | {%} | ✅ Approved |

---

## 2. PRD 요약

### 제품 개요
| 항목 | 내용 |
|------|------|
| 제품명 | {product_name} |
| 버전 | {version} |
| 목표 출시일 | {target_date} |

### 핵심 기능 요약

| # | 기능 | 우선순위 | 스토리 포인트 |
|---|------|---------|--------------|
| F1 | {feature_1} | P0 | {points} |
| F2 | {feature_2} | P0 | {points} |
| F3 | {feature_3} | P1 | {points} |
| F4 | {feature_4} | P1 | {points} |
| F5 | {feature_5} | P2 | {points} |

### 요구사항 통계
- **총 요구사항**: {total}개
- **기능 요구사항 (FR)**: {fr}개
- **비기능 요구사항 (NFR)**: {nfr}개

---

## 3. User Stories 요약

### 스토리 현황

| Epic | Stories | Points | 상태 |
|------|---------|--------|------|
| {epic_1} | {n}개 | {points} | ✅ Ready |
| {epic_2} | {n}개 | {points} | ✅ Ready |
| {epic_3} | {n}개 | {points} | 🟡 Refining |

### 총 스토리 통계
```
Total Stories: {total}
├── Ready:     {ready} ({%}%)
├── Refining:  {refining} ({%}%)
└── Backlog:   {backlog} ({%}%)

Total Points: {total_points}
MVP Scope:    {mvp_points} points ({%}%)
```

### Acceptance Criteria 커버리지
- **AC 정의됨**: {defined}개 스토리
- **AC 미정의**: {undefined}개 스토리 ⚠️

---

## 4. 기술 명세 요약

### 기술 스택 확정

| 레이어 | 기술 | 버전 | 선정 이유 |
|--------|------|------|----------|
| Frontend | {tech} | {ver} | {reason} |
| Backend | {tech} | {ver} | {reason} |
| Database | {tech} | {ver} | {reason} |
| Infra | {tech} | {ver} | {reason} |

### 비기능 요구사항 (NFR)

| NFR | 목표 | 측정 방법 |
|-----|------|----------|
| 성능 | {target} | {method} |
| 가용성 | {target} | {method} |
| 보안 | {target} | {method} |
| 확장성 | {target} | {method} |

### 기술적 리스크

| 리스크 | 영향 | 대응 방안 |
|--------|------|----------|
| {risk_1} | 🔴 | {mitigation} |
| {risk_2} | 🟡 | {mitigation} |

---

## 5. API 명세 요약

### API 현황

| 도메인 | Endpoints | 상태 |
|--------|-----------|------|
| {domain_1} | {n}개 | ✅ Designed |
| {domain_2} | {n}개 | ✅ Designed |
| {domain_3} | {n}개 | 🟡 In Progress |

### 주요 API 목록

| Method | Endpoint | 설명 | 인증 |
|--------|----------|------|------|
| POST | /api/v1/users | 사용자 생성 | ❌ |
| GET | /api/v1/users/{id} | 사용자 조회 | ✅ |
| ... | ... | ... | ... |

### API 문서화 상태
- **OpenAPI Spec**: {완료/미완료}
- **예제 요청/응답**: {완료/미완료}
- **에러 코드 정의**: {완료/미완료}

---

## 6. 데이터 모델 요약

### 핵심 엔티티

| 엔티티 | 필드 수 | 관계 | 상태 |
|--------|--------|------|------|
| User | {n} | {relations} | ✅ |
| {entity_2} | {n} | {relations} | ✅ |
| {entity_3} | {n} | {relations} | 🟡 |

### ERD 요약
```
[User] ─1:N─ [Order] ─N:M─ [Product]
   │                           │
   └──1:1── [Profile]    [Category]─┘
```

### 데이터 마이그레이션
- **초기 데이터**: {required/not_required}
- **마이그레이션 스크립트**: {준비됨/준비중}

---

## 7. 데이터 전략 요약

### 데이터 수집 계획

| 데이터 | 수집 방법 | 저장소 | 보존 기간 |
|--------|----------|--------|----------|
| 사용자 행동 | Event Tracking | {storage} | {period} |
| 트랜잭션 | DB 저장 | {storage} | {period} |

### Analytics 설정
- **도구**: {analytics_tool}
- **핵심 이벤트**: {events}개 정의
- **대시보드**: {준비됨/미준비}

---

## 8. 개발 준비도 점수

### Readiness Assessment

| 영역 | 점수 | 기준 |
|------|------|------|
| PRD 완성도 | {score}/100 | 모든 기능 정의됨 |
| Story 준비도 | {score}/100 | AC 포함, 추정 완료 |
| 기술 스펙 명확성 | {score}/100 | 스택/아키텍처 확정 |
| API 설계 완료 | {score}/100 | OpenAPI 문서화 |
| 데이터 모델 완료 | {score}/100 | ERD/스키마 확정 |
| 추정 가능성 | {score}/100 | 스토리 포인트 산정 |
| **총점** | **{total}/100** | |

### 점수 해석
```
90-100: READY - 즉시 개발 시작 가능
70-89:  ALMOST READY - 소소한 보완 후 시작
50-69:  PARTIAL - 일부 영역 추가 작업 필요
0-49:   NOT READY - Specification 재작업 필요
```

---

## 9. 미해결 사항

### Open Questions

| # | 질문 | 담당 | 해결 시한 |
|---|------|------|----------|
| 1 | {question_1} | {owner} | {deadline} |
| 2 | {question_2} | {owner} | {deadline} |

### 기술적 결정 대기 (TBD)

| 항목 | 옵션 | 결정 시한 |
|------|------|----------|
| {tbd_1} | A / B | {deadline} |
| {tbd_2} | A / B / C | {deadline} |

---

## 10. Phase 5 진행 권장사항

### 진행 결정: {READY / ALMOST READY / NOT READY}

### Estimation 단계 입력사항

| 항목 | 준비 상태 | 비고 |
|------|----------|------|
| 기능 목록 | ✅ | PRD에서 추출 |
| 스토리 포인트 | ✅ | User Stories에서 추출 |
| 기술 복잡도 | ✅ | Technical Spec에서 추출 |
| 리소스 요구사항 | 🟡 | 추가 정의 필요 |

### 다음 단계 체크리스트
- [ ] 모든 Open Questions 해결
- [ ] TBD 항목 결정
- [ ] 스토리 AC 100% 정의
- [ ] API 문서화 완료

---

*Phase 4 Specification 완료 | 다음: Phase 5 Estimation*
```

## 🎯 인터랙티브 가이드

### 종합 전 확인 질문

**Q1. PRD가 승인되었나요?**
- 승인됨 → 다음 질문으로
- 미승인 → "어떤 피드백이 있었나요?"

**Q2. 모든 User Story에 AC가 정의되었나요?**
- 100% 정의됨 → 다음 질문으로
- 부분 정의 → "AC 없는 스토리 목록은?"

**Q3. API 설계가 완료되었나요?**
- OpenAPI Spec 완료 → 다음 질문으로
- 미완료 → "남은 엔드포인트는?"

### 의사결정 포인트

| 시점 | 확인 내용 | 사용자 프롬프트 |
|------|----------|----------------|
| PRD 검토 | 기능 범위 | "PRD의 기능 범위가 적절한가요?" |
| Story 검토 | 추정치 | "스토리 포인트 추정에 동의하시나요?" |
| 기술 검토 | 스택 선정 | "기술 스택 선정에 이슈가 있나요?" |
| 최종 결정 | 준비도 | "개발 시작 준비가 되었나요?" |

---

## 퀄리티 체크리스트

```
□ PRD가 승인되었는가?
□ 모든 스토리에 AC가 있는가?
□ 기술 스택이 확정되었는가?
□ API 문서화가 완료되었는가?
□ 데이터 모델이 확정되었는가?
□ 미해결 사항이 식별되었는가?
```

---

*Specification은 개발의 설계도입니다. 명확할수록 개발이 순조롭습니다.*
