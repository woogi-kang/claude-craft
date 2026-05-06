#!/usr/bin/env python3
"""CYH Dashboard SaaS MVP 이슈 등록."""

import json
import subprocess
from dataclasses import dataclass

PROJECT_ID = "18031aa2-6cc7-4a99-ae6b-147494f07d0c"


@dataclass
class Issue:
    title: str
    priority: str
    assignee: str
    description: str
    children: list["Issue"] | None = None


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
        print(f"  x FAILED: {title}")
        return None
    data = json.loads(result.stdout)
    print(f"  ok {data['identifier']:8s} | {priority:6s} | {assignee:20s} | {title}")
    return data.get("id")


def register_phase(name: str, epic: Issue):
    print(f"\n--- {name} ---")
    epic_id = create_issue(epic.title, epic.priority, epic.assignee, epic.description)
    if epic.children and epic_id:
        for child in epic.children:
            create_issue(
                child.title,
                child.priority,
                child.assignee,
                child.description,
                parent_id=epic_id,
            )


# ============================================================
# Phase 1: MVP 대시보드
# ============================================================

PHASE_1 = Issue(
    title="[Dashboard] Phase 1: MVP 대시보드 (외국인환자 유치 관제탑)",
    priority="urgent",
    assignee="CYH Planner",
    description=(
        "## 비전\n"
        "원샷 진단 도구 → 구독형 SaaS 대시보드 전환.\n"
        "'외국인 환자 유치의 관제탑' — 매주 내 병원 상태를 업데이트.\n\n"
        "## 핵심 가치\n"
        "외국인 환자 1명 객단가 300-500만원. 월 89만원은 환자 0.2명분.\n"
        "월 1명만 더 오면 4배 ROI.\n\n"
        "## MVP 스코프 (9개 하위 이슈)\n"
        "1. 고객 인증 (Supabase Auth 확장)\n"
        "2. 대시보드 레이아웃 + 라우팅\n"
        "3. 스코어카드 (점수 추이 + 등급)\n"
        "4. 경쟁 병원 비교 (최대 10곳)\n"
        "5. AI 검색 노출 모니터링\n"
        "6. 주간 TODO 엔진 + 효과 측정\n"
        "7. 의료광고 법규 알림\n"
        "8. 리뷰 통합 피드 (Google API + Naver 스크래핑)\n"
        "9. 플랜 게이트 (Pro/Max/Enterprise)"
    ),
    children=[
        Issue(
            title="[Dash-1] 고객 인증 — Supabase Auth customer role 확장",
            priority="urgent",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "현재 Supabase Auth는 admin role만 사용. 병원 고객용 customer role 추가 필요.\n\n"
                "## 요구사항\n"
                "- [ ] 고객 회원가입/로그인 (이메일+비밀번호)\n"
                "- [ ] app_metadata에 role='customer', hospital_id, plan_tier 저장\n"
                "- [ ] RLS 정책: customer는 자기 hospital_id 데이터만 조회\n"
                "- [ ] 플랜 티어: 'pro'(39만), 'max'(89만), 'enterprise'(189만+)\n"
                "- [ ] 관리자가 고객 계정 생성 가능 (admin 대시보드에서)\n"
                "- [ ] 비밀번호 재설정, 이메일 인증\n"
                "- [ ] 미들웨어: /dashboard/* 경로 인증 필수\n\n"
                "## DB 변경\n"
                "- customer_profiles 테이블: user_id FK, hospital_id FK, plan_tier, billing_cycle, subscribed_at, expires_at\n\n"
                "## 관련 파일\n"
                "- apps/web/src/lib/supabase/ (Auth 클라이언트)\n"
                "- apps/web/src/middleware.ts (라우트 보호)"
            ),
        ),
        Issue(
            title="[Dash-2] 대시보드 레이아웃 + 네비게이션",
            priority="urgent",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "고객이 로그인 후 볼 메인 대시보드 레이아웃.\n\n"
                "## 요구사항\n"
                "- [ ] /dashboard 레이아웃 (사이드바 + 메인 컨텐츠)\n"
                "- [ ] 사이드바 네비게이션:\n"
                "  - Overview (스코어카드)\n"
                "  - Competitors (경쟁사 비교)\n"
                "  - AI Search (AI 검색 노출)\n"
                "  - Reviews (리뷰 통합 피드)\n"
                "  - TODO (주간 액션)\n"
                "  - Compliance (법규 알림)\n"
                "  - Keywords [Max] (키워드 인텔리전스)\n"
                "  - Pricing [Max] (가격 벤치마킹)\n"
                "  - Settings (설정)\n"
                "- [ ] 상단 바: 병원명, 플랜 뱃지, 마지막 스캔일, 알림 벨\n"
                "- [ ] 모바일 반응형 (사이드바 → 하단 탭)\n"
                "- [ ] 플랜별 메뉴 잠금 표시 (자물쇠 아이콘)\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/app/dashboard/layout.tsx\n"
                "- 신규: apps/web/src/components/dashboard/sidebar.tsx"
            ),
        ),
        Issue(
            title="[Dash-3] 스코어카드 — 점수 추이 + 카테고리 breakdown",
            priority="urgent",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "대시보드 메인 화면. 내 병원 현재 상태 한눈에.\n\n"
                "## 요구사항\n"
                "- [ ] /dashboard (Overview 페이지)\n"
                "- [ ] 상단 카드: 총점 (큰 숫자) + 등급 뱃지 + 지난 스캔 대비 변동 (+3/-5)\n"
                "- [ ] 6카테고리 서브스코어 수평 바 (이미 리포트에 있음, 재사용)\n"
                "- [ ] 점수 추이 라인 차트 (최근 12주, Recharts)\n"
                "  - 데이터 소스: score_history 테이블\n"
                "- [ ] 업종 평균 대비 위치 (백분위)\n"
                "- [ ] '마지막 스캔: 3일 전' + '다음 스캔: 4일 후' 표시\n"
                "- [ ] '지금 재스캔' 버튼 (플랜별 횟수 제한)\n"
                "  - Pro: 월 2회, Max: 일 1회, Enterprise: 무제한\n\n"
                "## 데이터 소스\n"
                "- audits 테이블 (최신 스캔 결과)\n"
                "- score_history 테이블 (추이)\n"
                "- benchmark (업종 평균)\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/app/dashboard/page.tsx\n"
                "- 재사용: components/report/radar-chart.tsx"
            ),
        ),
        Issue(
            title="[Dash-4] 경쟁 병원 비교 — 랭킹 + 격차 분석",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "같은 지역 경쟁 병원과 비교. Pro: 3곳, Max: 10곳.\n\n"
                "## 요구사항\n"
                "- [ ] /dashboard/competitors\n"
                "- [ ] 경쟁사 랭킹 테이블:\n"
                "  - 순위 | 병원명 | 총점 | SEO | AEO | 변동\n"
                "  - 내 병원 하이라이트 행\n"
                "  - 색상 코딩 (A=초록 ~ F=빨강)\n"
                "- [ ] 1위와의 격차 분석: '1위 대비 부족한 항목: Schema, 영문 콘텐츠, FAQ'\n"
                "- [ ] 레이더 차트: 내 병원 vs 경쟁사 상위 3곳 (6축)\n"
                "- [ ] 경쟁사 변동 알림: '경쟁사 B가 AEO 35->67 급상승'\n"
                "- [ ] 데이터 갱신: 재스캔 시 자동 + 경쟁사도 주기적 스캔\n\n"
                "## 백엔드\n"
                "- competitor_discovery.py 결과를 주기적으로 갱신\n"
                "- competitors 테이블: hospital_id, competitor_hospital_id, discovered_at\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/app/dashboard/competitors/page.tsx\n"
                "- 재사용: competitor-radar-benchmark.tsx"
            ),
        ),
        Issue(
            title="[Dash-5] AI 검색 노출 모니터링 — 키워드별 추적",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "CYH 최대 차별점. ChatGPT/Gemini/Perplexity/Claude에 질문했을 때 내 병원 언급 여부.\n"
                "Pro: 10개 키워드, Max: 50개.\n\n"
                "## 요구사항\n"
                "- [ ] /dashboard/ai-search\n"
                "- [ ] 키워드 × AI엔진 매트릭스:\n"
                "  - 행: 키워드 ('강남 피부과', 'Gangnam dermatology' 등)\n"
                "  - 열: ChatGPT | Gemini | Perplexity | Claude\n"
                "  - 셀: 언급됨(초록)/미언급(빨강)/부분언급(노랑) + 순위\n"
                "- [ ] 추이 차트: 주별 언급률 변화 (키워드당)\n"
                "- [ ] 신규 키워드 추가/삭제 관리\n"
                "- [ ] 자동 키워드 제안: 시술 기반 + 지역 + 다국어\n"
                "- [ ] 알림: '이번 주 ChatGPT에서 처음으로 언급되기 시작했습니다'\n\n"
                "## 백엔드\n"
                "- ai_mention_tracking 테이블: hospital_id, keyword, engine, mentioned, rank, checked_at\n"
                "- cron: 주 1회(Pro) / 일 1회(Max) AI 시뮬레이션 실행\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/app/dashboard/ai-search/page.tsx\n"
                "- 재사용: ai-simulation-matrix.tsx"
            ),
        ),
        Issue(
            title="[Dash-6] 주간 TODO 엔진 + 효과 측정",
            priority="high",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "스캔 결과를 점수 나열로 끝내지 말고 구체적 실행 항목으로 변환.\n"
                "'이번 주 할 일 3가지' → 완료 체크 → 다음 스캔에서 효과 측정.\n\n"
                "## 요구사항\n"
                "### 백엔드\n"
                "- [ ] todo_items 테이블: hospital_id, title, description, category, priority, estimated_impact, status(pending/done/skipped), created_at, completed_at, measured_impact\n"
                "- [ ] TODO 생성 로직 (스캔 후 자동):\n"
                "  - fail 항목 → urgent TODO (코드 스니펫 포함)\n"
                "  - warn 항목 → important TODO\n"
                "  - 경쟁사 대비 부족 항목 → recommended TODO\n"
                "  - 주당 최대 5개 (우선순위 정렬)\n"
                "- [ ] 효과 측정: TODO 완료 후 다음 스캔에서 해당 항목 점수 변화 기록\n"
                "  - '지난주 Schema 추가 → structured_data 0->80 (+80점)'\n\n"
                "### 프론트엔드\n"
                "- [ ] /dashboard/todo\n"
                "- [ ] 이번 주 TODO 카드 목록:\n"
                "  - [긴급] Schema.org 추가 (예상 +8점) [코드 보기]\n"
                "  - [중요] GBP 카테고리 재설정 (예상 +5점)\n"
                "  - [완료] 지난주: 메타 수정 → 실제 +4점\n"
                "- [ ] 완료 체크 + 스킵 사유\n"
                "- [ ] 히스토리: 지금까지 완료한 TODO + 누적 효과\n\n"
                "## 관련 파일\n"
                "- 신규: apps/worker/app/services/todo_engine.py\n"
                "- 신규: apps/web/src/app/dashboard/todo/page.tsx"
            ),
        ),
        Issue(
            title="[Dash-7] 의료광고 법규 알림 — 실시간 모니터링",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "의료법 §56 위반 시 1년 징역/1천만원 벌금. 보험 역할.\n"
                "스캔마다 법규 체크 → 위반 발견 시 즉시 알림.\n\n"
                "## 요구사항\n"
                "- [ ] /dashboard/compliance\n"
                "- [ ] 현재 상태 서머리: 위반 0건(초록) / N건(빨강)\n"
                "- [ ] 위반 목록:\n"
                "  - 위반 텍스트 하이라이트\n"
                "  - 해당 법 조항\n"
                "  - 수정 문구 제안 (AI 생성)\n"
                "  - 발견 URL + 스크린샷(선택)\n"
                "- [ ] 히스토리: 이전 스캔에서 발견 → 수정 → 해결 추적\n"
                "- [ ] 이메일 알림: Critical 위반 발견 시 즉시 발송\n"
                "- [ ] 등록번호/비급여 가격표 체크리스트\n\n"
                "## 데이터 소스\n"
                "- audit.details.medical_compliance (이미 수집됨)\n"
                "- audit.details.legal_footer (이미 수집됨)\n"
                "- audit.details.pipa_compliance (이미 수집됨)\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/app/dashboard/compliance/page.tsx\n"
                "- 재사용: medical-compliance.tsx 확장"
            ),
        ),
        Issue(
            title="[Dash-8] 리뷰 통합 피드 — Google API + Naver 스크래핑",
            priority="high",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "원장이 매일 5개 앱을 열어서 리뷰 확인하는 것을 한 화면으로 통합.\n"
                "Pro: 통합 피드 + Google 답변. Max: + 감성 분석 + 경쟁사 비교.\n\n"
                "## 요구사항\n"
                "### 백엔드 — 리뷰 수집\n"
                "- [ ] Google Business Profile API 연동:\n"
                "  - OAuth2로 병원 GBP 접근 권한 부여 (onboarding 시)\n"
                "  - accounts.locations.reviews.list → 리뷰 원문, 평점, 날짜, 작성자\n"
                "  - accounts.locations.reviews.updateReply → 답변 작성/수정\n"
                "  - 주기: 6시간마다 폴링\n"
                "- [ ] Naver Place 리뷰 스크래핑:\n"
                "  - naver_place.py 확장 — 리뷰 텍스트, 키워드 태그, 날짜 수집\n"
                "  - 주기: 12시간마다\n"
                "- [ ] reviews 테이블: hospital_id, platform(google/naver/gangnam_unni/babitalk), author, rating, text, date, reply_text, reply_date, sentiment\n"
                "- [ ] 강남언니/바비톡: 링크만 제공 (스크래핑 법적 리스크 회피)\n\n"
                "### 프론트엔드 — 리뷰 피드\n"
                "- [ ] /dashboard/reviews\n"
                "- [ ] 통합 피드 (시간순):\n"
                "  - 플랫폼 아이콘 + 별점 + 텍스트 + 날짜\n"
                "  - [답변하기] 버튼 (Google만 직접 답변 가능)\n"
                "  - [AI 답변 생성] → 한/영/일 답변 초안 생성\n"
                "- [ ] 필터: 플랫폼별, 별점별, 미답변만\n"
                "- [ ] 요약 카드: 전체 평점, 리뷰 수, 이번 주 신규, 미답변 수\n"
                "- [ ] [Max] 감성 분석: 긍정/부정 비율 추이, 부정 키워드 Top 5\n"
                "- [ ] [Max] 경쟁사 리뷰 비교: '경쟁사 평균 평점 4.3, 우리 4.1'\n\n"
                "## GBP OAuth 온보딩\n"
                "- [ ] 설정 페이지에서 'Google 리뷰 연결' 버튼\n"
                "- [ ] OAuth2 consent 화면 → 토큰 저장\n"
                "- [ ] 연결 해제 기능\n\n"
                "## 관련 파일\n"
                "- 신규: apps/worker/app/services/review_collector.py\n"
                "- 확장: apps/worker/app/services/naver_place.py\n"
                "- 신규: apps/web/src/app/dashboard/reviews/page.tsx"
            ),
        ),
        Issue(
            title="[Dash-9] 플랜 게이트 — Pro/Max/Enterprise 기능 분기",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "대시보드 기능을 플랜별로 분기. 상위 플랜 기능은 잠금 + 업그레이드 CTA.\n\n"
                "## 요구사항\n"
                "- [ ] usePlan() 훅: customer_profiles에서 plan_tier 조회\n"
                "- [ ] PlanGate 컴포넌트: 최소 플랜 미만이면 블러 + 자물쇠 + '업그레이드' 버튼\n"
                "- [ ] 플랜별 기능 매핑:\n"
                "  - Pro (39만): 스코어카드, 경쟁사 3곳, AI 모니터링 10키워드, TODO 월 5개, 법규 알림, 리뷰 피드+Google 답변, 월 2회 스캔\n"
                "  - Max (89만): + 경쟁사 10곳, AI 50키워드, TODO 주간+효과측정, 콘텐츠 생성 월 10건, 가격 벤치마킹, 리뷰 감성분석, 일 1회 스캔\n"
                "  - Enterprise (189만+): + 무제한 경쟁사/키워드/스캔, 멀티지점, 어트리뷰션, API, 전담 매니저\n"
                "- [ ] 설정 > 플랜 관리: 현재 플랜, 결제 정보, 업그레이드/다운그레이드\n"
                "- [ ] 업그레이드 모달: 각 플랜 기능 비교 테이블 + Toss 결제 연동\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/hooks/use-plan.ts\n"
                "- 신규: apps/web/src/components/dashboard/plan-gate.tsx\n"
                "- 기존: apps/web/src/app/api/payments/ (Toss 결제)"
            ),
        ),
    ],
)

# ============================================================
# Phase 2: 고도화
# ============================================================

PHASE_2 = Issue(
    title="[Dashboard] Phase 2: 고도화 (출시 후 8-12주)",
    priority="medium",
    assignee="CYH Planner",
    description=(
        "## Phase 1 MVP 출시 후 추가 기능\n\n"
        "1. 시술 가격 벤치마킹 [Max]\n"
        "2. 외국어 콘텐츠 생성 어시스턴트 [Max]\n"
        "3. GBP 최적화 가이드\n"
        "4. 키워드 인텔리전스 [Max]\n"
        "5. 원장 주간 요약 알림 (카톡/이메일)"
    ),
    children=[
        Issue(
            title="[Dash-P2-1] 시술 가격 벤치마킹 [Max]",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "동일 지역 동일 시술 가격 분포 시각화. Max 티어부터.\n"
                "'강남 보톡스 중앙값 7만원, 당신 8만원 — 상위 43%'\n\n"
                "## 요구사항\n"
                "- [ ] 가격 데이터 수집 파이프라인:\n"
                "  - 크롤링 시 가격 추출 (price_transparency_analyzer 확장)\n"
                "  - HIRA 비급여 공시 데이터 연동 (공공데이터 API)\n"
                "  - 시술×병원×가격×날짜 저장\n"
                "- [ ] 분포 계산: min/max/median/percentile\n"
                "- [ ] /dashboard/pricing\n"
                "  - 시술별 가격 분포 차트 (박스플롯 또는 히스토그램)\n"
                "  - 내 병원 위치 표시\n"
                "  - 경쟁사 이벤트 가격 모니터링\n"
                "  - 가격 포지셔닝 맵 (X: 가격, Y: 리뷰평점)"
            ),
        ),
        Issue(
            title="[Dash-P2-2] 외국어 콘텐츠 생성 어시스턴트 [Max]",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "한국어 시술 설명 → 영/일/중 SEO/AEO 최적화 콘텐츠 자동 생성.\n"
                "번역 대행 건당 15-30만원 대체. Max: 월 10건.\n\n"
                "## 요구사항\n"
                "- [ ] /dashboard/content\n"
                "- [ ] 콘텐츠 유형: FAQ, 시술 설명, 블로그, Schema.org 코드\n"
                "- [ ] 워크플로: 시술 선택 → 언어 선택 → AI 생성 → 편집 → 복사\n"
                "- [ ] AEO 최적화: 통계 포함, Q&A 구조, 출처 인용 (GEO 논문 기반)\n"
                "- [ ] 이미 있는 content_engine.py, aeo_content.py 재사용"
            ),
        ),
        Issue(
            title="[Dash-P2-3] GBP 최적화 가이드",
            priority="medium",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "외국인 환자 Google Maps 검색 → GBP 최적화 핵심.\n\n"
                "## 요구사항\n"
                "- [ ] GBP 체크리스트 카드:\n"
                "  - 카테고리 설정 (Dermatologist vs Skin Care Clinic)\n"
                "  - 사진 품질/수량 점수\n"
                "  - Q&A 응답률\n"
                "  - 리뷰 응답률/속도\n"
                "  - Languages spoken 속성\n"
                "  - 영업시간 정확성\n"
                "- [ ] '이 3장 사진을 교체하면 노출 개선' 같은 구체적 가이드"
            ),
        ),
        Issue(
            title="[Dash-P2-4] 키워드 인텔리전스 [Max]",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "외국인 환자가 검색하는 시술 키워드 트렌드.\n"
                "'일본인이 韓国 毛穴治療를 4만번 검색, 이 키워드로 랜딩 만든 강남 피부과 3곳뿐'\n\n"
                "## 요구사항\n"
                "- [ ] /dashboard/keywords\n"
                "- [ ] 트렌딩 키워드 목록 (영/일/중별)\n"
                "- [ ] 기회 키워드: 검색량 높은데 경쟁 낮은 것\n"
                "- [ ] 경쟁사 타겟 키워드 자동 추출\n"
                "- [ ] 이미 있는 keyword_engine.py, serp_checker.py 활용"
            ),
        ),
        Issue(
            title="[Dash-P2-5] 원장 주간 요약 알림 (이메일/카톡)",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "원장이 대시보드에 매일 로그인하지 않아도 핵심 변동을 파악.\n"
                "'원장이 직접 안 보고 직원에게 시키는' 문제 해결.\n\n"
                "## 요구사항\n"
                "- [ ] 주간 요약 이메일 (Resend):\n"
                "  - 이번 주 점수 변동\n"
                "  - 완료/미완료 TODO\n"
                "  - 신규 리뷰 요약\n"
                "  - 경쟁사 주요 변동\n"
                "  - AI 검색 노출 변화\n"
                "- [ ] 카카오톡 알림 (선택): KakaoTalk Channel 연동\n"
                "- [ ] cron: 매주 월요일 오전 9시 발송"
            ),
        ),
    ],
)


def main():
    print("=" * 60)
    print(" CYH Dashboard SaaS Issues Registration")
    print("=" * 60)

    register_phase("Phase 1: MVP 대시보드", PHASE_1)
    register_phase("Phase 2: 고도화", PHASE_2)

    print(f"\n{'=' * 60}")
    print(" Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
