#!/usr/bin/env python3
"""CYH Report UI 개편 이슈 등록 — 4 Phase, 11개 이슈."""

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


# ============================================================

PHASE_A = Issue(
    title="[Report] Phase A: 6-Category 기반 정렬",
    priority="urgent",
    assignee="CYH Planner",
    description=(
        "## 배경\n"
        "scorer.py는 6카테고리로 리팩토링됐지만 report-config.ts는 5카테고리.\n"
        "레이더 차트, Category Accordion, 스코어 표시가 백엔드와 불일치.\n"
        "이 Phase가 B/C/D 전체의 전제조건.\n\n"
        "## 포함 항목\n"
        "1. report-config.ts 5->6 카테고리 동기화\n"
        "2. 레이더 차트 6축 업데이트\n"
        "3. Category Accordion에 새 항목 매핑"
    ),
    children=[
        Issue(
            title="[A1] report-config.ts 5->6 카테고리 동기화 + 신규 항목 매핑",
            priority="urgent",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "scorer.py는 6카테고리(Technical SEO/Content/International/Authority/AI-AEO/Medical Compliance)이지만\n"
                "report-config.ts는 5카테고리(검색기본/속도성능/보안신뢰/국제화/AI검색).\n\n"
                "## 요구사항\n"
                "- [ ] report-config.ts REPORT_CATEGORIES를 6카테고리로 재편:\n"
                "  - Technical SEO: robots_txt, ai_crawler_audit, llms_txt, sitemap, meta_tags, headings, https, canonical, url_structure, errors_404, lcp, inp, cls, performance_score, mobile\n"
                "  - Content & On-Page: images_alt, links, content_clarity, eeat_signals, faq_content, geo_content_score\n"
                "  - International: multilingual_pages, hreflang, overseas_channels, international_search, language_matrix, cdn_latency\n"
                "  - Authority / Off-Page: structured_data, ai_search_mention, naver_place, beauty_platform, eeat_sameas\n"
                "  - AI & AEO: ai_robots_rules, ai_meta_tags, geo_content_score\n"
                "  - Medical Compliance: kr_compliance, jp_compliance, side_effect_disclosure, registration_numbers, price_disclosure, pipa_compliance\n"
                "- [ ] 카테고리별 아이콘, 색상, 한글 이름 업데이트\n"
                "- [ ] CategorySummary, CategoryAccordion 컴포넌트가 새 매핑 반영\n"
                "- [ ] report-detail-types.ts에 새 항목 타입 추가\n\n"
                "## 관련 파일\n"
                "- apps/web/src/lib/report-config.ts\n"
                "- apps/web/src/lib/report-detail-types.ts\n"
                "- apps/web/src/components/report/category-summary.tsx\n"
                "- apps/web/src/components/report/category-accordion.tsx\n\n"
                "## 완료 조건\n"
                "- 6카테고리가 리포트에 정상 렌더링\n"
                "- 기존 24개 체크 항목 표시 유지\n"
                "- 신규 항목 카드가 Accordion에 표시 (데이터 없으면 'N/A' fallback)"
            ),
        ),
        Issue(
            title="[A2] 레이더 차트 5축->6축 업데이트",
            priority="urgent",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "현재 RadarChart는 5축(검색기본/속도/보안/국제화/AI검색).\n"
                "6카테고리 서브스코어를 반영한 6축 레이더로 변경.\n\n"
                "## 요구사항\n"
                "- [ ] Recharts RadarChart 6축으로 변경\n"
                "- [ ] scorer.py의 category_scores JSON을 직접 사용\n"
                "- [ ] Medical Compliance 축에 Gating 적용 시 빨간색 강조\n"
                "- [ ] 축 이름: Technical / Content / International / Authority / AI-AEO / Compliance\n"
                "- [ ] 모바일에서 가독성 유지 (텍스트 크기 조정)\n\n"
                "## 관련 파일\n"
                "- apps/web/src/components/report/radar-chart.tsx\n\n"
                "## 완료 조건\n"
                "- 6축 레이더가 정상 렌더링\n"
                "- Gating 적용 시 시각적 구분"
            ),
        ),
    ],
)

PHASE_B = Issue(
    title="[Report] Phase B: 고가치 차별화 섹션",
    priority="high",
    assignee="CYH Planner",
    description=(
        "## 배경\n"
        "CYH의 최대 차별점인 Medical Compliance와 AI 크롤러 감사를 리포트에 반영.\n"
        "병원장에게 가장 임팩트 큰 섹션들.\n\n"
        "## 포함 항목\n"
        "1. Medical Compliance 상세 섹션 확장\n"
        "2. Compliance Alert 배너 (무료 영역)\n"
        "3. AI 크롤러 14봇 매트릭스"
    ),
    children=[
        Issue(
            title="[B1] Medical Compliance 상세 섹션 확장",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "현재 MedicalCompliance.tsx는 기본 표시만. 이것이 CYH 최대 차별점.\n"
                "의료법 위반은 1년 징역/1천만원 벌금 리스크 -> 병원장에게 가장 임팩트 큼.\n\n"
                "## 요구사항\n"
                "- [ ] 상단 서머리: 위반 X건(빨강) / 주의 Y건(노랑) / 정상 Z건(초록) 뱃지\n"
                "- [ ] 언어별 탭 UI (KR | EN | JP | ZH): 각 언어 페이지에서 발견된 위반\n"
                "- [ ] 위반 항목 카드:\n"
                "  - 위반 텍스트 하이라이트 (발견된 원문)\n"
                "  - 해당 법 조항 (의료법 제56조 등)\n"
                "  - 권장 수정안 (대체 표현 제안)\n"
                "- [ ] 등록번호 체크리스트 카드:\n"
                "  - 사업자등록번호: 감지됨/미감지\n"
                "  - 외국인환자유치 등록번호: 감지됨/미감지\n"
                "  - 비급여 가격표: 존재/미존재 + HIRA 형식 여부\n"
                "- [ ] PIPA 체크리스트: 개인정보처리방침/쿠키동의/CPO 공시\n"
                "- [ ] Gating 발동 시 섹션 상단 빨간 경고 박스\n\n"
                "## 데이터 소스\n"
                "- audit.details.medical_compliance (이미 수집됨)\n"
                "- audit.details.legal_footer (등록번호/가격표)\n"
                "- audit.details.pipa_compliance\n\n"
                "## 관련 파일\n"
                "- apps/web/src/components/report/medical-compliance.tsx (확장)\n"
                "- apps/web/src/app/report/[id]/page.tsx\n\n"
                "## 완료 조건\n"
                "- 실제 병원 사이트 스캔 데이터로 렌더링 확인\n"
                "- 위반 0건일 때 정상 표시, 위반 있을 때 상세 표시"
            ),
        ),
        Issue(
            title="[B2] Compliance Alert 배너 (무료 영역 최상단)",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "Gating Rule 발동 시 무료 영역에서도 '의료법 위반 감지' 경고를 보여줘야 함.\n"
                "이것이 이메일 전환의 핵심 트리거 — '상세 내역을 확인하려면 이메일 입력'.\n\n"
                "## 요구사항\n"
                "- [ ] ScoreHero 바로 아래에 조건부 배너:\n"
                "  - Gating 발동 시: 빨간 배너 '의료법 위반 N건 감지 - 점수가 49점으로 제한되었습니다'\n"
                "  - Critical 없지만 Warning 있을 시: 노란 배너 '의료 광고 주의사항 N건'\n"
                "  - 문제 없을 시: 배너 미표시\n"
                "- [ ] '상세 확인' 버튼 -> 이메일 게이트 또는 Medical Compliance 섹션으로 스크롤\n\n"
                "## 관련 파일\n"
                "- apps/web/src/app/report/[id]/page.tsx\n"
                "- 신규: apps/web/src/components/report/compliance-alert.tsx\n\n"
                "## 완료 조건\n"
                "- Gating 발동 케이스에서 배너 표시\n"
                "- 정상 케이스에서 배너 미표시"
            ),
        ),
        Issue(
            title="[B3] AI 크롤러 14봇 매트릭스 (Technical SEO 내)",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "robots.txt에서 14개 AI 봇 허용/차단 상태를 매트릭스로 시각화.\n"
                "'GPTBot 차단 -> ChatGPT 검색에서 제외' 같은 메시지가 병원장에게 직관적.\n\n"
                "## 요구사항\n"
                "- [ ] Category Accordion의 Technical SEO 내부에 봇 매트릭스 서브 컴포넌트\n"
                "- [ ] 14봇 테이블: 봇이름 | 상태(Allow/Disallow/미언급) | 영향\n"
                "- [ ] 상태별 색상: Allow=초록, Disallow=빨강, 미언급=회색\n"
                "- [ ] 필수 봇(Googlebot, bingbot) 차단 시 Critical 뱃지\n"
                "- [ ] AI 검색 봇 차단 시 '이 병원은 ChatGPT/Perplexity 검색에서 제외됩니다' 경고\n"
                "- [ ] llms.txt 상태도 같은 영역에 카드로 표시\n\n"
                "## 데이터 소스\n"
                "- audit.details.ai_crawler_audit (봇별 상태)\n"
                "- audit.details.llms_txt (존재/포맷)\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/components/report/ai-crawler-matrix.tsx\n"
                "- apps/web/src/components/report/category-accordion.tsx (통합)\n\n"
                "## 완료 조건\n"
                "- 14봇 매트릭스 렌더링\n"
                "- 데이터 없을 때 graceful fallback"
            ),
        ),
    ],
)

PHASE_C = Issue(
    title="[Report] Phase C: 데이터 시각화 (수집 완료 데이터 활용)",
    priority="high",
    assignee="CYH Planner",
    description=(
        "## 배경\n"
        "이미 수집되지만 리포트에 미표시인 데이터를 시각화.\n"
        "병원장이 바로 action 가능한 형태로 전달.\n\n"
        "## 포함 항목\n"
        "1. Naver Place vs GBP + 뷰티 플랫폼 카드\n"
        "2. CDN 레이턴시 지도\n"
        "3. GEO 콘텐츠 스코어 breakdown"
    ),
    children=[
        Issue(
            title="[C1] Naver Place vs GBP 비교 + 뷰티 플랫폼 리스팅 카드",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "'네이버 플레이스 리뷰 23개인데 경쟁사는 150개', '강남언니 미등록'\n"
                "-> 병원장에게 가장 actionable한 정보.\n\n"
                "## 요구사항\n"
                "- [ ] Authority 섹션 내 2칸 카드 레이아웃:\n"
                "  - 좌측: Naver Place vs GBP 비교\n"
                "    - 리뷰수 비교 바 차트\n"
                "    - 평균 평점 비교\n"
                "    - 최근 리뷰일\n"
                "    - 예약 연동 여부\n"
                "    - 미등록 시 경고 + 등록 가이드 링크\n"
                "  - 우측: 플랫폼 체크리스트\n"
                "    - 강남언니/UNNI: 등록/미등록\n"
                "    - 바비톡: 등록/미등록\n"
                "    - Xiaohongshu/RED: 등록/미등록\n"
                "    - 여신티켓: 등록/미등록\n"
                "    - 미등록 시 타겟 시장 대비 퍼널 손실 메시지\n\n"
                "## 데이터 소스\n"
                "- audit.details.naver_place\n"
                "- audit.details.beauty_platform\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/components/report/authority-platforms.tsx\n\n"
                "## 완료 조건\n"
                "- Naver Place 데이터 있을 때 비교 차트 렌더링\n"
                "- 데이터 없을 때 'Naver Place 미등록' 카드"
            ),
        ),
        Issue(
            title="[C2] CDN 레이턴시 리전 지도",
            priority="medium",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "'일본 환자가 사이트를 열면 3초 걸립니다' -> 바로 이해 가능한 메시지.\n"
                "숫자 나열보다 지도 시각화가 효과적.\n\n"
                "## 요구사항\n"
                "- [ ] International 섹션 내 레이턴시 카드\n"
                "- [ ] 4개 프로브 결과 시각화:\n"
                "  - Tokyo (일본 환자) | Singapore (동남아) | Hong Kong (중국) | US West (미국)\n"
                "  - 각 지역: TTFB 수치 + 등급 뱃지 (Good/NI/Poor)\n"
                "  - 색상: Good=초록 (<800ms), NI=노랑 (<2s), Poor=빨강 (>=2s)\n"
                "- [ ] CDN 미사용 + 해외 타겟 시 경고 메시지\n"
                "- [ ] 간단한 아시아 중심 지도 또는 4칸 그리드 (지도 라이브러리 없이)\n\n"
                "## 데이터 소스\n"
                "- audit.details.cdn_latency\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/components/report/cdn-latency-card.tsx\n\n"
                "## 완료 조건\n"
                "- 4개 리전 레이턴시 표시\n"
                "- 데이터 없을 때 '측정 불가' fallback"
            ),
        ),
        Issue(
            title="[C3] GEO 콘텐츠 스코어 breakdown",
            priority="medium",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "Princeton GEO 논문 기반 5개 지표를 breakdown으로 보여줌.\n"
                "'통계 추가하면 AI 인용률 +41%' 같은 구체적 개선 액션 전달.\n\n"
                "## 요구사항\n"
                "- [ ] Content & On-Page 또는 AI-AEO 섹션 내 카드\n"
                "- [ ] 5개 지표 수평 바 차트:\n"
                "  - 통계 밀도 (목표: 150-200단어당 1개)\n"
                "  - 출처 인용 (목표: 페이지당 3+)\n"
                "  - Q&A 구조 (FAQ/Answer Capsule 유무)\n"
                "  - 전문가 인용 (자격증 동반 인명)\n"
                "  - 프로모션 톤 (낮을수록 좋음 - 역방향)\n"
                "- [ ] 각 지표 옆에 연구 근거 한 줄 ('통계 포함 시 AI 인용률 +41% - Princeton GEO')\n"
                "- [ ] 종합 GEO Score 0-100\n\n"
                "## 데이터 소스\n"
                "- audit.details.geo_content_score 또는 audit.scores.geo_content_score\n\n"
                "## 관련 파일\n"
                "- 신규: apps/web/src/components/report/geo-score-breakdown.tsx\n\n"
                "## 완료 조건\n"
                "- 5개 지표 바 차트 렌더링\n"
                "- 프로모션 톤 역방향 표시"
            ),
        ),
    ],
)

PHASE_D = Issue(
    title="[Report] Phase D: PDF 동기화 + 빈 상태 수정",
    priority="medium",
    assignee="CYH Planner",
    description=(
        "## 배경\n"
        "웹 리포트와 PDF 불일치 수정 + competitor_analysis 데이터 연결.\n\n"
        "## 포함 항목\n"
        "1. PDF 템플릿 6카테고리 동기화\n"
        "2. competitor_analysis 백엔드 호출 연결"
    ),
    children=[
        Issue(
            title="[D1] PDF 리포트 템플릿 6카테고리 동기화",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "PDF는 이메일로 발송되는 영업 자료. 웹 리포트와 불일치하면 신뢰도 하락.\n\n"
                "## 요구사항\n"
                "- [ ] report.html Jinja2 템플릿을 6카테고리 구조로 변경\n"
                "- [ ] Executive Summary에 6카테고리 서브스코어 바 차트\n"
                "- [ ] Medical Compliance 섹션 추가 (위반 서머리 + 등록번호 체크리스트)\n"
                "- [ ] Gating 발동 시 빨간 경고 박스\n"
                "- [ ] 상세 데이터는 '웹 리포트에서 확인' 링크로 유도\n"
                "- [ ] AI 크롤러 요약 (허용/차단 수)\n\n"
                "## 관련 파일\n"
                "- apps/worker/app/templates/report.html\n"
                "- apps/worker/app/services/pdf_generator.py\n\n"
                "## 완료 조건\n"
                "- PDF가 6카테고리 구조로 렌더링\n"
                "- Gating 케이스 PDF 확인"
            ),
        ),
        Issue(
            title="[D2] competitor_discovery 호출 연결 + keyword_rankings UI",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "scanner.py에서 discover_competitors()가 호출되지 않아\n"
                "CompetitionAnalysis, CompetitiveGap 컴포넌트가 빈 상태.\n"
                "keyword_rankings도 수집되지만 UI 없음.\n\n"
                "## 요구사항\n"
                "- [ ] scanner.py에 discover_competitors() 호출 추가\n"
                "  - 결과를 scan_result['competitor_analysis']에 저장\n"
                "  - competitive_gap 데이터도 생성\n"
                "- [ ] keyword_rankings 데이터를 표시할 간단한 테이블 컴포넌트\n"
                "  - 키워드 | Naver 순위 | Google 순위 | 경쟁사 출현 여부\n"
                "- [ ] 기존 CompetitionAnalysis.tsx, CompetitiveGap.tsx가 데이터 수신 확인\n\n"
                "## 관련 파일\n"
                "- apps/worker/app/services/scanner.py\n"
                "- apps/worker/app/services/competitor_discovery.py\n"
                "- apps/web/src/components/report/ (경쟁사 관련 컴포넌트)\n\n"
                "## 완료 조건\n"
                "- 스캔 후 competitor_analysis 데이터가 details에 포함\n"
                "- 경쟁사 비교/갭 섹션이 실데이터로 렌더링"
            ),
        ),
    ],
)


def register_all():
    print("=" * 60)
    print(" CYH Report UI Issues Registration")
    print("=" * 60)

    total = 0
    success = 0

    for phase_name, epic in [
        ("Phase A: 6-Category 기반 정렬", PHASE_A),
        ("Phase B: 고가치 차별화 섹션", PHASE_B),
        ("Phase C: 데이터 시각화", PHASE_C),
        ("Phase D: PDF + 빈 상태 수정", PHASE_D),
    ]:
        print(f"\n--- {phase_name} ---")
        total += 1
        epic_id = create_issue(
            epic.title, epic.priority, epic.assignee, epic.description
        )
        if epic_id:
            success += 1
        if epic.children and epic_id:
            for child in epic.children:
                total += 1
                child_id = create_issue(
                    child.title,
                    child.priority,
                    child.assignee,
                    child.description,
                    parent_id=epic_id,
                )
                if child_id:
                    success += 1

    print(f"\n{'=' * 60}")
    print(f" Done: {success}/{total} issues created")
    print("=" * 60)


if __name__ == "__main__":
    register_all()
