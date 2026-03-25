"""Scanner orchestrator: runs all 15 checks and produces a score."""

import httpx

from ..checks.base import CheckResult
from ..checks.canonical import check_canonical
from ..checks.errors import check_errors
from ..checks.headings import check_headings
from ..checks.https_check import check_https
from ..checks.images import check_images
from ..checks.links import check_links
from ..checks.meta_tags import check_meta_tags
from ..checks.mobile import check_mobile
from ..checks.performance import check_performance
from ..checks.robots import check_robots
from ..checks.sitemap import check_sitemap
from ..checks.url_structure import check_url_structure
from ..config import settings
from .crawler import Crawler
from .scorer import calculate_score


async def run_scan(
    url: str,
    *,
    max_pages: int = 50,
    max_depth: int = 3,
) -> dict:
    """Run full technical SEO scan on a URL. Returns scored results."""
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

    # Sync checks (HTML parsing)
    all_results.append(check_meta_tags(main_page.html, url))
    all_results.append(check_headings(main_page.html))
    all_results.append(check_images(main_page.html))
    all_results.append(check_canonical(main_page.html, url))
    all_results.append(check_url_structure(url, crawled_urls))
    all_results.append(check_mobile(main_page.html))

    # Score
    score_data = calculate_score(all_results)

    return {
        "url": url,
        "pages_crawled": len(pages),
        **score_data,
    }
