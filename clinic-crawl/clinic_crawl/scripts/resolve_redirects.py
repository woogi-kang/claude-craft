"""Follow redirects for short URLs and detect dead links."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from rich.console import Console
from rich.progress import Progress

from clinic_crawl.config import ClinicCrawlConfig
from clinic_crawl.models.enums import CrawlCategory, CrawlPhase
from clinic_crawl.net import _MAX_REDIRECTS, validate_url
from clinic_crawl.scripts.clean_csv import build_url_map, load_csv
from clinic_crawl.storage import ClinicStorageManager

logger = logging.getLogger(__name__)
console = Console()

# Domains that use short URLs or redirects
SHORT_URL_DOMAINS = {"bit.ly", "goo.gl", "t.co", "han.gl", "vo.la", "me2.do"}


async def resolve_url(
    client: httpx.AsyncClient,
    url: str,
    timeout: float = 10.0,
) -> tuple[str | None, int | None, str | None]:
    """Follow redirects manually with SSRF validation at each hop.

    Returns:
        Tuple of (final_url, status_code, error_message).
        On success: (final_url, status_code, None)
        On failure: (None, None, error_description)
    """
    url_error = await validate_url(url)
    if url_error:
        return None, None, url_error

    try:
        current_url = url
        for _ in range(_MAX_REDIRECTS):
            response = await client.head(
                current_url,
                follow_redirects=False,
                timeout=timeout,
            )
            if not response.is_redirect:
                return str(response.url), response.status_code, None
            location = response.headers.get("location", "")
            if not location:
                return str(response.url), response.status_code, None
            next_url = urljoin(str(response.url), location)
            redirect_error = await validate_url(next_url)
            if redirect_error:
                return None, None, f"redirect_blocked:{redirect_error}"
            current_url = next_url
        return None, None, "too_many_redirects"
    except httpx.ConnectError:
        return None, None, "connection_refused"
    except httpx.TimeoutException:
        return None, None, "timeout"
    except httpx.HTTPError as e:
        return None, None, type(e).__name__


def _needs_redirect_check(url: str) -> bool:
    """Check if a URL likely uses a redirect/short URL domain."""
    try:
        host = urlparse(url).hostname or ""
        return host in SHORT_URL_DOMAINS
    except ValueError:
        return False


async def resolve_batch(
    config: ClinicCrawlConfig,
    max_concurrent: int = 30,
) -> None:
    """Resolve redirects for all triage_done hospitals with URLs."""
    rows = load_csv(Path(config.csv_path))
    url_map = build_url_map(rows)

    async with ClinicStorageManager(config) as storage:
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.TRIAGE_DONE)

        if not hospitals:
            console.print("[yellow]No hospitals in triage_done phase[/yellow]")
            return

        to_resolve = [
            h
            for h in hospitals
            if h.get("category")
            not in (
                CrawlCategory.NO_URL.value,
                CrawlCategory.INVALID_URL.value,
            )
            and h["hospital_no"] in url_map
        ]

        console.print(f"Resolving redirects for {len(to_resolve)} hospitals...")

        semaphore = asyncio.Semaphore(max_concurrent)
        dead_count = 0
        resolved_count = 0

        async with httpx.AsyncClient(
            headers={"User-Agent": config.prescan.user_agent},
        ) as client:
            with Progress() as progress:
                task = progress.add_task("Resolving...", total=len(to_resolve))

                async def resolve_one(hospital: dict) -> None:
                    nonlocal dead_count, resolved_count
                    async with semaphore:
                        hospital_no = hospital["hospital_no"]
                        url = url_map[hospital_no]
                        final_url, status_code, error = await resolve_url(
                            client,
                            url,
                        )

                        if error:
                            if error in ("connection_refused", "timeout"):
                                dead_count += 1
                                await storage.update_phase(
                                    hospital_no,
                                    CrawlPhase.FAILED,
                                    error_message=f"dead_link:{error}",
                                )
                            else:
                                logger.warning(
                                    "Resolve error for %d (%s): %s",
                                    hospital_no,
                                    url,
                                    error,
                                )
                        else:
                            resolved_count += 1
                            await storage.update_phase(hospital_no, CrawlPhase.RESOLVE_DONE)

                        progress.advance(task)

                await asyncio.gather(*[resolve_one(h) for h in to_resolve])

        console.print(f"[green]Resolved: {resolved_count}, Dead: {dead_count}[/green]")


async def main() -> None:
    config = ClinicCrawlConfig()
    await resolve_batch(config)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
