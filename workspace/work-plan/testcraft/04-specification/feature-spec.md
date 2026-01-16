# Feature Specification: TestCraft

> 기능 명세서
> 버전: 1.0
> 작성일: 2026-01-16
> 상태: Draft

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

### F-009: Excel Export

**우선순위**: P0 (MVP)

#### User Story

```
AS A QA 엔지니어
I WANT TO 테스트케이스를 Excel 파일로 내보내어
SO THAT 기존 워크플로우에서 활용하거나 외부 공유할 수 있다
```

#### Acceptance Criteria

```gherkin
Feature: Excel Export

  Scenario: 전체 TC Export
    Given TC 목록에서
    When "Export" 버튼을 클릭하고
    And "Excel (.xlsx)"를 선택하면
    Then 모든 TC가 포함된 Excel 파일이 다운로드된다

  Scenario: 선택 TC Export
    Given TC 목록에서 일부 TC를 선택한 상태에서
    When "Export" 버튼을 클릭하면
    Then 선택된 TC만 포함된 파일이 다운로드된다

  Scenario: 필터링된 TC Export
    Given TC 목록에서 필터가 적용된 상태에서
    When "Export" 버튼을 클릭하면
    Then 필터링된 TC만 포함된 파일이 다운로드된다

  Scenario: Export 파일 형식
    Given Excel 파일이 다운로드되면
    Then 다음 컬럼이 포함된다:
      - TC ID
      - 기능
      - 시나리오
      - 전제 조건
      - 테스트 단계 (줄바꿈 포함)
      - 예상 결과
      - 플랫폼
      - 카테고리
      - 우선순위
```

#### UI 요구사항

| 화면 | 요소 | 설명 |
|-----|------|------|
| Export 버튼 | 드롭다운 | Excel, CSV, Notion, TestRail |
| Export 옵션 | 범위 선택 | 전체/선택/필터 |
| | 포함 컬럼 | 체크박스로 선택 |
| | 파일명 | 기본값: {프로젝트명}_{날짜}.xlsx |

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
