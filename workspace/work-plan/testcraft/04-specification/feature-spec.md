# Feature Specification: TestCraft

> 기능 명세서
> 버전: 2.0
> 작성일: 2026-01-16
> 최종 수정: 2026-01-16
> 상태: Draft
> 변경사항: Claude-Gemini 협업 합의에 따른 대화형 TC 생성 기능 및 TC 품질 향상 기능 추가

---

## 1. 기능 명세 개요

### 1.1 문서 목적

이 문서는 TestCraft의 각 기능에 대한 상세 명세를 정의합니다. User Story, Acceptance Criteria, UI/UX 요구사항, 기술 요구사항을 포함합니다.

### 1.2 우선순위 범례

| 우선순위 | 설명 | 릴리스 |
|---------|------|--------|
| **P0** | MVP 필수 | v0.1 (4주) |
| **P1** | Early Adopter | v0.5 (8주) |
| **P2** | Growth | v1.0 (16주) |
| **P3** | Future | v1.0+ |

---

## 2. 인증 및 계정 (Authentication)

### F-001: 회원가입/로그인

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 계정을 생성하고 로그인하여
SO THAT 나의 프로젝트와 테스트케이스를 저장하고 관리할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 회원가입 및 로그인

  Scenario: 이메일 회원가입
    Given 사용자가 회원가입 페이지에 접속했을 때
    When 유효한 이메일과 비밀번호(8자 이상, 영문+숫자)를 입력하고
    And 회원가입 버튼을 클릭하면
    Then 인증 이메일이 발송되고
    And "이메일을 확인해주세요" 메시지가 표시된다

  Scenario: 이메일 인증 완료
    Given 인증 이메일의 링크를 클릭했을 때
    Then 계정이 활성화되고
    And 자동으로 로그인되어 대시보드로 이동한다

  Scenario: Google 소셜 로그인
    Given 사용자가 로그인 페이지에 접속했을 때
    When "Google로 계속하기" 버튼을 클릭하면
    Then Google OAuth 화면으로 이동하고
    And 인증 완료 시 자동으로 계정이 생성/로그인된다

  Scenario: GitHub 소셜 로그인
    Given 사용자가 로그인 페이지에 접속했을 때
    When "GitHub로 계속하기" 버튼을 클릭하면
    Then GitHub OAuth 화면으로 이동하고
    And 인증 완료 시 자동으로 계정이 생성/로그인된다

  Scenario: 비밀번호 찾기
    Given 사용자가 "비밀번호 찾기"를 클릭했을 때
    When 가입한 이메일을 입력하면
    Then 비밀번호 재설정 링크가 이메일로 발송된다
```

#### UI 요구사항

| 화면 | 요소 | 설명 |
|-----|------|------|
| 로그인 | 이메일 입력 | placeholder: "이메일 주소" |
| | 비밀번호 입력 | placeholder: "비밀번호", 비밀번호 표시 토글 |
| | 로그인 버튼 | Primary CTA |
| | 소셜 로그인 | Google, GitHub 버튼 |
| | 회원가입 링크 | "계정이 없으신가요? 회원가입" |
| | 비밀번호 찾기 | "비밀번호를 잊으셨나요?" |
| 회원가입 | 이메일 입력 | 실시간 유효성 검사 |
| | 비밀번호 입력 | 강도 표시기 (약함/보통/강함) |
| | 비밀번호 확인 | 일치 여부 실시간 표시 |
| | 이용약관 동의 | 체크박스 + 링크 |
| | 회원가입 버튼 | 모든 조건 충족 시 활성화 |

#### 기술 요구사항

- Supabase Auth 사용
- OAuth 2.0: Google, GitHub
- 비밀번호: bcrypt 해싱, 최소 8자
- 세션: JWT, 7일 만료
- Rate Limiting: 로그인 실패 5회/분

---

## 3. 프로젝트 관리 (Project Management)

### F-002: 프로젝트 생성

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 새로운 프로젝트를 생성하여
SO THAT 서비스별로 테스트케이스를 분리하여 관리할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 프로젝트 생성

  Scenario: 새 프로젝트 생성
    Given 로그인한 사용자가 대시보드에 있을 때
    When "새 프로젝트" 버튼을 클릭하고
    And 프로젝트 이름(필수), 설명(선택)을 입력하고
    And "생성" 버튼을 클릭하면
    Then 새 프로젝트가 생성되고
    And 프로젝트 상세 페이지로 이동한다

  Scenario: 프로젝트 이름 중복 검사
    Given 프로젝트 생성 폼에서
    When 이미 존재하는 프로젝트 이름을 입력하면
    Then "이미 사용 중인 이름입니다" 오류가 표시된다

  Scenario: 프로젝트 목록 조회
    Given 로그인한 사용자가 대시보드에 있을 때
    Then 내가 속한 모든 프로젝트 목록이 표시되고
    And 각 프로젝트의 TC 수, 마지막 업데이트 일시가 표시된다

  Scenario: 프로젝트 설정 변경
    Given 프로젝트 소유자가 프로젝트 설정에 있을 때
    When 프로젝트 이름이나 설명을 수정하고
    And "저장" 버튼을 클릭하면
    Then 변경사항이 저장되고
    And "저장되었습니다" 토스트가 표시된다

  Scenario: 프로젝트 삭제
    Given 프로젝트 소유자가 프로젝트 설정에 있을 때
    When "프로젝트 삭제" 버튼을 클릭하고
    And 확인 모달에서 프로젝트 이름을 입력하면
    Then 프로젝트와 모든 TC가 삭제되고
    And 대시보드로 이동한다
```

#### UI 요구사항

| 화면 | 요소 | 설명 |
|-----|------|------|
| 대시보드 | 프로젝트 카드 | 이름, TC 수, 최근 업데이트, 플랫폼 아이콘 |
| | 새 프로젝트 버튼 | "+" 아이콘 + "새 프로젝트" |
| | 검색 | 프로젝트명 검색 |
| | 정렬 | 최근순, 이름순, TC 수 |
| 프로젝트 생성 모달 | 이름 입력 | 필수, 최대 50자 |
| | 설명 입력 | 선택, 최대 200자 |
| | 생성/취소 버튼 | |

#### 기술 요구사항

- DB 테이블: `projects` (id, name, description, user_id, created_at, updated_at)
- 관계: User 1:N Project, Project 1:N TestCase
- 인덱스: user_id, name (unique per user)

---

## 4. PRD 업로드 및 분석 (PRD Upload & Analysis)

### F-003: PRD 업로드

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO PDF 형식의 기획서를 업로드하여
SO THAT AI가 분석하여 테스트케이스를 생성할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: PRD 업로드

  Scenario: PDF 파일 업로드
    Given 프로젝트 상세 페이지에서
    When "PRD 업로드" 버튼을 클릭하고
    And PDF 파일(최대 20MB)을 선택하면
    Then 파일이 업로드되고
    And 업로드 진행률이 표시된다

  Scenario: 드래그 앤 드롭 업로드
    Given 프로젝트 상세 페이지에서
    When PDF 파일을 업로드 영역에 드래그 앤 드롭하면
    Then 파일이 업로드되고
    And 업로드 진행률이 표시된다

  Scenario: 지원하지 않는 파일 형식
    Given 파일 업로드 시
    When PDF가 아닌 파일을 선택하면
    Then "PDF 파일만 업로드 가능합니다" 오류가 표시된다

  Scenario: 파일 크기 초과
    Given 파일 업로드 시
    When 20MB를 초과하는 파일을 선택하면
    Then "파일 크기는 20MB 이하여야 합니다" 오류가 표시된다

  Scenario: 업로드 후 미리보기
    Given 파일 업로드가 완료되면
    Then 파일명과 페이지 수가 표시되고
    And "분석 시작" 버튼이 활성화된다
```

#### UI 요구사항

| 화면 | 요소 | 설명 |
|-----|------|------|
| 업로드 영역 | 드롭존 | 점선 테두리, 아이콘, "PDF를 여기에 드롭하거나 클릭하여 선택" |
| | 파일 선택 버튼 | "파일 선택" |
| | 진행률 | 프로그레스 바 + 퍼센트 |
| 업로드 완료 | 파일 정보 | 파일명, 용량, 페이지 수 |
| | 미리보기 | 첫 페이지 썸네일 |
| | 삭제 버튼 | 파일 제거 |
| | 분석 시작 버튼 | Primary CTA |

#### 기술 요구사항

- 스토리지: Supabase Storage
- 파일 제한: PDF only, max 20MB
- 파싱: pdf.js (클라이언트) + pdf-parse (서버)
- 텍스트 추출: 페이지별 텍스트 + 레이아웃 정보

---

### F-010: Notion 연동

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A IT 기획자
I WANT TO Notion 페이지를 직접 연동하여
SO THAT 별도 파일 변환 없이 기획서를 가져올 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: Notion 연동

  Scenario: Notion 계정 연결
    Given 프로젝트 설정에서
    When "Notion 연동" 버튼을 클릭하면
    Then Notion OAuth 화면으로 이동하고
    And 권한 승인 시 연동이 완료된다

  Scenario: Notion 페이지 가져오기
    Given Notion이 연동된 상태에서
    When "Notion에서 가져오기"를 클릭하면
    Then 접근 가능한 페이지 목록이 표시되고
    And 페이지 선택 시 내용이 가져와진다

  Scenario: Notion URL 직접 입력
    Given Notion이 연동된 상태에서
    When Notion 페이지 URL을 직접 입력하면
    Then 해당 페이지 내용이 가져와진다
```

#### 기술 요구사항

- Notion API v1
- OAuth 2.0 연동
- 블록 타입 지원: paragraph, heading, list, table, image, toggle
- 하위 페이지 재귀적 가져오기 옵션

---

### F-018: Figma 연동

**우선순위**: P2 (Growth)

#### User Story

```
AS A 기획자
I WANT TO Figma 디자인을 연동하여
SO THAT UI 기반 테스트케이스를 생성할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: Figma 연동

  Scenario: Figma 계정 연결
    Given 프로젝트 설정에서
    When "Figma 연동" 버튼을 클릭하면
    Then Figma OAuth 화면으로 이동하고
    And 권한 승인 시 연동이 완료된다

  Scenario: Figma 프레임 가져오기
    Given Figma가 연동된 상태에서
    When Figma 파일 URL을 입력하면
    Then 파일 내 프레임 목록이 표시되고
    And 선택한 프레임의 레이아웃과 컴포넌트 정보가 추출된다

  Scenario: UI 기반 TC 생성
    Given Figma 프레임이 가져와진 상태에서
    When TC 생성을 요청하면
    Then 버튼, 입력, 네비게이션 등 UI 요소 기반 TC가 생성된다
```

---

## 5. 플랫폼 선택 (Platform Selection)

### F-004: 플랫폼 선택

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트 대상 플랫폼을 선택하여
SO THAT 해당 플랫폼에 특화된 테스트케이스를 받을 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 플랫폼 선택

  Scenario: 단일 플랫폼 선택
    Given PRD가 업로드된 상태에서
    When 플랫폼 선택 화면에서 "Android"를 선택하면
    Then Android가 선택 상태로 표시되고
    And Android 특화 옵션이 표시된다

  Scenario: 복수 플랫폼 선택
    Given 플랫폼 선택 화면에서
    When "Android"와 "iOS"를 모두 선택하면
    Then 두 플랫폼이 모두 선택 상태로 표시되고
    And 각 플랫폼별 TC가 생성된다

  Scenario: 전체 플랫폼 선택
    Given 플랫폼 선택 화면에서
    When "All"을 선택하면
    Then 모든 플랫폼(Android, iOS, Web, PC)이 선택되고
    And 각 플랫폼별 TC가 생성된다

  Scenario: 플랫폼별 옵션
    Given "Android"가 선택된 상태에서
    Then 다음 옵션이 표시된다:
      - 최소 지원 버전 (기본: Android 8.0)
      - 폴더블 지원 여부
      - 글로벌 배포 여부 (중국폰 호환)
```

#### UI 요구사항

| 화면 | 요소 | 설명 |
|-----|------|------|
| 플랫폼 선택 | 플랫폼 카드 | Android, iOS, Web, PC 아이콘 + 이름 |
| | All 선택 | "모든 플랫폼" 옵션 |
| | 선택 상태 | 체크 아이콘, 테두리 강조 |
| Android 옵션 | 최소 버전 | 드롭다운 (8.0, 9.0, 10.0, ...) |
| | 폴더블 지원 | 토글 |
| | 글로벌 배포 | 토글 (중국폰 호환) |
| iOS 옵션 | 최소 버전 | 드롭다운 (14.0, 15.0, 16.0, 17.0) |
| | iPad 지원 | 토글 |
| Web 옵션 | 반응형 | 토글 |
| | PWA | 토글 |
| PC 옵션 | OS 선택 | Windows, macOS, Linux 멀티셀렉트 |

---

## 6. TC 생성 (Test Case Generation)

### F-005: AI TC 생성

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 업로드한 기획서 기반으로 테스트케이스를 자동 생성하여
SO THAT 수동 작성 시간을 90% 이상 절약할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: AI TC 생성

  Scenario: TC 생성 시작
    Given PRD가 업로드되고 플랫폼이 선택된 상태에서
    When "테스트케이스 생성" 버튼을 클릭하면
    Then 생성 진행 상태가 표시되고
    And 예상 완료 시간이 표시된다

  Scenario: 생성 진행 상태
    Given TC 생성이 진행 중일 때
    Then 다음 단계가 순차적으로 표시된다:
      - PRD 분석 중... (30%)
      - 기능 추출 중... (50%)
      - TC 생성 중... (80%)
      - 엣지케이스 추가 중... (95%)
      - 완료! (100%)

  Scenario: 생성 완료
    Given TC 생성이 완료되면
    Then "N개의 테스트케이스가 생성되었습니다" 메시지가 표시되고
    And TC 목록 페이지로 이동하고
    And 생성된 TC 목록이 표시된다

  Scenario: 생성 실패 (PRD 해석 불가)
    Given PRD 내용이 불충분하거나 해석 불가할 때
    Then "기획서 내용을 분석할 수 없습니다" 오류가 표시되고
    And "더 상세한 기획서를 업로드해주세요" 안내가 표시된다

  Scenario: 생성 실패 (서버 오류)
    Given 서버 오류가 발생했을 때
    Then "일시적인 오류가 발생했습니다" 메시지가 표시되고
    And "다시 시도" 버튼이 표시된다
```

#### TC 생성 항목

| 항목 | 설명 | 예시 |
|-----|------|------|
| **TC ID** | 고유 식별자 | TC-001 |
| **기능** | 테스트 대상 기능 | 회원가입 |
| **시나리오** | 테스트 시나리오 이름 | 이메일 회원가입 성공 |
| **전제 조건** | 테스트 전 필요 상태 | 로그아웃 상태 |
| **테스트 단계** | 실행 절차 | 1. 회원가입 페이지 접속\n2. 이메일 입력... |
| **예상 결과** | 기대 동작 | 인증 이메일 발송, 완료 메시지 표시 |
| **플랫폼** | 대상 플랫폼 | Android |
| **카테고리** | TC 유형 | 기능/엣지케이스/경계값 |
| **우선순위** | 중요도 | High/Medium/Low |

#### 기술 요구사항

- LLM: GPT-4o (OpenAI) / Claude 3.5 (Anthropic)
- 프롬프트 엔지니어링: 구조화된 출력 (JSON)
- 스트리밍: 생성 과정 실시간 표시
- 타임아웃: 120초
- 재시도: 3회

---

### F-006: 엣지케이스 자동 포함

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 플랫폼별 엣지케이스가 자동으로 포함되어
SO THAT 경험 부족으로 인한 테스트 누락을 방지할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 엣지케이스 자동 포함

  Scenario: 기능별 엣지케이스 매칭
    Given "로그인" 기능에 대한 TC가 생성될 때
    Then 다음 엣지케이스가 자동으로 포함된다:
      - 비밀번호 5회 오류 시 계정 잠금
      - 세션 만료 후 재로그인
      - 소셜 로그인 취소 시

  Scenario: 플랫폼별 엣지케이스 추가
    Given Android가 선택된 상태에서 TC가 생성될 때
    Then 다음 Android 특화 엣지케이스가 추가된다:
      - Back 버튼으로 로그인 화면 이탈
      - 앱 전환 후 복귀 시 입력값 유지
      - 키보드 올라올 때 UI 대응

  Scenario: 엣지케이스 토글
    Given TC 목록에서
    When 특정 엣지케이스 TC의 "제외" 버튼을 클릭하면
    Then 해당 TC가 비활성화되고
    And Export 시 제외된다

  Scenario: 엣지케이스 카테고리 필터
    Given TC 목록에서
    When "엣지케이스만 보기" 필터를 활성화하면
    Then 자동 생성된 엣지케이스 TC만 표시된다
```

#### 엣지케이스 매칭 로직

```
PRD 기능 분석
     │
     ▼
┌─────────────────────────────────────────────────────────────┐
│                  기능-엣지케이스 매칭 엔진                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [키워드 매칭]                                                │
│  ├─ "로그인" → 인증 관련 엣지케이스 (15개)                    │
│  ├─ "결제" → 결제 관련 엣지케이스 (20개)                      │
│  ├─ "업로드" → 파일 처리 엣지케이스 (12개)                    │
│  └─ "푸시" → 알림 관련 엣지케이스 (8개)                       │
│                                                              │
│  [플랫폼 매칭]                                                │
│  ├─ Android → Android DB (150개)                            │
│  ├─ iOS → iOS DB (120개)                                    │
│  ├─ Web → Web DB (100개)                                    │
│  └─ PC → PC DB (80개)                                       │
│                                                              │
│  [컨텍스트 매칭]                                              │
│  ├─ "파일 업로드" + Android → 권한 거부, 저장소 접근          │
│  ├─ "로그인" + iOS → Face ID 실패, 백그라운드 복귀           │
│  └─ "결제" + Web → 세션 만료, 중복 탭                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
     │
     ▼
플랫폼별 엣지케이스 TC 생성
```

---

## 6.5 대화형 TC 세분화 (Interactive TC Refinement) - NEW

> **v2.0 추가**: Claude-Gemini 협업 합의에 따른 핵심 기능

### F-024: 대화형 TC 세분화 (Wizard UI)

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO TC 생성 과정에서 단계별 질문에 답하며 요구사항을 구체화하여
SO THAT AI가 내 요구사항에 정확히 맞는 맞춤형 TC를 생성할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 대화형 TC 세분화

  Scenario: 8단계 Wizard UI
    Given PRD가 업로드된 상태에서
    When "TC 생성" 버튼을 클릭하면
    Then 8단계 Wizard UI가 표시되고
    And 각 단계마다 진행률(1/8, 2/8...)이 표시된다

  Scenario: AI 기능 추출 및 사용자 편집 (Step 2)
    Given PRD 분석이 완료되면
    Then Epic > Feature > User Story 계층으로 기능이 추출되고
    And 드래그 앤 드롭으로 순서 변경이 가능하고
    And 클릭하여 추가/수정/삭제가 가능하다

  Scenario: PRD 분석 시각화
    Given AI가 기능을 추출하면
    Then PRD 원문에서 추출 근거가 하이라이팅되어 표시된다

  Scenario: 테스트 범위 질문 (Step 3)
    Given 기능 편집이 완료되면
    When 다음 단계로 이동하면
    Then 각 기능별로 테스트 범위 질문이 표시된다:
      - 정상 시나리오
      - 에러 케이스
      - 성능 테스트
      - 보안 테스트

  Scenario: 데이터 관점 질문 (Step 4)
    Given 테스트 범위 선택이 완료되면
    When 다음 단계로 이동하면
    Then 데이터 유형 선택 질문이 표시된다:
      - 정상 데이터
      - 비정상/예외 데이터 (SQL Injection, XSS 등)
      - 경계값 데이터 (최소/최대)

  Scenario: 사용자 페르소나 선택 (Step 5)
    Given 데이터 관점 선택이 완료되면
    When 다음 단계로 이동하면
    Then 사용자 유형 선택이 표시된다:
      - 신규 사용자 (튜토리얼, 온보딩)
      - 일반 사용자 (핵심 기능)
      - 파워 사용자 (고급 기능, 단축키)
      - 관리자 (어드민 기능)

  Scenario: 실시간 TC 미리보기
    Given TC 생성이 진행 중일 때
    Then 생성되는 TC가 실시간으로 오른쪽 패널에 표시되고
    And 예상 TC 개수가 옵션 선택 시마다 업데이트된다

  Scenario: 사전 설정 템플릿
    Given 테스트 범위 선택 화면에서
    When "스모크 테스트" 프리셋을 클릭하면
    Then 스모크 테스트에 적합한 옵션들이 자동 선택된다

  Scenario: 추가 요청 반영 (Step 8)
    Given TC 생성이 완료된 후
    When 추가 요청 입력란에 "결제 관련 엣지케이스 추가"를 입력하고
    And "추가 생성" 버튼을 클릭하면
    Then 추가 TC가 생성되어 목록에 추가된다
```

#### UI 요구사항

| 화면 | 요소 | 설명 |
|-----|------|------|
| Wizard | 진행률 표시 | Step 1/8, 2/8... + 프로그레스 바 |
| | 이전/다음 버튼 | 단계 이동 |
| | 취소 버튼 | 언제든 취소 가능 |
| Step 2 | 기능 트리 | Epic > Feature > User Story 계층 |
| | 드래그 핸들 | 순서 변경용 |
| | 편집/삭제 아이콘 | 각 항목 옆 |
| | PRD 원문 패널 | 하이라이팅된 원문 표시 |
| Step 3-5 | 체크박스 목록 | 다중 선택 가능 |
| | 실시간 카운터 | "예상 TC: N개" |
| | 프리셋 버튼 | 스모크/회귀/보안/접근성 |
| Step 7 | 분할 화면 | 좌: 진행 상황, 우: TC 미리보기 |
| Step 8 | 요약 카드 | 카테고리별 TC 수 |
| | 추가 요청 입력 | 자연어 입력 필드 |

---

### F-025: 부정적 TC 자동 생성

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO "만약 ~가 아니라면?" 시나리오가 자동 제안되어
SO THAT 놓치기 쉬운 에러 케이스를 빠짐없이 테스트할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 부정적 TC 자동 생성

  Scenario: 정상 TC에서 부정적 TC 자동 파생
    Given "유효한 이메일로 회원가입 성공" TC가 생성되면
    Then 다음 부정적 TC가 자동 제안된다:
      - "유효하지 않은 이메일 형식 입력 시 오류 메시지 표시"
      - "이미 가입된 이메일 입력 시 중복 안내"
      - "비밀번호 불일치 시 가입 버튼 비활성화"
      - "필수 항목 미입력 시 경고 표시"

  Scenario: 부정적 TC 카테고리 태깅
    Given 부정적 TC가 생성되면
    Then 카테고리가 "부정적 TC"로 자동 태깅되고
    And 필터에서 "부정적 TC만 보기"가 가능하다

  Scenario: 부정적 TC 토글
    Given TC 목록에서
    When 특정 부정적 TC를 제외하고 싶으면
    Then "제외" 토글로 비활성화할 수 있다
```

---

### F-026: 경계값 분석 자동 제안

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 입력 필드의 경계값 TC가 자동으로 생성되어
SO THAT 경계값 테스트를 누락 없이 수행할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 경계값 분석 자동 제안

  Scenario: 숫자/문자 제한 필드 경계값 TC 생성
    Given PRD에 "비밀번호는 8-20자"라는 제약이 있을 때
    Then 다음 경계값 TC가 자동 생성된다:
      - "7자 입력 시 오류 (최소-1)"
      - "8자 입력 시 성공 (최소)"
      - "20자 입력 시 성공 (최대)"
      - "21자 입력 시 오류 (최대+1)"

  Scenario: 경계값 TC 카테고리 태깅
    Given 경계값 TC가 생성되면
    Then 카테고리가 "경계값"으로 자동 태깅된다

  Scenario: 경계값 자동 탐지
    Given PRD 분석 시
    Then 숫자 범위, 문자 길이 제한 등이 자동 탐지되어
    And 해당 필드에 대한 경계값 TC가 제안된다
```

---

### F-027: PRD 분석 시각화

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A QA 엔지니어
I WANT TO AI가 어떤 근거로 기능을 추출했는지 확인하여
SO THAT AI 분석 결과를 신뢰하고 필요시 수정할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: PRD 분석 시각화

  Scenario: 원문 하이라이팅
    Given AI가 PRD에서 기능을 추출하면
    Then PRD 원문에서 해당 부분이 색상으로 하이라이팅된다

  Scenario: 하이라이트-기능 연결
    Given 하이라이팅된 PRD가 표시될 때
    When 특정 하이라이트를 클릭하면
    Then 해당 부분에서 추출된 기능이 강조 표시된다

  Scenario: 기능-원문 역추적
    Given 기능 목록이 표시될 때
    When 특정 기능을 클릭하면
    Then PRD 원문의 해당 부분으로 스크롤되고 하이라이팅된다
```

---

### F-028: 테스트 데이터 자동 생성

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트에 필요한 더미 데이터가 자동으로 채워져
SO THAT 테스트 데이터 준비 시간을 절약할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 테스트 데이터 자동 생성

  Scenario: 유효한 형식의 데이터 자동 생성
    Given TC에 "테스트 데이터" 컬럼이 있을 때
    Then AI가 적합한 더미 데이터를 자동 채운다:
      - 이메일: valid_user@example.com
      - 비밀번호: Test@1234
      - 전화번호: 010-1234-5678
      - 주소: 서울시 강남구 테스트로 123

  Scenario: 경계값 데이터 자동 생성
    Given 경계값 TC가 있을 때
    Then 해당 경계에 맞는 데이터가 자동 생성된다:
      - 7자 비밀번호: "Test@12"
      - 8자 비밀번호: "Test@123"

  Scenario: 데이터 재생성
    Given 자동 생성된 데이터가 있을 때
    When "재생성" 버튼을 클릭하면
    Then 새로운 더미 데이터가 생성된다
```

---

### F-029: 접근성 체크리스트

**우선순위**: P2 (Growth)

#### User Story

```
AS A QA 엔지니어
I WANT TO 기본 접근성 테스트 항목이 자동으로 포함되어
SO THAT 웹/앱 접근성 테스트를 빠짐없이 수행할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 접근성 체크리스트

  Scenario: 웹 접근성 TC 자동 추가
    Given Web 플랫폼이 선택되고 접근성 옵션이 활성화되면
    Then 다음 접근성 TC가 자동 추가된다:
      - "스크린 리더가 버튼 텍스트를 올바르게 읽는가?"
      - "키보드만으로 모든 기능 조작이 가능한가?"
      - "색상 대비가 WCAG 2.1 기준을 충족하는가?"
      - "포커스 인디케이터가 명확하게 표시되는가?"

  Scenario: 모바일 접근성 TC
    Given 모바일 플랫폼이 선택되고 접근성 옵션이 활성화되면
    Then 다음 접근성 TC가 자동 추가된다:
      - "TalkBack/VoiceOver로 모든 요소 접근 가능한가?"
      - "터치 타겟 크기가 44x44pt 이상인가?"
      - "확대 모드에서 UI가 깨지지 않는가?"

  Scenario: 접근성 프리셋
    Given 테스트 범위 선택에서
    When "접근성 테스트" 프리셋을 선택하면
    Then 접근성 관련 옵션이 자동 활성화된다
```

---

## 7. TC 관리 (Test Case Management)

### F-007: TC 목록 조회

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 생성된 테스트케이스 목록을 조회하여
SO THAT 전체 테스트 범위를 파악하고 관리할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: TC 목록 조회

  Scenario: 전체 TC 목록 조회
    Given 프로젝트에 TC가 생성된 상태에서
    When TC 목록 페이지에 접속하면
    Then 모든 TC가 테이블 형식으로 표시되고
    And 각 TC의 ID, 시나리오명, 플랫폼, 우선순위, 카테고리가 표시된다

  Scenario: TC 검색
    Given TC 목록에서
    When 검색창에 "로그인"을 입력하면
    Then 시나리오명 또는 기능에 "로그인"이 포함된 TC만 표시된다

  Scenario: TC 필터링
    Given TC 목록에서
    When 플랫폼 필터에서 "Android"를 선택하면
    Then Android TC만 표시된다
    When 우선순위 필터에서 "High"를 선택하면
    Then High 우선순위 TC만 표시된다

  Scenario: TC 정렬
    Given TC 목록에서
    When "우선순위" 컬럼 헤더를 클릭하면
    Then TC가 우선순위 기준으로 정렬된다

  Scenario: TC 상세 조회
    Given TC 목록에서
    When 특정 TC 행을 클릭하면
    Then TC 상세 정보가 사이드 패널 또는 모달로 표시된다
```

#### UI 요구사항

| 화면 | 요소 | 설명 |
|-----|------|------|
| TC 목록 | 검색창 | 실시간 검색 |
| | 필터 | 플랫폼, 우선순위, 카테고리, 기능 |
| | 테이블 | ID, 시나리오, 플랫폼, 우선순위, 카테고리 |
| | 페이지네이션 | 50개/페이지, 무한 스크롤 옵션 |
| | 일괄 선택 | 체크박스, 전체 선택 |
| TC 상세 | 모든 필드 | 읽기 전용 |
| | 편집 버튼 | "수정하기" |
| | 삭제 버튼 | "삭제" |

---

### F-008: TC 편집

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 생성된 테스트케이스를 수정하여
SO THAT AI 생성 결과를 보완하거나 커스터마이즈할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: TC 편집

  Scenario: TC 개별 편집
    Given TC 상세 화면에서
    When "수정하기" 버튼을 클릭하면
    Then 모든 필드가 편집 가능 상태가 되고
    And "저장" 및 "취소" 버튼이 표시된다

  Scenario: TC 저장
    Given TC 편집 중
    When 내용을 수정하고 "저장" 버튼을 클릭하면
    Then 변경 사항이 저장되고
    And "저장되었습니다" 토스트가 표시된다

  Scenario: TC 삭제
    Given TC 상세 화면에서
    When "삭제" 버튼을 클릭하고
    And 확인 모달에서 "삭제"를 클릭하면
    Then TC가 삭제되고
    And TC 목록으로 이동한다

  Scenario: TC 일괄 삭제
    Given TC 목록에서 여러 TC를 선택한 상태에서
    When "선택 삭제" 버튼을 클릭하고
    And 확인 모달에서 "삭제"를 클릭하면
    Then 선택된 모든 TC가 삭제된다

  Scenario: TC 복제
    Given TC 상세 화면에서
    When "복제" 버튼을 클릭하면
    Then 동일한 내용의 새 TC가 생성되고
    And 편집 모드로 열린다
```

---

### F-012: TC 우선순위

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트케이스에 우선순위를 지정하여
SO THAT 중요한 테스트부터 실행할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: TC 우선순위

  Scenario: AI 자동 우선순위 부여
    Given TC 생성 시
    Then AI가 다음 기준으로 우선순위를 부여한다:
      - High: 핵심 기능, 결제, 인증
      - Medium: 일반 기능
      - Low: 엣지케이스, 예외 처리

  Scenario: 우선순위 수동 변경
    Given TC 목록 또는 상세에서
    When 우선순위 드롭다운을 클릭하고
    And 새 우선순위를 선택하면
    Then 즉시 변경되고 저장된다

  Scenario: 우선순위별 정렬
    Given TC 목록에서
    When "우선순위순 정렬"을 선택하면
    Then High → Medium → Low 순으로 정렬된다
```

---

### F-013: TC 카테고리

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트케이스를 기능별로 그룹핑하여
SO THAT 특정 기능의 테스트를 쉽게 찾을 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: TC 카테고리

  Scenario: AI 자동 카테고리 분류
    Given TC 생성 시
    Then PRD 기능 단위로 카테고리가 자동 생성된다:
      - 회원가입/로그인
      - 메인 피드
      - 상품 상세
      - 결제
      ...

  Scenario: 카테고리 필터
    Given TC 목록에서
    When 카테고리 필터에서 "회원가입/로그인"을 선택하면
    Then 해당 카테고리 TC만 표시된다

  Scenario: 카테고리 수정
    Given TC 상세에서
    When 카테고리를 변경하면
    Then 즉시 반영된다

  Scenario: 새 카테고리 생성
    Given TC 편집 시
    When 카테고리 입력란에 새 이름을 입력하면
    Then 새 카테고리가 생성되고 선택된다
```

---

## 8. Export (내보내기)

### F-009: Excel Export (표준 템플릿)

**우선순위**: P0 (MVP)

> **v2.0 업데이트**: Claude-Gemini 협업 합의에 따른 ISTQB 표준 기반 템플릿 적용

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트케이스를 업계 표준 Excel 템플릿으로 내보내어
SO THAT 기존 워크플로우에서 활용하고 Jira/TestRail과 연동할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: Excel Export (표준 템플릿)

  Scenario: 전체 TC Export
    Given TC 목록에서
    When "Export" 버튼을 클릭하고
    And "Excel (.xlsx)"를 선택하면
    Then 표준 템플릿 형식의 Excel 파일이 다운로드된다

  Scenario: 선택 TC Export
    Given TC 목록에서 일부 TC를 선택한 상태에서
    When "Export" 버튼을 클릭하면
    Then 선택된 TC만 포함된 파일이 다운로드된다

  Scenario: 필터링된 TC Export
    Given TC 목록에서 필터가 적용된 상태에서
    When "Export" 버튼을 클릭하면
    Then 필터링된 TC만 포함된 파일이 다운로드된다

  Scenario: 표준 시트 구조
    Given Excel 파일이 다운로드되면
    Then 다음 시트가 포함된다:
      - Overview (프로젝트 요약)
      - Test Cases (TC 목록 - 엣지케이스 통합)
      - Execution Log (실행 기록)
      - Defect Mapping (결함 매핑)
      - Coverage Matrix (커버리지)
      - Glossary (용어 정의)

  Scenario: Test Cases 시트 컬럼
    Given Test Cases 시트를 확인하면
    Then 다음 16개 컬럼이 포함된다:
      - TC-ID, 기능, 시나리오, 전제조건
      - 테스트단계, 예상결과, 테스트 데이터 (NEW)
      - 실행 후 조건 (NEW), 플랫폼
      - 카테고리 (기능/엣지케이스/경계값/부정적/성능/보안)
      - 우선순위 (P0/P1/P2/P3), 상태
      - 연관 요구사항 ID (NEW), 테스트 환경 (NEW)
      - 담당자, 비고

  Scenario: 데이터 유효성 검사
    Given Excel 파일이 다운로드되면
    Then 다음 컬럼에 드롭다운이 적용된다:
      - 플랫폼: Android, iOS, Web, PC, All
      - 카테고리: 기능, 엣지케이스, 경계값, 부정적, 성능, 보안
      - 우선순위: P0, P1, P2, P3
      - 상태: 미실행, 통과, 실패, 차단, 건너뜀

  Scenario: 조건부 서식
    Given Excel 파일이 다운로드되면
    Then 다음 조건부 서식이 적용된다:
      - 상태=실패 → 빨간 배경
      - 상태=통과 → 초록 배경
      - 우선순위=P0 → 굵은 글씨
```

#### Excel 템플릿 구조

| 시트명 | 용도 | 주요 컬럼 |
|-------|------|----------|
| **Overview** | 프로젝트 요약 | 프로젝트명, 버전, 작성일, 플랫폼, 총 TC 수 |
| **Test Cases** | TC 목록 (통합) | 16개 컬럼 (상세 명세 참조) |
| **Execution Log** | 실행 기록 | TC-ID, 실행일, 실행자, 결과, 스크린샷 |
| **Defect Mapping** | 결함 매핑 | TC-ID, 결함ID, 심각도, 상태, 재현단계 |
| **Coverage Matrix** | 커버리지 | 요구사항ID, 관련TC, 커버리지상태 |
| **Glossary** | 용어 정의 | 용어, 약어, 정의, 예시, 관련 문서 |

#### UI 요구사항

| 화면 | 요소 | 설명 |
|-----|------|------|
| Export 버튼 | 드롭다운 | Excel, CSV, Notion, TestRail |
| Export 옵션 | 범위 선택 | 전체/선택/필터 |
| | 템플릿 선택 | 표준 템플릿 / 간소화 템플릿 |
| | 포함 시트 | 체크박스로 선택 |
| | 파일명 | 기본값: {프로젝트명}_TC_{날짜}.xlsx |

#### 기술 요구사항

- 라이브러리: xlsx 또는 exceljs
- 데이터 유효성: Excel Data Validation 적용
- 조건부 서식: Conditional Formatting 적용
- 인코딩: UTF-8 (한글 지원)
- 셀 서식: 자동 줄바꿈, 열 너비 자동 조정

---

### F-011: CSV Export

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트케이스를 CSV 파일로 내보내어
SO THAT 다른 도구나 스크립트에서 활용할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: CSV Export

  Scenario: CSV 다운로드
    Given TC 목록에서
    When "Export" → "CSV"를 선택하면
    Then UTF-8 인코딩된 CSV 파일이 다운로드된다

  Scenario: CSV 형식
    Given CSV 파일이 다운로드되면
    Then 첫 행은 헤더이고
    And 쉼표(,)로 구분되며
    And 줄바꿈 포함 필드는 따옴표로 감싸진다
```

---

### F-020: TestRail 연동

**우선순위**: P2 (Growth)

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트케이스를 TestRail에 직접 푸시하여
SO THAT 기존 TestRail 워크플로우와 통합할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: TestRail 연동

  Scenario: TestRail 계정 연결
    Given 프로젝트 설정에서
    When TestRail URL, 이메일, API 키를 입력하고
    And "연결 테스트" 버튼을 클릭하면
    Then 연결 성공/실패 결과가 표시된다

  Scenario: TestRail로 푸시
    Given TestRail이 연결된 상태에서
    When "Export" → "TestRail로 보내기"를 선택하고
    And 대상 프로젝트와 테스트 스위트를 선택하면
    Then TC가 TestRail에 생성되고
    And 완료 메시지가 표시된다

  Scenario: 동기화
    Given TestRail에 이미 푸시된 TC가 있을 때
    When TC를 수정하고 다시 푸시하면
    Then 기존 TC가 업데이트된다 (덮어쓰기/신규 선택 가능)
```

---

## 9. 팀 협업 (Team Collaboration)

### F-015: 팀 협업

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A 팀 리드
I WANT TO 팀원을 프로젝트에 초대하여
SO THAT 함께 테스트케이스를 관리할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 팀 협업

  Scenario: 팀원 초대
    Given 프로젝트 소유자가 설정에서
    When "팀원 초대" 버튼을 클릭하고
    And 이메일 주소와 역할을 입력하면
    Then 초대 이메일이 발송되고
    And 대기 중 초대 목록에 추가된다

  Scenario: 초대 수락
    Given 초대 이메일을 받은 사용자가
    When 초대 링크를 클릭하면
    Then 해당 프로젝트에 팀원으로 추가되고
    And 프로젝트 목록에 표시된다

  Scenario: 역할별 권한
    Given 역할이 다음과 같이 정의된다:
      | 역할 | 권한 |
      | Owner | 모든 권한, 프로젝트 삭제 |
      | Admin | TC CRUD, 팀원 관리, 설정 변경 |
      | Member | TC CRUD |
      | Viewer | TC 조회, Export만 |

  Scenario: 팀원 제거
    Given 프로젝트 설정에서
    When 팀원의 "제거" 버튼을 클릭하면
    Then 해당 팀원이 프로젝트에서 제거된다
```

---

### F-016: TC 댓글

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트케이스에 댓글을 남겨
SO THAT 팀원과 리뷰 의견을 주고받을 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: TC 댓글

  Scenario: 댓글 작성
    Given TC 상세 화면에서
    When 댓글 입력란에 내용을 작성하고
    And "게시" 버튼을 클릭하면
    Then 댓글이 추가되고
    And 작성자, 시간이 표시된다

  Scenario: 댓글 수정/삭제
    Given 내가 작성한 댓글에서
    When "수정" 또는 "삭제"를 클릭하면
    Then 해당 작업이 수행된다

  Scenario: 댓글 알림
    Given TC에 댓글이 달리면
    Then 해당 TC 작성자에게 알림이 전송된다
```

---

## 10. 기타 기능

### F-014: 요구사항-TC 추적성

**우선순위**: P1 (Early Adopter)

#### User Story

```
AS A QA 리드
I WANT TO 요구사항과 테스트케이스의 매핑을 확인하여
SO THAT 요구사항 커버리지를 검증할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 추적성 매트릭스

  Scenario: 자동 매핑
    Given PRD에서 추출된 요구사항이 있을 때
    Then 각 TC가 관련 요구사항에 자동 매핑된다

  Scenario: 매트릭스 조회
    Given 추적성 메뉴에서
    Then 행(요구사항) x 열(TC) 매트릭스가 표시되고
    And 커버되지 않은 요구사항이 하이라이트된다

  Scenario: 수동 매핑
    Given TC 편집에서
    When 관련 요구사항을 추가/제거하면
    Then 매트릭스에 반영된다
```

---

### F-021: 버전 관리

**우선순위**: P2 (Growth)

#### User Story

```
AS A QA 엔지니어
I WANT TO TC 변경 이력을 확인하여
SO THAT 이전 버전으로 복원하거나 변경 사유를 파악할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 버전 관리

  Scenario: 변경 이력 조회
    Given TC 상세에서 "히스토리" 탭을 클릭하면
    Then 변경 일시, 변경자, 변경 내용이 표시된다

  Scenario: 이전 버전 복원
    Given 변경 이력에서
    When 특정 버전의 "복원" 버튼을 클릭하면
    Then TC가 해당 버전으로 복원된다
```

---

### F-022: BDD/Gherkin 출력

**우선순위**: P2 (Growth)

#### User Story

```
AS A 개발자
I WANT TO TC를 Gherkin 형식으로 받아
SO THAT BDD 테스트 자동화에 활용할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: BDD 출력

  Scenario: Gherkin 형식 Export
    Given TC 목록에서
    When "Export" → "Gherkin (.feature)"을 선택하면
    Then Given-When-Then 형식의 .feature 파일이 다운로드된다

  Scenario: Gherkin 미리보기
    Given TC 상세에서 "Gherkin" 탭을 클릭하면
    Then Given-When-Then 형식으로 변환된 내용이 표시된다
```

---

### F-023: 분석 대시보드

**우선순위**: P2 (Growth)

#### User Story

```
AS A QA 리드
I WANT TO 전체 TC 현황을 대시보드로 확인하여
SO THAT 테스트 진행 상황을 한눈에 파악할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: 분석 대시보드

  Scenario: 대시보드 조회
    Given 프로젝트 대시보드에서
    Then 다음 지표가 표시된다:
      - 총 TC 수
      - 플랫폼별 TC 수 (차트)
      - 우선순위별 분포 (차트)
      - 카테고리별 분포 (차트)
      - 최근 생성/수정된 TC

  Scenario: 기간 필터
    Given 대시보드에서
    When 기간 필터를 변경하면
    Then 해당 기간 데이터로 갱신된다
```

---

## 11. 부록

### A. API 엔드포인트 (예정)

| 메서드 | 엔드포인트 | 설명 |
|-------|-----------|------|
| POST | /api/auth/signup | 회원가입 |
| POST | /api/auth/login | 로그인 |
| GET | /api/projects | 프로젝트 목록 |
| POST | /api/projects | 프로젝트 생성 |
| POST | /api/projects/:id/upload | PRD 업로드 |
| POST | /api/projects/:id/generate | TC 생성 |
| GET | /api/projects/:id/testcases | TC 목록 |
| PUT | /api/testcases/:id | TC 수정 |
| DELETE | /api/testcases/:id | TC 삭제 |
| GET | /api/projects/:id/export | Export |

### B. 데이터 모델 (예정)

```
User
├─ id: uuid
├─ email: string
├─ name: string
├─ created_at: timestamp
└─ updated_at: timestamp

Project
├─ id: uuid
├─ name: string
├─ description: string
├─ user_id: uuid (owner)
├─ created_at: timestamp
└─ updated_at: timestamp

ProjectMember
├─ project_id: uuid
├─ user_id: uuid
├─ role: enum (owner, admin, member, viewer)
└─ joined_at: timestamp

PRD
├─ id: uuid
├─ project_id: uuid
├─ file_url: string
├─ file_name: string
├─ page_count: int
├─ extracted_text: text
├─ created_at: timestamp
└─ updated_at: timestamp

TestCase
├─ id: uuid
├─ project_id: uuid
├─ prd_id: uuid
├─ tc_number: string (TC-001)
├─ feature: string
├─ scenario: string
├─ precondition: text
├─ steps: text[]
├─ expected_result: text
├─ platform: enum
├─ category: string
├─ priority: enum (high, medium, low)
├─ is_edge_case: boolean
├─ is_active: boolean
├─ created_at: timestamp
└─ updated_at: timestamp

Comment
├─ id: uuid
├─ test_case_id: uuid
├─ user_id: uuid
├─ content: text
├─ created_at: timestamp
└─ updated_at: timestamp
```

---

*Document generated by Planning Agent - Feature Spec Skill*
