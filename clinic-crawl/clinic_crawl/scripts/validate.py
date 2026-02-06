"""Validation and deduplication of crawl results."""

from __future__ import annotations

import asyncio
import logging

import httpx
from rich.console import Console

from clinic_crawl.config import ClinicCrawlConfig
from clinic_crawl.models.enums import CrawlPhase
from clinic_crawl.net import validate_url
from clinic_crawl.storage import ClinicStorageManager

logger = logging.getLogger(__name__)
console = Console()


async def verify_social_link(
    client: httpx.AsyncClient,
    url: str,
    timeout: float = 5.0,
) -> bool:
    """Check if a social link is reachable (HEAD request)."""
    url_error = await validate_url(url)
    if url_error:
        return False
    try:
        response = await client.head(url, follow_redirects=True, timeout=timeout)
        return response.status_code < 400
    except httpx.HTTPError:
        return False


async def validate_results(
    config: ClinicCrawlConfig,
    verify_links: bool = False,
) -> None:
    """Validate all crawl results and mark as validated.

    Args:
        config: Pipeline configuration.
        verify_links: If True, perform HEAD requests to verify social links.
    """
    async with ClinicStorageManager(config) as storage:
        hospitals = await storage.get_hospitals_by_phase(CrawlPhase.DEEP_CRAWL_DONE)
        prescan_done = await storage.get_hospitals_by_phase(CrawlPhase.PRESCAN_DONE)
        all_hospitals = hospitals + prescan_done

        if not all_hospitals:
            console.print("[yellow]No hospitals to validate[/yellow]")
            return

        console.print(f"Validating {len(all_hospitals)} hospitals...")

        verified = 0
        no_links = 0
        link_failures = 0

        client = None
        if verify_links:
            client = httpx.AsyncClient(headers={"User-Agent": config.prescan.user_agent})

        try:
            for hospital in all_hospitals:
                hospital_no = hospital["hospital_no"]
                social_links = await storage.get_social_links(hospital_no)

                if not social_links:
                    await storage.update_phase(hospital_no, CrawlPhase.VALIDATED)
                    no_links += 1
                    continue

                if verify_links and client:
                    reachable = await asyncio.gather(
                        *[verify_social_link(client, link["url"]) for link in social_links]
                    )
                    if not any(reachable):
                        await storage.update_phase(
                            hospital_no,
                            CrawlPhase.FAILED,
                            error_message="all_social_links_unreachable",
                        )
                        link_failures += 1
                        continue

                await storage.update_phase(hospital_no, CrawlPhase.VALIDATED)
                verified += 1
        finally:
            if client:
                await client.aclose()

        console.print("\n[green]Validation complete:[/green]")
        console.print(f"  Verified with links: {verified}")
        console.print(f"  No social links: {no_links}")
        if verify_links:
            console.print(f"  Link verification failures: {link_failures}")

        counts = await storage.get_phase_counts()
        console.print("\n[cyan]Phase Summary:[/cyan]")
        for phase, count in sorted(counts.items()):
            console.print(f"  {phase}: {count}")


async def main() -> None:
    config = ClinicCrawlConfig()
    await validate_results(config)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
