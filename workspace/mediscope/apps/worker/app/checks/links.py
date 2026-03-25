"""Internal links / broken links check (weight: 5%)."""

from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from .base import CheckResult, Grade


async def check_links(
    client: httpx.AsyncClient, html: str, base_url: str, *, max_check: int = 30
) -> CheckResult:
    soup = BeautifulSoup(html, "lxml")
    base_domain = urlparse(base_url).netloc
    issues: list[str] = []

    internal_links: list[str] = []
    for a in soup.find_all("a", href=True):
        href = str(a["href"])
        full = urljoin(base_url, href)
        parsed = urlparse(full)
        if parsed.netloc == base_domain and parsed.scheme in ("http", "https"):
            internal_links.append(full)

    unique_links = list(set(internal_links))[:max_check]
    broken = 0
    checked = 0

    for link in unique_links:
        try:
            resp = await client.head(link, follow_redirects=True)
            checked += 1
            if resp.status_code >= 400:
                broken += 1
                issues.append(f"깨진 링크: {link} (HTTP {resp.status_code})")
        except httpx.HTTPError:
            checked += 1
            broken += 1
            issues.append(f"접근 불가: {link}")

    details = {
        "total_internal_links": len(internal_links),
        "unique_checked": checked,
        "broken_count": broken,
    }

    if broken >= 6:
        return CheckResult(name="links", score=0.0, grade=Grade.FAIL, details=details, issues=issues)

    if broken >= 1:
        return CheckResult(name="links", score=0.5, grade=Grade.WARN, details=details, issues=issues)

    if len(internal_links) < 3:
        issues.append("내부 링크가 부족합니다 (3개 미만)")
        return CheckResult(name="links", score=0.5, grade=Grade.WARN, details=details, issues=issues)

    return CheckResult(name="links", score=1.0, grade=Grade.PASS, details=details)
