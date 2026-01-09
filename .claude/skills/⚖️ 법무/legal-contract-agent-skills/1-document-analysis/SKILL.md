---
name: legal-document-analysis
description: |
  계약서 구조 분석 및 조항별 분류.
  문서의 전체 구조를 파악하고 각 조항을 카테고리화합니다.
triggers:
  - "문서 분석"
  - "구조 분석"
  - "조항 분류"
  - "계약서 구조"
input:
  - 계약서 텍스트
  - 컨텍스트 문서 (선택)
output:
  - analysis/{project}-document-analysis.md
---

# Document Analysis Skill

계약서의 구조를 분석하고 조항을 카테고리별로 분류합니다.

## 분석 프레임워크

### 문서 구조 분류

```
┌─────────────────────────────────────────────────────────────┐
│                      문서 구조 분석                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 기본 정보 (Header)                                       │
│     - 계약 제목, 체결일, 당사자                               │
│                                                              │
│  2. 정의 (Definitions)                                       │
│     - 핵심 용어 정의                                         │
│                                                              │
│  3. 핵심 조항 (Core Terms)                                   │
│     - 계약 목적, 범위, 대가                                  │
│                                                              │
│  4. 권리/의무 (Rights & Obligations)                         │
│     - 각 당사자의 권리와 의무                                │
│                                                              │
│  5. 보호 조항 (Protective Clauses)                           │
│     - 비밀유지, 지적재산권, 손해배상                          │
│                                                              │
│  6. 종료 조항 (Termination)                                  │
│     - 해지, 만료, 종료 후 의무                               │
│                                                              │
│  7. 일반 조항 (Boilerplate)                                  │
│     - 불가항력, 통지, 분쟁해결, 기타                          │
│                                                              │
│  8. 서명 (Signature)                                         │
│     - 서명란, 날인                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 조항 카테고리 정의

### 카테고리 분류표

| 카테고리 | 영문 | 포함 조항 |
|----------|------|----------|
| **기본정보** | Header | 제목, 전문, 당사자, 체결일 |
| **정의** | Definitions | 용어 정의 |
| **핵심조항** | Core Terms | 목적, 범위, 대가, 지급조건 |
| **권리의무** | Rights/Obligations | 당사자별 권리와 의무 |
| **비밀유지** | Confidentiality | 비밀정보 정의, 유지의무, 예외 |
| **지적재산** | IP | 소유권, 라이선스, 양도 |
| **책임/배상** | Liability/Indemnity | 손해배상, 책임제한, 면책 |
| **보증** | Warranties | 진술 및 보증 |
| **기간/해지** | Term/Termination | 계약기간, 해지사유, 효과 |
| **분쟁해결** | Dispute | 준거법, 관할, 중재 |
| **일반조항** | Boilerplate | 불가항력, 양도, 통지, 완전합의 |
| **서명** | Signature | 서명란, 별첨 |

### 조항별 상세 태그

```yaml
clause_tags:
  # 핵심 상업 조건
  - purpose              # 목적
  - scope                # 범위
  - price                # 가격/대가
  - payment              # 지급조건
  - delivery             # 인도/제공

  # 보호 조항
  - confidentiality      # 비밀유지
  - ip_ownership         # IP 소유권
  - ip_license           # IP 라이선스
  - indemnification      # 손해배상
  - limitation           # 책임제한
  - warranty             # 보증
  - disclaimer           # 면책

  # 기간/종료
  - term                 # 기간
  - renewal              # 갱신
  - termination          # 해지
  - post_termination     # 종료 후 의무

  # 일반 조항
  - force_majeure        # 불가항력
  - assignment           # 양도
  - notice               # 통지
  - amendment            # 변경
  - severability         # 분리가능성
  - entire_agreement     # 완전합의
  - governing_law        # 준거법
  - jurisdiction         # 관할
  - arbitration          # 중재
```

## 분석 워크플로우

```
1. 문서 구조 파악
      │
      ├─ 목차 확인 (있는 경우)
      ├─ 조항 번호 체계 파악
      │
      ▼
2. 조항별 분류
      │
      ├─ 카테고리 할당
      ├─ 태그 부여
      │
      ▼
3. 누락 조항 식별
      │
      ├─ 표준 조항 대비
      ├─ 계약 유형별 필수 조항
      │
      ▼
4. 구조 이상 탐지
      │
      ├─ 중복 조항
      ├─ 순서 이상
      ├─ 참조 오류
      │
      ▼
5. 분석 결과 생성
   → workspace/work-legal/{project}/analysis/{project}-document-analysis.md
```

## 계약 유형별 필수 조항

### NDA (비밀유지계약)

```yaml
nda_required:
  - 비밀정보 정의
  - 비밀유지 의무
  - 허용 공개 범위
  - 비밀유지 기간
  - 반환/파기 의무
  - 분쟁해결

nda_recommended:
  - 잔존 지식 (Residual Knowledge)
  - 강제 공개 예외
  - 손해배상
  - 금지청구
```

### 서비스 계약 (MSA)

```yaml
msa_required:
  - 서비스 범위
  - 대가 및 지급
  - 서비스 수준 (SLA)
  - 지적재산권
  - 비밀유지
  - 손해배상
  - 책임제한
  - 기간/해지
  - 분쟁해결

msa_recommended:
  - 변경관리
  - 검수/승인
  - 보험
  - 감사권
```

### 라이선스 계약

```yaml
license_required:
  - 라이선스 범위 (독점/비독점)
  - 허용 용도
  - 지역 범위
  - 기간
  - 로열티/대가
  - 서브라이선스 가부
  - 지적재산권 귀속
  - 보증/면책

license_recommended:
  - 개선사항 처리
  - 감사권
  - 소스코드 에스크로
```

## 출력 템플릿

```markdown
# {Project Name} 문서 분석 결과

## 문서 개요

| 항목 | 내용 |
|------|------|
| 문서 유형 | {document_type} |
| 페이지 수 | {page_count} |
| 조항 수 | {clause_count} |
| 언어 | {language} |
| 번호 체계 | {numbering} (예: 제1조, Article 1) |

## 당사자 정보

| 역할 | 명칭 | 정의 |
|------|------|------|
| 갑 | {party_a} | {definition_a} |
| 을 | {party_b} | {definition_b} |

---

## 문서 구조

### 전체 구조도

```
{structure_overview}
```

### 조항 분류표

| 조항 번호 | 제목 | 카테고리 | 페이지 | 태그 |
|----------|------|----------|--------|------|
| 제1조 | 목적 | Core Terms | 1 | purpose |
| 제2조 | 정의 | Definitions | 1-2 | definitions |
| 제3조 | ... | ... | ... | ... |

---

## 카테고리별 분석

### 1. 기본정보 (Header)

| 조항 | 내용 요약 | 특이사항 |
|------|----------|---------|
| 전문 | {summary} | {note} |

### 2. 정의 (Definitions)

| 용어 | 정의 | 비고 |
|------|------|------|
| {term_1} | {definition_1} | |
| {term_2} | {definition_2} | |

### 3. 핵심조항 (Core Terms)

| 조항 | 내용 요약 | 주의사항 |
|------|----------|---------|
| {clause} | {summary} | {warning} |

### 4. 비밀유지 (Confidentiality)

| 항목 | 내용 |
|------|------|
| 비밀정보 범위 | {scope} |
| 예외 | {exceptions} |
| 유지 기간 | {duration} |

### 5. 지적재산권 (IP)

| 항목 | 내용 |
|------|------|
| 기존 IP | {existing_ip} |
| 신규 IP | {new_ip} |
| 라이선스 | {license} |

### 6. 책임/배상 (Liability/Indemnity)

| 항목 | 내용 |
|------|------|
| 손해배상 범위 | {indemnity_scope} |
| 책임제한 | {limitation} |
| 면책 | {disclaimer} |

### 7. 기간/해지 (Term/Termination)

| 항목 | 내용 |
|------|------|
| 계약 기간 | {term} |
| 갱신 | {renewal} |
| 해지 사유 | {termination_causes} |
| 해지 통지 | {notice_period} |
| 종료 후 의무 | {post_termination} |

### 8. 분쟁해결 (Dispute)

| 항목 | 내용 |
|------|------|
| 준거법 | {governing_law} |
| 관할 | {jurisdiction} |
| 중재 | {arbitration} |

---

## 누락/권장 조항

### 🔴 누락된 필수 조항

| 조항 | 필요 이유 | 권고 |
|------|----------|------|
| {missing_1} | {reason_1} | {recommendation_1} |
| {missing_2} | {reason_2} | {recommendation_2} |

### 🟡 권장 조항 (미포함)

| 조항 | 설명 | 중요도 |
|------|------|--------|
| {recommended_1} | {description_1} | {priority_1} |

---

## 구조 이상 탐지

### ⚠️ 주의사항

| 유형 | 위치 | 설명 |
|------|------|------|
| 중복 | 제5조, 제12조 | 비밀유지 의무 중복 정의 |
| 참조 오류 | 제8조 3항 | "제10조"가 존재하지 않음 |
| 불명확 | 제7조 | 주어 불명확 ("당사자"가 누구인지) |

---

## 정의 용어 색인

| 용어 | 정의 위치 | 사용 위치 |
|------|----------|----------|
| {term_1} | 제2조 1항 | 제5조, 제7조, 제12조 |
| {term_2} | 제2조 2항 | 제3조, 제8조 |

---

## 다음 단계

분석 완료 후 권장 순서:
1. [ ] Risk Assessment → 위험 조항 평가
2. [ ] Summary Extract → 핵심 조건 요약
3. [ ] Clause Library → 표준 조항 비교

---

*문서 분석은 계약 검토의 첫 단계입니다.*
*구조를 파악한 후 상세 분석을 진행하세요.*

⚠️ 면책: 이 분석은 참고용이며, 최종 결정은 법률 전문가와 상의하세요.
```

## 분석 포인트

### 주의해서 볼 조항

```yaml
high_attention:
  - 손해배상 (무제한 배상 여부)
  - 책임제한 (상한, 면책 범위)
  - 해지 조항 (일방 해지, 통지 기간)
  - 자동 갱신 (갱신 조건, 거부 기간)
  - 비밀유지 (기간, 범위)
  - 경쟁금지 (기간, 범위, 지역)
  - 지적재산권 (귀속, 양도)
  - 준거법/관할 (불리한 관할)
```

### 빈번한 문제 패턴

| 패턴 | 설명 | 위험도 |
|------|------|--------|
| 불명확한 정의 | 핵심 용어 정의 누락 | 🟠 |
| 불균형 해지권 | 일방만 해지 가능 | 🔴 |
| 무제한 배상 | 배상 상한 없음 | 🔴 |
| 과도한 면책 | 상대방 과실도 면책 | 🔴 |
| 자동 갱신 함정 | 거부 기간 짧음 | 🟡 |
| 참조 오류 | 없는 조항 참조 | 🟡 |

## 다음 스킬 연결

문서 분석 완료 후:

1. **위험 평가** → Risk Assessment Skill
2. **요약 추출** → Summary Extract Skill
3. **조항 비교** → Clause Library Skill

---

*문서 구조를 정확히 파악하는 것이 효과적인 검토의 시작입니다.*
