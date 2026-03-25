"""404/redirect error check (weight: 5%)."""

import httpx

from .base import CheckResult, Grade


async def check_errors(
    client: httpx.AsyncClient, crawled_urls: list[str], *, max_check: int = 50
) -> CheckResult:
    issues: list[str] = []
    error_count = 0
    redirect_chains = 0
    checked = 0

    for url in crawled_urls[:max_check]:
        try:
            # Don't follow redirects to detect chains
            resp = await client.get(url, follow_redirects=False)
            checked += 1

            if resp.status_code >= 400:
                error_count += 1
                issues.append(f"HTTP {resp.status_code}: {url}")

            # Detect redirect chains
            if resp.status_code in (301, 302, 307, 308):
                location = resp.headers.get("location", "")
                if location:
                    try:
                        resp2 = await client.get(location, follow_redirects=False)
                        if resp2.status_code in (301, 302, 307, 308):
                            redirect_chains += 1
                            issues.append(f"리다이렉트 체인: {url}")
                    except httpx.HTTPError:
                        pass
        except httpx.HTTPError:
            checked += 1
            error_count += 1

    details = {
        "checked": checked,
        "error_count": error_count,
        "redirect_chains": redirect_chains,
    }

    if error_count >= 6:
        return CheckResult(
            name="errors_404", score=0.0, grade=Grade.FAIL, details=details, issues=issues
        )

    if error_count >= 1 or redirect_chains >= 1:
        return CheckResult(
            name="errors_404", score=0.5, grade=Grade.WARN, details=details, issues=issues
        )

    return CheckResult(name="errors_404", score=1.0, grade=Grade.PASS, details=details)
