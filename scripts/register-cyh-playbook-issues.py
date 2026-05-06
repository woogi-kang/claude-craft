#!/usr/bin/env python3
"""CYH SEO/AEO Playbook 기반 이슈 일괄 등록 (2026-04-22)."""

import json
import subprocess
from dataclasses import dataclass

PROJECT_ID = "18031aa2-6cc7-4a99-ae6b-147494f07d0c"


@dataclass
class Issue:
    title: str
    priority: str  # urgent, high, medium, low
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
    """Create a single issue via multica CLI. Returns issue ID or None."""
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
        print(f"    stderr: {result.stderr[:200]}")
        return None

    try:
        data = json.loads(result.stdout)
        identifier = data.get("identifier", "???")
        issue_id = data.get("id", "")
        print(f"  ✓ {identifier:8s} | {priority:6s} | {assignee:20s} | {title}")
        return issue_id
    except json.JSONDecodeError:
        print(f"  ✗ JSON parse error: {title}")
        print(f"    stdout: {result.stdout[:200]}")
        return None


# ============================================================
# Issue Definitions
# ============================================================

PHASE_1 = Issue(
    title="[Playbook] Phase 1: 즉시 도입 가능 항목 (7개)",
    priority="urgent",
    assignee="CYH Planner",
    description=(
        "## 배경\n"
        "Korean Dermatology SEO/AEO Audit Playbook 분석 결과 도출된 **즉시 도입 가능** 항목.\n"
        "기존 코드에 최소 수정으로 가장 큰 차별화를 달성할 수 있는 7개 항목.\n\n"
        "## 포함 항목\n"
        "1. AI 크롤러 robots.txt 14봇 개별 감사\n"
        "2. llms.txt 존재/포맷 검증\n"
        "3. 의료법 §56 다국어 금지패턴 확장 (EN/ZH 추가)\n"
        "4. 비급여 가격표 감지 (2025.4.1 의원급 확대)\n"
        "5. 사업자등록번호 / 외국인환자유치 등록번호 footer 감지\n"
        "6. hreflang 10가지 오류 패턴 심화 검증\n"
        "7. MedicalClinic/Physician Schema.org 전용 검증\n\n"
        "## 완료 조건\n"
        "- 7개 하위 이슈 모두 구현 + 테스트 통과\n"
        "- 기존 24개 체크 항목 회귀 없음\n\n"
        "## 참고\n"
        "- 소스: SEO/AEO Audit Playbook (Compass Research)\n"
        "- Playbook 섹션: §1 hreflang, §3 AEO, §4 Medical Content, §5 Checklist"
    ),
    children=[
        Issue(
            title="[P0-1] AI 크롤러 robots.txt 14봇 개별 감사 체크",
            priority="urgent",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "AI 검색 트래픽 급증 (Adobe: AI referrals +527%, ChatGPT referrals +52% YoY).\n"
                "OpenAI: OAI-SearchBot 차단 시 ChatGPT Search 답변에서 제외.\n"
                "현재 robots.txt 체크는 존재 여부만 확인, AI 봇별 개별 감사 없음.\n\n"
                "## 요구사항\n"
                "- [ ] `apps/worker/app/checks/robots.py` 확장 또는 신규 `ai_crawler_audit.py`\n"
                "- [ ] 14개 우선순위 봇 개별 확인:\n"
                "  - 필수 허용: Googlebot, bingbot (차단=Critical)\n"
                "  - AI 검색: GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-User, Claude-SearchBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended\n"
                "  - 추가: CCBot, Meta-ExternalAgent, Bytespider, DuckAssistBot\n"
                "- [ ] 봇별 Allow/Disallow/미언급 상태 매트릭스 리턴\n"
                "- [ ] deprecated 봇(Claude-Web, anthropic-ai) 경고\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/checks/robots.py`\n"
                "- `apps/worker/app/services/scanner.py`\n"
                "- `apps/worker/app/services/scorer.py`\n\n"
                "## 완료 조건\n"
                "- pytest 통과, 기존 robots_txt 회귀 없음\n"
                "- 14봇 감사 결과가 리포트에 표시"
            ),
        ),
        Issue(
            title="[P0-2] llms.txt 존재 및 포맷 검증 체크",
            priority="urgent",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "llms.txt (llmstxt.org, 2024.9) — AI 에이전트 전용 사이트 설명 파일.\n"
                "Anthropic, Cloudflare, Vercel, Stripe 채택. MS/OpenAI 크롤러가 fetch 확인됨.\n\n"
                "## 요구사항\n"
                "- [ ] `/llms.txt` 존재 (HTTP GET 200)\n"
                "- [ ] 포맷 검증: H1 이름, blockquote 요약, H2 링크 목록\n"
                "- [ ] `/llms-full.txt` 존재 (optional)\n"
                '- [ ] `<link rel="alternate" type="text/markdown">` head 태그\n'
                "- [ ] 심각도: Low\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/checks/geo_aeo.py` 또는 신규\n"
                "- product-spec에 check_llms_txt() 계획 있음\n\n"
                "## 완료 조건\n"
                "- pytest 통과\n"
                "- 미존재 시 생성 가이드 recommendation 제공"
            ),
        ),
        Issue(
            title="[P0-3] 의료법 §56 다국어 금지패턴 확장 (EN/ZH)",
            priority="urgent",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "현재 medical_compliance.py는 KR+JP만 구현.\n"
                "외국인환자 유치 사이트는 EN/ZH 페이지에도 동일 규제.\n"
                "§56②8 과장광고: 2023-24 집행의 31.7%, 최빈 위반.\n\n"
                "## 요구사항\n"
                "- [ ] 영어 금지패턴: best, #1, No.1, world-class, guaranteed, 100% safe, no side effects, perfect, miracle, only\n"
                "- [ ] 영어 치료보장: guaranteed cure, 100% effective, permanent results\n"
                "- [ ] 중국어(간체) 금지패턴: 最好, 第一, 最佳, 唯一, 顶级, 世界级, 完美, 奇迹\n"
                "- [ ] 중국어 치료보장: 保证治愈, 100%有效, 永久效果\n"
                "- [ ] 기존 KR 보완: 최초, 최대, 제일, TOP1 추가\n"
                "- [ ] 페이지 언어 감지 후 해당 언어 패턴만 적용\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/services/medical_compliance.py`\n\n"
                "## 완료 조건\n"
                "- 한/영/일/중 각각 테스트 케이스\n"
                "- 기존 KR/JP 스캔 회귀 없음"
            ),
        ),
        Issue(
            title="[P0-4] 비급여 가격표 + 사업자/유치등록번호 footer 감지",
            priority="high",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "비급여 가격 공시: 2025.4.1 의원급 확대 (MOHW 고시 2023-192).\n"
                "외국인환자유치 등록번호(제XXXX-XXXXX호) 외국어 페이지 필수.\n"
                "사업자등록번호(XXX-XX-XXXXX) footer 필수.\n\n"
                "## 요구사항\n"
                "- [ ] 비급여 가격표 감지 (키워드: 비급여, 가격표, 진료비, 수가)\n"
                "- [ ] HIRA 형식 테이블 (4컬럼: 분류/비용/특이사항/변경일)\n"
                "- [ ] 사업자등록번호 regex: \\d{3}-\\d{2}-\\d{5}\n"
                "- [ ] 외국인환자유치 등록번호 regex: 제?\\s*\\d{4}-\\d{5}\\s*호?\n"
                "- [ ] 심각도: 등록번호=Critical, 가격표=High\n\n"
                "## 완료 조건\n"
                "- 실제 병원 사이트 3곳 테스트\n"
                "- footer 영역 한정 스캔"
            ),
        ),
        Issue(
            title="[P0-5] hreflang 10가지 오류 패턴 심화 검증",
            priority="high",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "hreflang은 외국인환자 유치 사이트의 가장 중요하면서 가장 많이 깨지는 신호.\n"
                "현재 존재 여부만 체크. Playbook은 10가지 구체적 오류 패턴 정의.\n\n"
                "## 요구사항 — 10가지 오류 패턴:\n"
                "1. Missing return tag (A→B O, B→A X)\n"
                "2. Invalid BCP-47 code (en_US → en-US)\n"
                "3. hreflang → 4xx/5xx/redirect URL\n"
                "4. Underscore instead of hyphen\n"
                "5. Multiple URLs per language group\n"
                "6. Multiple x-default tags\n"
                "7. Sitemap hreflang != on-page hreflang\n"
                "8. Mixed methods (head + sitemap)\n"
                "9. hreflang → non-canonical URL\n"
                "10. Missing self-reference\n"
                "- [ ] 최소 언어셋: ko + en + ja + zh-Hans + x-default\n"
                "- [ ] HTML lang과 hreflang 일치 검증\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/checks/multilingual.py`\n\n"
                "## 완료 조건\n"
                "- 10가지 패턴 각각 테스트\n"
                "- 다국어 사이트 실제 테스트 1곳+"
            ),
        ),
        Issue(
            title="[P0-6] MedicalClinic/Physician Schema.org 전용 검증",
            priority="high",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "일반 structured_data 체크는 있지만 의료 특화 스키마 검증 없음.\n"
                "AI 엔진은 MedicalWebPage, MedicalClinic, Physician 우선 추출.\n"
                "§56②7 부작용 공시 = seriousAdverseOutcome 필드.\n\n"
                "## 요구사항\n"
                "- [ ] MedicalClinic: @type, availableService, openingHours, geo, sameAs (>=6)\n"
                "- [ ] Physician: medicalSpecialty, hasCredential, memberOf, knowsLanguage, identifier(면허번호)\n"
                "- [ ] MedicalProcedure: procedureType, bodyLocation, seriousAdverseOutcome, performedBy\n"
                "- [ ] MedicalWebPage: lastReviewed <=24개월, reviewedBy, audience, specialty\n"
                "- [ ] Entity 연결: worksFor, performedBy @id 참조\n"
                "- [ ] 심각도: MedicalClinic 미사용=High, 세부 필드 누락=Medium\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/checks/structured_data.py`\n\n"
                "## 완료 조건\n"
                "- 필드 완성도 점수 리턴\n"
                "- JSON-LD 코드 스니펫 recommendation 포함"
            ),
        ),
    ],
)

PHASE_2 = Issue(
    title="[Playbook] Phase 2: 중기 차별화 항목 (7개)",
    priority="high",
    assignee="CYH Planner",
    description=(
        "## 배경\n"
        "Playbook 분석 결과 도출된 **차별화 핵심** 항목. 1-2 스프린트.\n"
        "경쟁사(Dragon Metrics, Profound, PatientPop)가 못 하는 영역.\n\n"
        "## 포함 항목\n"
        "1. Medical Compliance Gating Rule (Critical → 49점 캡)\n"
        "2. 6-Category 스코어카드 리팩토링\n"
        "3. 언어×페이지유형 매트릭스 시각화\n"
        "4. Naver Place 스크래핑 연동\n"
        "5. 메신저 채널 딥링크 검증\n"
        "6. CDN/레이턴시 멀티 리전 프로브\n"
        "7. Princeton GEO 논문 기반 콘텐츠 스코어링\n\n"
        "## 완료 조건\n"
        "- 7개 하위 이슈 모두 구현 + 테스트 통과\n"
        "- 리포트 UI 업데이트 반영"
    ),
    children=[
        Issue(
            title="[P1-1] Medical Compliance Gating Rule (Critical → 49점 캡)",
            priority="high",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "의료법 위반은 최적화 이슈가 아니라 법적 리스크.\n"
                "Medical Compliance Critical 1개 → 전체 49점(Poor) 캡.\n"
                "§56 위반: 1년 징역/1천만원. 유치 미등록: 3년/3천만원.\n\n"
                "## 요구사항\n"
                "- [ ] scorer.py gating rule: compliance Critical → total_score = min(score, 49)\n"
                "- [ ] 캡 적용 시 리포트 경고 배너\n"
                "- [ ] 캡 사유(어떤 Critical) 구체 표시\n"
                "- [ ] grade 조정: 49점 이하 → 최대 D\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/services/scorer.py`\n"
                "- `apps/web/src/app/report/[id]/`\n\n"
                "## 완료 조건\n"
                "- compliance critical 있음 → 49점 이하\n"
                "- compliance critical 없음 → 기존 로직"
            ),
        ),
        Issue(
            title="[P1-2] 6-Category 스코어카드 리팩토링",
            priority="high",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "현재 4카테고리 → 6카테고리:\n"
                "Technical SEO 25% / Content & On-Page 15% / International 20% / "
                "Authority 15% / AI-AEO 10% / Medical Compliance 15%\n\n"
                "## 요구사항\n"
                "- [ ] scorer.py WEIGHTS 재편\n"
                "- [ ] 카테고리별 서브스코어 계산\n"
                "- [ ] 기존 total_score API 하위호환\n"
                "- [ ] 리포트 executive summary 6개 수평 바\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/services/scorer.py`\n"
                "- `apps/web/src/app/report/[id]/`"
            ),
        ),
        Issue(
            title="[P1-3] 언어×페이지유형 매트릭스 시각화",
            priority="high",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "6×4 language-pair audit matrix — 경쟁사가 없는 유일한 시각화.\n"
                "일본어 FAQ가 자동번역 한국어, 중국어 예약에 reCAPTCHA(중국 차단) 등.\n\n"
                "## 요구사항\n"
                "- [ ] 매트릭스 UI: Y=EN/JA/ZH-Hans/ZH-Hant/TH/RU, X=Landing/FAQ/Price/Booking\n"
                "- [ ] 셀 상태: ✅정상 / ⚠️문제 / ❌미존재\n"
                "- [ ] 셀 클릭 → 상세 (URL, 감지 언어, 문제점)\n"
                "- [ ] 백엔드: multilingual_analyzer.py 매트릭스 데이터\n"
                "- [ ] 언어 감지: cld3/langdetect 실제 콘텐츠 확인\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/services/multilingual_analyzer.py`\n"
                "- `apps/web/src/app/report/[id]/`"
            ),
        ),
        Issue(
            title="[P1-4] Naver Place 리스팅 데이터 수집",
            priority="high",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "Naver Place = 한국판 GBP. 외국인 환자가 번역 리뷰 접하는 경로.\n"
                "순위 요인: 예약수, 리뷰수/최신성, 키워드 매칭, 영수증 인증.\n\n"
                "## 요구사항\n"
                "- [ ] 병원명 기반 Naver Place 검색\n"
                "- [ ] 수집: 리뷰수, 평균평점, 최근 리뷰일, 저장수, 예약 가능\n"
                "- [ ] GBP 대비 비교 (리뷰수/평점 격차)\n"
                "- [ ] Playwright 스크래핑, 7일 캐싱\n"
                "- [ ] 심각도: 미등록=High\n\n"
                "## 관련 파일\n"
                "- 신규: `apps/worker/app/services/naver_place.py`\n"
                "- 참고: `apps/worker/app/services/serp_checker.py`"
            ),
        ),
        Issue(
            title="[P1-5] 메신저 채널 딥링크 실존 검증",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "WeChat 없으면 중국 환자 전환 불가. 현재 존재 여부만 체크.\n\n"
                "## 요구사항\n"
                "- [ ] KakaoTalk: pf.kakao.com, open.kakao.com → HTTP HEAD 200\n"
                "- [ ] Line: line.me, lin.ee, page.line.me → HTTP HEAD\n"
                "- [ ] WhatsApp: wa.me → 번호 형식 검증\n"
                "- [ ] WeChat: weixin://, QR 이미지 존재 감지\n"
                "- [ ] 시장별 필수: 일본→Line, 중국→WeChat, 동남아→WhatsApp\n"
                "- [ ] 타겟 시장 대비 누락 경고\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/checks/multilingual.py`"
            ),
        ),
        Issue(
            title="[P1-6] CDN/레이턴시 멀티 리전 프로브",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "Seoul→Tokyo 30-40ms, →US West 130-150ms, →Singapore 75-90ms.\n"
                "Cafe24 호스팅 병원 사이트의 해외 레이턴시 심각. TTFB>3s → 이탈.\n\n"
                "## 요구사항\n"
                "- [ ] 멀티 리전 TTFB: Tokyo, Singapore, Hong Kong, US West\n"
                "- [ ] 외부 프로브 API 또는 Cloudflare Workers\n"
                "- [ ] 등급: Good<800ms, NI<2s, Poor>=2s\n"
                "- [ ] CDN 감지 (cf-ray, x-cdn, x-amz-cf-id)\n"
                "- [ ] 한국 호스팅(Cafe24, 가비아) ASN 감지 시 경고\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/checks/performance.py` 확장"
            ),
        ),
        Issue(
            title="[P1-7] Princeton GEO 논문 기반 콘텐츠 AEO 스코어링",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "Princeton GEO(arXiv:2311.09735, KDD 2024):\n"
                "통계 +41%, 인용 +30-40%, Q&A +25.45%, 프로모션 톤 -26.19%.\n\n"
                "## 요구사항\n"
                "- [ ] 통계 밀도: 숫자+단위 / 150-200단어당 1개\n"
                "- [ ] 출처 인용: PubMed/DOI/NIH 링크 수 (최소 3/페이지)\n"
                "- [ ] Q&A 구조: FAQ 섹션, H2+40-80단어 Answer Capsule\n"
                "- [ ] 전문가 인용: 자격증 동반 인명 패턴\n"
                "- [ ] 프로모션 톤 감지 (높으면 감점)\n"
                "- [ ] 페이지당 GEO Score 0-100\n\n"
                "## 관련 파일\n"
                "- `apps/worker/app/checks/geo_aeo.py` 확장"
            ),
        ),
    ],
)

PHASE_3 = Issue(
    title="[Playbook] Phase 3: 장기 전략적 확장 (8개)",
    priority="medium",
    assignee="CYH Planner",
    description=(
        "## 배경\n"
        "구현 복잡도 높거나 시장 검증 후 판단 필요. Phase 1-2 완료 후 진행.\n\n"
        "## 포함 항목\n"
        "1. Baidu 최적화 (ICP, meta, 간체자)\n"
        "2. Xiaohongshu/RED 브랜드 계정 확인\n"
        "3. Gangnam Unni / UNNI Global 리스팅 체크\n"
        "4. E-E-A-T 심화 (Wikidata Q-ID, sameAs)\n"
        "5. PIPA 개인정보보호법 컴플라이언스\n"
        "6. 경쟁사 자동 벤치마킹 레이더 차트\n"
        "7. 일본 시장 특화 (keigo, 税込, Line CTA)\n"
        "8. 가격 투명성 스코어"
    ),
    children=[
        Issue(
            title="[P2-1] Baidu 최적화 체크 (ICP, 간체자, meta keywords)",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "Baidu ICP 없이 순위 어려움. 단, 중국 환자는 Xiaohongshu 중심으로 이동 중.\n\n"
                "## 요구사항\n"
                "- [ ] ICP 번호 footer 감지 (京ICP备XXXXXXXX号)\n"
                "- [ ] ICP 미보유 시 대안 안내 (HK CDN, WeChat/RED 집중)\n"
                "- [ ] Baidu meta: title<=30자, description<=78자, meta keywords\n"
                "- [ ] 간체자 확인 (번체자 경고)\n"
                "- [ ] 금지어: 最/第一/最佳/最好/唯一/顶级"
            ),
        ),
        Issue(
            title="[P2-2] Xiaohongshu(RED) 브랜드 계정 존재 확인",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "Xiaohongshu가 의료미용 디스커버리에서 Baidu 추월.\n"
                "600M daily searches, 330M+ MAU, 70% 여성.\n\n"
                "## 요구사항\n"
                "- [ ] 사이트에서 xiaohongshu.com, xhslink.com 링크 감지\n"
                "- [ ] RED 미존재 + 중국어 페이지 → '중국 퍼널 불완전' 경고\n"
                "- [ ] 스크래핑 없음 (링크 존재만)"
            ),
        ),
        Issue(
            title="[P2-3] Gangnam Unni / UNNI Global 리스팅 존재 확인",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "UNNI: 7-8M 사용자, 130만 JP 가입, 1,800+ 클리닉, 13언어.\n"
                "미등록 시 일본 퍼널 대규모 손실.\n\n"
                "## 요구사항\n"
                "- [ ] gangnamunni.com, unni.com 링크 감지\n"
                "- [ ] 미등록 + 일본어 페이지 → 경고\n"
                "- [ ] Babitalk, Yeoshin Ticket 보조 감지\n"
                "- [ ] 심각도: High (JP 타겟 한정)"
            ),
        ),
        Issue(
            title="[P2-4] E-E-A-T 심화 (Wikidata Q-ID, sameAs 도메인)",
            priority="low",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "Entity 인식 기반 Wikidata Q-ID. sameAs >=6 권위 도메인.\n\n"
                "## 요구사항\n"
                "- [ ] sameAs 배열 도메인 수 카운트\n"
                "- [ ] 권장: Wikidata, LinkedIn, GBP, 피부과학회, KHIDI, Healthgrades\n"
                "- [ ] sameAs <3 → Medium 경고\n"
                "- [ ] 심각도: Low (교육적 안내)"
            ),
        ),
        Issue(
            title="[P2-5] PIPA 개인정보보호법 컴플라이언스 체크",
            priority="medium",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "개인정보보호법 2023.9.15 개정. 과태료 총매출 3%.\n\n"
                "## 요구사항\n"
                "- [ ] 개인정보 처리방침 링크 (다국어별)\n"
                "- [ ] 쿠키 동의 배너 존재\n"
                "- [ ] CPO 성명/연락처 표시\n"
                "- [ ] 연락폼 최소 수집 원칙\n"
                "- [ ] 국외 이전 동의 (외국인 환자 데이터)"
            ),
        ),
        Issue(
            title="[P2-6] 경쟁사 자동 벤치마킹 레이더 차트",
            priority="medium",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "SERP seed query로 상위 5개 클리닉 자동 선택 → 6카테고리 비교.\n\n"
                "## 요구사항\n"
                "- [ ] 경쟁사 3-5개 자동 선별 (SERP + 지역 필터)\n"
                "- [ ] 6카테고리 레이더 차트 (radar/spider)\n"
                "- [ ] 항목별 '이 병원 vs 경쟁사 평균' 바 차트\n"
                "- [ ] executive summary 삽입\n\n"
                "## 의존성\n"
                "- [P1-2] 6-Category 스코어카드 완료 필요"
            ),
        ),
        Issue(
            title="[P2-7] 일본 시장 특화 감사 (keigo, 税込, Line CTA)",
            priority="low",
            assignee="CYH Backend Dev",
            description=(
                "## 배경\n"
                "일본 = 외국인환자 #1. iPhone 65-70%, Line 95M MAU.\n\n"
                "## 요구사항\n"
                "- [ ] JP meta title <=28-32 전각, description <=49-80 전각\n"
                "- [ ] keigo 감지 (ます/です 비율)\n"
                "- [ ] 税込/税別 가격 표시\n"
                "- [ ] Line Official Account QR/링크 (JP 페이지)\n"
                "- [ ] 3종 문자 혼용 자연성\n"
                "- [ ] リスク・副作用・ダウンタイム 공시"
            ),
        ),
        Issue(
            title="[P2-8] 가격 투명성 스코어",
            priority="low",
            assignee="CYH Frontend Dev",
            description=(
                "## 배경\n"
                "가격 투명성 = 환자 신뢰 #2 (언어 다음).\n\n"
                "## 요구사항\n"
                "- [ ] 사이트 내 가격 정보 존재 감지\n"
                "- [ ] 시술별 가격 구조: unit vs 패키지 vs 이벤트\n"
                "- [ ] 가격 페이지 다국어 제공\n"
                "- [ ] 통화 현지화 (JPY, USD, CNY, THB)\n"
                "- [ ] 가격 투명성 점수 0-100"
            ),
        ),
    ],
)


def register_all():
    """Register all issues."""
    print("=" * 50)
    print(" CYH Playbook Issues Registration")
    print("=" * 50)
    print()

    total = 0
    success = 0

    for phase_name, epic in [
        ("Phase 1: 즉시 도입 (P0)", PHASE_1),
        ("Phase 2: 중기 차별화 (P1)", PHASE_2),
        ("Phase 3: 장기 확장 (P2)", PHASE_3),
    ]:
        print(f"--- {phase_name} ---")

        # Create epic
        total += 1
        epic_id = create_issue(
            epic.title, epic.priority, epic.assignee, epic.description
        )
        if epic_id:
            success += 1

        # Create children
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

        print()

    print("=" * 50)
    print(f" Done: {success}/{total} issues created")
    print("=" * 50)
    print()
    print(f"확인: multica issue list --project {PROJECT_ID}")


if __name__ == "__main__":
    register_all()
