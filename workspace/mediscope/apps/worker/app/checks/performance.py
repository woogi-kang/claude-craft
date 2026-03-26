"""Core Web Vitals + performance score (covers LCP/INP/CLS/perf_score — 4 items, weight: 15%)."""

import httpx

from ..config import settings
from .base import CheckResult, Grade


async def check_performance(
    client: httpx.AsyncClient, url: str
) -> list[CheckResult]:
    """Returns 4 CheckResults: lcp, inp, cls, performance_score."""
    results: list[CheckResult] = []

    api_key = settings.pagespeed_api_key
    psi_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params: dict = {"url": url, "strategy": "mobile", "category": "PERFORMANCE"}
    if api_key:
        params["key"] = api_key

    try:
        resp = await client.get(psi_url, params=params, timeout=60)
        if resp.status_code != 200:
            return _fallback_results("PageSpeed API 호출 실패")
        data = resp.json()
    except (httpx.HTTPError, ValueError):
        return _fallback_results("PageSpeed API 접속 불가")

    metrics = (
        data.get("lighthouseResult", {})
        .get("audits", {})
    )
    categories = data.get("lighthouseResult", {}).get("categories", {})

    # LCP (weight: 5%) — good: ≤2.5s
    lcp_ms = _get_numeric(metrics, "largest-contentful-paint", "numericValue")
    lcp_s = lcp_ms / 1000 if lcp_ms else None
    results.append(_score_metric("lcp", lcp_s, good=2.5, poor=4.0, unit="s"))

    # INP (weight: 3%) — good: ≤200ms
    inp_ms = _get_numeric(metrics, "interaction-to-next-paint", "numericValue")
    if inp_ms is None:
        inp_ms = _get_numeric(metrics, "max-potential-fid", "numericValue")
    inp_val = inp_ms if inp_ms else None
    results.append(_score_metric("inp", inp_val, good=200, poor=500, unit="ms"))

    # CLS (weight: 3%) — good: ≤0.1
    cls_val = _get_numeric(metrics, "cumulative-layout-shift", "numericValue")
    results.append(_score_metric("cls", cls_val, good=0.1, poor=0.25, unit=""))

    # Performance score (weight: 4%) — Lighthouse 0-100
    perf_score_raw = categories.get("performance", {}).get("score")
    perf_score = perf_score_raw * 100 if perf_score_raw is not None else None
    results.append(_score_perf(perf_score))

    return results


def _get_numeric(audits: dict, key: str, field: str) -> float | None:
    audit = audits.get(key, {})
    val = audit.get(field)
    if val is not None:
        return float(val)
    return None


def _score_metric(
    name: str, value: float | None, good: float, poor: float, unit: str
) -> CheckResult:
    if value is None:
        return CheckResult(
            name=name, score=0.5, grade=Grade.WARN,
            details={"value": None}, issues=[f"{name} 측정 불가"],
        )

    details = {"value": round(value, 3), "unit": unit, "good_threshold": good, "poor_threshold": poor}

    if value <= good:
        return CheckResult(name=name, score=1.0, grade=Grade.PASS, details=details)
    if value <= poor:
        return CheckResult(
            name=name, score=0.5, grade=Grade.WARN, details=details,
            issues=[f"{name}: {value}{unit} (권장: {good}{unit} 이하)"],
        )
    return CheckResult(
        name=name, score=0.0, grade=Grade.FAIL, details=details,
        issues=[f"{name}: {value}{unit} (기준 초과: {poor}{unit})"],
    )


def _score_perf(score: float | None) -> CheckResult:
    if score is None:
        return CheckResult(
            name="performance_score", score=0.5, grade=Grade.WARN,
            details={"value": None}, issues=["성능 점수 측정 불가"],
        )

    details = {"value": round(score, 1)}
    normalized = score / 100  # 0.0-1.0

    if score >= 90:
        return CheckResult(name="performance_score", score=1.0, grade=Grade.PASS, details=details)
    if score >= 50:
        return CheckResult(
            name="performance_score", score=0.5, grade=Grade.WARN, details=details,
            issues=[f"성능 점수: {score:.0f}/100 (90 이상 권장)"],
        )
    return CheckResult(
        name="performance_score", score=0.0, grade=Grade.FAIL, details=details,
        issues=[f"성능 점수: {score:.0f}/100 (매우 낮음)"],
    )


def _fallback_results(reason: str) -> list[CheckResult]:
    names = ["lcp", "inp", "cls", "performance_score"]
    return [
        CheckResult(name=n, score=0.5, grade=Grade.WARN, issues=[reason])
        for n in names
    ]
