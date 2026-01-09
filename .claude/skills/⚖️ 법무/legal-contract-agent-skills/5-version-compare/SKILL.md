---
name: legal-version-compare
description: |
  계약서 버전간 변경사항 비교 분석.
  초안과 수정본, 또는 협상 과정의 여러 버전을 비교합니다.
triggers:
  - "버전 비교"
  - "변경사항"
  - "수정 내역"
  - "Version Compare"
  - "레드라인 비교"
input:
  - 이전 버전 계약서
  - 현재 버전 계약서
output:
  - review/{project}-version-diff.md
---

# Version Compare Skill

계약서의 여러 버전 간 변경사항을 식별하고 분석합니다.

## 비교 유형

### 1. 양측 비교 (Two-Way)

```
버전 A (초안)  ←→  버전 B (수정본)
```

- 초안 vs 최종본
- 우리 제안 vs 상대방 수정
- Before vs After

### 2. 다중 비교 (Multi-Way)

```
버전 1 → 버전 2 → 버전 3 → 최종본
   │         │         │
   └────┬────┴────┬────┘
        변경 이력 추적
```

- 협상 히스토리 전체 추적
- 각 라운드별 변경사항

---

## 변경 유형 분류

### 변경 카테고리

```yaml
change_types:
  addition:       # 신규 추가
    symbol: "➕"
    color: green

  deletion:       # 삭제
    symbol: "➖"
    color: red

  modification:   # 수정
    symbol: "✏️"
    color: yellow

  moved:          # 위치 이동
    symbol: "↔️"
    color: blue

  formatting:     # 형식 변경
    symbol: "📝"
    color: gray
```

### 변경 심각도

```yaml
severity_levels:
  critical:       # 핵심 조건 변경
    symbol: "🔴"
    examples:
      - "책임 상한 삭제"
      - "손해배상 범위 확대"
      - "해지권 제한"

  significant:    # 중요 변경
    symbol: "🟠"
    examples:
      - "기간 변경"
      - "지급 조건 변경"
      - "비밀유지 범위 변경"

  minor:          # 경미한 변경
    symbol: "🟡"
    examples:
      - "문구 표현 변경"
      - "조항 번호 변경"
      - "오탈자 수정"

  formatting:     # 형식적 변경
    symbol: "⚪"
    examples:
      - "단락 분리"
      - "번호 체계 변경"
      - "용어 통일"
```

---

## 비교 영역

### 1. 조항별 비교

```yaml
clause_comparison:
  - clause_number: "제X조"
    title: "{clause_title}"
    version_a: "{text_a}"
    version_b: "{text_b}"
    change_type: "modification"
    severity: "significant"
    analysis: "{what_changed_and_impact}"
```

### 2. 핵심 조건 비교

```yaml
key_terms_comparison:
  contract_amount:
    version_a: "1억원"
    version_b: "1억 2천만원"
    change: "+20%"

  contract_term:
    version_a: "1년"
    version_b: "2년"
    change: "기간 연장"

  liability_cap:
    version_a: "계약금액 2배"
    version_b: "계약금액 1배"
    change: "상한 축소"
```

### 3. 숫자/날짜 비교

```yaml
numeric_comparison:
  - item: "계약 금액"
    version_a: "100,000,000원"
    version_b: "120,000,000원"
    difference: "+20,000,000원 (+20%)"

  - item: "해지 통지 기간"
    version_a: "30일"
    version_b: "14일"
    difference: "-16일 (-53%)"
```

---

## 워크플로우

```
1. 버전 입력
      │
      ├─ 버전 A 로드
      ├─ 버전 B 로드
      │
      ▼
2. 구조 분석
      │
      ├─ 조항 매핑
      ├─ 번호 체계 정렬
      │
      ▼
3. 텍스트 비교
      │
      ├─ Diff 생성
      ├─ 변경 유형 분류
      │
      ▼
4. 변경 분석
      │
      ├─ 심각도 평가
      ├─ 영향도 분석
      │
      ▼
5. 리포트 생성
   → workspace/work-legal/{project}/review/{project}-version-diff.md
```

---

## 출력 템플릿

```markdown
# {Project Name} 버전 비교 분석

## 비교 개요

| 항목 | 내용 |
|------|------|
| 버전 A | {version_a_name} ({date_a}) |
| 버전 B | {version_b_name} ({date_b}) |
| 비교 일자 | {comparison_date} |
| 변경 라운드 | {round_number} |

---

## 변경 요약

### 변경 통계

| 유형 | 개수 | 비율 |
|------|------|------|
| ➕ 추가 | {n} | {%} |
| ➖ 삭제 | {n} | {%} |
| ✏️ 수정 | {n} | {%} |
| ↔️ 이동 | {n} | {%} |
| **총계** | **{total}** | 100% |

### 심각도별 분포

| 심각도 | 개수 | 주요 변경 |
|--------|------|----------|
| 🔴 Critical | {n} | {summary} |
| 🟠 Significant | {n} | {summary} |
| 🟡 Minor | {n} | {summary} |
| ⚪ Formatting | {n} | - |

### 협상 방향 분석

| 분석 항목 | 결과 |
|----------|------|
| 우리측 유리 변경 | {n}건 |
| 우리측 불리 변경 | {n}건 |
| 중립적 변경 | {n}건 |
| **순 평가** | {net_favorable/unfavorable} |

---

## 🔴 Critical Changes

### C-001: {change_title}

| 항목 | 내용 |
|------|------|
| **위치** | 제{X}조 {Y}항 |
| **변경 유형** | {addition/deletion/modification} |

**이전 (버전 A):**
> "{text_a}"

**이후 (버전 B):**
> "{text_b}"

**변경 분석:**
{analysis}

**영향:**
- {impact_1}
- {impact_2}

**권고:**
{recommendation}

---

### C-002: {change_title}

(동일 형식 반복)

---

## 🟠 Significant Changes

### S-001: {change_title}

| 항목 | 버전 A | 버전 B | 영향 |
|------|--------|--------|------|
| 위치 | 제{X}조 | 제{Y}조 | {impact} |

**변경 내용:**
- Before: {text_a}
- After: {text_b}
- 분석: {analysis}

---

## 🟡 Minor Changes

| ID | 위치 | 변경 유형 | 내용 | 비고 |
|----|------|----------|------|------|
| M-001 | 제{X}조 | 수정 | {summary} | {note} |
| M-002 | 제{Y}조 | 추가 | {summary} | {note} |

---

## ⚪ Formatting Changes

| ID | 위치 | 변경 내용 |
|----|------|----------|
| F-001 | 제{X}조 | 단락 분리 |
| F-002 | 전체 | 용어 통일 ("갑" → "당사자 1") |

---

## 핵심 조건 비교표

### 금전적 조건

| 항목 | 버전 A | 버전 B | 변경 | 평가 |
|------|--------|--------|------|------|
| 계약 금액 | {a} | {b} | {diff} | {status} |
| 지급 조건 | {a} | {b} | {diff} | {status} |
| 손해배상 상한 | {a} | {b} | {diff} | {status} |
| 위약금 | {a} | {b} | {diff} | {status} |

### 기간 관련

| 항목 | 버전 A | 버전 B | 변경 | 평가 |
|------|--------|--------|------|------|
| 계약 기간 | {a} | {b} | {diff} | {status} |
| 자동 갱신 | {a} | {b} | {diff} | {status} |
| 해지 통지 | {a} | {b} | {diff} | {status} |
| 비밀유지 기간 | {a} | {b} | {diff} | {status} |

### 권리/의무

| 항목 | 버전 A | 버전 B | 변경 | 평가 |
|------|--------|--------|------|------|
| IP 귀속 | {a} | {b} | {diff} | {status} |
| 경쟁금지 | {a} | {b} | {diff} | {status} |
| 준거법 | {a} | {b} | {diff} | {status} |
| 관할 | {a} | {b} | {diff} | {status} |

---

## 조항별 상세 Diff

### 제1조 (목적)

```diff
- 본 계약은 갑이 을에게 소프트웨어 개발을 위탁하고,
+ 본 계약은 갑이 을에게 소프트웨어 개발 및 유지보수를 위탁하고,
  을이 이를 수행함에 있어 필요한 사항을 정함을 목적으로 한다.
```

**분석:** 범위에 "유지보수" 추가. 범위 확대로 을의 의무 증가.

---

### 제12조 (손해배상)

```diff
  을은 본 계약 위반으로 인하여 갑에게 발생한
- 직접 손해를 배상한다. 단, 손해배상의 총액은 계약금액을 초과하지 않는다.
+ 모든 손해를 배상한다.
```

**분석:** 🔴 Critical - 손해배상 범위가 "직접 손해"에서 "모든 손해"로 확대되고, 상한 조항이 삭제됨.

---

(조항별 반복)

---

## 변경 이력 타임라인

```
버전 1 (초안)           버전 2 (1차 협상)        버전 3 (2차 협상)        최종본
─────────────────────────────────────────────────────────────────────────────
2024.01.05              2024.01.15              2024.01.25              2024.02.01
│                       │                       │                       │
├─ 초안 작성            ├─ 5개 조항 수정        ├─ 3개 조항 수정        ├─ 확정
│                       │  - 책임 상한 협의     │  - 해지 조건 조정     │
│                       │  - IP 조항 수정       │  - 비밀유지 기간 합의 │
│                       │  - 기간 연장          │                       │
```

---

## 협상 포지션 분석

### 상대방 우선순위 추정

변경 패턴 분석 결과:

| 우선순위 | 조항 | 근거 |
|----------|------|------|
| 1순위 | 책임제한 | 상한 삭제 시도 |
| 2순위 | IP 귀속 | 전면 양도 요구 |
| 3순위 | 해지권 | 일방 해지 추가 |

### 양보-요구 패턴

| 상대방 양보 | 상대방 요구 |
|------------|------------|
| 기간 연장 | 책임 상한 삭제 |
| 지급 조건 완화 | IP 전면 양도 |

---

## 다음 협상 권고

### 수용 가능

| 변경 | 수용 근거 |
|------|----------|
| {change_1} | {rationale} |

### 수정 필요

| 변경 | 대응 방안 |
|------|----------|
| {change_2} | {counter_proposal} |

### 거부 권고

| 변경 | 거부 근거 |
|------|----------|
| {change_3} | {rationale} |

---

## 주의사항

### ⚠️ 주의 필요 변경

1. **{change_1}**
   - 변경 내용: {detail}
   - 리스크: {risk}
   - 권고: {recommendation}

---

⚠️ 면책: 이 비교 분석은 참고용이며, 최종 결정은 법률 전문가와 상의하세요.
```

## 비교 기준

### 텍스트 매칭 규칙

```yaml
matching_rules:
  exact_match: "완전 일치"
  semantic_match: "의미 동일, 표현 상이"
  partial_match: "부분 일치"
  no_match: "신규/삭제"
```

### 무시 항목

```yaml
ignore_patterns:
  - 공백 차이
  - 조사 변경 (은/는, 이/가)
  - 번호 체계만 변경
  - 날짜 형식 (YYYY.MM.DD vs YYYY-MM-DD)
```

## 다음 스킬 연결

버전 비교 완료 후:

1. **위험 평가** → Risk Assessment Skill (새 위험 평가)
2. **수정 제안** → Redline Suggest Skill (대응 수정안)
3. **협상 전략** → Negotiation Points Skill (협상 대응)

---

*버전 비교는 협상의 흐름을 파악하는 핵심입니다.*

⚠️ 면책: 이 분석은 참고용이며, 최종 결정은 법률 전문가와 상의하세요.
