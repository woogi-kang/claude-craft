# 용어 사전: TestCraft

> Glossary
> 버전: 1.0
> 작성일: 2026-01-16
> 상태: Draft

---

## 1. 개요

이 문서는 TestCraft 프로젝트에서 사용되는 주요 용어를 정의합니다. 팀 내 커뮤니케이션의 일관성을 유지하고, 문서 간 용어 통일을 위해 사용됩니다.

### 1.1 용어 사용 규칙

1. **공식 용어**: 문서에서는 공식 용어를 사용합니다.
2. **약어**: 처음 등장 시 전체 명칭과 함께 표기합니다. (예: TC(Test Case))
3. **영문/한글**: 기술 용어는 영문 우선, 일반 용어는 한글 우선
4. **일관성**: 문서 내에서 동일한 개념은 동일한 용어로 표기합니다.

---

## 2. 핵심 용어

### 2.1 테스트 관련

| 용어 | 정의 | 사용 컨텍스트 | 동의어/관련어 |
|------|------|---------------|--------------|
| **TC** | Test Case. 특정 기능이나 시나리오를 검증하기 위한 테스트 항목. 전제조건, 테스트 단계, 예상 결과를 포함함 | 전체 | 테스트케이스, Test Case |
| **테스트케이스** | TC의 한글 표현. 공식 문서에서는 "TC" 사용 권장 | 전체 | TC |
| **엣지케이스** | Edge Case. 경계 조건이나 예외적 상황에서의 테스트 시나리오. 일반적 사용 패턴을 벗어나는 케이스 | TC 유형 | 경계값 테스트, 예외 케이스 |
| **기능 테스트** | Functional Test. 명세된 기능이 요구사항대로 동작하는지 검증하는 테스트 | TC 유형 | Functional Test |
| **회귀 테스트** | Regression Test. 기존 기능이 변경 후에도 정상 동작하는지 확인하는 테스트 | TC 유형 | Regression Test |
| **인수 조건** | Acceptance Criteria. 기능이 "완료"로 인정되기 위해 충족해야 하는 조건. Given-When-Then 형식 권장 | PRD, 기능 명세 | AC, 수락 조건 |
| **Traceability** | 추적성. 요구사항과 테스트케이스 간의 연결 관계 | TC 관리 | 요구사항 추적 |

### 2.2 문서 관련

| 용어 | 정의 | 사용 컨텍스트 | 동의어/관련어 |
|------|------|---------------|--------------|
| **PRD** | Product Requirements Document. 제품 요구사항 문서. 기능, 비기능 요구사항, 제약사항 등을 정의 | 입력 문서 | 기획서, 요구사항 문서 |
| **기획서** | 제품/기능의 요구사항과 상세 명세를 담은 문서. TestCraft의 주요 입력 소스 | 입력 문서 | PRD, 스펙 문서 |
| **IA** | Information Architecture. 정보 구조. 화면 구성, 네비게이션, 정보 계층을 정의 | 설계 문서 | 정보 구조, 사이트맵 |
| **UX Strategy** | 사용자 경험 전략. 사용자 여정, 인터랙션 패턴, 디자인 원칙을 정의 | 설계 문서 | UX 전략 |
| **User Journey** | 사용자 여정. 사용자가 목표를 달성하기 위해 거치는 단계별 경험 | 설계 문서 | 사용자 시나리오 |
| **Wireframe** | 와이어프레임. UI의 레이아웃과 구조를 표현한 저충실도 설계안 | 설계 문서 | 목업, 스케치 |

### 2.3 제품/기능 관련

| 용어 | 정의 | 사용 컨텍스트 | 동의어/관련어 |
|------|------|---------------|--------------|
| **TestCraft** | 본 프로젝트명. PRD/기획서를 분석하여 TC를 자동 생성하는 AI 기반 SaaS | 전체 | - |
| **TC 생성** | TestCraft의 핵심 기능. PDF 업로드 → AI 분석 → TC 자동 생성 과정 | 기능 | 테스트케이스 생성 |
| **플랫폼** | 테스트 대상 환경. Android, iOS, Web, PC(Desktop) 중 선택 | 기능 | 타겟 플랫폼 |
| **Export** | 생성된 TC를 외부 형식(Excel, CSV 등)으로 내보내는 기능 | 기능 | 내보내기 |
| **프로젝트** | TestCraft 내에서 TC를 관리하는 단위. 하나의 제품/서비스에 대응 | 기능 | Project |

### 2.4 기술 관련

| 용어 | 정의 | 사용 컨텍스트 | 동의어/관련어 |
|------|------|---------------|--------------|
| **LLM** | Large Language Model. 대규모 언어 모델. TC 생성에 활용 (예: GPT-4) | 기술 | AI 모델, 언어 모델 |
| **PDF 파싱** | PDF 문서에서 텍스트와 구조를 추출하는 과정 | 기술 | PDF 추출 |
| **프롬프트** | Prompt. LLM에게 작업을 지시하는 텍스트 입력 | 기술 | 지시문 |
| **POC** | Proof of Concept. 개념 증명. 핵심 기술의 실현 가능성을 검증하는 단계 | 개발 | 프로토타입, 기술 검증 |
| **MVP** | Minimum Viable Product. 최소 기능 제품. 핵심 기능만 포함한 초기 버전 | 개발 | 최소 제품 |

---

## 3. 플랫폼별 용어

### 3.1 Android

| 용어 | 정의 | 엣지케이스 연관 |
|------|------|----------------|
| **Back Button** | Android 시스템 뒤로가기 버튼 | 모든 화면에서 처리 필요 |
| **Deep Link** | 앱 내 특정 화면으로 직접 진입하는 URL | 상태 복원 케이스 |
| **Permission** | 앱이 시스템 기능에 접근하기 위한 권한 | 권한 거부 케이스 |
| **Process Kill** | 시스템이 백그라운드 앱 프로세스를 종료 | 상태 복원 케이스 |
| **Foldable** | 폴더블 디바이스. 화면 접힘/펼침 지원 | 화면 전환 케이스 |
| **Battery Saver** | 배터리 절약 모드. 백그라운드 제한 | 백그라운드 작업 케이스 |

### 3.2 iOS

| 용어 | 정의 | 엣지케이스 연관 |
|------|------|----------------|
| **Safe Area** | 노치/인디케이터 영역을 제외한 안전 표시 영역 | UI 레이아웃 케이스 |
| **Dynamic Island** | iPhone 14 Pro 이상의 상단 인터랙티브 영역 | UI 대응 케이스 |
| **Face ID** | 얼굴 인식 생체 인증 | 인증 실패 케이스 |
| **Touch ID** | 지문 인식 생체 인증 | 인증 실패 케이스 |
| **App Life Cycle** | 앱 생명주기. Active, Background, Suspended 등 | 상태 전환 케이스 |
| **Keychain** | iOS 보안 저장소. 토큰, 비밀번호 저장 | 보안 케이스 |

### 3.3 Web

| 용어 | 정의 | 엣지케이스 연관 |
|------|------|----------------|
| **반응형** | Responsive. 화면 크기에 따라 레이아웃 조정 | 해상도별 케이스 |
| **PWA** | Progressive Web App. 웹앱을 네이티브처럼 설치/사용 | 오프라인 케이스 |
| **Session** | 사용자 인증 상태를 유지하는 기간 | 세션 만료 케이스 |
| **LCP** | Largest Contentful Paint. 핵심 성능 지표 | 성능 케이스 |
| **Cross-Browser** | 여러 브라우저에서 동일하게 동작 | 브라우저 호환 케이스 |

---

## 4. 비즈니스 용어

### 4.1 지표 관련

| 용어 | 정의 | 사용 컨텍스트 |
|------|------|---------------|
| **MAU** | Monthly Active Users. 월간 활성 사용자 수 | KPI |
| **MRR** | Monthly Recurring Revenue. 월간 반복 매출 | KPI |
| **ARPU** | Average Revenue Per User. 사용자당 평균 매출 | KPI |
| **CAC** | Customer Acquisition Cost. 고객 획득 비용 | KPI |
| **LTV** | Lifetime Value. 고객 생애 가치 | KPI |
| **NPS** | Net Promoter Score. 순추천지수 | KPI |
| **Retention** | 유지율. 일정 기간 후 재방문하는 사용자 비율 | KPI |
| **Churn** | 이탈률. 서비스 사용을 중단하는 비율 | KPI |

### 4.2 가격/과금 관련

| 용어 | 정의 | 사용 컨텍스트 |
|------|------|---------------|
| **Freemium** | 기본 무료 + 유료 프리미엄 모델 | 가격 전략 |
| **Basic Plan** | 기본 유료 플랜 ($10/월) | 가격 플랜 |
| **Pro Plan** | 고급 유료 플랜 ($25/월) | 가격 플랜 |
| **전환율** | Conversion Rate. 무료 → 유료 전환 비율 | KPI |

---

## 5. 우선순위 체계

### 5.1 기능 우선순위 (MoSCoW)

| 용어 | 정의 | 적용 |
|------|------|------|
| **Must Have** | MVP에 반드시 포함. 없으면 출시 불가 | F-001 ~ F-009 |
| **Should Have** | Early Adopter 단계에 포함. 사용성 향상 | F-010 ~ F-017 |
| **Could Have** | Growth 단계에 포함. 경쟁력 강화 | F-018 ~ F-024 |
| **Won't Have** | v1.0 범위 외. 향후 검토 | F-025 ~ F-028 |

### 5.2 이슈 우선순위

| 용어 | 정의 | 대응 시간 |
|------|------|----------|
| **P0 (Critical)** | 서비스 불가 또는 핵심 기능 장애 | 즉시 |
| **P1 (Major)** | 주요 기능 장애, 우회 방법 존재 | 24시간 내 |
| **P2 (Minor)** | 불편하지만 사용 가능 | Sprint 내 |
| **P3 (Low)** | 개선 사항, 품질 향상 | 백로그 |

### 5.3 TC 우선순위

| 용어 | 정의 | 테스트 실행 |
|------|------|-----------|
| **High** | 핵심 기능, 반드시 테스트 | 매 릴리스 |
| **Medium** | 중요 기능, 가능하면 테스트 | 주요 릴리스 |
| **Low** | 부가 기능, 시간 여유 시 | 필요시 |

---

## 6. 약어 목록

| 약어 | 전체 명칭 | 한글 |
|-----|----------|------|
| AC | Acceptance Criteria | 인수 조건 |
| API | Application Programming Interface | 응용 프로그램 인터페이스 |
| ARPU | Average Revenue Per User | 사용자당 평균 매출 |
| BDD | Behavior-Driven Development | 행위 주도 개발 |
| CAC | Customer Acquisition Cost | 고객 획득 비용 |
| CI/CD | Continuous Integration/Continuous Deployment | 지속적 통합/배포 |
| CSV | Comma-Separated Values | 쉼표 구분 값 |
| DB | Database | 데이터베이스 |
| E2E | End-to-End | 종단 간 |
| GTM | Go-to-Market | 시장 진출 |
| IA | Information Architecture | 정보 구조 |
| KPI | Key Performance Indicator | 핵심 성과 지표 |
| LCP | Largest Contentful Paint | - |
| LLM | Large Language Model | 대규모 언어 모델 |
| LTV | Lifetime Value | 고객 생애 가치 |
| MAU | Monthly Active Users | 월간 활성 사용자 |
| MRR | Monthly Recurring Revenue | 월간 반복 매출 |
| MVP | Minimum Viable Product | 최소 기능 제품 |
| NFR | Non-Functional Requirements | 비기능 요구사항 |
| NPS | Net Promoter Score | 순추천지수 |
| OAuth | Open Authorization | 개방형 인증 |
| PDF | Portable Document Format | - |
| PM | Product Manager | 제품 관리자 |
| POC | Proof of Concept | 개념 증명 |
| PRD | Product Requirements Document | 제품 요구사항 문서 |
| PWA | Progressive Web App | 프로그레시브 웹앱 |
| QA | Quality Assurance | 품질 보증 |
| RBAC | Role-Based Access Control | 역할 기반 접근 제어 |
| SaaS | Software as a Service | 서비스형 소프트웨어 |
| TC | Test Case | 테스트케이스 |
| TDD | Test-Driven Development | 테스트 주도 개발 |
| UI | User Interface | 사용자 인터페이스 |
| UX | User Experience | 사용자 경험 |
| WTP | Willingness to Pay | 지불 의향 |

---

## 7. 문서 내 용어 통일 가이드

### 7.1 권장 표기

| 상황 | 권장 | 비권장 |
|-----|------|--------|
| 테스트케이스 | TC | 테스트케이스, Test Case, 테케 |
| 기획서 | PRD 또는 기획서 | 스펙, 명세서 |
| 엣지케이스 | 엣지케이스 | 에지케이스, Edge Case |
| 사용자 | 사용자 | 유저, User |
| 플랫폼 | Android, iOS, Web | 안드로이드, 아이폰 |

### 7.2 처음 등장 시 표기

```markdown
# 올바른 예
TestCraft는 PRD(Product Requirements Document)를 분석하여
TC(Test Case)를 자동 생성합니다.

# 이후 사용
PRD를 업로드하면 TC가 생성됩니다.
```

---

## 8. 변경 이력

| 버전 | 날짜 | 변경 내용 | 작성자 |
|-----|------|----------|--------|
| 1.0 | 2026-01-16 | 초안 작성 | Alfred |

---

## 9. 참고 문서

- [PRD](/workspace/work-plan/testcraft/04-specification/prd.md)
- [Information Architecture](/workspace/work-plan/testcraft/04-specification/information-architecture.md)
- [User Journey](/workspace/work-plan/testcraft/04-specification/user-journey.md)

---

*Document generated by Alfred - Glossary Skill*
