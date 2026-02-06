"""Fast HTTP-based prescan for social links and doctor page URLs using regex."""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from rich.console import Console
from rich.progress import Progress

from clinic_crawl.config import ClinicCrawlConfig
from clinic_crawl.models.enums import (
    CrawlPhase,
    ExtractionMethod,
    SocialPlatform,
)
from clinic_crawl.net import MAX_HTML_SIZE, safe_get, validate_url
from clinic_crawl.patterns import SOCIAL_SCAN_PATTERNS
from clinic_crawl.storage import ClinicStorageManager

logger = logging.getLogger(__name__)
console = Console()

# Doctor page URL patterns in href attributes
DOCTOR_PAGE_PATTERNS = [
    r'href=["\']([^"\']*(?:doctor|의료진|원장|전문의|staff|team|about)[^"\']*)["\']',
]

COMPILED_SOCIAL = SOCIAL_SCAN_PATTERNS
COMPILED_DOCTOR = [re.compile(p, re.IGNORECASE) for p in DOCTOR_PAGE_PATTERNS]


@dataclass
class PrescanResult:
    """Result from prescanning a single URL."""

    hospital_no: int
    url: str
    status_code: int | None = None
    social_links: list[tuple[SocialPlatform, str]] = field(default_factory=list)
    doctor_page_urls: list[str] = field(default_factory=list)
    error: str | None = None
    server_header: str | None = None
    platform_hint: str | None = None


def extract_social_from_html(html: str) -> list[tuple[SocialPlatform, str]]:
    """Extract social links from HTML content using regex."""
    found: list[tuple[SocialPlatform, str]] = []
    seen_urls: set[str] = set()

    for pattern, platform in COMPILED_SOCIAL:
        for match in pattern.finditer(html):
            url = match.group(0).rstrip("\"'<>);,.")
            if url not in seen_urls:
                seen_urls.add(url)
                found.append((platform, url))

    return found


def extract_doctor_pages_from_html(html: str) -> list[str]:
    """Extract potential doctor page URLs from HTML."""
    found: list[str] = []
    seen: set[str] = set()

    for pattern in COMPILED_DOCTOR:
        for match in pattern.finditer(html):
            href = match.group(1)
            if href and href not in seen and not href.startswith("#"):
                seen.add(href)
                found.append(href)

    return found


def detect_platform(html: str, server: str | None) -> str | None:
    """Detect the website platform from HTML or server header."""
    html_lower = html[:5000].lower()

    if "imweb" in html_lower or (server and "imweb" in server.lower()):
        return "imweb"
    if "mobidoc" in html_lower:
        return "mobidoc"
    if "modoo" in html_lower:
        return "modoo"
    if "wordpress" in html_lower or "wp-content" in html_lower:
        return "wordpress"
    if "_next" in html_lower or "__next" in html_lower:
        return "nextjs"
    if "wixsite" in html_lower:
        return "wix"

    return None


async def prescan_url(
    client: httpx.AsyncClient,
    hospital_no: int,
    url: str,
    timeout: float = 10.0,
) -> PrescanResult:
    """Prescan a single URL for social links and doctor pages."""
    result = PrescanResult(hospital_no=hospital_no, url=url)

    # SSRF check before making the request
    url_error = await validate_url(url)
    if url_error:
        result.error = url_error
        return result

    try:
        response = await safe_get(
            client,
            url,
            timeout=timeout,
            max_size=MAX_HTML_SIZE,
        )
        result.status_code = response.status_code
        result.server_header = response.headers.get("server")

        if response.status_code == 200:
            html = response.text
            result.social_links = extract_social_from_html(html)
            result.doctor_page_urls = extract_doctor_pages_from_html(html)
            result.platform_hint = detect_platform(html, result.server_header)

    except httpx.ConnectError:
        result.error = "connection_refused"
    except httpx.TimeoutException:
        result.error = "timeout"
    except ValueError as e:
        result.error = str(e)
    except httpx.HTTPError as e:
        result.error = f"{type(e).__name__}: {e}"

    return result


async def run_prescan(
    config: ClinicCrawlConfig,
    urls: list[tuple[int, str]],  # (hospital_no, url)
) -> list[PrescanResult]:
    """Prescan all URLs concurrently."""
    semaphore = asyncio.Semaphore(config.prescan.max_concurrent)
    results: list[PrescanResult] = []

    async with httpx.AsyncClient(
        headers={"User-Agent": config.prescan.user_agent},
    ) as client:
        with Progress() as progress:
            task = progress.add_task("Prescanning...", total=len(urls))

            async def scan_one(hospital_no: int, url: str) -> PrescanResult:
                async with semaphore:
                    result = await prescan_url(
                        client, hospital_no, url, config.prescan.timeout_seconds
                    )
                    progress.advance(task)
                    return result

            results = await asyncio.gather(*[scan_one(h_no, url) for h_no, url in urls])

    return list(results)


async def save_prescan_results(
    storage: ClinicStorageManager,
    results: list[PrescanResult],
) -> tuple[int, int]:
    """Save prescan results to storage. Returns (social_count, error_count)."""
    social_count = 0
    error_count = 0

    for result in results:
        if result.error:
            await storage.update_phase(
                result.hospital_no,
                CrawlPhase.FAILED,
                error_message=result.error,
            )
            error_count += 1
            continue

        # Save social links found
        for platform, url in result.social_links:
            await storage.save_social_link(
                hospital_no=result.hospital_no,
                platform=platform.value,
                url=url,
                extraction_method=ExtractionMethod.PRESCAN_REGEX,
                confidence=0.8,  # Regex matches are high but not perfect confidence
            )
            social_count += 1

        await storage.update_phase(result.hospital_no, CrawlPhase.PRESCAN_DONE)

    return social_count, error_count


async def main() -> None:
    config = ClinicCrawlConfig()

    async with ClinicStorageManager(config) as storage:
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.RESOLVE_DONE)

        if not hospitals:
            console.print("[yellow]No hospitals in resolve_done phase. Run resolve first.[/yellow]")
            return

        from clinic_crawl.scripts.clean_csv import build_url_map, load_csv

        rows = load_csv(Path(config.csv_path))
        url_map = build_url_map(rows)

        urls = [
            (h["hospital_no"], url_map[h["hospital_no"]])
            for h in hospitals
            if h["hospital_no"] in url_map
        ]

        console.print(f"Prescanning {len(urls)} URLs...")
        results = await run_prescan(config, urls)

        social_count, error_count = await save_prescan_results(storage, results)

        # Summary
        with_social = sum(1 for r in results if r.social_links)
        with_doctor = sum(1 for r in results if r.doctor_page_urls)

        console.print("\n[green]Prescan complete:[/green]")
        console.print(f"  Total scanned: {len(results)}")
        console.print(f"  With social links: {with_social}")
        console.print(f"  Social links found: {social_count}")
        console.print(f"  With doctor pages: {with_doctor}")
        console.print(f"  Errors: {error_count}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
