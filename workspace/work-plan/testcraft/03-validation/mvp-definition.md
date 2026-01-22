# TestCraft - MVP Definition

> 핵심 가설 검증을 위한 최소 기능 정의

---

## 1. MVP Philosophy

### 핵심 원칙

```
┌─────────────────────────────────────────────────────────────────┐
│                      MVP Philosophy                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   "PRD를 넣으면 테스트케이스가 나온다"                           │
│                                                                  │
│   이 한 가지가 작동하면 MVP는 성공                               │
│                                                                  │
│   ┌──────────┐      ┌──────────┐      ┌──────────┐             │
│   │   PRD    │ ───▶ │    AI    │ ───▶ │   TC     │             │
│   │  Upload  │      │  Engine  │      │  Output  │             │
│   └──────────┘      └──────────┘      └──────────┘             │
│                                                                  │
│   검증 기간: 8주                                                 │
│   목표 사용자: 100명 (Free), 10명 (Paid)                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Hypotheses (핵심 가설)

### Hypothesis 1: Problem-Solution Fit

| 가설 | 검증 지표 | 성공 기준 |
|-----|----------|----------|
| QA 담당자는 PRD→TC 변환에 과도한 시간을 쓰고 있다 | 사용자 인터뷰 | 80%가 "주 5시간 이상" 응답 |
| TestCraft가 이 시간을 80% 이상 줄여줄 수 있다 | TC 생성 시간 측정 | 평균 30분 이내 완료 |

### Hypothesis 2: Value Proposition

| 가설 | 검증 지표 | 성공 기준 |
|-----|----------|----------|
| AI 생성 TC가 수동 작성 TC 품질의 80% 이상이다 | QA 전문가 품질 평가 | 10명 중 8명 "실무 사용 가능" |
| 플랫폼별 엣지케이스가 핵심 차별점이다 | 기능 사용률 | 엣지케이스 사용률 60% 이상 |

### Hypothesis 3: Willingness to Pay

| 가설 | 검증 지표 | 성공 기준 |
|-----|----------|----------|
| 월 $12에 기꺼이 결제할 의향이 있다 | Free → Paid 전환율 | 5% 이상 |
| 팀 단위 도입 시 $22/user 지불 | Team 플랜 선택률 | Pro 대비 30% |

---

## 3. MVP Scope (MoSCoW)

### Must Have (MVP 필수)

| # | 기능 | 설명 | 가설 연결 |
|---|------|------|----------|
| M1 | **PRD 업로드** | PDF, MD, DOCX 파일 업로드 | H1 |
| M2 | **플랫폼 선택** | Android, iOS, Web 중 택1 | H2 |
| M3 | **TC 자동 생성** | GPT-4 기반 TC 생성 | H1 |
| M4 | **엣지케이스 포함** | 플랫폼별 기본 엣지케이스 | H2 |
| M5 | **CSV Export** | 결과물 다운로드 | H1 |
| M6 | **사용자 인증** | 이메일 로그인, Google OAuth | H3 |
| M7 | **사용량 제한** | Free: 5TC/월 | H3 |

### Should Have (MVP 후 1차)

| # | 기능 | 설명 | 우선순위 |
|---|------|------|---------|
| S1 | Excel Export | 서식 포함 Excel 파일 | High |
| S2 | TC 수정/편집 | 웹에서 직접 편집 | High |
| S3 | 히스토리 | 이전 생성 TC 목록 | High |
| S4 | 팀 멤버 초대 | 기본 팀 기능 | Medium |

### Could Have (향후 로드맵)

| # | 기능 | 설명 | 예상 시점 |
|---|------|------|----------|
| C1 | TestRail 연동 | 직접 Export | Month 6 |
| C2 | Jira 연동 | 이슈 자동 생성 | Month 6 |
| C3 | Notion Export | 노션 형식 Export | Month 4 |
| C4 | 커스텀 템플릿 | TC 포맷 커스터마이징 | Month 5 |
| C5 | API 제공 | CI/CD 연동용 | Month 8 |

### Won't Have (MVP 제외)

| # | 기능 | 제외 이유 |
|---|------|----------|
| W1 | 자체 TC 관리 시스템 | 기존 도구와 경쟁 피함 |
| W2 | 테스트 실행 기능 | 범위 확장 방지 |
| W3 | 다국어 지원 | 초기 타겟 한국/영어권 |
| W4 | 모바일 앱 | 웹 우선 |

---

## 4. MVP Feature Specification

### M1: PRD 업로드

```
┌─────────────────────────────────────────────────────────┐
│                    PRD Upload Flow                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Supported Formats:                                      │
│  ├── PDF (.pdf) - 최대 10MB                             │
│  ├── Markdown (.md) - 최대 1MB                          │
│  ├── Word (.docx) - 최대 10MB                           │
│  └── Plain Text (.txt) - 최대 1MB                       │
│                                                          │
│  Processing:                                             │
│  1. 파일 유효성 검증                                     │
│  2. 텍스트 추출 (pdf-parse, mammoth)                    │
│  3. 구조 분석 (섹션, 기능 목록)                          │
│  4. 요구사항 추출                                        │
│                                                          │
│  Error Handling:                                         │
│  - 지원되지 않는 형식 → "지원 형식: PDF, MD, DOCX"      │
│  - 파일 크기 초과 → "최대 10MB까지 업로드 가능"         │
│  - 파싱 실패 → "파일을 읽을 수 없습니다. 다시 시도"     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### M2: 플랫폼 선택

```
┌─────────────────────────────────────────────────────────┐
│                  Platform Selection                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [Android]     [iOS]     [Web]     [PC] (Phase 2)       │
│      ○           ○         ●          ○                 │
│                                                          │
│  선택 시 적용되는 엣지케이스:                            │
│                                                          │
│  Android:                                                │
│  - 백버튼 처리                                           │
│  - 생명주기 (백그라운드/포그라운드)                      │
│  - 권한 요청 시나리오                                    │
│  - 다양한 해상도/밀도                                    │
│                                                          │
│  iOS:                                                    │
│  - 제스처 네비게이션                                     │
│  - 앱 전환 시 상태 유지                                  │
│  - Face ID/Touch ID                                      │
│  - 노치/다이나믹 아일랜드                                │
│                                                          │
│  Web:                                                    │
│  - 브라우저 호환성 (Chrome, Safari, Firefox)             │
│  - 반응형 브레이크포인트                                 │
│  - 새로고침/뒤로가기                                     │
│  - 쿠키/로컬스토리지                                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### M3: TC 자동 생성

```
┌─────────────────────────────────────────────────────────┐
│                 TC Generation Engine                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Input:                                                  │
│  ├── 추출된 요구사항 목록                               │
│  ├── 선택된 플랫폼                                       │
│  └── 플랫폼별 엣지케이스 라이브러리                     │
│                                                          │
│  Process (GPT-4):                                        │
│  1. 요구사항 → 테스트 시나리오 변환                     │
│  2. 각 시나리오 → 상세 테스트 스텝 생성                 │
│  3. 플랫폼 엣지케이스 매칭 및 추가                      │
│  4. 우선순위 태깅 (High/Medium/Low)                     │
│                                                          │
│  Output Structure:                                       │
│  ├── TC ID                                               │
│  ├── 테스트 시나리오 제목                               │
│  ├── 사전 조건 (Precondition)                           │
│  ├── 테스트 스텝 (Steps)                                │
│  ├── 예상 결과 (Expected Result)                        │
│  ├── 우선순위 (Priority)                                │
│  ├── 플랫폼 태그                                        │
│  └── 엣지케이스 여부                                    │
│                                                          │
│  Generation Time: 평균 30초 ~ 2분 (PRD 복잡도에 따라)   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### M4: 엣지케이스 포함

```
┌─────────────────────────────────────────────────────────┐
│               Edge Case Library (MVP)                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  공통 엣지케이스 (20개):                                 │
│  ├── 네트워크 오프라인/불안정                           │
│  ├── 빈 상태 (Empty State)                              │
│  ├── 경계값 입력 (최소/최대)                            │
│  ├── 특수문자/이모지 입력                               │
│  ├── 동시성 (중복 요청)                                 │
│  └── ...                                                 │
│                                                          │
│  Android 전용 (15개):                                    │
│  ├── 하드웨어 백버튼                                    │
│  ├── 앱 강제 종료 후 재시작                             │
│  ├── 권한 거부 시나리오                                 │
│  └── ...                                                 │
│                                                          │
│  iOS 전용 (15개):                                        │
│  ├── 스와이프 백 제스처                                 │
│  ├── 시스템 다크모드 전환                               │
│  ├── 생체 인증 실패                                     │
│  └── ...                                                 │
│                                                          │
│  Web 전용 (15개):                                        │
│  ├── 브라우저 탭 전환                                   │
│  ├── 세션 만료                                          │
│  ├── 다중 탭 동시 사용                                  │
│  └── ...                                                 │
│                                                          │
│  Total MVP: 65개 엣지케이스                              │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### M5-M7: 기타 필수 기능

```
M5: CSV Export
├── UTF-8 BOM (한글 호환)
├── 컬럼: TC ID, 시나리오, 사전조건, 스텝, 예상결과, 우선순위, 태그
└── 파일명: TestCraft_{날짜}_{PRD명}.csv

M6: 사용자 인증
├── 이메일/비밀번호 로그인
├── Google OAuth 2.0
├── 이메일 인증 (옵션)
└── 비밀번호 재설정

M7: 사용량 제한
├── Free: 5 TC 생성/월
├── 카운터 표시: "이번 달 3/5 TC 사용"
├── 한도 도달 시 업그레이드 유도 모달
└── 매월 1일 리셋
```

---

## 5. Technical MVP Architecture

### Tech Stack

```
┌─────────────────────────────────────────────────────────┐
│                   MVP Tech Stack                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Frontend:                                               │
│  ├── Next.js 14 (App Router)                            │
│  ├── TypeScript                                          │
│  ├── Tailwind CSS                                        │
│  └── shadcn/ui                                           │
│                                                          │
│  Backend:                                                │
│  ├── Next.js API Routes                                  │
│  ├── Supabase (Auth + DB)                               │
│  └── OpenAI GPT-4 API                                    │
│                                                          │
│  Infrastructure:                                         │
│  ├── Vercel (Hosting)                                    │
│  ├── Supabase (PostgreSQL)                              │
│  └── Cloudflare R2 (File Storage)                       │
│                                                          │
│  3rd Party:                                              │
│  ├── pdf-parse (PDF 파싱)                               │
│  ├── mammoth (DOCX 파싱)                                │
│  ├── Stripe (결제)                                       │
│  └── Resend (이메일)                                     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Data Model (Simplified)

```sql
-- Users
users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE,
  plan ENUM('free', 'pro', 'team'),
  tc_count_this_month INT DEFAULT 0,
  created_at TIMESTAMP
)

-- Projects (PRD)
projects (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  name VARCHAR,
  platform ENUM('android', 'ios', 'web'),
  prd_content TEXT,
  created_at TIMESTAMP
)

-- Test Cases
test_cases (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects,
  scenario VARCHAR,
  precondition TEXT,
  steps TEXT[],
  expected_result TEXT,
  priority ENUM('high', 'medium', 'low'),
  is_edge_case BOOLEAN,
  tags VARCHAR[]
)
```

---

## 6. MVP Timeline

### 8-Week Plan

```
Week 1-2: Foundation
├── 프로젝트 셋업 (Next.js, Supabase)
├── 인증 시스템 구현
├── 기본 UI 레이아웃
└── 파일 업로드 기능

Week 3-4: Core Engine
├── PRD 파싱 로직
├── GPT-4 TC 생성 프롬프트 개발
├── 엣지케이스 라이브러리 구축
└── 생성 결과 DB 저장

Week 5-6: Output & Polish
├── TC 결과 화면
├── CSV Export
├── 사용량 제한 로직
├── UI/UX 개선

Week 7-8: Launch Prep
├── 결제 연동 (Stripe)
├── 랜딩 페이지
├── 버그 수정 및 테스트
└── 베타 사용자 초대
```

### Milestones

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 2 | Alpha | 로그인 + 파일 업로드 작동 |
| 4 | Internal Beta | TC 생성 E2E 작동 |
| 6 | Closed Beta | 10명 외부 테스터 |
| 8 | Public Launch | Product Hunt 준비 완료 |

---

## 7. Success Criteria

### MVP 성공 기준 (Week 8 기준)

| 카테고리 | 지표 | 목표 | 측정 방법 |
|---------|------|------|----------|
| **Acquisition** | 가입자 수 | 100명 | Supabase Auth |
| **Activation** | 첫 TC 생성 | 60% | DB Query |
| **Quality** | TC 품질 만족도 | 4.0/5.0 | 사용자 설문 |
| **Revenue** | 유료 전환 | 5명 | Stripe |
| **Retention** | 2주 재방문 | 30% | Analytics |

### Go/No-Go 기준

```
┌─────────────────────────────────────────────────────────┐
│                  GO/NO-GO Decision                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  GO (다음 단계 진행):                                    │
│  ├── 3개 이상 핵심 지표 달성                            │
│  ├── TC 품질 만족도 4.0 이상                            │
│  └── 유료 전환 3명 이상                                 │
│                                                          │
│  PIVOT (방향 수정):                                      │
│  ├── 가입자 100명 이상, but 활성화 30% 미만             │
│  └── TC 품질 불만족, but 문제 해결 가능                 │
│                                                          │
│  NO-GO (중단 검토):                                      │
│  ├── 가입자 30명 미만                                   │
│  ├── TC 품질 만족도 3.0 미만                            │
│  └── 유료 전환 0명                                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Risk & Mitigation

### Technical Risks

| 리스크 | 확률 | 영향 | 완화 전략 |
|-------|------|------|----------|
| AI 품질 불안정 | Medium | High | 프롬프트 반복 최적화, 품질 필터 |
| PRD 파싱 실패 | Medium | Medium | 다양한 포맷 테스트, 폴백 옵션 |
| 비용 초과 | Low | Medium | 사용량 모니터링, 캐싱 |

### Market Risks

| 리스크 | 확률 | 영향 | 완화 전략 |
|-------|------|------|----------|
| 경쟁사 유사 출시 | Medium | Medium | 빠른 출시, 엣지케이스 차별화 |
| 낮은 관심도 | Medium | High | 콘텐츠 마케팅 선행 |
| 유료 전환 저조 | Medium | High | Free 한도 조정, 가치 증명 |

---

## 9. Post-MVP Roadmap

### Phase 2 (Month 3-4)

- Excel Export (서식 포함)
- TC 수정/편집 기능
- 히스토리 기능
- PC 플랫폼 추가

### Phase 3 (Month 5-6)

- Notion Export
- TestRail 연동
- 커스텀 템플릿
- 팀 협업 기능

### Phase 4 (Month 7-12)

- Jira 연동
- API 제공
- 엔터프라이즈 기능
- 추가 엣지케이스 라이브러리

---

## 10. Summary

### MVP 한 문장 정의

> "PRD 파일을 업로드하면 플랫폼별 엣지케이스가 포함된 테스트케이스를 CSV로 다운로드할 수 있는 웹 서비스"

### MVP 핵심 기능

```
┌─────────────────────────────────────────────────────────┐
│                     MVP = 7 Features                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│   1. PRD 업로드 (PDF/MD/DOCX)                           │
│   2. 플랫폼 선택 (Android/iOS/Web)                      │
│   3. TC 자동 생성 (GPT-4)                               │
│   4. 엣지케이스 포함 (65개 라이브러리)                  │
│   5. CSV Export                                          │
│   6. 사용자 인증 (Email/Google)                         │
│   7. 사용량 제한 (Free 5TC/월)                          │
│                                                          │
│   개발 기간: 8주                                         │
│   목표: 100 Free, 5 Paid                                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

*Generated by Planning Agent - MVP Definition Skill*
*Last Updated: 2026-01-16*
