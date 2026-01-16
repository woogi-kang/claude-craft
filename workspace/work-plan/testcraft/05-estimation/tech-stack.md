# TestCraft - Tech Stack Recommendation

> MVP 개발을 위한 기술 스택 추천 및 Make vs Buy 분석

---

## 1. Tech Stack Overview

### 권장 스택 요약

```
+------------------------------------------------------------------+
|                    TestCraft Tech Stack                           |
+------------------------------------------------------------------+
|                                                                   |
|  Frontend:                                                        |
|  +----------------+  +----------------+  +----------------+       |
|  |   Next.js 14   |  |   TypeScript   |  |  Tailwind CSS  |       |
|  |  (App Router)  |  |     5.x        |  |   + shadcn/ui  |       |
|  +----------------+  +----------------+  +----------------+       |
|                                                                   |
|  Backend:                                                         |
|  +----------------+  +----------------+  +----------------+       |
|  |   Next.js API  |  |   Supabase     |  |   OpenAI       |       |
|  |    Routes      |  |  (Auth + DB)   |  |   GPT-4o       |       |
|  +----------------+  +----------------+  +----------------+       |
|                                                                   |
|  Infrastructure:                                                  |
|  +----------------+  +----------------+  +----------------+       |
|  |    Vercel      |  |   Supabase     |  |  Cloudflare R2 |       |
|  |   (Hosting)    |  | (PostgreSQL)   |  |  (Storage)     |       |
|  +----------------+  +----------------+  +----------------+       |
|                                                                   |
|  3rd Party:                                                       |
|  +----------------+  +----------------+  +----------------+       |
|  |    Stripe      |  |    Resend      |  |   pdf-parse    |       |
|  |   (Payment)    |  |   (Email)      |  | (PDF Parsing)  |       |
|  +----------------+  +----------------+  +----------------+       |
|                                                                   |
+------------------------------------------------------------------+
```

---

## 2. Frontend Decision Matrix

### Option Analysis: Next.js vs React (CRA/Vite)

| 평가 기준 | Next.js 14 | React + Vite | 비고 |
|----------|-----------|--------------|------|
| **SSR/SEO** | O (내장) | X (별도 구성) | 랜딩 페이지 SEO 중요 |
| **라우팅** | O (파일 기반) | X (react-router) | 설정 간소화 |
| **API Routes** | O (내장) | X (별도 서버) | 백엔드 통합 용이 |
| **배포** | O (Vercel 최적화) | O (다양한 옵션) | Vercel 원클릭 배포 |
| **학습 곡선** | 중간 (App Router) | 낮음 | App Router 새로움 |
| **커뮤니티** | 매우 큼 | 매우 큼 | 동등 |
| **성능** | 우수 (자동 최적화) | 양호 | 이미지, 폰트 최적화 |

### 결정: Next.js 14 (App Router)

```
선택 이유:
+---------------------------------------------------------------+
|                                                                |
|   1. 올인원 솔루션                                              |
|      - 프론트엔드 + API 라우트로 백엔드 분리 불필요              |
|      - MVP 개발 속도 극대화                                     |
|                                                                |
|   2. SEO 필수                                                  |
|      - 랜딩 페이지, 가격 페이지 검색 노출 중요                   |
|      - SSR/SSG 네이티브 지원                                    |
|                                                                |
|   3. Vercel 통합                                               |
|      - 제로 설정 배포                                           |
|      - 프리뷰 배포, 분석 내장                                   |
|                                                                |
|   4. 미래 확장성                                                |
|      - Server Actions, Streaming 등 최신 기능                   |
|      - React 생태계 완전 호환                                   |
|                                                                |
+---------------------------------------------------------------+
```

### UI Framework: Tailwind CSS + shadcn/ui

| 옵션 | 선택 여부 | 이유 |
|-----|---------|------|
| **Tailwind CSS** | O | 빠른 스타일링, 커스터마이징 용이 |
| **shadcn/ui** | O | 복사-붙여넣기 컴포넌트, 완전한 제어 |
| Material UI | X | 번들 크기, 커스터마이징 제한 |
| Chakra UI | X | shadcn이 더 가볍고 현대적 |
| Ant Design | X | 엔터프라이즈 스타일, B2C에 부적합 |

---

## 3. Backend Decision Matrix

### Option Analysis: Next.js API Routes vs FastAPI vs Node.js

| 평가 기준 | Next.js API | FastAPI | Node.js (Express) |
|----------|------------|---------|-------------------|
| **개발 속도** | 매우 빠름 | 빠름 | 빠름 |
| **타입 안정성** | O (TS) | O (Python typing) | O (TS 필요) |
| **AI 통합** | O | 매우 좋음 | O |
| **스케일링** | Serverless | 서버 필요 | 서버 필요 |
| **프론트 통합** | 완벽 | 분리 필요 | 분리 필요 |
| **러닝 커브** | 낮음 | 중간 | 낮음 |
| **운영 비용** | 낮음 (Vercel) | 중간 | 중간 |

### 결정: Next.js API Routes

```
선택 이유:
+---------------------------------------------------------------+
|                                                                |
|   1. 모노레포 단순화                                            |
|      - 프론트엔드와 백엔드 동일 저장소                           |
|      - 타입 공유, 개발 환경 통합                                |
|                                                                |
|   2. Serverless 장점                                           |
|      - 사용량 기반 과금 (MVP에 이상적)                          |
|      - 자동 스케일링                                            |
|      - 서버 관리 불필요                                         |
|                                                                |
|   3. 빠른 이터레이션                                            |
|      - API 변경 시 프론트엔드 즉시 반영                         |
|      - 배포 파이프라인 단일화                                   |
|                                                                |
|   제한사항 인지:                                                |
|   - 장시간 실행 작업 → Vercel Background Jobs 활용              |
|   - 복잡한 비즈니스 로직 → 향후 분리 가능                       |
|                                                                |
+---------------------------------------------------------------+
```

### FastAPI 대안 시나리오

```
FastAPI 선택이 적합한 경우:
+---------------------------------------------------------------+
|                                                                |
|   1. ML/AI 중심 서비스                                         |
|      - Python 기반 AI 라이브러리 직접 사용                      |
|      - 자체 모델 학습/추론 필요                                 |
|                                                                |
|   2. 복잡한 데이터 처리                                         |
|      - NumPy, Pandas 활용 필요                                  |
|      - 대용량 파일 처리                                         |
|                                                                |
|   TestCraft의 경우:                                            |
|   - OpenAI API 호출만 필요 (Python 라이브러리 불필요)           |
|   - 복잡한 데이터 처리 없음                                     |
|   → Next.js API로 충분                                         |
|                                                                |
+---------------------------------------------------------------+
```

---

## 4. AI/LLM Decision Matrix

### Option Analysis: OpenAI vs Claude vs 자체 모델

| 평가 기준 | OpenAI GPT-4o | Claude 3.5 | 자체 모델 |
|----------|--------------|------------|----------|
| **품질** | 최상급 | 최상급 | 불확실 |
| **비용** | $5/1M input | $3/1M input | 높은 초기 비용 |
| **속도** | 빠름 | 빠름 | 인프라 의존 |
| **도입 시간** | 즉시 | 즉시 | 수개월 |
| **커스터마이징** | Fine-tuning 가능 | 제한적 | 완전 제어 |
| **의존성** | 높음 | 높음 | 없음 |

### 결정: OpenAI GPT-4o (Primary) + Claude 3.5 (Backup)

```
선택 전략:
+---------------------------------------------------------------+
|                                                                |
|   Primary: OpenAI GPT-4o                                       |
|   +----------------------------------------------------------+|
|   |  - TC 생성 품질 검증 완료 (프롬프트 최적화 가능)           ||
|   |  - 구조화된 출력 (JSON Mode) 안정적                       ||
|   |  - Function Calling으로 엣지케이스 매칭                   ||
|   +----------------------------------------------------------+|
|                                                                |
|   Backup: Claude 3.5 Sonnet                                   |
|   +----------------------------------------------------------+|
|   |  - OpenAI 장애 시 폴백                                    ||
|   |  - 비용 최적화 (일부 작업에 활용)                         ||
|   |  - A/B 테스트용 대안                                      ||
|   +----------------------------------------------------------+|
|                                                                |
|   자체 모델 로드맵 (향후):                                     |
|   +----------------------------------------------------------+|
|   |  - Year 2 이후 검토                                       ||
|   |  - 유저 데이터 충분히 확보 후 Fine-tuning                 ||
|   |  - TC 생성 특화 모델 개발 가능성                          ||
|   +----------------------------------------------------------+|
|                                                                |
+---------------------------------------------------------------+
```

### LLM 비용 추정

| 사용 시나리오 | Input 토큰 | Output 토큰 | 비용/건 |
|-------------|----------|------------|--------|
| PRD 분석 (10페이지) | 5,000 | - | $0.025 |
| TC 생성 (20개) | 2,000 | 8,000 | $0.05 |
| 엣지케이스 매칭 | 1,000 | 3,000 | $0.02 |
| **총 1회 생성** | **8,000** | **11,000** | **~$0.10** |

```
월간 비용 추정 (GPT-4o 기준):

Free 사용자 100명 × 5건/월 = 500건 → $50
Pro 사용자 50명 × 50건/월 = 2,500건 → $250
Team 사용자 20명 × 100건/월 = 2,000건 → $200

총 월간 AI 비용: ~$500 (초기)
```

---

## 5. Database Decision Matrix

### Option Analysis: Supabase vs Firebase vs PlanetScale

| 평가 기준 | Supabase | Firebase | PlanetScale |
|----------|----------|----------|-------------|
| **DB 타입** | PostgreSQL | NoSQL | MySQL |
| **Auth 내장** | O | O | X |
| **실시간** | O | O | X |
| **SQL 지원** | O | X | O |
| **가격** | 관대한 무료 | 관대한 무료 | 유료 시작 |
| **마이그레이션** | 쉬움 | 어려움 | 쉬움 |
| **확장성** | 좋음 | 매우 좋음 | 매우 좋음 |

### 결정: Supabase

```
선택 이유:
+---------------------------------------------------------------+
|                                                                |
|   1. PostgreSQL 장점                                           |
|      - 관계형 데이터 (User → Project → TC) 자연스러운 표현      |
|      - 복잡한 쿼리, 조인, 트랜잭션 지원                        |
|      - JSONB로 반정형 데이터도 처리 가능                       |
|                                                                |
|   2. 올인원 BaaS                                               |
|      - Auth, Storage, Edge Functions 통합                      |
|      - 실시간 구독 (팀 협업 기능에 활용)                       |
|      - Row Level Security (RLS)                                |
|                                                                |
|   3. 개발자 경험                                               |
|      - 자동 생성 API (REST, GraphQL)                           |
|      - TypeScript 타입 자동 생성                               |
|      - 로컬 개발 환경 (Supabase CLI)                           |
|                                                                |
|   4. 비용 효율                                                 |
|      - 무료: 500MB DB, 1GB Storage, 50,000 MAU                 |
|      - Pro ($25/월): 8GB DB, 100GB Storage                     |
|                                                                |
+---------------------------------------------------------------+
```

### Data Model Overview

```sql
-- 핵심 테이블 구조

-- Users (Supabase Auth 연동)
users (
  id UUID PRIMARY KEY REFERENCES auth.users,
  email VARCHAR UNIQUE,
  name VARCHAR,
  plan ENUM('free', 'pro', 'team'),
  tc_count_this_month INT DEFAULT 0,
  tc_reset_date DATE,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- Projects
projects (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users,
  name VARCHAR NOT NULL,
  description TEXT,
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  UNIQUE(user_id, name)
)

-- PRD Files
prd_files (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects,
  file_name VARCHAR,
  file_url VARCHAR,
  file_size INT,
  page_count INT,
  extracted_text TEXT,
  status ENUM('uploading', 'processing', 'ready', 'error'),
  created_at TIMESTAMP
)

-- Test Cases
test_cases (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects,
  prd_id UUID REFERENCES prd_files,
  tc_number VARCHAR, -- TC-001
  feature VARCHAR,
  scenario VARCHAR NOT NULL,
  precondition TEXT,
  steps JSONB, -- [{step: 1, action: "...", expected: "..."}]
  expected_result TEXT,
  platform ENUM('android', 'ios', 'web', 'pc'),
  category VARCHAR,
  priority ENUM('high', 'medium', 'low'),
  is_edge_case BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
)

-- Indexes
CREATE INDEX idx_test_cases_project ON test_cases(project_id);
CREATE INDEX idx_test_cases_platform ON test_cases(platform);
CREATE INDEX idx_projects_user ON projects(user_id);
```

---

## 6. Infrastructure & DevOps

### Hosting: Vercel

| 항목 | 선택 | 이유 |
|-----|------|------|
| **프론트엔드** | Vercel | Next.js 최적화, 자동 배포 |
| **API** | Vercel Serverless | Next.js API Routes |
| **Database** | Supabase | Managed PostgreSQL |
| **Storage** | Supabase Storage / Cloudflare R2 | PDF 파일 저장 |
| **CDN** | Vercel Edge | 자동 포함 |

### Vercel 비용 추정

```
Hobby (무료):
- 개인 프로젝트, 비상업적 용도
- 100GB 대역폭/월

Pro ($20/월):
- 상업 프로젝트
- 1TB 대역폭/월
- 팀 멤버 무제한
- 고급 분석

예상 선택: Pro ($20/월) - MVP 런칭 시점
```

### CI/CD Pipeline

```
GitHub Actions + Vercel 통합:

main branch:
+------------------+     +------------------+     +------------------+
|     Push/PR      | --> |   Lint + Test    | --> |  Vercel Deploy   |
|                  |     |   TypeScript     |     |   Production     |
+------------------+     +------------------+     +------------------+

feature branch:
+------------------+     +------------------+     +------------------+
|     Push/PR      | --> |   Lint + Test    | --> |  Vercel Preview  |
|                  |     |   TypeScript     |     |    Deployment    |
+------------------+     +------------------+     +------------------+
```

---

## 7. 3rd Party Services

### Make vs Buy 분석

| 기능 | Build | Buy | 결정 | 이유 |
|-----|-------|-----|------|------|
| **인증** | 2주 | Supabase Auth | Buy | 보안, 시간 절약 |
| **결제** | 4주 | Stripe | Buy | PCI 준수, 검증됨 |
| **이메일** | 1주 | Resend | Buy | 전달률, API |
| **PDF 파싱** | 2주 | pdf-parse | Buy | 복잡한 엣지케이스 |
| **DOCX 파싱** | 1주 | mammoth | Buy | 검증된 라이브러리 |
| **AI 엔진** | 수개월 | OpenAI API | Buy | 품질, 시간 |
| **분석** | 2주 | Vercel Analytics | Buy | 통합, 무료 |

### 서비스별 상세

| 서비스 | 용도 | 가격 | 월 예상 비용 |
|-------|------|------|------------|
| **Supabase** | Auth, DB, Storage | Free → $25/월 | $0-25 |
| **Vercel** | Hosting, CDN | $20/월 | $20 |
| **OpenAI** | TC 생성 | 사용량 기반 | $500 |
| **Stripe** | 결제 | 2.9% + 30c | 매출의 3% |
| **Resend** | 이메일 | 3,000건/월 무료 | $0 |
| **Cloudflare R2** | 파일 저장 | 10GB 무료 | $0-5 |

### 월간 인프라 비용 추정

```
MVP (Month 1-3):
+----------------------------------------------------------+
|  서비스         | 비용      | 비고                        |
+----------------------------------------------------------+
|  Vercel Pro     | $20       | 호스팅                      |
|  Supabase Free  | $0        | 무료 티어 충분              |
|  OpenAI         | $100-300  | 초기 사용량 적음            |
|  Resend         | $0        | 무료 티어                   |
|  Cloudflare R2  | $0        | 무료 티어                   |
+----------------------------------------------------------+
|  총계           | ~$120-320 |                            |
+----------------------------------------------------------+

성장기 (Month 6+):
+----------------------------------------------------------+
|  서비스         | 비용      | 비고                        |
+----------------------------------------------------------+
|  Vercel Pro     | $20       |                            |
|  Supabase Pro   | $25       | 사용량 증가                 |
|  OpenAI         | $500-1000 | 사용자 증가                 |
|  Resend         | $20       | Pro 플랜                   |
|  Cloudflare R2  | $5        | 스토리지 증가              |
+----------------------------------------------------------+
|  총계           | ~$570-1070|                            |
+----------------------------------------------------------+
```

---

## 8. Development Tools

### Core Tools

| 카테고리 | 도구 | 용도 |
|---------|------|------|
| **IDE** | VS Code / Cursor | 코드 편집 |
| **패키지 매니저** | pnpm | 빠른 설치, 디스크 효율 |
| **린터** | ESLint + Prettier | 코드 품질 |
| **타입체크** | TypeScript 5.x | 타입 안전성 |
| **테스트** | Vitest + Playwright | 단위/E2E 테스트 |
| **버전 관리** | Git + GitHub | 소스 코드 관리 |

### Recommended VS Code Extensions

```
필수:
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- TypeScript + JavaScript
- Supabase (공식)

권장:
- GitHub Copilot
- Error Lens
- GitLens
- Thunder Client (API 테스트)
```

---

## 9. Security Considerations

### Security Checklist

| 영역 | 조치 | 구현 |
|-----|------|------|
| **인증** | JWT + Refresh Token | Supabase Auth |
| **데이터 전송** | HTTPS (TLS 1.3) | Vercel 자동 |
| **데이터 저장** | 암호화 (AES-256) | Supabase 기본 |
| **접근 제어** | RLS (Row Level Security) | Supabase |
| **API 보안** | Rate Limiting | Vercel + Middleware |
| **환경 변수** | Secrets 관리 | Vercel Env Variables |
| **의존성** | 취약점 스캔 | Dependabot |

### Environment Variables

```
# .env.local (예시)

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_ROLE_KEY=xxx

# OpenAI
OPENAI_API_KEY=sk-xxx

# Stripe
STRIPE_SECRET_KEY=sk_live_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Resend
RESEND_API_KEY=re_xxx
```

---

## 10. Tech Stack Summary

### Final Decisions

```
+------------------------------------------------------------------+
|                  TestCraft Final Tech Stack                       |
+------------------------------------------------------------------+

Frontend:
  Framework:     Next.js 14 (App Router)
  Language:      TypeScript 5.x
  Styling:       Tailwind CSS 3.x
  Components:    shadcn/ui
  State:         React Query + Zustand
  Forms:         React Hook Form + Zod

Backend:
  API:           Next.js API Routes (Serverless)
  Runtime:       Node.js 20 LTS
  ORM:           Prisma (optional) / Supabase Client

AI/ML:
  Primary:       OpenAI GPT-4o
  Backup:        Claude 3.5 Sonnet
  SDK:           openai, @anthropic-ai/sdk

Database:
  Primary:       Supabase (PostgreSQL 15)
  Cache:         Edge Config (Vercel)

Infrastructure:
  Hosting:       Vercel (Pro)
  CDN:           Vercel Edge Network
  Storage:       Supabase Storage / Cloudflare R2
  Domain:        Cloudflare (DNS)

3rd Party:
  Auth:          Supabase Auth (Google, GitHub OAuth)
  Payment:       Stripe
  Email:         Resend
  PDF Parse:     pdf-parse
  DOCX Parse:    mammoth
  Analytics:     Vercel Analytics + Posthog

DevOps:
  CI/CD:         GitHub Actions + Vercel
  Monitoring:    Vercel Dashboard + Sentry
  Logging:       Vercel Logs + Supabase Logs

+------------------------------------------------------------------+
```

### Risk Mitigation

| 리스크 | 완화 전략 |
|-------|----------|
| OpenAI 의존성 | Claude 백업, 추상화 레이어 |
| Vercel 비용 증가 | 사용량 모니터링, 캐싱 최적화 |
| Supabase 한계 | 마이그레이션 경로 확보 (표준 PostgreSQL) |
| 보안 취약점 | 자동 업데이트, 취약점 스캔 |

---

*Generated by Planning Agent - Tech Stack Skill*
*Last Updated: 2026-01-16*
