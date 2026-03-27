"""Scanner orchestrator: runs all checks and produces a score."""

import httpx

from ..checks.base import CheckResult
from ..checks.canonical import check_canonical
from ..checks.errors import check_errors
from ..checks.geo_aeo import check_ai_search_mention, check_content_clarity
from ..checks.headings import check_headings
from ..checks.https_check import check_https
from ..checks.images import check_images
from ..checks.links import check_links
from ..checks.meta_tags import check_meta_tags
from ..checks.multilingual import (
    check_hreflang,
    check_multilingual_pages,
    check_overseas_channels,
)
from ..checks.mobile import check_mobile
from ..checks.performance import check_performance
from ..checks.robots import check_robots
from ..checks.sitemap import check_sitemap
from ..checks.structured_data import (
    check_eeat_signals,
    check_faq_content,
    check_structured_data,
)
from ..checks.url_structure import check_url_structure
from ..config import settings
from .crawler import Crawler
from .scorer import calculate_score


async def run_scan(
    url: str,
    *,
    max_pages: int = 50,
    max_depth: int = 3,
    check_geo: bool = True,
    hospital_name: str = "",
    specialty: str = "",
    region: str = "",
    hospital_id: str | None = None,
) -> dict:
    """Run full SEO + GEO/AEO scan on a URL. Returns scored results."""
    crawler = Crawler(max_pages=max_pages, max_depth=max_depth)

    # Crawl pages
    pages = await crawler.crawl(url)
    if not pages:
        return {
            "url": url,
            "error": "사이트에 접근할 수 없습니다",
            "total_score": 0,
            "grade": "F",
            "category_scores": {},
        }

    main_page = pages[0]
    crawled_urls = [p.url for p in pages]
    all_results: list[CheckResult] = []

    # Run checks — async checks need an HTTP client
    async with httpx.AsyncClient(
        timeout=settings.crawler_timeout,
        follow_redirects=True,
        headers={"User-Agent": "MediScope-Bot/1.0"},
    ) as client:
        # Async checks
        all_results.append(await check_robots(client, url))
        all_results.append(await check_sitemap(client, url))
        all_results.append(await check_https(client, url))
        all_results.append(await check_links(client, main_page.html, url))
        all_results.append(await check_errors(client, crawled_urls))

        # Performance checks (returns 4 results: lcp, inp, cls, performance_score)
        perf_results = await check_performance(client, url)
        all_results.extend(perf_results)

        # GEO/AEO: AI search mention (async, optional)
        if check_geo:
            all_results.append(
                await check_ai_search_mention(
                    client, url, hospital_name, specialty, region
                )
            )

    # Sync checks (HTML parsing)
    all_results.append(check_meta_tags(main_page.html, url))
    all_results.append(check_headings(main_page.html))
    all_results.append(check_images(main_page.html))
    all_results.append(check_canonical(main_page.html, url))
    all_results.append(check_url_structure(url, crawled_urls))
    all_results.append(check_mobile(main_page.html))

    # Multilingual checks (sync, 3 separate checks)
    all_results.append(check_multilingual_pages(main_page.html, crawled_urls))
    all_results.append(check_hreflang(main_page.html))
    all_results.append(check_overseas_channels(main_page.html))

    # GEO/AEO: HTML-based checks (sync)
    if check_geo:
        all_results.append(check_structured_data(main_page.html))
        all_results.append(check_faq_content(main_page.html))
        all_results.append(check_eeat_signals(main_page.html, url))
        all_results.append(check_content_clarity(main_page.html))

    # Score
    score_data = calculate_score(all_results)

    scan_result = {
        "url": url,
        "pages_crawled": len(pages),
        **score_data,
    }

    if hospital_id:
        from .monitoring import record_score_history

        await record_score_history(
            hospital_id=hospital_id,
            audit_id=None,
            total_score=score_data.get("total_score", 0),
            grade=score_data.get("grade", "F"),
            category_scores=score_data.get("category_scores", {}),
        )

    return scan_result
