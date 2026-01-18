# Legal & Contract Agent 설계 계획서

> 계약 검토부터 문서 생성까지 법률 업무를 체계적으로 지원하는 Agent

---

## 핵심 원칙

### 면책 조항 (필수)

```
⚠️ 중요 고지사항

이 Agent는 법률 전문가를 대체하지 않습니다.
모든 출력은 자격 있는 변호사의 검토가 필요합니다.
최종 법적 결정은 반드시 법률 전문가와 상의하세요.

이 도구는:
✅ 시간 절약 (초기 검토, 초안 작성)
✅ 체크포인트 제공 (놓칠 수 있는 항목 식별)
✅ 구조화된 분석 (일관된 형식)

이 도구는 아님:
❌ 법률 자문
❌ 최종 검토 대체
❌ 법적 책임 부담
```

### 퀄리티 기대치

```
"주니어 법무팀원이 1차 검토한 수준"

바로 쓸 수 있는 80% 완성도.
나머지 20%는 법률 전문가의 판단과 수정.
```

| 강한 영역 | 약한 영역 (검토 필수) |
|----------|---------------------|
| 표준 조항 식별 | 복잡한 법적 해석 |
| 누락 조항 체크 | 관할권별 차이 |
| 위험 조항 플래그 | 비즈니스 맥락 판단 |
| 문서 구조화 | 협상 전략 |
| 버전 비교 | 선례/판례 분석 |

---

## Agent 개요

### 기본 정보

```yaml
name: legal-contract-agent
category: ⚖️ 법무
description: |
  계약 검토, 위험 분석, 문서 생성을 지원하는 법무 Agent.
  NDA, 서비스 계약, 라이선스 계약 등 다양한 계약 유형을 처리합니다.
  "계약서 검토해줘", "NDA 초안 작성해줘", "위험 조항 찾아줘" 등의 요청에 반응.
```

### 지원 문서 유형

| 유형 | 영문명 | 예시 |
|------|--------|------|
| 비밀유지계약 | NDA | 상호 NDA, 일방 NDA |
| 서비스 계약 | MSA, SaaS Agreement | 서비스 이용약관, SLA |
| 라이선스 계약 | License Agreement | 소프트웨어 라이선스, IP 라이선스 |
| 고용 계약 | Employment Agreement | 근로계약서, 비경쟁 조항 |
| 투자 계약 | Investment Agreement | Term Sheet, SHA, SSA |
| 파트너십 | Partnership Agreement | JV, 제휴 계약 |
| 이용약관 | Terms of Service | 웹사이트 TOS, Privacy Policy |
| 공급 계약 | Supply Agreement | 구매 계약, 유통 계약 |

---

## 전체 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                     Legal & Contract Agent                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   사용자 요청 (문서 업로드 또는 요청)                               │
│        │                                                          │
│        ▼                                                          │
│   ┌──────────────┐                                                │
│   │Context Intake│  ◀── 계약 유형, 당사자, 목적, 관할권 파악        │
│   │(컨텍스트 수집)│                                                 │
│   └──────┬───────┘                                                │
│          │                                                        │
│          ▼                                                        │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │              Phase 1: 분석 (Analysis)                     │    │
│   │  ┌────────┐  ┌────────┐  ┌────────┐                     │    │
│   │  │Document│→ │  Risk  │→ │Summary │                     │    │
│   │  │Analysis│  │Assess. │  │Extract │                     │    │
│   │  └────────┘  └────────┘  └────────┘                     │    │
│   └─────────────────────────────────────────────────────────┘    │
│          │                                                        │
│          ▼                                                        │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │              Phase 2: 검토 (Review)                       │    │
│   │  ┌────────┐  ┌────────┐  ┌────────┐                     │    │
│   │  │Clause  │→ │Compare │→ │Compli- │                     │    │
│   │  │Library │  │Versions│  │ance    │                     │    │
│   │  └────────┘  └────────┘  └────────┘                     │    │
│   └─────────────────────────────────────────────────────────┘    │
│          │                                                        │
│          ▼                                                        │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │              Phase 3: 실행 (Execution)                    │    │
│   │  ┌────────┐  ┌────────┐  ┌────────┐                     │    │
│   │  │Redline │→ │Negoti- │→ │Document│                     │    │
│   │  │Suggest │  │ation   │  │Generate│                     │    │
│   │  └────────┘  └────────┘  └────────┘                     │    │
│   └─────────────────────────────────────────────────────────┘    │
│          │                                                        │
│          ▼                                                        │
│   ┌─────────────────────────────────────────────────────────┐    │
│   │              Phase 4: 검증 (Validation)                   │    │
│   │  ┌────────┐  ┌────────┐                                  │    │
│   │  │Checklist│→│ Review │                                  │    │
│   │  └────────┘  └────────┘                                  │    │
│   └─────────────────────────────────────────────────────────┘    │
│          │                                                        │
│          ▼                                                        │
│   최종 산출물 (검토 보고서, 수정된 계약서, 체크리스트)               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skills 구성 (12개)

### Phase 0: Context Intake

| # | Skill | 역할 | 수집 정보 |
|---|-------|------|----------|
| 0 | **legal-context** | 계약 컨텍스트 수집 | 계약 유형, 당사자, 관할권, 목적 |

### Phase 1: Analysis (분석)

| # | Skill | 역할 | 프레임워크 |
|---|-------|------|-----------|
| 1 | **document-analysis** | 계약서 구조 분석 | 조항별 분류 |
| 2 | **risk-assessment** | 위험 조항 식별 | Risk Matrix |
| 3 | **summary-extract** | 핵심 조건 추출 | Key Terms 템플릿 |

### Phase 2: Review (검토)

| # | Skill | 역할 | 프레임워크 |
|---|-------|------|-----------|
| 4 | **clause-library** | 표준 조항 비교 | Playbook 매칭 |
| 5 | **version-compare** | 버전 비교/변경 추적 | Diff 분석 |
| 6 | **compliance-check** | 규정 준수 확인 | Compliance 체크리스트 |

### Phase 3: Execution (실행)

| # | Skill | 역할 | 프레임워크 |
|---|-------|------|-----------|
| 7 | **redline-suggest** | 수정 제안 (레드라인) | 협상 포지션별 |
| 8 | **negotiation-points** | 협상 포인트 도출 | BATNA 분석 |
| 9 | **document-generate** | 계약서 초안 생성 | 템플릿 기반 |

### Phase 4: Validation (검증)

| # | Skill | 역할 | 프레임워크 |
|---|-------|------|-----------|
| 10 | **checklist** | 체크리스트 검토 | 유형별 체크리스트 |
| 11 | **final-review** | 최종 검토 리포트 | 종합 평가 |

---

## 상세 Skill 설계

### Skill 0: legal-context (컨텍스트 수집)

```yaml
name: legal-context
description: 계약 검토/생성의 기초가 되는 컨텍스트 수집
triggers:
  - "계약서 검토"
  - "법무 시작"
  - "계약 분석"
```

**수집 항목:**

```yaml
contract_info:
  type: ""                    # NDA, MSA, Employment 등
  title: ""                   # 계약서 제목
  version: ""                 # 버전 (초안, 상대방안, 최종안)
  language: ""                # 언어 (한국어, 영어, 이중언어)

parties:
  our_party:
    name: ""                  # 우리측 당사자
    role: ""                  # 제공자/수령자, 라이센서/라이센시
    position: ""              # 강한 협상력/약한 협상력/대등
  counter_party:
    name: ""                  # 상대방
    type: ""                  # 대기업, 스타트업, 개인, 정부
    known_concerns: []        # 알려진 우려사항

context:
  purpose: ""                 # 계약 목적
  background: ""              # 배경 설명
  deal_value: ""              # 계약 규모 (금액, 기간)
  urgency: ""                 # 긴급도 (높음/보통/낮음)

legal:
  jurisdiction: ""            # 관할권 (대한민국, 미국 델라웨어 등)
  governing_law: ""           # 준거법
  industry_regulations: []    # 산업 규제 (금융, 의료, 개인정보 등)

preferences:
  risk_tolerance: ""          # 위험 수용도 (보수적/중립/적극적)
  priority_terms: []          # 중요 조항 (가격, 기간, 책임제한)
  must_haves: []              # 필수 조항
  deal_breakers: []           # 절대 수용 불가 조항
```

---

### Skill 1: document-analysis (문서 분석)

```yaml
name: legal-document-analysis
description: 계약서 구조 분석 및 조항별 분류
```

**분석 프레임워크:**

```
┌─────────────────────────────────────────────────────────┐
│                    문서 구조 분석                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. 기본 정보 (Header)                                   │
│     - 계약 제목, 체결일, 당사자                           │
│                                                          │
│  2. 정의 (Definitions)                                   │
│     - 핵심 용어 정의                                     │
│                                                          │
│  3. 핵심 조항 (Core Terms)                               │
│     - 계약 목적, 범위, 대가                              │
│                                                          │
│  4. 권리/의무 (Rights & Obligations)                     │
│     - 각 당사자의 권리와 의무                            │
│                                                          │
│  5. 보호 조항 (Protective Clauses)                       │
│     - 비밀유지, 지적재산권, 손해배상                      │
│                                                          │
│  6. 일반 조항 (Boilerplate)                              │
│     - 불가항력, 통지, 분쟁해결                           │
│                                                          │
│  7. 서명 (Signature)                                     │
│     - 서명란, 날인                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**출력 예시:**

```markdown
# 문서 분석 결과

## 문서 개요
| 항목 | 내용 |
|------|------|
| 문서 유형 | 상호 비밀유지계약 (Mutual NDA) |
| 페이지 수 | 8 |
| 조항 수 | 15 |
| 언어 | 한국어 |

## 조항 구조
| 조항 번호 | 제목 | 카테고리 | 페이지 |
|----------|------|----------|--------|
| 제1조 | 목적 | Core Terms | 1 |
| 제2조 | 정의 | Definitions | 1-2 |
| 제3조 | 비밀정보의 범위 | Core Terms | 2 |
| ... | ... | ... | ... |

## 누락 가능성 있는 조항
- [ ] 비밀유지 기간 명시 없음
- [ ] 분쟁 해결 조항 불명확
```

---

### Skill 2: risk-assessment (위험 평가)

```yaml
name: legal-risk-assessment
description: 위험 조항 식별 및 심각도 평가
```

**Risk Matrix:**

```
                        영향도 (Impact)
                   낮음      보통      높음
              ┌─────────┬─────────┬─────────┐
         높음 │  🟡     │  🟠     │  🔴     │
   발생       │ Medium  │  High   │ Critical│
   가능성     ├─────────┼─────────┼─────────┤
   (Likeli-  보통 │  🟢     │  🟡     │  🟠     │
   hood)      │  Low    │ Medium  │  High   │
              ├─────────┼─────────┼─────────┤
         낮음 │  🟢     │  🟢     │  🟡     │
              │  Low    │  Low    │ Medium  │
              └─────────┴─────────┴─────────┘
```

**위험 조항 카테고리:**

| 카테고리 | 위험 요소 | 예시 |
|----------|----------|------|
| **책임** | 무제한 손해배상 | "모든 손해에 대해 전액 배상" |
| **기간** | 자동 갱신 | "이의 없으면 자동 1년 연장" |
| **해지** | 일방적 해지권 | "상대방은 언제든 해지 가능" |
| **지적재산** | IP 양도 | "결과물 IP 전부 양도" |
| **비밀유지** | 과도한 범위 | "모든 정보가 비밀정보" |
| **경쟁금지** | 과도한 기간/범위 | "5년간 동종업계 금지" |
| **관할** | 불리한 관할 | "상대방 소재지 관할" |
| **면책** | 과도한 면책 | "상대방 과실에도 면책" |

**출력 템플릿:**

```markdown
# 위험 평가 보고서

## Risk Summary

| 심각도 | 개수 | 즉시 조치 필요 |
|--------|------|---------------|
| 🔴 Critical | 2 | ✓ |
| 🟠 High | 3 | ✓ |
| 🟡 Medium | 5 | - |
| 🟢 Low | 8 | - |

## Critical Risks (🔴)

### R-001: 무제한 손해배상
| 항목 | 내용 |
|------|------|
| 조항 | 제12조 3항 |
| 원문 | "을은 갑에게 발생한 일체의 손해를 배상한다" |
| 위험 | 손해배상 상한 없음, 간접손해 포함 |
| 권고 | 직접손해로 제한, 상한금액 설정 |
| 수정안 | "을의 배상책임은 직접손해에 한하며, 총 계약금액을 상한으로 한다" |
```

---

### Skill 3: summary-extract (요약 추출)

```yaml
name: legal-summary-extract
description: 핵심 계약 조건 추출 및 요약
```

**Key Terms Template:**

```markdown
# 계약 핵심 조건 요약

## 1. 기본 정보
| 항목 | 내용 |
|------|------|
| 계약 제목 | |
| 계약일 | |
| 효력 발생일 | |
| 당사자 (갑) | |
| 당사자 (을) | |

## 2. 거래 조건
| 항목 | 내용 |
|------|------|
| 계약 목적/범위 | |
| 계약 기간 | |
| 대가/가격 | |
| 지급 조건 | |

## 3. 핵심 권리/의무
### 갑의 권리
-
### 갑의 의무
-
### 을의 권리
-
### 을의 의무
-

## 4. 보호 조항
| 항목 | 내용 |
|------|------|
| 비밀유지 기간 | |
| 손해배상 상한 | |
| 지적재산권 귀속 | |
| 경쟁금지 | |

## 5. 계약 종료
| 항목 | 내용 |
|------|------|
| 해지 사유 | |
| 해지 통지 기간 | |
| 자동 갱신 여부 | |
| 종료 후 의무 | |

## 6. 분쟁 해결
| 항목 | 내용 |
|------|------|
| 준거법 | |
| 관할 법원 | |
| 중재 조항 | |
```

---

### Skill 4: clause-library (조항 라이브러리)

```yaml
name: legal-clause-library
description: 표준 조항 vs 검토 대상 조항 비교
```

**Playbook 구조:**

```yaml
clause_categories:
  - name: "손해배상 (Indemnification)"
    our_position:
      conservative: "직접손해, 계약금액 상한"
      moderate: "예견가능 손해, 2x 계약금액"
      aggressive: "고의/중과실만"

    red_flags:
      - "무제한 배상"
      - "간접손해/결과적손해 포함"
      - "제3자 청구 전액 부담"

    fallback_language: |
      "당사자의 배상책임은 직접손해에 한하며,
      배상 총액은 계약금액을 상한으로 한다.
      단, 고의 또는 중과실의 경우 이 제한을 적용하지 않는다."

  - name: "비밀유지 (Confidentiality)"
    our_position:
      conservative: "3년, 좁은 범위"
      moderate: "5년, 표준 범위"
      aggressive: "무기한, 넓은 범위"

    red_flags:
      - "무기한 유지"
      - "모든 정보 = 비밀정보"
      - "파기 증명 요구"
```

---

### Skill 5: version-compare (버전 비교)

```yaml
name: legal-version-compare
description: 계약서 버전 간 변경사항 추적
```

**출력 예시:**

```markdown
# 버전 비교 결과

## 비교 대상
| 항목 | Version A | Version B |
|------|-----------|-----------|
| 파일명 | NDA_초안.docx | NDA_상대방수정.docx |
| 날짜 | 2024-01-10 | 2024-01-15 |

## 변경 요약
| 유형 | 개수 |
|------|------|
| 추가 | 3 |
| 삭제 | 1 |
| 수정 | 7 |

## 중요 변경사항 (검토 필요)

### 🔴 제8조 손해배상
**Before:**
> "배상 상한은 계약금액으로 한다"

**After:**
> "을은 갑에게 발생한 모든 손해를 배상한다"

**영향**: 무제한 배상 책임 → 거부 권고

### 🟠 제3조 비밀유지 기간
**Before:**
> "계약 종료 후 3년간"

**After:**
> "계약 종료 후 5년간"

**영향**: 의무 기간 연장 → 협상 고려
```

---

### Skill 6: compliance-check (규정 준수)

```yaml
name: legal-compliance-check
description: 관련 법규 및 규정 준수 여부 확인
```

**체크리스트 (예: 개인정보보호):**

```markdown
# 개인정보보호 규정 준수 체크리스트

## 개인정보보호법 (PIPA)
- [ ] 개인정보 수집 목적 명시
- [ ] 수집 항목 최소화
- [ ] 보유 기간 명시
- [ ] 제3자 제공 동의
- [ ] 위탁 사항 명시
- [ ] 파기 절차 규정

## GDPR (해당 시)
- [ ] 처리 법적 근거 명시
- [ ] 정보주체 권리 보장
- [ ] DPA 요건 충족
- [ ] 국외 이전 조항

## 산업별 규제
### 금융
- [ ] 금융실명법 준수
- [ ] 신용정보법 준수

### 의료
- [ ] 의료법 준수
- [ ] 민감정보 처리 동의
```

---

### Skill 7: redline-suggest (수정 제안)

```yaml
name: legal-redline-suggest
description: 조항별 수정안 제시 (레드라인)
```

**수정 제안 구조:**

```markdown
# 수정 제안서 (Redline Suggestions)

## 조항별 수정안

### 제12조 손해배상

**현재 조항:**
> 을은 본 계약 위반으로 인하여 갑에게 발생한 일체의 손해를 배상한다.

**문제점:**
- 배상 범위 무제한 (간접손해 포함)
- 배상 상한 없음

**수정안 (Option A - 보수적):**
> 을의 손해배상책임은 직접손해에 한하며, 그 총액은 을이 본 계약에 따라 수령한 금액을 상한으로 한다. ~~일체의 손해를 배상한다.~~

**수정안 (Option B - 균형적):**
> 을은 본 계약 위반으로 인하여 갑에게 발생한 통상손해 및 특별손해 중 예견가능한 손해를 배상하되, 그 총액은 계약금액의 2배를 상한으로 한다.

**협상 포인트:**
- 최소 목표: 직접손해 제한
- 희망 목표: 계약금액 상한
- 양보 가능: 2x 계약금액까지
```

---

### Skill 8: negotiation-points (협상 포인트)

```yaml
name: legal-negotiation-points
description: 협상 전략 및 포인트 도출
```

**BATNA 분석:**

```markdown
# 협상 전략 가이드

## 우리측 분석

### BATNA (Best Alternative)
- 대안이 있는가?
- 계약 불성립 시 영향?

### 협상력 평가
| 요소 | 점수 (1-5) | 근거 |
|------|----------|------|
| 시장 대안 | 3 | 다른 공급자 2곳 존재 |
| 긴급도 | 2 | 상대방이 더 급함 |
| 거래 규모 | 4 | 우리가 큰 고객 |
| **총점** | **9/15** | 중간 협상력 |

## 협상 우선순위

### 🔴 Must Have (필수)
1. 손해배상 상한 설정
2. 해지 통지 기간 30일

### 🟠 Should Have (중요)
3. 지적재산권 공동 소유
4. 자동갱신 삭제

### 🟢 Nice to Have (희망)
5. 관할 우리측 소재지
6. 중재 조항 추가

## 양보 전략

| Give (양보 가능) | Get (획득 목표) |
|-----------------|----------------|
| 비밀유지 5년 수용 | 손해배상 상한 획득 |
| 경쟁금지 1년 수용 | IP 공동소유 획득 |
```

---

### Skill 9: document-generate (문서 생성)

```yaml
name: legal-document-generate
description: 계약서 초안 생성
```

**지원 템플릿:**

| 유형 | 한글 | 영문 | 이중언어 |
|------|------|------|----------|
| NDA (상호) | ✅ | ✅ | ✅ |
| NDA (일방) | ✅ | ✅ | ✅ |
| 서비스 계약 | ✅ | ✅ | - |
| 라이선스 계약 | ✅ | ✅ | - |
| 업무위탁계약 | ✅ | - | - |
| 개인정보처리위탁 | ✅ | - | - |

---

### Skill 10: checklist (체크리스트)

```yaml
name: legal-checklist
description: 계약 유형별 체크리스트 검토
```

**NDA 체크리스트 예시:**

```markdown
# NDA 체크리스트

## 필수 항목
- [ ] 당사자 정보 정확
- [ ] 비밀정보 범위 정의
- [ ] 비밀유지 기간 명시
- [ ] 허용되는 공개 범위
- [ ] 반환/파기 조항

## 권장 항목
- [ ] 잔존 조항 (Residual Knowledge)
- [ ] 강제 공개 예외 (법원 명령 등)
- [ ] 직원 비밀유지 의무
- [ ] 손해배상 조항
- [ ] 분쟁해결 조항

## 주의 항목
- [ ] 비밀정보 범위가 과도하지 않은지
- [ ] 기간이 합리적인지 (보통 3-5년)
- [ ] 일방적으로 불리한 조항 없는지
```

---

### Skill 11: final-review (최종 검토)

```yaml
name: legal-final-review
description: 종합 검토 및 서명 전 최종 확인
```

**최종 검토 보고서:**

```markdown
# 최종 검토 보고서

## 계약 개요
| 항목 | 내용 |
|------|------|
| 계약명 | |
| 버전 | Final v3 |
| 검토 완료일 | |

## 검토 결과 요약

| 영역 | 상태 | 이슈 |
|------|------|------|
| 문서 완결성 | 🟢 | - |
| 위험 조항 | 🟡 | 2개 Minor |
| 규정 준수 | 🟢 | - |
| 형식 요건 | 🟢 | - |

## 서명 전 확인사항

### ✅ 완료됨
- [x] 당사자 정보 확인
- [x] 금액/기간 숫자 확인
- [x] 핵심 조건 협상 완료
- [x] 법무팀 검토 완료

### ⚠️ 주의사항
- 제8조 손해배상: 상한 2배로 합의됨 (기록 보관)
- 제12조 분쟁해결: 중재 조항 추가됨

## 승인

| 역할 | 이름 | 서명 | 날짜 |
|------|------|------|------|
| 법무 | | ⬜ | |
| 사업 | | ⬜ | |
| 경영진 | | ⬜ | |

---
*⚠️ 본 검토는 참고용이며, 최종 법적 자문은 자격 있는 변호사와 상의하세요.*
```

---

## 출력물 구조

```
workspace/work-legal/
│
└── {project-name}/
    │
    ├── context/
    │   └── {project}-context.md          # 계약 컨텍스트
    │
    ├── analysis/
    │   ├── {project}-document-analysis.md # 문서 분석
    │   ├── {project}-risk-assessment.md   # 위험 평가
    │   └── {project}-summary.md           # 핵심 조건 요약
    │
    ├── review/
    │   ├── {project}-clause-comparison.md # 조항 비교
    │   ├── {project}-version-diff.md      # 버전 비교
    │   └── {project}-compliance.md        # 규정 준수
    │
    ├── execution/
    │   ├── {project}-redline.md           # 수정 제안
    │   ├── {project}-negotiation.md       # 협상 포인트
    │   └── {project}-draft.md             # 생성된 초안
    │
    ├── checklist/
    │   └── {project}-checklist.md         # 체크리스트
    │
    └── reports/
        └── {project}-final-review.md      # 최종 검토 보고서
```

---

## 사용 시나리오

### 시나리오 1: NDA 검토

```
사용자: "상대방이 보낸 NDA 검토해줘. 우리는 협상력이 약해."

Agent 실행:
0. [Context] 계약 유형, 당사자, 협상 포지션 파악
1. [Analysis] 문서 구조 분석
2. [Risk] 위험 조항 식별 → 비밀유지 무기한, 손해배상 무제한
3. [Summary] 핵심 조건 추출
4. [Clause] 표준 NDA 대비 비교
7. [Redline] 수정안 3가지 옵션 제시
8. [Negotiation] 양보/획득 전략
10. [Checklist] NDA 체크리스트
11. [Review] 최종 리포트
```

### 시나리오 2: 계약서 초안 작성

```
사용자: "SaaS 서비스 이용약관 만들어줘"

Agent 실행:
0. [Context] 서비스 내용, 타겟 고객, 가격 구조
6. [Compliance] 전자상거래법, 개인정보보호법 체크
9. [Generate] 이용약관 초안 생성
10. [Checklist] 이용약관 필수 항목 확인
11. [Review] 검토 및 수정 권고
```

### 시나리오 3: 버전 비교

```
사용자: "우리 초안이랑 상대방 수정안 비교해줘"

Agent 실행:
0. [Context] 두 버전 정보
5. [Compare] 변경사항 추적
2. [Risk] 변경된 조항 위험 평가
7. [Redline] 재수정 제안
8. [Negotiation] 협상 대응 전략
```

---

## 명령어 가이드

### 전체 프로세스

```
"계약서 검토해줘"
"NDA 분석해줘"
"이 계약 위험한 부분 찾아줘"
```

### 개별 Skill 호출

```
/legal-context       # 컨텍스트 수집
/legal-analyze       # 문서 분석
/legal-risk          # 위험 평가
/legal-summary       # 요약 추출
/legal-clause        # 조항 비교
/legal-compare       # 버전 비교
/legal-compliance    # 규정 준수
/legal-redline       # 수정 제안
/legal-negotiate     # 협상 포인트
/legal-generate      # 문서 생성
/legal-checklist     # 체크리스트
/legal-review        # 최종 검토
```

---

## 다음 단계: 구현 계획

### Phase 1: Core Skills (우선 구현)
1. `legal-context` - 컨텍스트 수집
2. `legal-risk-assessment` - 위험 평가
3. `legal-summary-extract` - 요약 추출
4. `legal-final-review` - 최종 검토

### Phase 2: Analysis Skills
5. `legal-document-analysis` - 문서 분석
6. `legal-clause-library` - 조항 라이브러리
7. `legal-checklist` - 체크리스트

### Phase 3: Execution Skills
8. `legal-redline-suggest` - 수정 제안
9. `legal-negotiation-points` - 협상 포인트
10. `legal-document-generate` - 문서 생성

### Phase 4: Advanced Skills
11. `legal-version-compare` - 버전 비교
12. `legal-compliance-check` - 규정 준수

---

## 참고 자료

### 법률 AI 사례
- Harvey AI (계약 분석, 실사)
- Thomson Reuters CoCounsel
- Robin AI (계약 인텔리전스)

### 프레임워크
- IRAC (Issue, Rule, Application, Conclusion)
- Contract Lifecycle Management
- Risk Matrix (Impact x Likelihood)

---

*이 계획서를 기반으로 legal-contract-agent를 구현합니다.*
*최종 결정은 항상 자격 있는 법률 전문가와 상의하세요.*
