# CheckYourHospital

AI 병원 홈페이지 진단 플랫폼 — 병원 URL을 입력하면 SEO/GEO/AEO 15개 항목을 종합 진단하여 리포트를 제공합니다.

## 아키텍처

```
사용자 → Vercel (Next.js)
           ├── 랜딩/스캔/리포트 UI
           ├── API Routes (/api/audits, /api/leads)
           └── Supabase (PostgreSQL + Auth)
                    ↕
         Cloud Run (FastAPI)
           ├── 15개 SEO 진단 엔진
           ├── Playwright (Chromium 크롤링)
           └── PageSpeed Insights API
```

## 프로젝트 구조

```
workspace/mediscope/
├── apps/
│   ├── web/              # Next.js 15 (Frontend + API Gateway)
│   │   ├── src/app/      # App Router pages + API routes
│   │   └── src/lib/      # Supabase client, Resend, utils
│   └── worker/           # FastAPI (크롤링 엔진)
│       ├── app/checks/   # 15개 진단 모듈
│       ├── app/services/ # scanner, crawler, scorer
│       ├── app/security/ # SSRF 방지, rate limit
│       └── Dockerfile    # Cloud Run 배포용
├── packages/
│   └── shared/           # 공유 타입 (TS + Pydantic) + SQL 스키마
└── supabase/             # 마이그레이션
```

## 기술 스택

### Frontend (Vercel)
- Next.js 15 App Router
- TypeScript, Tailwind CSS, shadcn/ui
- TanStack Query v5, Recharts
- Supabase SSR, Resend (이메일)

### Worker (Cloud Run)
- FastAPI + Pydantic v2
- Playwright (Chromium) — 크롤링 + 스크린샷
- httpx, BeautifulSoup4, lxml
- PageSpeed Insights API

### 인프라
- **DB**: Supabase (PostgreSQL + RLS + Auth)
- **Frontend 배포**: Vercel
- **Worker 배포**: Google Cloud Run (서울, asia-northeast3)
- **이메일**: Resend
- **예상 비용**: MVP 월 ~$0 (Cloud Run 무료 쿼터 내)

## 진단 항목 (15개)

| 카테고리 | 항목 | 가중치 |
|----------|------|--------|
| 기술 SEO | robots.txt, sitemap, meta tags, headings, images ALT, links, HTTPS, canonical, URL 구조, 404/redirect | 50% |
| 성능 | LCP, INP, CLS, Lighthouse 점수, 모바일 반응형 | 20% |

## 로컬 개발

```bash
# Frontend
cd apps/web
cp .env.local.example .env.local  # 환경변수 설정
pnpm install && pnpm dev

# Worker
cd apps/worker
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env  # 환경변수 설정
uvicorn app.main:app --port 8000 --reload
```

## 배포

```bash
# Frontend → Vercel
cd apps/web && vercel deploy

# Worker → Cloud Run
cd apps/worker && bash deploy.sh
```

## 환경변수

### Frontend (apps/web/.env.local)
```
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=
SUPABASE_SECRET_KEY=
WORKER_URL=
WORKER_API_KEY=
RESEND_API_KEY=
```

### Worker (apps/worker/.env)
```
SUPABASE_URL=
SUPABASE_SECRET_KEY=
WORKER_API_KEY=
PAGESPEED_API_KEY=
```

## 기획 문서

- 검증 보고서: `workspace/work-plan/medical-tourism-seo/03-validation/`
- PRD: `workspace/work-plan/medical-tourism-seo/04-specification/prd.md`
- 리서치: `workspace/work-plan/medical-tourism-seo/05-research/`
