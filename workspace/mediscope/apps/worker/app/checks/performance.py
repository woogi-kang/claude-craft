"""Core Web Vitals + performance score (covers LCP/INP/CLS/perf_score — 4 items, weight: 15%)."""

import httpx

from ..config import settings
from .base import CheckResult, Grade

# Display names / descriptions / recommendations for each performance metric
_META: dict[str, tuple[str, str, str]] = {
    "lcp": (
        "메인 콘텐츠 로딩 속도",
        "페이지에서 가장 큰 이미지나 텍스트가 화면에 나타나는 데 걸리는 시간입니다",
        "이미지 최적화(WebP 변환, 압축), 서버 응답 속도 개선을 웹 개발자에게 요청하세요",
    ),
    "inp": (
        "터치/클릭 반응 속도",
        "버튼을 누르거나 메뉴를 클릭했을 때 반응하는 속도입니다",
        "불필요한 스크립트 정리, 서드파티 위젯 최적화를 웹 개발자에게 요청하세요",
    ),
    "cls": (
        "화면 밀림 현상",
        "페이지가 로딩되면서 내용이 갑자기 밀려나는 정도입니다",
        "이미지/광고에 크기(width, height)를 미리 지정해 달라고 웹 개발자에게 요청하세요",
    ),
    "performance_score": (
        "종합 성능 점수 (Lighthouse)",
        "구글이 매기는 모바일 성능 종합 점수입니다 (100점 만점)",
        "이미지 최적화, 불필요한 코드 제거, 서버 속도 개선 등 종합적인 성능 튜닝이 필요합니다",
    ),
}


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
    display_name, description, recommendation = _META[name]

    if value is None:
        return CheckResult(
            name=name, score=0.5, grade=Grade.WARN,
            display_name=display_name, description=description,
            recommendation=recommendation,
            details={"value": None}, issues=[f"{name} 측정 불가"],
        )

    details = {"value": round(value, 3), "unit": unit, "good_threshold": good, "poor_threshold": poor}

    if value <= good:
        return CheckResult(
            name=name, score=1.0, grade=Grade.PASS,
            display_name=display_name, description=description,
            recommendation=recommendation,
            details=details,
        )
    if value <= poor:
        return CheckResult(
            name=name, score=0.5, grade=Grade.WARN,
            display_name=display_name, description=description,
            recommendation=recommendation,
            details=details,
            issues=[f"{name}: {value}{unit} (권장: {good}{unit} 이하)"],
        )
    return CheckResult(
        name=name, score=0.0, grade=Grade.FAIL,
        display_name=display_name, description=description,
        recommendation=recommendation,
        details=details,
        issues=[f"{name}: {value}{unit} (기준 초과: {poor}{unit})"],
    )


def _score_perf(score: float | None) -> CheckResult:
    display_name, description, recommendation = _META["performance_score"]

    if score is None:
        return CheckResult(
            name="performance_score", score=0.5, grade=Grade.WARN,
            display_name=display_name, description=description,
            recommendation=recommendation,
            details={"value": None}, issues=["성능 점수 측정 불가"],
        )

    details = {"value": round(score, 1)}

    if score >= 90:
        return CheckResult(
            name="performance_score", score=1.0, grade=Grade.PASS,
            display_name=display_name, description=description,
            recommendation=recommendation,
            details=details,
        )
    if score >= 50:
        return CheckResult(
            name="performance_score", score=0.5, grade=Grade.WARN,
            display_name=display_name, description=description,
            recommendation=recommendation,
            details=details,
            issues=[f"성능 점수: {score:.0f}/100 (90 이상 권장)"],
        )
    return CheckResult(
        name="performance_score", score=0.0, grade=Grade.FAIL,
        display_name=display_name, description=description,
        recommendation=recommendation,
        details=details,
        issues=[f"성능 점수: {score:.0f}/100 (매우 낮음)"],
    )


def _fallback_results(reason: str) -> list[CheckResult]:
    names = ["lcp", "inp", "cls", "performance_score"]
    return [
        CheckResult(
            name=n, score=0.5, grade=Grade.WARN,
            fail_type="api_error",
            display_name=_META[n][0],
            description=_META[n][1],
            recommendation=_META[n][2],
            issues=[reason],
        )
        for n in names
    ]
