"""robots.txt check (weight: 5%)."""

import httpx

from .base import CheckResult, Grade

_DISPLAY_NAME = "검색엔진 접근 허용"
_DESCRIPTION = "구글/네이버가 홈페이지를 읽어도 되는지 알려주는 설정 파일입니다"
_RECOMMENDATION = "웹 개발자에게 robots.txt 파일을 생성하고 검색엔진 접근을 허용해달라고 요청하세요"


async def check_robots(client: httpx.AsyncClient, base_url: str) -> CheckResult:
    url = f"{base_url.rstrip('/')}/robots.txt"

    try:
        resp = await client.get(url, follow_redirects=True)
    except httpx.HTTPError:
        return CheckResult(
            name="robots_txt",
            score=0.0,
            grade=Grade.FAIL,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=["robots.txt를 가져올 수 없습니다"],
        )

    if resp.status_code != 200:
        return CheckResult(
            name="robots_txt",
            score=0.0,
            grade=Grade.FAIL,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=[f"robots.txt가 존재하지 않습니다 (HTTP {resp.status_code})"],
        )

    text = resp.text
    issues: list[str] = []
    has_sitemap = "sitemap:" in text.lower()

    # Check for full block
    lines = text.lower().splitlines()
    full_block = any(
        line.strip() == "disallow: /"
        for line in lines
    )

    if full_block:
        return CheckResult(
            name="robots_txt",
            score=0.0,
            grade=Grade.FAIL,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=["robots.txt가 전체 사이트를 차단하고 있습니다 (Disallow: /)"],
        )

    if not has_sitemap:
        issues.append("Sitemap 디렉티브가 없습니다")

    # Check multilingual path blocking
    for lang_path in ["/en/", "/ja/", "/zh/", "/ko/"]:
        if f"disallow: {lang_path}" in text.lower():
            issues.append(f"다국어 경로 {lang_path}가 차단되어 있습니다")

    disallow_count = text.lower().count("disallow:")
    if disallow_count > 5:
        issues.append(f"과도한 Disallow 규칙 ({disallow_count}개)")

    if issues:
        return CheckResult(
            name="robots_txt",
            score=0.5,
            grade=Grade.WARN,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            details={"has_sitemap_directive": has_sitemap, "disallow_count": disallow_count},
            issues=issues,
        )

    return CheckResult(
        name="robots_txt",
        score=1.0,
        grade=Grade.PASS,
        display_name=_DISPLAY_NAME,
        description=_DESCRIPTION,
        recommendation=_RECOMMENDATION,
        details={"has_sitemap_directive": has_sitemap, "disallow_count": disallow_count},
    )
