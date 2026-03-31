# 모바일 청첩장 SaaS - 기술 아키텍처

## 1. 현재 -> SaaS 전환 전략

### 현재 (단일 프로젝트)

```
현재:
├── 하드코딩된 데이터 (커플 정보, 사진 경로 등)
├── 단일 인스턴스 (하나의 청첩장만 존재)
├── Firebase (일부 데이터)
├── Google Drive API (GuestSnap)
└── 정적 배포 (Vercel)
```

### 목표 (멀티테넌트 SaaS)

```
목표:
├── 데이터 기반 렌더링 (DB에서 커플 데이터 로드)
├── 멀티테넌트 (수천 개의 청첩장 동시 서빙)
├── 에디터 UI (비개발자가 데이터 입력)
├── 결제 -> 자동 발급 파이프라인
└── 관리자 대시보드
```

### 전환 단계

```
Phase 1: 데이터 분리 (Week 1-2)
─────────────────────────────────
  - 하드코딩된 데이터 → JSON 스키마로 추출
  - 환경변수 / 설정 파일 기반 렌더링
  - 기존 섹션 컴포넌트를 props 기반으로 리팩토링

Phase 2: DB + API 연동 (Week 3-4)
─────────────────────────────────
  - Supabase PostgreSQL 스키마 설계
  - API Routes로 CRUD 구현
  - 동적 라우팅: /invitation/[slug]

Phase 3: 에디터 구축 (Week 5-6)
─────────────────────────────────
  - 섹션별 입력 폼 UI
  - 실시간 미리보기
  - 이미지 업로드 파이프라인

Phase 4: 결제 + 발급 (Week 7-8)
─────────────────────────────────
  - 토스페이먼츠 연동
  - 결제 완료 → URL 발급 자동화
  - 카카오 공유 연동
```

## 2. 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                        클라이언트                                  │
│                                                                  │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────────────┐      │
│  │ 랜딩     │  │   에디터      │  │   청첩장 뷰어          │      │
│  │ 페이지   │  │   /editor     │  │   /invitation/[slug]  │      │
│  │ /        │  │               │  │                       │      │
│  │ SSG      │  │   Client-side │  │   SSR + ISR           │      │
│  └──────────┘  └──────┬───────┘  └───────────┬───────────┘      │
│                        │                      │                  │
└────────────────────────┼──────────────────────┼──────────────────┘
                         │                      │
                    Next.js 16 App Router
                    (Vercel 호스팅)
                         │
┌────────────────────────┼──────────────────────┼──────────────────┐
│                     API Routes                                    │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ /api/    │  │ /api/    │  │ /api/    │  │ /api/    │       │
│  │ auth     │  │ editor   │  │ payment  │  │ admin    │       │
│  │          │  │          │  │          │  │          │       │
│  │ Supabase │  │ 섹션CRUD │  │ 토스     │  │ 관리자   │       │
│  │ Auth     │  │ 이미지   │  │ 페이먼츠 │  │ 대시보드 │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │             │             │               │
└───────┼─────────────┼─────────────┼─────────────┼───────────────┘
        │             │             │             │
┌───────┼─────────────┼─────────────┼─────────────┼───────────────┐
│       ▼             ▼             ▼             ▼               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Supabase │  │ Supabase │  │ 토스     │  │ Vercel   │       │
│  │ Auth     │  │ DB       │  │ Payments │  │ Analytics│       │
│  │          │  │ (PgSQL)  │  │          │  │          │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                     │                                           │
│                ┌────┴────┐                                     │
│                │ Vercel  │                                     │
│                │ Blob    │                                     │
│                │ (이미지)│                                     │
│                └─────────┘                                     │
│                    데이터 레이어                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 3. 데이터베이스 스키마

### 핵심 테이블

```sql
-- 사용자 (Supabase Auth 연동)
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 청첩장 (핵심)
CREATE TABLE invitations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  slug TEXT UNIQUE NOT NULL,          -- URL 슬러그
  status TEXT DEFAULT 'draft',         -- draft | published | expired
  tier TEXT NOT NULL,                  -- basic | premium | arcade

  -- 기본 정보
  groom_name TEXT,
  bride_name TEXT,
  wedding_date TIMESTAMPTZ,
  wedding_venue TEXT,
  wedding_address TEXT,

  -- 섹션 설정 (JSONB)
  sections JSONB DEFAULT '{}',         -- 각 섹션 on/off + 순서 + 데이터
  theme JSONB DEFAULT '{}',            -- 테마/색상/폰트

  -- 메타
  expires_at TIMESTAMPTZ,
  view_count INTEGER DEFAULT 0,
  share_count INTEGER DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- 섹션 데이터 (JSONB 예시)
-- sections: {
--   "hero": { "enabled": true, "order": 1, "data": { "photo": "url", "subtitle": "..." } },
--   "greeting": { "enabled": true, "order": 2, "data": { "message": "...", "parents": {...} } },
--   "gallery": { "enabled": true, "order": 3, "data": { "photos": ["url1", "url2", ...] } },
--   "interview": { "enabled": false, "order": 4, "data": { "questions": [...] } },
--   "arcade": { "enabled": true, "order": 99, "data": { "characters": {...} } }
-- }

-- 주문/결제
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  invitation_id UUID REFERENCES invitations(id),
  tier TEXT NOT NULL,
  addons JSONB DEFAULT '[]',
  amount INTEGER NOT NULL,             -- 원 단위
  payment_key TEXT,                     -- 토스 결제 키
  status TEXT DEFAULT 'pending',       -- pending | paid | refunded | cancelled
  paid_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- RSVP 응답
CREATE TABLE rsvp_responses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invitation_id UUID REFERENCES invitations(id),
  guest_name TEXT NOT NULL,
  attending BOOLEAN,
  guest_count INTEGER DEFAULT 1,
  meal_type TEXT,                       -- 양식/한식/어린이
  message TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- GuestSnap (하객 업로드)
CREATE TABLE guest_snaps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invitation_id UUID REFERENCES invitations(id),
  uploader_name TEXT,
  file_url TEXT NOT NULL,
  file_type TEXT,                       -- image | video
  file_size INTEGER,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- 방문 로그
CREATE TABLE visit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invitation_id UUID REFERENCES invitations(id),
  visitor_ip TEXT,
  user_agent TEXT,
  referrer TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

## 4. 섹션 기반 에디터 설계

### 에디터 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                      에디터 UI                                    │
│                                                                  │
│  ┌────────────────────┐  ┌────────────────────────────────┐     │
│  │   왼쪽 패널         │  │   오른쪽 패널 (미리보기)         │     │
│  │   (편집 도구)       │  │                                │     │
│  │                    │  │   ┌────────────────────────┐   │     │
│  │  [섹션 목록]        │  │   │                        │   │     │
│  │  ☑ Hero           │  │   │    모바일 프리뷰        │   │     │
│  │  ☑ Greeting       │  │   │    (실시간 반영)        │   │     │
│  │  ☑ Gallery        │  │   │                        │   │     │
│  │  ☐ Interview      │  │   │    375 x 812px         │   │     │
│  │  ☐ Timeline       │  │   │    (iPhone 프레임)     │   │     │
│  │  ☑ WeddingInfo    │  │   │                        │   │     │
│  │  ☑ Location       │  │   └────────────────────────┘   │     │
│  │  ☑ Account        │  │                                │     │
│  │  ☐ RSVP           │  │                                │     │
│  │  ☐ Guestbook      │  │                                │     │
│  │  ☐ Arcade         │  │                                │     │
│  │                    │  │                                │     │
│  │  [선택된 섹션 편집] │  │                                │     │
│  │  ┌──────────────┐ │  │                                │     │
│  │  │ Hero 설정     │ │  │                                │     │
│  │  │ - 사진 업로드 │ │  │                                │     │
│  │  │ - 날짜 선택   │ │  │                                │     │
│  │  │ - 문구 입력   │ │  │                                │     │
│  │  └──────────────┘ │  │                                │     │
│  └────────────────────┘  └────────────────────────────────┘     │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  [미리보기]    [저장]    [결제하기]    [도움말]              │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 에디터 상태 관리

```typescript
// Zustand store
interface EditorStore {
  invitation: Invitation;
  sections: SectionConfig[];
  activeSection: string | null;
  isDirty: boolean;

  // Actions
  toggleSection: (sectionId: string) => void;
  reorderSections: (from: number, to: number) => void;
  updateSectionData: (sectionId: string, data: any) => void;
  setActiveSection: (sectionId: string) => void;
  save: () => Promise<void>;
}

interface SectionConfig {
  id: string;           // 'hero' | 'greeting' | 'gallery' | ...
  enabled: boolean;
  order: number;
  data: Record<string, any>;
  tier: 'basic' | 'premium' | 'arcade';  // 어느 티어부터 사용 가능
}
```

### 섹션 → 티어 매핑

| 섹션 | Basic | Premium | Arcade |
|------|-------|---------|--------|
| Hero | O | O | O |
| Greeting | O | O | O |
| CoupleIntro | O | O | O |
| Gallery | O (20장) | O (50장) | O (50장) |
| WeddingInfo | O | O | O |
| Location | O | O | O |
| Account | O | O | O |
| Share | O | O | O |
| Footer | O | O | O |
| Video | O | O | O |
| Interview | - | O | O |
| Timeline | - | O | O |
| GuestSnap | O | O | O |
| MusicPlayer | - | O | O |
| MouseTrail | - | O | O |
| RSVP | - | O | O |
| Guestbook | - | O | O |
| TerminalIntro | - | - | O |
| Arcade Mode | - | - | O |
| 3D Effects | - | O | O |

## 5. 기술 스택 상세

| 레이어 | 기술 | 버전 | 선택 이유 |
|--------|------|------|----------|
| **Frontend** | Next.js | 16.x | 기존 프로젝트 동일, SSR/ISR |
| | React | 19 | 기존 동일, Server Components |
| | TypeScript | 5.x | 기존 동일 |
| | Tailwind CSS | v4 | 기존 동일 |
| | Framer Motion | latest | 기존 동일, 애니메이션 |
| | Three.js | latest | 기존 동일, 3D |
| | Zustand | latest | 에디터 상태 관리 |
| | TanStack Query | latest | 서버 상태 관리 |
| **Backend** | Next.js API Routes | - | 별도 서버 불필요 |
| | Supabase | latest | Auth + DB + Storage |
| **Database** | PostgreSQL | 15+ | Supabase managed |
| **Storage** | Vercel Blob | - | 이미지 업로드 |
| **Payment** | 토스페이먼츠 | - | 국내 결제 |
| **Hosting** | Vercel | Pro | SSR + Edge |
| **Analytics** | Vercel Analytics | - | 기본 분석 |
| **Monitoring** | Sentry | - | 에러 추적 |

## 6. Make vs Buy 결정

| 영역 | 결정 | 서비스 | 이유 |
|------|------|--------|------|
| 인증 | Buy | Supabase Auth | 소셜 로그인 + 보안 |
| 데이터베이스 | Buy | Supabase (PostgreSQL) | 관리형, 무료 티어 |
| 결제 | Buy | 토스페이먼츠 | 국내 결제, 카카오페이/네이버페이 |
| 이미지 저장 | Buy | Vercel Blob | Next.js 통합 |
| 이메일 | Buy | Resend | 결제 확인/알림 |
| 에디터 UI | Make | 자체 개발 | 핵심 차별화 |
| 청첩장 렌더링 | Make | 자체 개발 | 핵심 자산 |
| 아케이드 모드 | Make | 자체 개발 | 핵심 차별화 |

## 7. 월간 인프라 비용 추정

| 서비스 | 무료 티어 | 성장 시 (월 300건) | 스케일 (월 1000건) |
|--------|----------|-------------------|-------------------|
| Vercel Pro | $20 | $20 | $20 |
| Supabase Pro | $25 | $25 | $25 |
| Vercel Blob | $0 (1GB) | $5 | $20 |
| 토스페이먼츠 | 3.5% 수수료 | ~31만원 | ~105만원 |
| Resend | 무료 (3K/월) | 무료 | $20 |
| Sentry | 무료 | 무료 | $26 |
| 도메인 | ~2만원/년 | ~2만원/년 | ~2만원/년 |
| **합계** | **~8만원/월** | **~40만원/월** | **~120만원/월** |

---

*다음 단계: Effort Estimation -> Roadmap -> GTM Strategy*
