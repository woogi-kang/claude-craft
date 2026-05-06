#!/usr/bin/env python3
"""CYH PR rebase + fix 이슈 등록."""

import json
import subprocess

PROJECT_ID = "18031aa2-6cc7-4a99-ae6b-147494f07d0c"


def create_issue(
    title: str, priority: str, assignee: str, description: str
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
        "todo",
        "--output",
        "json",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ FAILED: {title}")
        return None
    data = json.loads(result.stdout)
    print(f"  ✓ {data['identifier']:8s} | {priority:6s} | {title}")
    return data.get("id")


print("=" * 60)
print(" CYH PR Rebase + Fix Issues")
print("=" * 60)

# --- Group 1: Rebase only ---
print("\n--- Rebase (충돌 해결) ---")

rebase_prs = [
    (2, "feature/procedure-extractor", "병원 홈페이지 주력 시술 자동 추출"),
    (8, "feat/llms-txt-check", "llms.txt check (worker)"),
    (
        3,
        "feat/aeo-llms-txt-ai-robots-meta-checks",
        "llms.txt + AI robots + meta tags — #8 머지 후 rebase",
    ),
    (11, "feat/compliance-gating-rule", "Medical Compliance Gating Rule"),
    (
        12,
        "feat/woo-88-6category-scorecard",
        "6-Category Scorecard — #11 머지 후 rebase",
    ),
    (15, "feat/woo-91-messenger-deeplink-verification", "메신저 채널 딥링크 검증"),
    (20, "feat/pipa-compliance-check", "PIPA 개인정보보호법"),
    (22, "feat/japan-market-checks", "Japan market checks"),
    (23, "feat/eeat-sameas-check", "E-E-A-T sameAs / Wikidata"),
    (25, "feat/woo-95-baidu-optimization", "Baidu 최적화"),
    (26, "feat/woo-83-legal-footer-checks", "비급여 가격표 + 등록번호"),
]

for pr_num, branch, desc in rebase_prs:
    create_issue(
        f"[Rebase] PR #{pr_num} {desc}",
        "urgent",
        "CYH Backend Dev",
        (
            f"## 작업\n"
            f"PR #{pr_num} (`{branch}`)이 main과 충돌 발생.\n"
            f"rebase하여 충돌을 해결하고 force-push 해주세요.\n\n"
            f"## 절차\n"
            f"1. `multica repo checkout https://github.com/Memoriz-KR/CheckYourHospital.git`\n"
            f"2. `git checkout {branch}`\n"
            f"3. `git rebase main` — 충돌 해결\n"
            f"4. `git push --force-with-lease`\n"
            f"5. 테스트 통과 확인\n\n"
            f"## 주의\n"
            f"- scorer.py 충돌 시: 현재 main의 가중치 구조 기준으로 병합\n"
            f"- scanner.py 충돌 시: 기존 체크 항목 유지하며 새 체크 추가"
        ),
    )

# --- Group 2: Code fixes needed ---
print("\n--- Code Fix (보안/품질 수정) ---")

create_issue(
    "[Fix] PR #4 결제 시스템 보안 취약점 수정",
    "urgent",
    "CYH Backend Dev",
    (
        "## 보안 이슈 (리뷰에서 발견)\n"
        "PR #4 `feature/payment-system`에 심각한 보안 취약점:\n\n"
        "1. **웹훅 서명 미검증**: Toss Payments 웹훅에서 signature 검증 없음 → 위조 웹훅으로 구독 활성화 가능\n"
        "2. **금액 변조 가능**: 클라이언트가 전달한 금액을 서버에서 검증하지 않음\n"
        "3. **TOSS_SECRET_KEY 빈 값 fallback**: 시크릿 키가 없으면 빈 문자열로 폴백\n"
        "4. **구독 생성 race condition**: 동시 요청 시 중복 구독 가능\n\n"
        "## 수정 사항\n"
        "- [ ] 웹훅 HMAC-SHA256 서명 검증 추가\n"
        "- [ ] 서버측 금액 검증 (plan_id → 서버 가격표 조회)\n"
        "- [ ] TOSS_SECRET_KEY 필수화 (없으면 startup 실패)\n"
        "- [ ] 구독 생성 시 DB unique constraint 또는 advisory lock\n"
        "- [ ] rebase main 후 push"
    ),
)

create_issue(
    "[Fix] PR #6 AI 추천 시뮬레이션 — 중복 제거 + rate limit + 테스트",
    "high",
    "CYH Backend Dev",
    (
        "## 리뷰 피드백\n"
        "1. **중복 함수**: geo_aeo.py와 새 엔진 간 query 함수 중복 → 공통 모듈로 추출\n"
        "2. **Rate limit 없음**: 요청당 최대 40개 외부 API 호출 → per-endpoint throttle 추가\n"
        "3. **테스트 없음**: 최소 유닛 테스트 추가\n"
        "- [ ] rebase main 후 push"
    ),
)

create_issue(
    "[Fix] PR #7 AEO 콘텐츠 생성 — 보안 + 테스트",
    "urgent",
    "CYH Backend Dev",
    (
        "## 보안 이슈\n"
        "1. **예외 상세 노출**: Exception 내용이 클라이언트에 그대로 전달 → generic error message로 교체\n"
        "2. **LLM 출력 미검증**: 생성된 콘텐츠가 sanitize 없이 저장 → HTML escape / 금지 패턴 필터\n"
        "3. **Quota race condition**: 동시 요청 시 quota 초과 가능\n"
        "4. **1100+ 라인 단일 파일**: 분할 필요\n"
        "5. **테스트 없음**\n"
        "- [ ] rebase main 후 push"
    ),
)

create_issue(
    "[Fix] PR #15 메신저 딥링크 — SSRF 방지",
    "high",
    "CYH Backend Dev",
    (
        "## 보안 이슈\n"
        "`_verify_link`가 리다이렉트를 따라 임의 URL에 요청 → SSRF 리스크.\n\n"
        "## 수정\n"
        "- [ ] 허용 도메인 화이트리스트: pf.kakao.com, open.kakao.com, line.me, lin.ee, "
        "page.line.me, wa.me, api.whatsapp.com\n"
        "- [ ] `allow_redirects=False` 후 Location 헤더만 확인\n"
        "- [ ] sequential HEAD → asyncio.gather 병렬화\n"
        "- [ ] rebase main 후 push"
    ),
)

create_issue(
    "[Fix] PR #19 경쟁사 레이더 — N+1 쿼리 + 인증",
    "high",
    "CYH Frontend Dev",
    (
        "## 리뷰 피드백\n"
        "1. **N+1 쿼리**: 경쟁사별 DB 개별 조회 → batch query로 변경\n"
        "2. **인증 없음**: API route에 auth 체크 누락\n"
        "3. **ilike on URL without index**: 인덱스 추가 또는 쿼리 최적화\n"
        "4. **중복 MEDICAL_REGIONS**: 공유 상수로 추출\n"
        "- [ ] rebase main 후 push"
    ),
)

create_issue(
    "[Fix] PR #21 가격 투명성 — 테스트 + regex 오탐",
    "high",
    "CYH Frontend Dev",
    (
        "## 리뷰 피드백\n"
        "1. **테스트 없음**: 399줄 analyzer에 유닛 테스트 필요\n"
        "2. **통화 regex 오탐**: '원' 이 일반 한국어 단어에서 false positive\n"
        "3. **inline type assertion**: page.tsx에서 massive assertion → 타입 분리\n"
        "- [ ] rebase main 후 push"
    ),
)

print("\n" + "=" * 60)
print(" Done!")
print("=" * 60)
