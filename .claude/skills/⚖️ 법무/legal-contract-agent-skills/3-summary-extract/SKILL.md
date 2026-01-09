---
name: legal-summary-extract
description: |
  핵심 계약 조건 추출 및 요약.
  경영진/비전문가도 이해할 수 있는 형태로 핵심 사항을 정리합니다.
triggers:
  - "계약 요약"
  - "핵심 조건"
  - "주요 내용"
  - "요약해줘"
  - "Key Terms"
input:
  - 계약서 텍스트
  - 컨텍스트 문서 (권장)
output:
  - analysis/{project}-summary.md
---

# Summary Extract Skill

계약서의 핵심 조건을 추출하여 이해하기 쉽게 요약합니다.

## 목적

```
전체 계약서 (20페이지)
      │
      ▼
핵심 요약 (2페이지)
      │
      ▼
경영진/비전문가도 빠르게 이해
```

## 추출 항목

### 1. 기본 정보

```yaml
basic_info:
  title: ""           # 계약 제목
  type: ""            # 계약 유형
  date: ""            # 체결일/효력발생일
  parties:
    - name: ""        # 당사자 1
      role: ""        # 역할
    - name: ""        # 당사자 2
      role: ""        # 역할
```

### 2. 거래 조건 (Commercial Terms)

```yaml
commercial_terms:
  purpose: ""                 # 계약 목적
  scope: ""                   # 범위
  deliverables: []            # 결과물/서비스
  price:
    amount: ""                # 금액
    currency: ""              # 통화
    structure: ""             # 구조 (일시불, 분할, 성과급)
  payment:
    terms: ""                 # 지급 조건
    schedule: ""              # 지급 일정
    method: ""                # 지급 방법
```

### 3. 기간 및 갱신

```yaml
term:
  effective_date: ""          # 효력 발생일
  initial_term: ""            # 초기 기간
  renewal:
    auto: true/false          # 자동 갱신 여부
    notice_period: ""         # 갱신 거부 통지 기간
    renewal_term: ""          # 갱신 기간
  termination:
    for_cause: []             # 유책 해지 사유
    for_convenience: ""       # 임의 해지 조건
    notice_period: ""         # 해지 통지 기간
```

### 4. 핵심 의무

```yaml
obligations:
  party_a:                    # 갑의 의무
    - ""
    - ""
  party_b:                    # 을의 의무
    - ""
    - ""
```

### 5. 보호 조항

```yaml
protective_clauses:
  confidentiality:
    scope: ""                 # 비밀정보 범위
    duration: ""              # 유지 기간
    exceptions: []            # 예외

  ip:
    existing: ""              # 기존 IP 처리
    new: ""                   # 신규 IP 귀속
    license: ""               # 라이선스 범위

  liability:
    cap: ""                   # 책임 상한
    exclusions: []            # 면책 사항
    indemnity: ""             # 손해배상 범위
```

### 6. 분쟁해결

```yaml
dispute:
  governing_law: ""           # 준거법
  jurisdiction: ""            # 관할
  arbitration: ""             # 중재 조항
  mediation: ""               # 조정 조항
```

## 요약 수준

### Level 1: Executive Summary (1분 읽기)

```
핵심만 3-5줄로 요약
- 무엇을 위한 계약?
- 얼마에?
- 언제까지?
- 가장 중요한 조건은?
```

### Level 2: Key Terms Summary (5분 읽기)

```
주요 조건 표 형식으로 정리
- 거래 조건
- 기간/해지
- 책임/배상
- 주의사항
```

### Level 3: Detailed Summary (15분 읽기)

```
전체 조항을 카테고리별로 요약
- 각 조항의 핵심 내용
- 특이사항/주의사항
- 누락된 항목
```

## 워크플로우

```
1. 계약서 전체 스캔
      │
      ▼
2. 핵심 항목 추출
      │
      ├─ 기본 정보
      ├─ 거래 조건
      ├─ 기간/갱신
      ├─ 의무 사항
      ├─ 보호 조항
      ├─ 분쟁해결
      │
      ▼
3. 수치/날짜 정확성 확인
      │
      ▼
4. 특이사항/주의점 표시
      │
      ▼
5. 요약 문서 생성
   → workspace/work-legal/{project}/analysis/{project}-summary.md
```

## 출력 템플릿

```markdown
# {Project Name} 계약 요약

## Executive Summary

> **한 줄 요약**: {one_line_summary}

| 핵심 항목 | 내용 |
|----------|------|
| 계약 유형 | {type} |
| 상대방 | {counter_party} |
| 계약 금액 | {amount} |
| 계약 기간 | {term} |
| 핵심 리스크 | {key_risk} |

### 주요 판단 포인트

✅ **긍정적**: {positive_points}

⚠️ **주의 필요**: {caution_points}

❌ **문제 사항**: {problem_points}

---

## Key Terms Summary

### 1. 기본 정보

| 항목 | 내용 |
|------|------|
| 계약 제목 | {title} |
| 계약 유형 | {type} |
| 체결일 | {date} |
| 효력 발생일 | {effective_date} |

### 당사자

| 역할 | 명칭 | 설명 |
|------|------|------|
| 갑 | {party_a} | {description_a} |
| 을 | {party_b} | {description_b} |

---

### 2. 거래 조건

| 항목 | 내용 |
|------|------|
| **목적** | {purpose} |
| **범위** | {scope} |
| **결과물** | {deliverables} |

### 대가

| 항목 | 내용 |
|------|------|
| 총 금액 | {total_amount} |
| 지급 구조 | {payment_structure} |
| 지급 일정 | {payment_schedule} |
| 지급 조건 | {payment_terms} |

---

### 3. 계약 기간

| 항목 | 내용 |
|------|------|
| 초기 기간 | {initial_term} |
| 자동 갱신 | {auto_renewal} |
| 갱신 거부 통지 | {renewal_notice} |

### 해지 조건

| 유형 | 조건 | 통지 기간 |
|------|------|----------|
| 유책 해지 | {for_cause} | {notice_1} |
| 임의 해지 | {for_convenience} | {notice_2} |

---

### 4. 핵심 의무

#### 갑 ({party_a})의 의무

1. {obligation_a_1}
2. {obligation_a_2}
3. {obligation_a_3}

#### 을 ({party_b})의 의무

1. {obligation_b_1}
2. {obligation_b_2}
3. {obligation_b_3}

---

### 5. 보호 조항

#### 비밀유지

| 항목 | 내용 |
|------|------|
| 범위 | {conf_scope} |
| 기간 | {conf_duration} |
| 예외 | {conf_exceptions} |

#### 지적재산권

| 항목 | 내용 |
|------|------|
| 기존 IP | {existing_ip} |
| 신규 IP | {new_ip} |
| 라이선스 | {license} |

#### 책임제한

| 항목 | 내용 |
|------|------|
| 책임 상한 | {liability_cap} |
| 면책 사항 | {exclusions} |
| 손해배상 | {indemnity} |

---

### 6. 분쟁해결

| 항목 | 내용 |
|------|------|
| 준거법 | {governing_law} |
| 관할 법원 | {jurisdiction} |
| 중재 조항 | {arbitration} |

---

## 중요 일자 캘린더

| 날짜 | 이벤트 | 비고 |
|------|--------|------|
| {date_1} | 계약 체결 | |
| {date_2} | 효력 발생 | |
| {date_3} | 1차 지급 | {amount_1} |
| {date_4} | 갱신 거부 마감 | 갱신 원치 않으면 통지 필요 |
| {date_5} | 계약 만료 | |

---

## 숫자로 보는 계약

| 항목 | 수치 | 비고 |
|------|------|------|
| 총 계약금액 | {amount} | |
| 계약 기간 | {term} | |
| 손해배상 상한 | {cap} | 계약금액의 X배 |
| 비밀유지 기간 | {conf_term} | 종료 후 |
| 해지 통지 기간 | {notice} | |

---

## 특이사항 & 주의점

### ⚠️ 반드시 확인

1. **{caution_1}**
   - 위치: 제X조
   - 내용: {detail_1}

2. **{caution_2}**
   - 위치: 제Y조
   - 내용: {detail_2}

### 📝 참고사항

- {note_1}
- {note_2}

---

## 비교표 (표준 조건 대비)

| 항목 | 이 계약 | 업계 표준 | 차이 |
|------|---------|----------|------|
| 손해배상 상한 | {this} | 계약금액 1-2배 | {diff} |
| 비밀유지 기간 | {this} | 3-5년 | {diff} |
| 해지 통지 | {this} | 30-90일 | {diff} |

---

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│            {CONTRACT_TITLE}                  │
├─────────────────────────────────────────────┤
│                                              │
│  상대방: {counter_party}                     │
│  금  액: {amount}                            │
│  기  간: {term}                              │
│                                              │
│  핵심 포인트:                                 │
│  • {key_point_1}                             │
│  • {key_point_2}                             │
│  • {key_point_3}                             │
│                                              │
│  주의사항:                                    │
│  ⚠️ {warning}                                │
│                                              │
└─────────────────────────────────────────────┘
```

---

⚠️ 면책: 이 요약은 참고용이며, 전체 계약서 검토를 대체하지 않습니다.
최종 결정은 법률 전문가와 상의하세요.
```

## 요약 시 주의사항

### 정확성 우선

```yaml
accuracy_rules:
  - 금액, 날짜, 기간은 반드시 정확히
  - 불확실한 경우 "확인 필요" 표시
  - 해석이 필요한 경우 원문 병기
  - 누락된 정보는 "명시되지 않음" 표시
```

### 중립성 유지

```yaml
neutrality_rules:
  - 사실 기반 요약
  - 주관적 판단은 별도 표시
  - 양 당사자 관점 균형
```

### 명확성 확보

```yaml
clarity_rules:
  - 전문 용어는 괄호로 설명
  - 복잡한 조건은 단순화
  - 표와 도식 활용
```

## 다음 스킬 연결

요약 완료 후:

1. **위험 평가** → Risk Assessment Skill
2. **조항 비교** → Clause Library Skill
3. **협상 포인트** → Negotiation Points Skill

---

*좋은 요약은 핵심을 놓치지 않으면서 이해하기 쉽게 전달합니다.*

⚠️ 면책: 이 요약은 참고용이며, 최종 결정은 법률 전문가와 상의하세요.
