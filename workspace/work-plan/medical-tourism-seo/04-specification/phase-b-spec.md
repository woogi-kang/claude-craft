# Phase B 상세 구현 명세서

> 프로젝트: MediScope (CheckYourHospital)
> Phase: B — 최적화 서비스 도구
> 작성일: 2026-03-27
> 기반 문서: PRD v1.0 (Phase A/A+ 구현 완료 기준)

---

## 1. 개요

### 1.1 Phase B 목표

Phase A/A+에서 구축한 진단 도구를 **수익화 가능한 서비스 플랫폼**으로 확장한다.
무료 진단 → 리드 전환 → 유료 프로젝트 관리까지 전체 영업 퍼널을 완성하고,
관리자/고객 양측의 대시보드를 고도화한다.

### 1.2 5가지 기능 요약

| 우선순위 | 기능 | 비즈니스 가치 | 난이도 |
|:--------:|------|--------------|:------:|
| **P0** | 관리자 인증 (Admin Auth) | 보안 필수 — 인증 없이 다른 기능 출시 불가 | 낮음 |
| **P1** | 다국어 진단 체크 (Multilingual Check) | 진단 완성도 100% — 예비 5% 가중치 활용 | 중간 |
| **P2** | PDF 리포트 생성 | 리드 이메일에 PDF 첨부 → 전환율 향상 핵심 | 중간 |
| **P3** | Before/After 비교 리포트 | 유료 고객에게 최적화 효과 증명 → 재계약 근거 | 중간 |
| **P4** | 프로젝트 관리 대시보드 | 유료 서비스 운영 인프라 — 영업 전환의 마지막 조각 | 높음 |

### 1.3 우선순위 정당화

1. **Admin Auth (P0)**: 현재 `/admin/*` 경로에 접근 제한이 없다. 리드/진단 데이터가 공개 상태이므로 보안 최우선 조치.
2. **Multilingual Check (P1)**: scorer.py에 예비 5% 가중치가 남아있고, PRD F1.4에 명세된 항목. 진단 커버리지를 100%로 완성.
3. **PDF 리포트 (P2)**: PRD의 Core Flow에서 리드 수집 후 PDF 발송이 핵심 전환 트리거. 현재 HTML만 제공하므로 전환율 개선 필수.
4. **Before/After (P3)**: score_history 테이블이 이미 존재하고 데이터 축적 중. 유료 고객에게 ROI를 시각화하여 재계약을 유도.
5. **프로젝트 관리 (P4)**: projects 테이블이 이미 존재하나 미사용. 유료 고객 관리의 백본이지만 다른 기능에 의존하므로 최후순위.

---

## 2. 기능별 상세 명세

---

### 2.1 관리자 인증 (Admin Auth) — P0

#### 2.1.1 목적 및 비즈니스 가치

- 현재 `/admin/*` 경로가 인증 없이 접근 가능 → 리드 데이터, 진단 결과, 구독 정보가 공개 상태
- Supabase Auth 기반 email/password 인증으로 보호
- `app_metadata.role = 'admin'` 체크로 일반 사용자와 관리자를 구분

#### 2.1.2 현재 상태 분석

- `/admin/login/page.tsx`: Supabase Auth `signInWithPassword` 로직 **이미 구현됨**
- `createClient()` (브라우저용), `createServerSupabaseClient()` (서버용) 존재
- RLS 정책에서 `app_metadata.role = 'admin'` 체크 **이미 적용됨**
- **누락된 것**: Next.js middleware에서 `/admin/*` 경로 보호 + 로그인 페이지에서 admin role 검증

#### 2.1.3 기술 스펙

**신규 파일:**

| 파일 | 역할 |
|------|------|
| `apps/web/src/middleware.ts` | `/admin/*` 경로 보호 (로그인 세션 없으면 `/admin/login`으로 리다이렉트) |
| `apps/web/src/lib/auth.ts` | admin role 검증 유틸리티 |

**변경 파일:**

| 파일 | 변경 내용 |
|------|-----------|
| `apps/web/src/app/admin/login/page.tsx` | admin role 검증 추가 (일반 유저 로그인 차단), 로그아웃 버튼 |
| `apps/web/src/app/admin/layout.tsx` | 서버사이드 세션 체크, 로그아웃 버튼 추가 |

**middleware.ts 핵심 로직:**

```
1. /admin/login 경로 → pass through
2. /admin/* 경로 → Supabase 세션 확인
   - 세션 없음 → redirect /admin/login
   - 세션 있지만 app_metadata.role !== 'admin' → redirect /admin/login?error=unauthorized
3. 기타 경로 → pass through (Supabase Auth 쿠키 refresh 처리)
```

**auth.ts 유틸리티:**

```typescript
// 서버 컴포넌트/API Route에서 사용
export async function getAdminUser() → User | null
export async function requireAdmin() → User (unauthorized 시 redirect)
```

#### 2.1.4 UI/UX 명세

- `/admin/login`: 기존 UI 유지, 에러 메시지 추가 ("관리자 계정만 접근 가능합니다")
- `/admin/layout.tsx`: 사이드바 하단에 로그아웃 버튼 + 현재 로그인 이메일 표시

#### 2.1.5 구현 방법

Next.js App Router + `@supabase/ssr`의 표준 middleware 패턴 사용. 별도 라이브러리 불필요.

---

### 2.2 다국어 진단 체크 (Multilingual Check) — P1

#### 2.2.1 목적 및 비즈니스 가치

- PRD F1.4에 정의된 "다국어/해외 환자 대응" 카테고리 구현
- scorer.py의 예비 5% 가중치(현재 total 0.95)를 활용하여 진단 완성도 100% 달성
- 의료관광의 핵심 경쟁력인 다국어 지원 여부를 정량적으로 평가

#### 2.2.2 PRD F1.4 참조 항목

| 진단 항목 | 체크 내용 | PRD 가중치 | 구현 방법 |
|-----------|----------|:----------:|----------|
| 다국어 페이지 | 영어/일본어/중국어 페이지 존재 여부 | 예비에서 배정 | 크롤링 + 언어 감지 |
| hreflang 태그 | 다국어 페이지간 hreflang 설정 | 예비에서 배정 | HTML 파싱 |
| 해외 채널 연동 | LINE, WeChat, WhatsApp 링크/위젯 | 예비에서 배정 | HTML 파싱 |

#### 2.2.3 기술 스펙

**WEIGHTS 키 추가 (scorer.py):**

```python
WEIGHTS: dict[str, float] = {
    # ... 기존 0.95 유지 ...

    # Multilingual (0.05) — 예비 가중치 배정
    "multilingual": 0.05,
}
# Total weight: 1.00
```

> **설계 결정**: PRD에서는 다국어 페이지(5%), hreflang(3%), 해외 채널(2%)로 세분화했으나,
> 현재 WEIGHTS 구조가 항목당 1키인 점을 고려하여 **단일 키 `multilingual`로 통합하고
> 내부에서 서브스코어 3개를 합산**한다. details에 개별 서브스코어를 기록하여
> 리포트에서 세부 항목별 Pass/Warn/Fail을 표시한다.

**신규 파일:**

| 파일 | 역할 |
|------|------|
| `apps/worker/app/checks/multilingual.py` | 다국어 체크 모듈 |

**변경 파일:**

| 파일 | 변경 내용 |
|------|-----------|
| `apps/worker/app/services/scorer.py` | WEIGHTS에 `"multilingual": 0.05` 추가 |
| `apps/worker/app/services/scanner.py` | `check_multilingual` import 및 호출 추가 |
| `apps/web/src/app/report/[id]/page.tsx` | CATEGORY_MAP에 multilingual 매핑 추가 |
| `apps/web/src/app/api/reports/[id]/route.ts` | CATEGORY_LABELS에 multilingual 추가 |
| `apps/web/src/lib/types.ts` | Category 타입에 multilingual 추가 |

**multilingual.py 체크 상세:**

```python
def check_multilingual(
    main_html: str,
    crawled_pages: list[CrawlResult],
    base_url: str,
) -> CheckResult:
    """다국어/해외 환자 대응 종합 체크."""
```

서브스코어 3개 (각각 0.0-1.0, 가중 합산):

| 서브체크 | 내부 가중치 | 체크 항목 | Pass 기준 |
|----------|:----------:|----------|----------|
| hreflang_check (30%) | 0.30 | `<link rel="alternate" hreflang="...">` 태그 존재 여부 | 2개 이상 hreflang 태그 존재 |
| lang_pages_check (50%) | 0.50 | 영어(`en`)/일본어(`ja`)/중국어(`zh`) 페이지 존재 여부 | 1개 이상 외국어 페이지 존재 |
| overseas_channel_check (20%) | 0.20 | LINE/WeChat/WhatsApp 링크 존재 여부 | 1개 이상 해외 채널 링크 |

**lang_pages_check 세부 로직:**

1. 크롤링된 페이지의 `<html lang="...">` 속성 체크
2. URL 패턴 체크: `/en/`, `/ja/`, `/zh/`, `/en-us/`, `?lang=en` 등
3. 페이지 내 `<meta http-equiv="content-language">` 체크
4. 언어별 감지 결과를 details에 기록

**overseas_channel_check 세부 로직:**

검색 패턴:
```
LINE:     href에 "line.me", "lin.ee" 포함
WeChat:   href에 "weixin.qq.com" 포함, 또는 텍스트에 "WeChat", "微信" 포함
WhatsApp: href에 "wa.me", "whatsapp.com" 포함
```

#### 2.2.4 UI/UX 명세

- 리포트 페이지 바 차트에 "다국어" 카테고리 추가
- HTML 리포트 테이블에 "다국어 지원" 항목 추가
- details에 서브체크 결과 표시 (hreflang, 다국어 페이지, 해외 채널 각각)

---

### 2.3 PDF 리포트 생성 — P2

#### 2.3.1 목적 및 비즈니스 가치

- PRD Core Flow의 Step 4 "이메일로 상세 PDF 리포트 발송" 구현
- 현재 `/api/reports/[id]`는 HTML만 제공 — 인쇄 시 브라우저 의존
- PDF를 이메일에 첨부하여 리드 전환율 향상 (첨부파일 있는 이메일 → 열람률 +30%)
- 유료 상담 시 고객에게 전달할 공식 리포트로 활용

#### 2.3.2 구현 방법 비교

| 방법 | 장점 | 단점 | 비용 | 추천 |
|------|------|------|:----:|:----:|
| **Playwright HTML→PDF** | 기존 HTML 템플릿 재활용, CSS 완벽 지원, worker에 이미 Playwright 가능 | 메모리 사용량 높음(200-500MB), Cold start 느림 | 무료 | **추천** |
| `@react-pdf/renderer` | React 컴포넌트로 PDF 생성, Next.js 친화적 | CSS 호환성 제한, 차트 렌더링 어려움, 학습 곡선 | 무료 | 비추천 |
| `html-pdf-node` (puppeteer) | Playwright와 유사 | Playwright 대비 장점 없음, 추가 의존성 | 무료 | 비추천 |
| 외부 API (DocRaptor, PDFShift) | 서버 리소스 불필요, 안정적 | 비용 ($), 외부 의존성, 데이터 전송 보안 | $15-50/월 | 대안 |

#### 2.3.3 추천: Worker에서 Playwright HTML→PDF

**근거:**
1. Worker (FastAPI)에 이미 httpx + BeautifulSoup 기반 크롤러가 있어 Playwright 추가 용이
2. 기존 `/api/reports/[id]`의 HTML 템플릿을 그대로 재활용
3. PDF 생성은 스캔 완료 후 한 번만 실행 → 동시성 부담 낮음
4. Supabase Storage에 저장하여 반복 다운로드 시 재생성 불필요

#### 2.3.4 기술 스펙

**PDF 리포트 구조 (PRD F2.2 기반):**

```
1. Executive Summary (1페이지)
   - 종합 점수 원형 게이지 + 등급
   - 핵심 문제 Top 3 (Fail 항목 중 가중치 높은 순)
   - Pass/Warn/Fail 카운트 요약

2. 카테고리별 상세 진단 (2-3페이지)
   - 항목별 점수 바 + Pass/Warn/Fail 배지
   - 각 항목의 issues 표시
   - 개선 권고사항 (suggestion 필드)

3. 경쟁사 벤치마크 (1페이지, 데이터 있는 경우)
   - 동일 지역 분포 차트
   - 상위 25%/중위/하위 25% 비교

4. 개선 로드맵 (1페이지)
   - Fail → 우선순위 critical/high
   - Warn → 우선순위 medium
   - 예상 개선 효과
```

**신규 파일:**

| 파일 | 역할 |
|------|------|
| `apps/worker/app/services/pdf_generator.py` | Playwright 기반 HTML→PDF 생성 |
| `apps/worker/app/templates/report.html` | PDF용 HTML 템플릿 (Jinja2) |
| `apps/web/src/app/api/reports/[id]/pdf/route.ts` | PDF 다운로드 엔드포인트 (Storage URL redirect) |

**변경 파일:**

| 파일 | 변경 내용 |
|------|-----------|
| `apps/worker/app/api/routes.py` | PDF 생성 트리거 엔드포인트 추가 |
| `apps/worker/app/services/scanner.py` | 스캔 완료 후 PDF 생성 호출 |
| `apps/worker/app/config.py` | `supabase_storage_bucket` 설정 추가 |
| `apps/web/src/app/api/leads/route.ts` | 리드 생성 시 PDF URL 첨부하여 이메일 발송 |
| `apps/web/src/lib/resend.ts` | PDF 첨부 기능 추가 (`sendReportEmail` 파라미터 확장) |
| `apps/web/src/app/report/[id]/page.tsx` | "PDF 다운로드" 버튼 추가 |

**Worker API 엔드포인트:**

```
POST /api/generate-pdf
{
  "audit_id": "uuid"
}

Response (200):
{
  "pdf_url": "https://xxx.supabase.co/storage/v1/object/public/reports/{audit_id}.pdf",
  "size_bytes": 245000
}
```

**PDF 생성 플로우:**

```
1. 스캔 완료 (scanner.py)
2. → PDF 생성 호출 (pdf_generator.py)
3. → HTML 템플릿 렌더링 (Jinja2 + audit 데이터)
4. → Playwright page.pdf() 실행
5. → Supabase Storage에 업로드 (reports/{audit_id}.pdf)
6. → audits.report_url 업데이트
```

**이메일 PDF 첨부 플로우:**

```
1. POST /api/leads (리드 생성)
2. → audits.report_url 확인
3. → report_url이 있으면 PDF fetch → 이메일 첨부 발송
4. → report_url이 없으면 기존 HTML 링크만 발송 (fallback)
```

#### 2.3.5 UI/UX 명세

- `/report/[id]` 페이지: 상단 "상세 리포트 보기 / 인쇄" 옆에 "PDF 다운로드" 버튼 추가
- 리드 제출 후 성공 메시지: "PDF 리포트를 이메일로 발송했습니다"
- PDF 파일명: `CheckYourHospital-{도메인}-{날짜}.pdf`

---

### 2.4 Before/After 비교 리포트 — P3

#### 2.4.1 목적 및 비즈니스 가치

- 유료 고객에게 최적화 작업의 ROI를 **시각적으로 증명**
- 재계약/업셀 근거 자료로 활용 ("3개월간 38점 → 78점 상승")
- score_history 테이블이 이미 존재하고 스캔 시 자동 기록 중

#### 2.4.2 현재 상태 분석

- `score_history` 테이블: hospital_id, audit_id, total_score, grade, category_scores(JSONB), created_at
- `scanner.py`에서 `hospital_id`가 있으면 `record_score_history()` 자동 호출
- 프론트엔드에 score_history 조회 UI 없음

#### 2.4.3 기술 스펙

**신규 파일:**

| 파일 | 역할 |
|------|------|
| `apps/web/src/app/client/[hospitalId]/page.tsx` | 고객 뷰 — 점수 추이 + Before/After |
| `apps/web/src/app/client/[hospitalId]/layout.tsx` | 고객 뷰 레이아웃 (토큰 기반 인증) |
| `apps/web/src/app/api/score-history/[hospitalId]/route.ts` | 점수 이력 API |
| `apps/web/src/app/api/client-auth/route.ts` | 고객 토큰 검증 API |
| `apps/web/src/components/score-trend-chart.tsx` | 점수 추이 Line Chart (재사용 컴포넌트) |
| `apps/web/src/components/before-after-table.tsx` | Before/Now/Target 비교 테이블 |
| `apps/web/src/app/admin/hospitals/[id]/page.tsx` | 관리자: 병원별 모니터링 상세 |

**변경 파일:**

| 파일 | 변경 내용 |
|------|-----------|
| `apps/web/src/app/admin/layout.tsx` | 네비게이션에 "병원 관리" 메뉴 추가 |
| `apps/web/src/app/admin/dashboard/page.tsx` | 최근 점수 변동 위젯 추가 |

**고객 뷰 접근 방식 비교:**

| 방식 | 장점 | 단점 | 추천 |
|------|------|------|:----:|
| **토큰 기반 (URL에 token 쿼리 파라미터)** | 로그인 불필요, 이메일 링크로 바로 접근 | 토큰 유출 시 접근 가능 | **추천** |
| 비밀번호 보호 | 간단한 보안 | UX 불편 (비밀번호 기억) | 대안 |
| Supabase Auth 고객 계정 | 보안 최상 | 고객에게 계정 생성 부담 | 향후 |

**토큰 기반 접근 설계:**

```
1. 관리자가 프로젝트 생성 시 client_token (JWT, exp: 90일) 자동 발생
2. 토큰에 포함: { hospital_id, project_id, exp }
3. 고객에게 URL 전달: /client/{hospitalId}?token=xxx
4. middleware에서 토큰 검증 → 해당 hospital_id 데이터만 접근 허용
```

**점수 이력 API:**

```
GET /api/score-history/{hospitalId}?token=xxx

Response (200):
{
  "hospital_id": "uuid",
  "hospital_name": "강남피부과",
  "history": [
    { "date": "2026-03-01", "total_score": 38, "grade": "D", "category_scores": {...} },
    { "date": "2026-03-15", "total_score": 52, "grade": "C", "category_scores": {...} },
    ...
  ],
  "before": { "total_score": 38, "date": "2026-03-01", "category_scores": {...} },
  "current": { "total_score": 78, "date": "2026-03-27", "category_scores": {...} },
  "target": { "total_score": 85, "category_scores": {...} }
}
```

#### 2.4.4 UI/UX 명세

**고객 뷰 (`/client/[hospitalId]`):**

```
┌─────────────────────────────────────────────────┐
│ CheckYourHospital — 강남피부과 모니터링          │
├─────────────────────────────────────────────────┤
│                                                  │
│  점수 추이 (Recharts LineChart)                  │
│  ┌──────────────────────────────────────────┐   │
│  │ 100 ┃                        ●──●──★ 78  │   │
│  │  50 ┃          ●──●──●──●──●             │   │
│  │   0 ┃ ●──●──●                            │   │
│  │     ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━    │   │
│  │     W1  W2  W3  W4  W5  W6  W7  W8      │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  카테고리별 Before/Now/Target                    │
│  ┌──────────────┬────────┬───────┬────────┐    │
│  │ 항목         │ Before │ Now   │ Target │    │
│  ├──────────────┼────────┼───────┼────────┤    │
│  │ 기술 SEO     │ 32     │ 78 ↑  │ 85     │    │
│  │ 성능         │ 45     │ 72 ↑  │ 80     │    │
│  │ GEO/AEO      │ 18     │ 65 ↑  │ 80     │    │
│  │ 다국어       │ 0      │ 72 ↑  │ 80     │    │
│  └──────────────┴────────┴───────┴────────┘    │
│                                                  │
│  최근 변경사항                                   │
│  - 03/20: sitemap.xml 생성 + 제출 완료          │
│  - 03/18: 일본어 페이지 5개 추가                │
│                                                  │
└─────────────────────────────────────────────────┘
```

**관리자 병원 상세 (`/admin/hospitals/[id]`):**

- 동일 레이아웃 + 프로젝트 연결 + 재스캔 버튼 + target 점수 편집

---

### 2.5 프로젝트 관리 대시보드 — P4

#### 2.5.1 목적 및 비즈니스 가치

- 리드 → 유료 고객 전환 후 **최적화 작업을 체계적으로 관리**
- 기존 projects 테이블(미사용)을 활성화
- 고객에게 작업 진행 상황을 투명하게 공유 → 신뢰 구축

#### 2.5.2 현재 상태 분석

- `projects` 테이블 존재: id, lead_id, hospital_id, status, plan(JSONB), start_date, end_date
- RLS 정책: admin role 전체 접근 설정 완료
- 프론트엔드 UI/API 없음

#### 2.5.3 기술 스펙

**DB 스키마 확장:**

projects.plan JSONB 구조 표준화:

```json
{
  "target_score": 85,
  "target_categories": {
    "technical_seo": 85,
    "performance": 80,
    "geo_aeo": 80,
    "multilingual": 80
  },
  "tasks": [
    {
      "id": "task-1",
      "category": "technical_seo",
      "title": "robots.txt 생성 및 최적화",
      "description": "Googlebot, Bingbot 허용 설정",
      "priority": "critical",
      "status": "done",
      "completed_at": "2026-03-15T10:00:00Z"
    },
    {
      "id": "task-2",
      "category": "technical_seo",
      "title": "sitemap.xml 생성",
      "priority": "critical",
      "status": "in_progress"
    }
  ],
  "notes": [
    { "date": "2026-03-14", "content": "킥오프 미팅 완료", "author": "admin" }
  ]
}
```

**신규 테이블 (마이그레이션 필요):**

```sql
-- projects 테이블 확장 컬럼
ALTER TABLE projects ADD COLUMN IF NOT EXISTS name TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS contract_amount INTEGER;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS before_audit_id UUID REFERENCES audits(id);
ALTER TABLE projects ADD COLUMN IF NOT EXISTS latest_audit_id UUID REFERENCES audits(id);
ALTER TABLE projects ADD COLUMN IF NOT EXISTS client_token TEXT UNIQUE;
```

**신규 파일:**

| 파일 | 역할 |
|------|------|
| `apps/web/src/app/admin/projects/page.tsx` | 프로젝트 목록 |
| `apps/web/src/app/admin/projects/[id]/page.tsx` | 프로젝트 상세 (작업 체크리스트 + Before/After) |
| `apps/web/src/app/admin/projects/new/page.tsx` | 프로젝트 생성 (리드 선택 → 프로젝트 전환) |
| `apps/web/src/app/api/projects/route.ts` | 프로젝트 CRUD API |
| `apps/web/src/app/api/projects/[id]/route.ts` | 프로젝트 상세/수정 API |
| `apps/web/src/app/api/projects/[id]/tasks/route.ts` | 작업 항목 관리 API |
| `apps/web/src/app/client/[hospitalId]/project/page.tsx` | 고객 뷰: 프로젝트 진행 상황 |
| `apps/web/src/components/task-checklist.tsx` | 작업 체크리스트 컴포넌트 |
| `apps/web/src/components/progress-ring.tsx` | 진행률 원형 게이지 |

**변경 파일:**

| 파일 | 변경 내용 |
|------|-----------|
| `apps/web/src/app/admin/layout.tsx` | 네비게이션에 "프로젝트" 메뉴 추가 |
| `apps/web/src/app/admin/leads/page.tsx` | "프로젝트 전환" 버튼 추가 |

**프로젝트 API:**

```
# 목록
GET /api/projects
Response: { projects: [...], total: number }

# 생성 (리드 → 프로젝트 전환)
POST /api/projects
{
  "lead_id": "uuid",
  "hospital_id": "uuid",
  "name": "강남피부과 SEO 최적화",
  "contract_amount": 3000000,
  "start_date": "2026-04-01",
  "end_date": "2026-06-30",
  "target_score": 85
}
Response (201): { id: "uuid", client_token: "jwt..." }

# 작업 추가/수정
PATCH /api/projects/{id}/tasks
{
  "action": "add" | "update" | "remove",
  "task": { "id": "...", "title": "...", ... }
}
```

#### 2.5.4 UI/UX 명세

**관리자 프로젝트 목록 (`/admin/projects`):**

```
┌────────────────────────────────────────────────────────┐
│ 프로젝트 관리                        [+ 새 프로젝트]   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │ 강남피부과 SEO 최적화    진행 중    ████░ 72%   │  │
│  │ 38점 → 78점 (+40)       2026.04.01 ~ 06.30     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
│  ┌─────────────────────────────────────────────────┐  │
│  │ 서울성형외과 GEO 개선    계획 중    ░░░░░  0%   │  │
│  │ 52점 → 목표 80점        2026.04.15 ~ 07.15     │  │
│  └─────────────────────────────────────────────────┘  │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**프로젝트 상세 (`/admin/projects/[id]`):**

- 상단: 프로젝트 정보 (병원명, 기간, 계약 금액, 진행률)
- 중단: Before/After 점수 비교 (ScoreTrendChart 재사용)
- 하단: 작업 체크리스트 (드래그 정렬, 체크/언체크, 메모)

---

## 3. DB 마이그레이션

**파일**: `packages/shared/supabase/migrations/004_phase_b.sql`

```sql
-- Phase B: Admin Auth + Multilingual + PDF + Projects Enhancement
-- 004_phase_b.sql

-- ============================================================
-- 1. projects 테이블 확장
-- ============================================================
ALTER TABLE projects ADD COLUMN IF NOT EXISTS name TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS contract_amount INTEGER;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS before_audit_id UUID REFERENCES audits(id);
ALTER TABLE projects ADD COLUMN IF NOT EXISTS latest_audit_id UUID REFERENCES audits(id);
ALTER TABLE projects ADD COLUMN IF NOT EXISTS client_token TEXT UNIQUE;

CREATE INDEX IF NOT EXISTS idx_projects_client_token ON projects(client_token) WHERE client_token IS NOT NULL;

-- ============================================================
-- 2. score_history에 target 점수 추가
-- ============================================================
-- target은 projects.plan.target_categories에 저장하므로 별도 컬럼 불필요

-- ============================================================
-- 3. audits에 report_pdf_url 추가 (HTML report_url과 구분)
-- ============================================================
-- 기존 report_url 컬럼을 PDF URL로 재활용 (현재 미사용)
-- 추가 컬럼 없음

-- ============================================================
-- 4. 고객 뷰 RLS 정책 (토큰 기반)
-- ============================================================
-- score_history는 이미 anon SELECT 허용 (003_phase_aplus.sql)
-- projects의 고객 접근은 API Route에서 토큰 검증 (service_role 사용)

-- ============================================================
-- 5. leads.status 확장
-- ============================================================
-- 기존 status에 'project' 값 추가 (체크 제약 없으므로 가능)
-- 리드 → 프로젝트 전환 시 leads.status = 'contracted'

-- ============================================================
-- 6. projects status 체크 제약 추가
-- ============================================================
ALTER TABLE projects
    DROP CONSTRAINT IF EXISTS chk_projects_status;
ALTER TABLE projects
    ADD CONSTRAINT chk_projects_status
    CHECK (status IN ('planning', 'in_progress', 'completed', 'cancelled'));
```

---

## 4. 파일 변경 맵

```
apps/worker/app/
├── checks/
│   └── multilingual.py                    [신규] 다국어 체크 모듈
├── services/
│   ├── scanner.py                         [변경] multilingual 체크 추가, PDF 생성 호출
│   ├── scorer.py                          [변경] WEIGHTS에 multilingual 추가
│   └── pdf_generator.py                   [신규] Playwright HTML→PDF
├── templates/
│   └── report.html                        [신규] PDF용 Jinja2 HTML 템플릿
├── api/
│   └── routes.py                          [변경] PDF 생성 엔드포인트 추가
└── config.py                              [변경] storage bucket 설정 추가

apps/web/src/
├── middleware.ts                           [신규] /admin/* 경로 보호
├── lib/
│   ├── auth.ts                            [신규] admin role 검증 유틸리티
│   ├── resend.ts                          [변경] PDF 첨부 기능 추가
│   └── types.ts                           [변경] Category에 multilingual 추가
├── components/
│   ├── score-trend-chart.tsx              [신규] 점수 추이 Line Chart
│   ├── before-after-table.tsx             [신규] Before/Now/Target 테이블
│   ├── task-checklist.tsx                 [신규] 작업 체크리스트
│   └── progress-ring.tsx                  [신규] 진행률 원형 게이지
├── app/
│   ├── admin/
│   │   ├── layout.tsx                     [변경] 로그아웃 + 메뉴 추가
│   │   ├── login/page.tsx                 [변경] admin role 검증 추가
│   │   ├── dashboard/page.tsx             [변경] 점수 변동 위젯 추가
│   │   ├── leads/page.tsx                 [변경] 프로젝트 전환 버튼 추가
│   │   ├── hospitals/
│   │   │   └── [id]/page.tsx              [신규] 병원별 모니터링 상세
│   │   └── projects/
│   │       ├── page.tsx                   [신규] 프로젝트 목록
│   │       ├── [id]/page.tsx              [신규] 프로젝트 상세
│   │       └── new/page.tsx               [신규] 프로젝트 생성
│   ├── client/
│   │   └── [hospitalId]/
│   │       ├── layout.tsx                 [신규] 고객 뷰 레이아웃 (토큰 인증)
│   │       ├── page.tsx                   [신규] 점수 추이 + Before/After
│   │       └── project/page.tsx           [신규] 프로젝트 진행 상황
│   ├── api/
│   │   ├── reports/[id]/
│   │   │   ├── route.ts                   [변경] CATEGORY_LABELS에 multilingual 추가
│   │   │   └── pdf/route.ts               [신규] PDF 다운로드 (Storage redirect)
│   │   ├── score-history/
│   │   │   └── [hospitalId]/route.ts      [신규] 점수 이력 API
│   │   ├── client-auth/route.ts           [신규] 고객 토큰 검증
│   │   ├── projects/
│   │   │   ├── route.ts                   [신규] 프로젝트 목록/생성
│   │   │   └── [id]/
│   │   │       ├── route.ts               [신규] 프로젝트 상세/수정
│   │   │       └── tasks/route.ts         [신규] 작업 관리
│   │   └── leads/route.ts                 [변경] PDF URL 첨부 이메일
│   └── report/[id]/page.tsx               [변경] PDF 다운로드 버튼, multilingual 매핑

packages/shared/supabase/migrations/
└── 004_phase_b.sql                        [신규] 스키마 마이그레이션
```

**신규 파일: 21개 / 변경 파일: 14개**

---

## 5. 구현 순서 (의존성 기반 DAG)

```
Week 1 (병렬 가능)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌─────────────────┐     ┌─────────────────┐
  │  P0: Admin Auth │     │ P1: Multilingual │
  │  (2일)          │     │  Check (3일)     │
  │                 │     │                  │
  │ - middleware.ts │     │ - multilingual.py│
  │ - auth.ts       │     │ - scorer.py 변경 │
  │ - login 수정    │     │ - scanner.py 변경│
  │ - layout 수정   │     │ - 리포트 UI 변경 │
  └────────┬────────┘     └────────┬─────────┘
           │                       │
           │    ┌──────────────────┘
           │    │
           v    v
Week 2 (P0 완료 필요)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌──────────────────────┐     ┌──────────────┐
  │  P2: PDF 리포트 생성  │     │ DB Migration │
  │  (4일)               │     │ 004_phase_b  │
  │                      │     │ (0.5일)      │
  │ - pdf_generator.py   │     └──────┬───────┘
  │ - report.html 템플릿  │            │
  │ - Worker API         │            │
  │ - resend.ts 변경     │            │
  │ - PDF 다운로드 UI    │            │
  └──────────┬───────────┘            │
             │                        │
             v                        v
Week 3 (PDF, Migration 완료 필요)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌───────────────────────────────────────────────┐
  │  P3: Before/After 비교 리포트 (3일)            │
  │                                                │
  │ - score-trend-chart.tsx, before-after-table.tsx│
  │ - /api/score-history API                       │
  │ - /client/[hospitalId] 고객 뷰                 │
  │ - /admin/hospitals/[id] 관리자 뷰              │
  │ - 토큰 기반 인증                               │
  └──────────────────────┬────────────────────────┘
                         │
                         v
Week 4 (Before/After 완료 필요)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌───────────────────────────────────────────────┐
  │  P4: 프로젝트 관리 대시보드 (4일)              │
  │                                                │
  │ - /admin/projects CRUD                         │
  │ - 작업 체크리스트 (task-checklist.tsx)          │
  │ - 리드 → 프로젝트 전환                         │
  │ - /client/[hospitalId]/project 고객 뷰         │
  │ - 진행률 게이지 (progress-ring.tsx)            │
  └───────────────────────────────────────────────┘
```

**총 예상 기간: 2주 (10 영업일)**

**병렬화 가능 구간:**
- Week 1: Admin Auth ∥ Multilingual Check (독립적)
- Week 2: PDF 리포트 ∥ DB Migration (독립적)

**순차 의존성:**
- Admin Auth → 모든 관리자 기능 (PDF, Projects)
- DB Migration → Before/After, Projects
- Before/After → Projects (ScoreTrendChart 재사용)

---

## 6. 예상 환경변수

### 6.1 신규 추가 필요

| 변수명 | 용도 | 위치 | 예시 값 |
|--------|------|------|---------|
| `SUPABASE_STORAGE_BUCKET` | PDF 저장 버킷명 | Worker `.env` | `reports` |
| `CLIENT_TOKEN_SECRET` | 고객 뷰 JWT 서명 키 | Web `.env` | `your-secret-key-here` |

### 6.2 기존 변수 (변경 없음, 확인 필요)

| 변수명 | 용도 | 확인 사항 |
|--------|------|-----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase 프로젝트 URL | Web — 이미 설정됨 |
| `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` | Supabase anon key | Web — 이미 설정됨 |
| `SUPABASE_SECRET_KEY` | Supabase service_role key | Web + Worker — 이미 설정됨 |
| `RESEND_API_KEY` | 이메일 발송 | Web — 이미 설정됨 |
| `WORKER_API_KEY` | Worker 인증 | Worker — 이미 설정됨 |

### 6.3 Supabase 대시보드 설정

| 설정 | 설명 |
|------|------|
| Auth 관리자 계정 생성 | Supabase Dashboard → Authentication → Users에서 admin 계정 생성 |
| app_metadata 설정 | 해당 유저의 app_metadata에 `{"role": "admin"}` 추가 |
| Storage 버킷 생성 | `reports` 버킷 생성 (public access 또는 signed URL) |

---

## 부록: 리스크 및 고려사항

### A. PDF 생성 성능

- Playwright PDF 생성은 약 2-5초 소요 (첫 실행 시 브라우저 부팅 포함 10-15초)
- Worker에서 Playwright 브라우저 풀 유지하여 Cold start 방지
- PDF 생성 실패 시 fallback: HTML 리포트 URL만 이메일 발송

### B. 고객 토큰 보안

- JWT exp: 90일 (프로젝트 기간 고려)
- 토큰 유출 시 관리자가 projects.client_token 재생성 가능
- 향후 Phase C에서 고객 Supabase Auth 계정으로 업그레이드 가능

### C. 다국어 체크 정확도

- hreflang/lang 속성 기반 체크는 정확도 높음
- URL 패턴 기반 언어 감지는 false positive 가능 → 보수적 판정 (Warn)
- 향후 실제 텍스트 언어 감지 (langdetect 라이브러리) 추가 가능
