"""HTTPS / SSL check (weight: 3%)."""

import ssl
from urllib.parse import urlparse

import httpx

from .base import CheckResult, Grade

_DISPLAY_NAME = "보안 연결 (자물쇠)"
_DESCRIPTION = "홈페이지가 암호화된 안전한 연결을 사용하는지 확인합니다"
_RECOMMENDATION = (
    '호스팅 업체에 "SSL 인증서 설치"를 요청하세요. 무료 인증서(Let\'s Encrypt)도 있습니다'
)


async def check_https(client: httpx.AsyncClient, url: str) -> CheckResult:
    parsed = urlparse(url)
    issues: list[str] = []
    details: dict = {}

    # Check if site uses HTTPS
    if parsed.scheme != "https":
        # Try HTTPS version
        https_url = url.replace("http://", "https://", 1)
        try:
            resp = await client.get(https_url, follow_redirects=False)
            details["https_available"] = True
            issues.append("사이트가 HTTP를 사용하고 있습니다 (HTTPS 사용 권장)")
        except httpx.HTTPError:
            details["https_available"] = False
            issues.append("HTTPS를 사용할 수 없습니다")
            return CheckResult(
                name="https", score=0.0, grade=Grade.FAIL,
                display_name=_DISPLAY_NAME, description=_DESCRIPTION,
                recommendation=_RECOMMENDATION,
                details=details, issues=issues,
            )

    # Check HTTP → HTTPS redirect
    http_url = url.replace("https://", "http://", 1)
    try:
        resp = await client.get(http_url, follow_redirects=False)
        details["http_redirects_to_https"] = resp.status_code in (301, 302, 307, 308)
        if not details["http_redirects_to_https"]:
            issues.append("HTTP → HTTPS 리다이렉트가 설정되지 않았습니다")
    except httpx.HTTPError:
        details["http_redirects_to_https"] = False

    # Check for mixed content (basic heuristic from HTML)
    try:
        resp = await client.get(url, follow_redirects=True)
        html = resp.text
        mixed = 'src="http://' in html or "src='http://" in html
        details["has_mixed_content"] = mixed
        if mixed:
            issues.append("Mixed Content가 감지되었습니다")
    except httpx.HTTPError:
        pass

    if parsed.scheme != "https":
        return CheckResult(
            name="https", score=0.0, grade=Grade.FAIL,
            display_name=_DISPLAY_NAME, description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            details=details, issues=issues,
        )

    if issues:
        return CheckResult(
            name="https", score=0.5, grade=Grade.WARN,
            display_name=_DISPLAY_NAME, description=_DESCRIPTION,
            recommendation=_RECOMMENDATION,
            details=details, issues=issues,
        )

    return CheckResult(
        name="https", score=1.0, grade=Grade.PASS,
        display_name=_DISPLAY_NAME, description=_DESCRIPTION,
        recommendation=_RECOMMENDATION,
        details=details,
    )
