# Legal Contract Agent 사용 가이드

## 개요

Legal Contract Agent는 계약서 검토, 위험 분석, 문서 생성을 지원하는 법무 전문 Agent입니다.

---

## 중요 고지사항

```
이 Agent는 법률 전문가를 대체하지 않습니다.
모든 출력은 자격 있는 변호사의 검토가 필요합니다.
최종 법적 결정은 반드시 법률 전문가와 상의하세요.

이 도구의 역할:
- 시간 절약 (초기 검토, 초안 작성)
- 체크포인트 제공 (놓칠 수 있는 항목 식별)
- 구조화된 분석 (일관된 형식)

이 도구가 아닌 것:
- 법률 자문
- 최종 검토 대체
- 법적 책임 부담
```

---

## 지원 계약 유형 비교

| 유형 | 주요 검토 포인트 | 적합한 사용 시나리오 |
|------|-----------------|---------------------|
| **NDA (비밀유지계약)** | 비밀정보 범위, 의무기간, 예외조항 | 협력사/투자자 NDA 검토, 상호 NDA 작성 |
| **서비스 계약 (MSA/SaaS)** | SLA, 책임제한, 해지조건 | B2B 서비스 계약, 플랫폼 이용계약 |
| **라이선스 계약** | 사용범위, 로열티, 지재권 귀속 | SW 라이선스, 기술이전 계약 |
| **고용 계약** | 비경쟁, 비밀유지, 퇴직금 | 직원/임원 고용계약 |
| **투자 계약** | 지분, 이사회, 청산우선권 | 시드/시리즈 투자 |
| **이용약관** | 서비스 범위, 책임제한, 탈퇴 | 앱/웹 서비스 운영 |

---

## 사용 시나리오

### 시나리오 1: NDA 검토

```
사용자: "상대방이 보낸 NDA 검토해줘. 우리는 협상력이 약해."

Agent 실행:
0. [Context] 계약 유형, 당사자, 협상 포지션 파악
1. [Analysis] 문서 구조 분석
2. [Risk] 위험 조항 식별
3. [Summary] 핵심 조건 추출
4. [Clause] 표준 NDA 대비 비교
7. [Redline] 수정안 옵션 제시
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

### 시나리오 4: 위험 분석만

```
사용자: "이 계약서에서 위험한 조항만 찾아줘"

Agent 실행:
0. [Context] 계약 유형, 우리 역할 확인
2. [Risk] 위험 조항 식별 및 심각도 평가
7. [Redline] 수정 제안
```

---

## 명령어 레퍼런스

### 전체 프로세스 실행
| 명령어 | 설명 |
|--------|------|
| `계약서 검토해줘` | 전체 검토 프로세스 실행 |
| `NDA 분석해줘` | NDA 특화 분석 |
| `이 계약 전체 리뷰해줘` | 전체 리뷰 + 최종 리포트 |

### 개별 Skill 호출
| 명령어 | Skill | 설명 |
|--------|-------|------|
| `/legal-context` | Context Intake | 컨텍스트 수집 |
| `/legal-analyze` | Document Analysis | 문서 구조 분석 |
| `/legal-risk` | Risk Assessment | 위험 평가 |
| `/legal-summary` | Summary Extract | 핵심 조건 추출 |
| `/legal-clause` | Clause Library | 표준 조항 비교 |
| `/legal-compare` | Version Compare | 버전 비교 |
| `/legal-compliance` | Compliance Check | 규정 준수 확인 |
| `/legal-redline` | Redline Suggest | 수정 제안 |
| `/legal-negotiate` | Negotiation Points | 협상 포인트 |
| `/legal-generate` | Document Generate | 문서 생성 |
| `/legal-checklist` | Checklist | 체크리스트 |
| `/legal-review` | Final Review | 최종 검토 |

### 파이프라인 제어
```
"위험 평가만 해줘"
"수정 제안부터 해줘"
"체크리스트만 확인해줘"
"피드백 반영해서 수정해줘"
```

---

## 출력물 구조

```
workspace/work-legal/
└── {project-name}/
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

## 문제 해결

| 문제 | 원인 | 해결 방법 |
|-----|------|----------|
| 분석이 부정확 | 문서 형식 문제 | 텍스트로 변환 후 재시도 |
| 위험 과소평가 | 컨텍스트 부족 | Context Intake 충실히 |
| 조항 해석 오류 | 복잡한 법률 용어 | 법률 전문가 검토 필수 |
| 관할권 차이 | 다른 법률 체계 | 해당 관할권 명시 |
| 산업 규제 누락 | 규제 정보 부재 | 업계 규제 정보 제공 |

---

## 다른 에이전트와의 연동

| 연동 Agent | 사용 시나리오 |
|------------|--------------|
| `ppt-agent` | 법무 검토 결과를 경영진 보고용 프레젠테이션으로 |
| `marketing-agent` | 파트너십 계약 마케팅 자료 작성 |
| `tech-blog-agent` | 계약 관련 법률 해설 블로그 |

---

*Legal Contract Agent v2.0 - Progressive Disclosure 적용*
