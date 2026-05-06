#!/usr/bin/env python3
"""WeddingCraft Phase 0 — 기존 이슈 업데이트 + 누락 이슈 등록.

기존 이슈 21개와 2026-04-23 코드베이스 점검 결과를 대조하여:
1. 기존 이슈에 누락된 세부 작업을 sub-issue로 등록
2. 아예 빠져있는 영역을 새 이슈로 등록

대상 인프라: GCP (Cloud Run, Cloud SQL, Firebase Auth) + Cloudflare (R2, CDN)
"""

import json
import subprocess

PROJECT_ID = "dc92d0e4-76fa-4c50-9382-33116a3fd9d9"

# ── 기존 이슈 ID (parent 연결용) ─────────────────────────
EXISTING = {
    "WOO-13": "5d1ae1dc-720",  # 프로젝트 정리
    "WOO-19": "fb7206af-953",  # DB 스키마 (Cloud SQL + Prisma)
    "WOO-20": "5e52ef52-910",  # 인증 시스템 (Firebase Auth)
    "WOO-28": "7ee9d8d8-37c",  # 사진/미디어 업로드
    "WOO-30": "30391969-aeb",  # GCP 인프라 구성
    "WOO-31": "17c89533-954",  # 보안 강화
    "WOO-38": "7b0f92fc-4f8",  # Vercel → Cloud Run
    "WOO-39": "07a1c227-de7",  # Supabase → Prisma
    "WOO-40": "9ca448c6-bb7",  # Supabase → Cloud SQL
}


def get_full_id(short_id: str) -> str:
    """짧은 ID에서 전체 ID를 조회."""
    result = subprocess.run(
        ["multica", "issue", "list", "--project", PROJECT_ID, "--output", "json"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return short_id
    data = json.loads(result.stdout)
    items = data.get("data", data) if isinstance(data, dict) else data
    for item in items:
        if isinstance(item, dict) and item.get("id", "").startswith(short_id):
            return item["id"]
    return short_id


def create_issue(
    title: str,
    priority: str,
    assignee: str,
    description: str,
    parent_id: str | None = None,
) -> str | None:
    cmd = [
        "multica",
        "issue",
        "create",
        "--project",
        PROJECT_ID,
        "--title",
        title,
        "--priority",
        priority,
        "--assignee",
        assignee,
        "--description",
        description,
        "--status",
        "backlog",
        "--output",
        "json",
    ]
    if parent_id:
        cmd.extend(["--parent", parent_id])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ FAILED: {title}")
        if result.stderr:
            print(f"    stderr: {result.stderr.strip()}")
        return None
    data = json.loads(result.stdout)
    ident = data.get("identifier", "?")
    print(f"  ✓ {ident:8s} | {priority:6s} | {assignee:20s} | {title}")
    return data.get("id")


# ── 전체 ID 조회 (첫 호출에서 캐싱) ─────────────────────
print("기존 이슈 ID 조회 중...")
result = subprocess.run(
    ["multica", "issue", "list", "--project", PROJECT_ID, "--output", "json"],
    capture_output=True,
    text=True,
)
full_ids = {}
if result.returncode == 0:
    data = json.loads(result.stdout)
    items = data.get("data", data) if isinstance(data, dict) else data
    for item in items:
        if isinstance(item, dict):
            for key, short in EXISTING.items():
                if item["id"].startswith(short):
                    full_ids[key] = item["id"]
                    break

print(f"  매핑 완료: {len(full_ids)}/{len(EXISTING)} 이슈")
print()


# ═══════════════════════════════════════════════════════════
# Phase 0: 프로젝트 정리 + 인프라 통일
# ═══════════════════════════════════════════════════════════

print("=" * 70)
print(" Phase 0: 프로젝트 정리 + 인프라 통일 — 누락 이슈 등록")
print("=" * 70)

# ── WOO-13 하위: 개인 데이터 제거 세부 작업 ──────────────
parent_13 = full_ids.get("WOO-13")

print("\n── WOO-13 하위: 프로젝트 정리 세부 ──")

create_issue(
    "[정리-1] 개인 데이터 완전 제거 (constants.ts, gallery.ts)",
    "urgent",
    "Wedding Frontend Dev",
    (
        "## 배경\n"
        "src/lib/constants.ts에 강태욱/김선경 개인정보(이름, 연락처, 계좌번호 6개, 주소, 좌표)가\n"
        "하드코딩되어 있음. gallery.ts에 개인 사진 30장 하드코딩.\n\n"
        "## 작업 내용\n"
        "- [ ] src/lib/constants.ts — WEDDING_INFO 객체 전체 제거\n"
        "- [ ] src/lib/gallery.ts — 하드코딩 사진 배열 제거\n"
        "- [ ] src/app/invitation/page.tsx — 개인 정적 청첩장 페이지 삭제\n"
        "- [ ] src/app/page.tsx — /invitation 리다이렉트 삭제\n"
        "- [ ] TODO-WEDDING-INFO.md — 개인정보 체크리스트 삭제\n"
        "- [ ] getSiteUrl() — VERCEL_* fallback 제거\n\n"
        "## 완료 조건\n"
        "- grep -r '강태욱\\|김선경\\|010-1234' src/ 결과 0건\n"
        "- 빌드 성공"
    ),
    parent_13,
)

create_issue(
    "[정리-2] 16개 섹션 컴포넌트 props 전환",
    "urgent",
    "Wedding Frontend Dev",
    (
        "## 배경\n"
        "src/components/sections/ 의 16개 컴포넌트가 WEDDING_INFO를 직접 import.\n"
        "멀티테넌트에서는 DB에서 받은 데이터를 props로 전달해야 함.\n\n"
        "## 작업 내용\n"
        "- [ ] Hero, Greeting, CoupleIntro, Interview, Gallery, Video, Timeline 등\n"
        "      16개 컴포넌트에서 `import { WEDDING_INFO }` 제거\n"
        "- [ ] 각 컴포넌트에 Props 타입 정의 + props 기반으로 전환\n"
        "- [ ] src/app/layout.tsx — 하드코딩 OG 메타데이터 동적 생성으로 전환\n\n"
        "## 완료 조건\n"
        "- grep -r 'WEDDING_INFO' src/components/ 결과 0건\n"
        "- 기존 InvitationRenderer를 통한 렌더링 정상 동작"
    ),
    parent_13,
)

create_issue(
    "[정리-3] 섹션 타입 네이밍 통일 (camelCase → snake_case)",
    "high",
    "Wedding Frontend Dev",
    (
        "## 배경\n"
        "현재 두 가지 섹션 타입 정의가 불일치:\n"
        "- saas/invitation.ts: 'weddingInfo', 'coupleIntro' (camelCase, 20종)\n"
        "- renderer/types.ts: 'wedding_info', 'couple_intro' (snake_case, 16종)\n\n"
        "## 작업 내용\n"
        "- [ ] snake_case를 단일 소스로 통일 (DB 컬럼 친화적)\n"
        "- [ ] src/types/saas/invitation.ts SectionType 변경\n"
        "- [ ] 에디터 스토어 내부도 snake_case 사용\n"
        "- [ ] data-transformer.ts 변환 레이어 간소화\n"
        "- [ ] 누락된 4개 섹션 타입 renderer에 추가\n\n"
        "## 완료 조건\n"
        "- SectionType 정의가 프로젝트 전체에서 1곳만 존재\n"
        "- 에디터 ↔ DB ↔ 렌더러 간 변환 없이 동일 타입 사용"
    ),
    parent_13,
)

create_issue(
    "[정리-4] Firebase 의존성 제거 + 방명록 Supabase→Cloud SQL 전환",
    "high",
    "Wedding Frontend Dev",
    (
        "## 배경\n"
        "현재 방명록이 Firebase Firestore + Giscus(GitHub Discussions) 이중 구현.\n"
        "GCP + Cloudflare 구조에서 Firebase는 불필요한 외부 의존성.\n"
        "Cloud SQL로 통합 시 guestbook_entries 테이블 사용.\n\n"
        "## 작업 내용\n"
        "- [ ] src/lib/firebase.ts 삭제\n"
        "- [ ] package.json에서 firebase 패키지 제거\n"
        "- [ ] NEXT_PUBLIC_FIREBASE_* 환경변수 6개 제거\n"
        "- [ ] Giscus 관련 설정 (constants.ts GISCUS_CONFIG) 제거\n"
        "- [ ] 방명록 컴포넌트를 Cloud SQL guestbook_entries 테이블 기반으로 전환\n\n"
        "## 완료 조건\n"
        "- grep -r 'firebase' src/ 결과 0건\n"
        "- 방명록 CRUD가 Cloud SQL을 통해 정상 동작"
    ),
    parent_13,
)

# ── WOO-28 하위: Google Drive → Cloudflare R2 ───────────
parent_28 = full_ids.get("WOO-28")

print("\n── WOO-28 하위: Google Drive → R2 전환 ──")

create_issue(
    "[R2-1] Cloudflare R2 스토리지 클라이언트 구현",
    "high",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "GuestSnap이 현재 Google Drive API(11개 함수, 746줄)에 의존.\n"
        "Cloudflare R2(S3 호환)로 전환하여 조직 패턴(memoriz R2)과 통일.\n\n"
        "## 작업 내용\n"
        "- [ ] @aws-sdk/client-s3, @aws-sdk/s3-request-presigner 설치\n"
        "- [ ] src/lib/guestsnap/storage-client.ts 신규 작성\n"
        "  - createGuestFolder() → 키 프리픽스 기반 ({invitationId}/{guestName}/)\n"
        "  - createPresignedUploadUrl() → S3 PutObject presigned URL\n"
        "  - getUploadCount() → ListObjectsV2 count\n"
        "  - verifyUpload() → HeadObject\n"
        "  - checkStorageStatus() → HeadBucket\n"
        "- [ ] src/lib/guestsnap/storage-config.ts 신규 (환경변수 검증)\n"
        "- [ ] R2 버킷 CORS 설정 문서화\n\n"
        "## 환경변수\n"
        "R2_ENDPOINT, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY,\n"
        "R2_BUCKET_NAME, R2_PUBLIC_URL\n\n"
        "## 완료 조건\n"
        "- 로컬에서 R2 presigned URL 업로드 테스트 통과"
    ),
    parent_28,
)

create_issue(
    "[R2-2] GuestSnap API 라우트 R2 전환",
    "high",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "5개 GuestSnap API 라우트가 google-drive-client.ts를 호출 중.\n"
        "storage-client.ts(R2)로 교체 필요.\n\n"
        "## 작업 내용\n"
        "- [ ] POST /api/guestsnap/session → R2 키 프리픽스 생성\n"
        "- [ ] POST /api/guestsnap/upload/init → R2 presigned URL 반환\n"
        "- [ ] POST /api/guestsnap/upload/complete → R2 HeadObject 검증\n"
        "- [ ] GET /api/guestsnap/status → R2 HeadBucket 체크\n"
        "- [ ] 세션 쿠키: folderPath(Drive ID) → keyPrefix(R2 키) 전환\n"
        "- [ ] google-drive-client.ts, drive-config.ts 삭제\n"
        "- [ ] googleapis 패키지 제거\n\n"
        "## 완료 조건\n"
        "- GuestSnap 전체 플로우 (세션→업로드→완료→알림) R2로 동작\n"
        "- grep -r 'googleapis\\|google-drive' src/ 결과 0건"
    ),
    parent_28,
)

# ── WOO-30 하위: CI/CD ──────────────────────────────────
parent_30 = full_ids.get("WOO-30")

print("\n── WOO-30 하위: CI/CD 파이프라인 ──")

create_issue(
    "[CI/CD-1] GitHub Actions 워크플로우 구성",
    "high",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "현재 CI/CD 파이프라인 없음. CheckYourHospital 패턴을 따라\n"
        "GitHub Actions → Cloud Build → Cloud Run 배포 구성.\n\n"
        "## 작업 내용\n"
        "- [ ] .github/workflows/ci.yml — PR 시 lint + test\n"
        "- [ ] .github/workflows/deploy.yml — master push 시 Cloud Run 배포\n"
        "- [ ] deploy.sh — 수동 배포 스크립트 (CheckYourHospital 패턴)\n"
        "- [ ] GCP Service Account 키 GitHub Secrets 등록\n"
        "- [ ] Build-time env vars (NEXT_PUBLIC_*) 분리\n\n"
        "## 관련 파일\n"
        "- 참고: workspace/mediscope/apps/web/deploy.sh\n\n"
        "## 완료 조건\n"
        "- master push → 자동 배포 → Cloud Run 서비스 업데이트"
    ),
    parent_30,
)

# ── WOO-31 하위: 보안 세부 ──────────────────────────────
parent_31 = full_ids.get("WOO-31")

print("\n── WOO-31 하위: 보안 세부 ──")

create_issue(
    "[보안-1] HTTP 보안 헤더 미들웨어 추가",
    "urgent",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "현재 보안 헤더 전무. XSS, 클릭재킹, MIME 스니핑 공격에 노출.\n\n"
        "## 작업 내용\n"
        "- [ ] src/middleware.ts에 보안 헤더 추가:\n"
        "  - Content-Security-Policy\n"
        "  - X-Frame-Options: DENY\n"
        "  - X-Content-Type-Options: nosniff\n"
        "  - Strict-Transport-Security\n"
        "  - Referrer-Policy: strict-origin-when-cross-origin\n"
        "  - Permissions-Policy\n\n"
        "## 완료 조건\n"
        "- securityheaders.com 스캔 A 등급 이상"
    ),
    parent_31,
)

create_issue(
    "[보안-2] Toss 웹훅 HMAC-SHA256 서명 검증 구현",
    "urgent",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "src/lib/payment/toss.ts line 132: verifyWebhookSignature()가 항상 true 반환.\n"
        "공격자가 웹훅 URL만 알면 결제 위조 가능.\n\n"
        "## 작업 내용\n"
        "- [ ] Toss Payments HMAC-SHA256 서명 검증 로직 구현\n"
        "- [ ] 웹훅 핸들러에서 서명 불일치 시 403 반환\n"
        "- [ ] 테스트 작성 (유효/무효 서명)\n\n"
        "## 완료 조건\n"
        "- 유효하지 않은 서명으로 웹훅 호출 시 403 반환\n"
        "- 유효 서명 시 정상 처리"
    ),
    parent_31,
)

create_issue(
    "[보안-3] 환경변수 Zod 스키마 검증",
    "high",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "환경변수 누락 시 런타임에서 조용히 실패. 배포 후 장애 원인 파악 어려움.\n\n"
        "## 작업 내용\n"
        "- [ ] src/lib/env.ts — Zod 스키마로 필수 환경변수 정의\n"
        "- [ ] 서버 시작 시 검증 (실패 시 명확한 에러 메시지)\n"
        "- [ ] Build-time(NEXT_PUBLIC_*) vs Runtime 분리\n\n"
        "## 검증 대상\n"
        "NEXT_PUBLIC_SUPABASE_URL → Cloud SQL 연결 문자열로 변경 예정\n"
        "TOSS_SECRET_KEY, R2_*, RESEND_API_KEY 등\n\n"
        "## 완료 조건\n"
        "- 필수 환경변수 1개 누락 시 서버 시작 실패 + 명확한 에러 로그"
    ),
    parent_31,
)

create_issue(
    "[보안-4] Sentry 에러 모니터링 연동",
    "high",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "현재 에러 처리가 console.error()만 사용. 프로덕션 장애 감지 불가.\n\n"
        "## 작업 내용\n"
        "- [ ] @sentry/nextjs 설치\n"
        "- [ ] sentry.client.config.ts + sentry.server.config.ts\n"
        "- [ ] next.config.ts에 withSentryConfig 래핑\n"
        "- [ ] 결제 실패, GuestSnap 업로드 실패 등 핵심 에러 캡처\n"
        "- [ ] 환경변수: SENTRY_DSN, SENTRY_AUTH_TOKEN\n\n"
        "## 완료 조건\n"
        "- 의도적 에러 발생 시 Sentry 대시보드에 이벤트 표시"
    ),
    parent_31,
)

# ── 완전 신규 이슈 (기존에 없는 영역) ────────────────────

print("\n── 신규 이슈: 기존에 누락된 영역 ──")

create_issue(
    "[Phase0] Vercel 의존성 완전 제거",
    "high",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "WOO-38(Cloud Run 전환)의 선행 작업.\n"
        "Vercel 관련 코드/설정을 먼저 제거해야 깨끗한 마이그레이션 가능.\n\n"
        "## 작업 내용\n"
        "- [ ] .vercel/ 디렉토리 삭제\n"
        "- [ ] .vercelignore 삭제\n"
        "- [ ] package.json: env:pull 스크립트 제거\n"
        "- [ ] src/lib/constants.ts: VERCEL_URL, VERCEL_PROJECT_PRODUCTION_URL 참조 제거\n"
        "- [ ] getSiteUrl() → NEXT_PUBLIC_SITE_URL만 사용\n"
        "- [ ] next.config.ts: output: 'standalone' 추가\n"
        "- [ ] .gitignore에 .vercel/ 제거 (더 이상 불필요)\n\n"
        "## 완료 조건\n"
        "- grep -ri 'vercel' src/ 결과 0건\n"
        "- next build 성공 (standalone 모드)"
    ),
)

create_issue(
    "[Phase0] Dockerfile 작성 (Cloud Run용 Next.js standalone)",
    "high",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "CheckYourHospital(cyh-web) 패턴을 따라 multi-stage Dockerfile 작성.\n"
        "memoriz-b5ba9 프로젝트, asia-northeast3 리전에 배포.\n\n"
        "## 작업 내용\n"
        "- [ ] Dockerfile (3-stage: deps → builder → runner)\n"
        "  - node:22-slim 기반\n"
        "  - pnpm install → next build (standalone)\n"
        "  - sharp 설치 (이미지 최적화)\n"
        "  - PORT=8080\n"
        "- [ ] .dockerignore 작성\n"
        "- [ ] deploy.sh 작성 (gcloud run deploy)\n"
        "  - --memory 512Mi --max-instances 3\n"
        "  - Build-time env vars 분리\n"
        "- [ ] 로컬 Docker 빌드 + 실행 테스트\n\n"
        "## 참고\n"
        "workspace/mediscope/apps/web/Dockerfile\n\n"
        "## 완료 조건\n"
        "- docker build + docker run → localhost:8080 접속 정상\n"
        "- gcloud run deploy → Cloud Run 서비스 생성 확인"
    ),
)

create_issue(
    "[Phase0] R2 버킷 생성 + CORS + 도메인 설정",
    "high",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "GuestSnap 파일 저장용 R2 버킷 인프라 준비.\n"
        "memoriz Cloudflare 계정에서 관리.\n\n"
        "## 작업 내용\n"
        "- [ ] Cloudflare 대시보드에서 wedding-guestsnap 버킷 생성 (APAC 리전)\n"
        "- [ ] CORS 정책 설정:\n"
        "  - AllowedOrigins: 프로덕션 도메인 + localhost:3000\n"
        "  - AllowedMethods: GET, PUT, HEAD\n"
        "  - AllowedHeaders: Content-Type, Content-Length\n"
        "- [ ] R2 API 토큰 생성 (Object Read/Write 권한)\n"
        "- [ ] 커스텀 도메인 매핑 (선택: guestsnap.weddingcraft.kr)\n"
        "- [ ] 버킷 키 구조 문서화:\n"
        "  {invitationId}/{guestName}/{filename}\n\n"
        "## 완료 조건\n"
        "- curl로 presigned URL 통한 파일 업로드/다운로드 테스트 성공"
    ),
)

create_issue(
    "[Phase0] 에디터 저장 연결 (에디터 → DB)",
    "urgent",
    "Wedding Frontend Dev",
    (
        "## 배경\n"
        "src/stores/editor-store.ts의 save() 함수가 setTimeout(500ms) mock.\n"
        "에디터에서 수정한 내용이 DB에 저장되지 않음.\n"
        "[slug] 페이지에서 기존 초대장 로드도 미구현 (TODO 주석만 존재).\n\n"
        "## 작업 내용\n"
        "- [ ] save() → POST/PUT /api/invitations/[id]/sections 호출\n"
        "- [ ] [invitationId]/page.tsx → GET /api/invitations/[id] fetch + 스토어 로드\n"
        "- [ ] 자동저장 (debounce 3초) + 저장 상태 UI 피드백\n"
        "- [ ] 에러 핸들링 (네트워크 실패, 인증 만료)\n"
        "- [ ] 권한 검증 (본인 초대장만 편집 가능)\n\n"
        "## 참고 파일\n"
        "- src/stores/editor-store.ts:245-248 (mock save)\n"
        "- src/app/(editor)/editor/[invitationId]/page.tsx:15 (TODO)\n\n"
        "## 완료 조건\n"
        "- 에디터에서 섹션 수정 → DB 저장 → 새로고침 후 복원"
    ),
)

create_issue(
    "[Phase0] 대시보드 mock 데이터 → 실 DB 쿼리 전환",
    "high",
    "Wedding Frontend Dev",
    (
        "## 배경\n"
        "8개 대시보드 페이지 전부 MOCK_* 상수 사용. API 호출 0건.\n\n"
        "## 작업 내용\n"
        "- [ ] /dashboard — 실 초대장 요약 + 최근 활동 쿼리\n"
        "- [ ] /dashboard/invitation — 사용자 초대장 목록 CRUD\n"
        "- [ ] /dashboard/analytics — analytics_events 집계\n"
        "- [ ] /dashboard/rsvp — rsvp_responses 조회 + CSV 내보내기\n"
        "- [ ] /dashboard/guestsnap — R2 파일 목록 + 스토리지 사용량\n"
        "- [ ] /dashboard/notifications — 알림 설정 CRUD\n"
        "- [ ] /dashboard/settings — 사용자 프로필/결제 내역\n"
        "- [ ] /dashboard/afterparty — afterparty_places CRUD\n"
        "- [ ] 모든 페이지에 인증 컨텍스트 + 에러/로딩 상태\n"
        "- [ ] MOCK_* 상수 및 mock-data.ts 삭제\n\n"
        "## 완료 조건\n"
        "- grep -r 'MOCK_' src/app/ 결과 0건\n"
        "- 대시보드 전체 실 데이터로 동작"
    ),
)

create_issue(
    "[인프라] Cloud SQL 인스턴스 생성 + Prisma 스키마 마이그레이션",
    "urgent",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "WOO-19, WOO-39, WOO-40의 실행 작업.\n"
        "현재 Supabase 스키마(9테이블)를 Cloud SQL PostgreSQL + Prisma로 이전.\n\n"
        "## 작업 내용\n"
        "- [ ] Cloud SQL PostgreSQL 인스턴스 생성 (asia-northeast3)\n"
        "  - 머신 타입: db-f1-micro (초기) → 필요시 확장\n"
        "  - 자동 백업 활성화\n"
        "- [ ] Prisma 설치 + prisma/schema.prisma 작성\n"
        "  - Supabase 9테이블 → Prisma 모델 변환\n"
        "  - orders 테이블 필드 보강 (payment_key UNIQUE, method, receipt_url)\n"
        "- [ ] Prisma migrate 실행\n"
        "- [ ] Cloud SQL Auth Proxy 또는 직접 연결 설정\n"
        "- [ ] src/lib/supabase/ → src/lib/db/ (Prisma client) 전환\n"
        "- [ ] 모든 API 라우트의 Supabase 쿼리 → Prisma 쿼리 전환\n"
        "- [ ] @supabase/ssr, @supabase/supabase-js 패키지 제거\n\n"
        "## 현재 Supabase 테이블\n"
        "profiles, invitations, section_data, rsvp_responses,\n"
        "guestbook_entries, guestsnap_sessions, guestsnap_files,\n"
        "orders, analytics_events, afterparty_places\n\n"
        "## 완료 조건\n"
        "- Prisma Studio로 전체 테이블 확인\n"
        "- 기존 API 라우트 전부 Cloud SQL 기반 동작\n"
        "- grep -r 'supabase' src/ 결과 0건 (auth 제외)"
    ),
)

create_issue(
    "[인프라] Firebase Auth 연동 (Supabase Auth 대체)",
    "urgent",
    "Wedding Infra Engineer",
    (
        "## 배경\n"
        "WOO-20의 구체화. Supabase Auth → Firebase Auth(GCP 네이티브)로 전환.\n\n"
        "## 작업 내용\n"
        "- [ ] Firebase 프로젝트에 Auth 활성화 (memoriz-b5ba9)\n"
        "- [ ] 이메일/비밀번호 + 카카오 OAuth + Google OAuth 설정\n"
        "- [ ] firebase-admin SDK 서버 사이드 설치 + 초기화\n"
        "- [ ] src/middleware.ts — Supabase 세션 → Firebase ID Token 검증\n"
        "- [ ] /auth/login, /auth/signup, /auth/forgot-password 페이지 생성\n"
        "- [ ] /auth/callback — OAuth 콜백 처리\n"
        "- [ ] AuthProvider (React Context) — 세션 상태 관리\n"
        "- [ ] UserMenu 컴포넌트 (로그인/로그아웃)\n"
        "- [ ] @supabase/ssr의 세션 관리 → Firebase 커스텀 쿠키 기반 전환\n\n"
        "## 완료 조건\n"
        "- 이메일 회원가입 → 로그인 → 대시보드 접근 → 로그아웃 플로우 동작\n"
        "- 미인증 사용자 /dashboard 접근 시 /auth/login 리다이렉트"
    ),
)

create_issue(
    "[Phase0] 결제 DB 저장 + orders 테이블 보강",
    "high",
    "Wedding Frontend Dev",
    (
        "## 배경\n"
        "결제 확인 후 DB 저장 로직 없음. 웹훅 핸들러에 TODO 5개.\n"
        "orders 테이블에 결제 확인 필드 부족.\n\n"
        "## 작업 내용\n"
        "- [ ] orders 테이블 필드 추가:\n"
        "  - payment_key (UNIQUE)\n"
        "  - method (카드/계좌이체 등)\n"
        "  - receipt_url\n"
        "  - approved_at\n"
        "  - addon 정보 저장 (JSONB)\n"
        "- [ ] POST /api/payment/confirm — 결제 성공 시 DB insert\n"
        "- [ ] POST /api/payment/webhook — 상태별 DB update\n"
        "  - DONE → paid, CANCELED → refunded 매핑\n"
        "- [ ] 멱등성 키 구현 (중복 결제 방지)\n\n"
        "## 완료 조건\n"
        "- 테스트 결제 → orders 테이블 레코드 생성 확인\n"
        "- 웹훅 재전송 시 중복 처리 없음"
    ),
)

print("\n" + "=" * 70)
print(" 등록 완료")
print("=" * 70)
