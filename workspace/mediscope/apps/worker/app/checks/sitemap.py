"""sitemap.xml check (weight: 5%)."""

import httpx
from xml.etree import ElementTree

from .base import CheckResult, Grade

SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

_DISPLAY_NAME = "페이지 목록 제출"
_DESCRIPTION = "홈페이지의 모든 페이지 목록을 검색엔진에 알려주는 파일입니다"
_RECOMMENDATION = (
    "웹 개발자에게 sitemap.xml 파일을 만들고 Google Search Console에 등록해달라고 요청하세요"
)


async def check_sitemap(client: httpx.AsyncClient, base_url: str) -> CheckResult:
    url = f"{base_url.rstrip('/')}/sitemap.xml"
    issues: list[str] = []

    try:
        resp = await client.get(url, follow_redirects=True)
    except httpx.HTTPError:
        return CheckResult(
            name="sitemap",
            score=0.0,
            grade=Grade.FAIL,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=["sitemap.xml을 가져올 수 없습니다"],
        )

    if resp.status_code != 200:
        return CheckResult(
            name="sitemap",
            score=0.0,
            grade=Grade.FAIL,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=["sitemap.xml이 존재하지 않습니다"],
        )

    try:
        root = ElementTree.fromstring(resp.text)
    except ElementTree.ParseError:
        return CheckResult(
            name="sitemap",
            score=0.0,
            grade=Grade.FAIL,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=["sitemap.xml XML 파싱 실패"],
        )

    urls = root.findall(".//sm:url", SITEMAP_NS)
    if not urls:
        # Try without namespace
        urls = root.findall(".//url")

    url_count = len(urls)
    if url_count == 0:
        return CheckResult(
            name="sitemap",
            score=0.0,
            grade=Grade.FAIL,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            issues=["sitemap.xml에 URL이 없습니다"],
        )

    # Check lastmod
    lastmod_elements = root.findall(".//sm:lastmod", SITEMAP_NS)
    if not lastmod_elements:
        lastmod_elements = root.findall(".//lastmod")
    has_lastmod = len(lastmod_elements) > 0

    if not has_lastmod:
        issues.append("lastmod 정보가 없습니다")

    if url_count < 10:
        issues.append(f"URL이 {url_count}개로 부족합니다 (10개 미만)")

    if issues:
        return CheckResult(
            name="sitemap",
            score=0.5,
            grade=Grade.WARN,
            display_name=_DISPLAY_NAME,
            description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            details={"url_count": url_count, "has_lastmod": has_lastmod},
            issues=issues,
        )

    return CheckResult(
        name="sitemap",
        score=1.0,
        grade=Grade.PASS,
        display_name=_DISPLAY_NAME,
        description=_DESCRIPTION,
        recommendation=_RECOMMENDATION,
        details={"url_count": url_count, "has_lastmod": has_lastmod},
    )
