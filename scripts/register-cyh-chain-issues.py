#!/usr/bin/env python3
"""CYH 체인/멀티지점 병원 지원 이슈 등록."""

import json
import subprocess

PROJECT_ID = "18031aa2-6cc7-4a99-ae6b-147494f07d0c"


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


print("=" * 60)
print(" CYH Chain/Multi-Branch Support Issues")
print("=" * 60)

# Epic
epic_id = create_issue(
    "[Chain] 체인/멀티지점 병원 지원",
    "high",
    "CYH Planner",
    (
        "## 배경\n"
        "한국 대형 피부과/성형외과 체인(Oracle 30+지점, Renewme 4, Made U 11, ID Hospital 등)은\n"
        "허브 사이트 + 지점별 독립 사이트(서브도메인/독립도메인) 구조로 운영.\n"
        "현재 CYH는 URL 1개 = 병원 1개로 가정하여, 허브 URL 입력 시 실제 지점 콘텐츠를 놓침.\n\n"
        "## 실제 사례: Oracle Clinic\n"
        "- oracleclinic.com → 50+ 지점 목록 허브 (콘텐츠 거의 없음)\n"
        "- daechi.oracleclinic.com → 실제 지점 사이트 (Next.js)\n"
        "- cdoracleclinic.com → 제휴 지점 (독립 도메인, iMWeb)\n"
        "- oraclemedicalgroup.com → 다국어 허브 (EN/ZH/JP)\n\n"
        "## 구현 단계\n"
        "1. 허브 사이트 자동 감지\n"
        "2. 지점 URL 자동 추출\n"
        "3. '허브입니다' 안내 UI\n"
        "4. 지점 선택 → 개별 스캔 UI\n"
        "5. 배치 지점 스캔 (Enterprise)\n"
        "6. 체인 통합 리포트"
    ),
)

print()

# 1. 허브 감지
create_issue(
    "[Chain-1] 허브 사이트 자동 감지 로직",
    "high",
    "CYH Backend Dev",
    (
        "## 배경\n"
        "크롤링 시 '이 사이트가 허브/포털인지 실제 병원 사이트인지' 자동 판별.\n"
        "허브 특징: 외부 도메인/서브도메인 링크 밀도 높음, 자체 콘텐츠 적음, 지점 목록 패턴.\n\n"
        "## 요구사항\n"
        "- [ ] 크롤링 결과에서 외부 링크 분석:\n"
        "  - 서브도메인 링크 수 (예: daechi.oracleclinic.com, gangnam.oracleclinic.com)\n"
        "  - 외부 도메인이지만 같은 브랜드로 보이는 링크 수\n"
        "- [ ] 허브 판별 기준:\n"
        "  - 서브도메인/외부 클리닉 링크 >= 5개\n"
        "  - 자체 콘텐츠 페이지 < 10개\n"
        "  - 지점 목록 키워드 감지 (지점, 분원, branch, clinic, 네트워크)\n"
        "- [ ] scan_result에 site_type 필드 추가:\n"
        "  - 'hub': 허브/포털 사이트\n"
        "  - 'branch': 개별 지점 사이트\n"
        "  - 'standalone': 단독 병원\n"
        "- [ ] 허브일 경우 발견된 지점 URL 목록도 리턴\n"
        "  - branch_urls: [{url, name, type(subdomain/external)}]\n\n"
        "## 관련 파일\n"
        "- apps/worker/app/services/crawler.py (링크 수집 확장)\n"
        "- apps/worker/app/services/scanner.py (site_type 판별 로직)\n\n"
        "## 완료 조건\n"
        "- oracleclinic.com → site_type: 'hub', branch_urls: 20+\n"
        "- daechi.oracleclinic.com → site_type: 'branch'\n"
        "- 일반 단독 병원 → site_type: 'standalone'"
    ),
    epic_id,
)

# 2. 지점 URL 추출
create_issue(
    "[Chain-2] 허브 페이지에서 지점 URL 자동 추출",
    "high",
    "CYH Backend Dev",
    (
        "## 배경\n"
        "허브 감지 후, 실제 지점 URL을 정확히 추출해야 함.\n"
        "Oracle은 onclick 핸들러에 URL이 있고, 다른 체인은 href에 직접 있을 수 있음.\n\n"
        "## 요구사항\n"
        "- [ ] 지점 URL 추출 전략 (우선순위):\n"
        "  1. href에서 서브도메인/외부 도메인 링크 추출\n"
        "  2. onclick 핸들러에서 URL 파싱 (window.open, location.href 등)\n"
        "  3. iframe src에서 추출\n"
        "- [ ] 지점 정보 보강:\n"
        "  - 지점명 (링크 텍스트 또는 주변 텍스트)\n"
        "  - 지역 (주소 패턴 매칭)\n"
        "  - URL 타입 (서브도메인 vs 독립 도메인)\n"
        "- [ ] 중복 제거 (같은 지점의 다른 경로)\n"
        "- [ ] 유효성 검증 (HTTP HEAD → 200 확인)\n\n"
        "## 관련 파일\n"
        "- 신규: apps/worker/app/services/hub_detector.py\n\n"
        "## 완료 조건\n"
        "- Oracle 허브에서 20+ 지점 URL 정확 추출\n"
        "- 지점명, 지역 정보 포함"
    ),
    epic_id,
)

# 3. 허브 안내 UI
create_issue(
    "[Chain-3] '허브 사이트입니다' 안내 UI + 지점 목록",
    "high",
    "CYH Frontend Dev",
    (
        "## 배경\n"
        "site_type='hub'일 때 리포트에 안내 메시지 + 발견된 지점 목록 표시.\n"
        "사용자가 실제 진단할 지점을 선택할 수 있도록.\n\n"
        "## 요구사항\n"
        "- [ ] 리포트 상단에 파란색 정보 배너:\n"
        "  - '이 URL은 N개 지점의 허브(포털) 사이트입니다'\n"
        "  - '실제 지점 사이트를 진단하면 더 정확한 결과를 얻을 수 있습니다'\n"
        "- [ ] 지점 목록 카드:\n"
        "  - 지점명 | URL | 지역 | 타입(서브도메인/독립)\n"
        "  - 각 지점 옆에 '이 지점 진단하기' 버튼\n"
        "  - 클릭 시 해당 지점 URL로 새 스캔 시작\n"
        "- [ ] 허브 리포트 자체는 정상 표시 (점수는 허브 기준)\n"
        "- [ ] '전체 지점 배치 진단' 버튼 (Enterprise 티어 CTA)\n\n"
        "## 관련 파일\n"
        "- 신규: apps/web/src/components/report/hub-site-banner.tsx\n"
        "- apps/web/src/app/report/[id]/page.tsx\n\n"
        "## 완료 조건\n"
        "- hub 타입 리포트에서 배너 + 지점 목록 표시\n"
        "- standalone/branch 타입에서는 배너 미표시\n"
        "- 지점 클릭 시 새 스캔 정상 시작"
    ),
    epic_id,
)

# 4. 지점 선택 스캔 UI
create_issue(
    "[Chain-4] 지점 선택 → 개별 스캔 플로우",
    "medium",
    "CYH Frontend Dev",
    (
        "## 배경\n"
        "허브 URL 입력 시 '지점을 선택하세요' 중간 단계를 추가.\n"
        "스캔 시작 전에 사용자가 올바른 지점을 선택하도록.\n\n"
        "## 요구사항\n"
        "- [ ] 스캔 플로우 분기:\n"
        "  - URL 입력 → 빠른 크롤링(1페이지만) → 허브 여부 판별\n"
        "  - standalone/branch → 기존 플로우 (바로 전체 스캔)\n"
        "  - hub → 지점 선택 화면 표시\n"
        "- [ ] 지점 선택 화면:\n"
        "  - 발견된 지점 목록 (이름, URL, 지역)\n"
        "  - 라디오 버튼 또는 카드 선택\n"
        "  - '선택한 지점 진단하기' 버튼\n"
        "  - '허브 사이트 그대로 진단하기' 옵션도 유지\n"
        "- [ ] 선택 후 해당 지점 URL로 정상 스캔 시작\n\n"
        "## 관련 파일\n"
        "- apps/web/src/app/page.tsx (랜딩 URL 입력)\n"
        "- apps/web/src/app/scan/[id]/page.tsx\n"
        "- 신규 API: POST /api/audits/detect-hub (빠른 판별)\n\n"
        "## 완료 조건\n"
        "- oracleclinic.com 입력 시 지점 선택 화면 표시\n"
        "- 단독 병원 입력 시 기존 플로우 유지"
    ),
    epic_id,
)

# 5. 배치 지점 스캔
create_issue(
    "[Chain-5] 배치 지점 스캔 (Enterprise 티어)",
    "medium",
    "CYH Backend Dev",
    (
        "## 배경\n"
        "Enterprise 고객이 전 지점을 한 번에 스캔.\n"
        "Oracle 30+지점, Made U 11지점 등 대규모 배치.\n\n"
        "## 요구사항\n"
        "- [ ] 배치 스캔 API: POST /api/chain/batch-scan\n"
        "  - 입력: hub_url 또는 branch_urls 배열\n"
        "  - 각 지점을 개별 audit으로 생성\n"
        "  - chain_id로 그룹핑 (audits 테이블에 chain_id 컬럼 추가)\n"
        "- [ ] 병렬도 제한: 동시 최대 5개 지점 스캔\n"
        "- [ ] 진행 상황 API: GET /api/chain/{chain_id}/status\n"
        "  - 전체 N개 중 완료 M개, 진행 중 K개\n"
        "- [ ] 요금 제한: Free/Growth는 1개, Pro 5개, Enterprise 무제한\n\n"
        "## DB 변경\n"
        "- chains 테이블: id, hub_url, branch_count, created_at\n"
        "- audits에 chain_id FK 추가 (nullable)\n\n"
        "## 완료 조건\n"
        "- 5개 지점 배치 스캔 테스트\n"
        "- 진행 상황 정상 추적"
    ),
    epic_id,
)

# 6. 체인 통합 리포트
create_issue(
    "[Chain-6] 체인 통합 리포트 (지점 간 비교 + 요약)",
    "medium",
    "CYH Frontend Dev",
    (
        "## 배경\n"
        "전 지점 배치 스캔 후 체인 전체를 한눈에 볼 수 있는 통합 리포트.\n"
        "어떤 지점이 잘하고 어떤 지점이 부족한지 비교.\n\n"
        "## 요구사항\n"
        "- [ ] 체인 리포트 페이지: /chain/{chain_id}\n"
        "- [ ] 체인 요약 섹션:\n"
        "  - 전 지점 평균 점수\n"
        "  - 최고/최저 점수 지점\n"
        "  - 6카테고리별 전 지점 평균\n"
        "- [ ] 지점 비교 테이블:\n"
        "  - 지점명 | 총점 | Tech | Content | Intl | Authority | AEO | Compliance\n"
        "  - 색상 코딩 (A=초록 ~ F=빨강)\n"
        "  - 정렬/필터 가능\n"
        "- [ ] 일관성 체크:\n"
        "  - Schema 사용 통일 여부\n"
        "  - 브랜딩 일관성 (로고, 색상, CTA)\n"
        "  - 다국어 지원 격차 (본원은 있는데 분원은 없는 경우)\n"
        "- [ ] 개별 지점 클릭 → 해당 지점 리포트로 이동\n"
        "- [ ] PDF 체인 요약 리포트 (선택)\n\n"
        "## 관련 파일\n"
        "- 신규: apps/web/src/app/chain/[id]/page.tsx\n"
        "- 신규: apps/web/src/components/report/chain-summary.tsx\n\n"
        "## 완료 조건\n"
        "- 5개 지점 데이터로 체인 리포트 렌더링\n"
        "- 지점 간 비교 테이블 정상 표시"
    ),
    epic_id,
)

print(f"\n{'=' * 60}")
print(" Done!")
print("=" * 60)
