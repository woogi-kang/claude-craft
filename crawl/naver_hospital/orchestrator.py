"""
Hospital crawl orchestrator: coordinates the full pipeline.

Reads hospital names from CSV, runs search -> home -> info -> photos
pipeline for each, with retry logic and progress tracking.
"""

from __future__ import annotations

import asyncio
import csv
import logging
import time
from pathlib import Path

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table

from crawl.config import CrawlerConfig
from crawl.hospital_schema import NaverHospitalPlace
from crawl.naver_hospital.browser import BrowserController
from crawl.naver_hospital.downloader import PhotoDownloader
from crawl.naver_hospital.human_behavior import (
    RequestThrottler,
    between_places_delay,
)
from crawl.naver_hospital.scrapers.detection import BanDetectedError
from crawl.naver_hospital.scrapers.home import scrape_home
from crawl.naver_hospital.scrapers.information import scrape_information
from crawl.naver_hospital.scrapers.photos import scrape_photos
from crawl.naver_hospital.scrapers.search import search_place
from crawl.naver_hospital.storage import StorageManager

logger = logging.getLogger(__name__)
console = Console()


class HospitalCrawlOrchestrator:
    """Orchestrates the full hospital crawling pipeline."""

    def __init__(self, config: CrawlerConfig) -> None:
        self._config = config
        self._storage = StorageManager(config)
        self._throttler = RequestThrottler(
            min_interval=config.delays.rate_limit_seconds,
            multiplier=config.delay_multiplier,
        )
        self._shutdown_requested = False

    def request_shutdown(self) -> None:
        """Signal the orchestrator to stop after the current hospital."""
        self._shutdown_requested = True

    async def run(self, csv_path: str) -> dict:
        """Run the full crawl pipeline from CSV input.

        Args:
            csv_path: Path to CSV file with hospital names.

        Returns:
            Summary dict with crawl statistics.
        """
        # Load hospital names
        names = self._load_csv(csv_path)
        if not names:
            console.print("[red]No hospital names found in CSV.[/red]")
            return {"error": "No hospital names found"}

        console.print(f"Loaded [bold]{len(names)}[/bold] hospitals from CSV")

        # Initialize storage with try/finally for guaranteed cleanup
        try:
            await self._storage.initialize()
            await self._storage.recover_interrupted()

            new_count = await self._storage.register_hospitals(names)
            console.print(
                f"Registered: [green]{new_count}[/green] new, "
                f"[yellow]{len(names) - new_count}[/yellow] already tracked"
            )

            # Get pending hospitals (supports resume)
            pending = await self._storage.get_pending_hospitals()
            if not pending:
                console.print("[green]All hospitals already crawled![/green]")
                return await self._storage.get_summary()

            # Apply max_places limit
            if self._config.max_places:
                pending = pending[: self._config.max_places]

            console.print(f"Crawling [bold]{len(pending)}[/bold] hospitals...")

            # Launch browser and crawl
            async with BrowserController(self._config) as browser:
                page = await browser.new_page()
                downloader = PhotoDownloader(
                    self._config,
                    cookies=await browser.get_cookies_for_httpx(),
                )

                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    TextColumn("({task.completed}/{task.total})"),
                    console=console,
                ) as progress:
                    task = progress.add_task("Crawling", total=len(pending))

                    for idx, name in enumerate(pending):
                        if self._shutdown_requested:
                            console.print(
                                "[yellow]Shutdown requested, stopping.[/yellow]"
                            )
                            break

                        progress.update(task, description=f"[cyan]{name}[/cyan]")

                        page = await self._ensure_healthy_page(browser, page)
                        await self._crawl_single(
                            page, browser, downloader, name
                        )

                        progress.advance(task)

                        if idx < len(pending) - 1:
                            await between_places_delay(
                                self._config.delays, self._config.delay_multiplier
                            )

            # Print summary
            summary = await self._storage.get_summary()
            self._print_summary(summary)
            return summary

        finally:
            await self._storage.close()

    async def _ensure_healthy_page(
        self, browser: BrowserController, page
    ):
        """Recreate page if it has become unresponsive."""
        try:
            await page.evaluate("() => document.readyState")
            return page
        except Exception:
            logger.warning("Page unresponsive, creating new page")
            try:
                await page.close()
            except Exception:
                pass
            return await browser.new_page()

    async def _crawl_single(
        self,
        page,
        browser: BrowserController,
        downloader: PhotoDownloader,
        hospital_name: str,
    ) -> bool:
        """Crawl a single hospital through the full pipeline."""
        await self._storage.mark_in_progress(hospital_name)

        for attempt in range(self._config.retry.max_retries):
            try:
                return await self._crawl_pipeline(
                    page, browser, downloader, hospital_name
                )
            except BanDetectedError as e:
                logger.error("Ban detected for '%s': %s", hospital_name, e)
                await self._storage.mark_failed(hospital_name, f"Ban: {e}")
                # Longer cooldown on ban
                import random

                cooldown = random.uniform(
                    self._config.retry.cooldown_on_ban_min,
                    self._config.retry.cooldown_on_ban_max,
                )
                logger.warning("Cooling down for %.0fs after ban", cooldown)
                await asyncio.sleep(cooldown)
                return False
            except Exception as e:
                logger.warning(
                    "Attempt %d/%d failed for '%s': %s",
                    attempt + 1,
                    self._config.retry.max_retries,
                    hospital_name,
                    e,
                )
                if attempt < self._config.retry.max_retries - 1:
                    delay = min(
                        self._config.retry.base_delay * (2 ** attempt),
                        self._config.retry.max_delay,
                    )
                    await asyncio.sleep(delay)

        await self._storage.mark_failed(hospital_name, "Max retries exceeded")
        return False

    async def _crawl_pipeline(
        self,
        page,
        browser: BrowserController,
        downloader: PhotoDownloader,
        hospital_name: str,
    ) -> bool:
        """Execute search -> home -> info -> photos pipeline."""
        start = time.monotonic()

        # Step 1: Search for place ID
        await self._throttler.wait()
        place_id = await search_place(page, hospital_name, self._config)
        if not place_id:
            await self._storage.mark_failed(hospital_name, "Place not found")
            return False

        # Check if already crawled by place_id
        if await self._storage.is_place_crawled(place_id):
            logger.info("Place %s already crawled, skipping", place_id)
            await self._storage.mark_completed_duplicate(hospital_name, place_id)
            return True

        # Step 2: Scrape home page
        await self._throttler.wait()
        home_data = await scrape_home(page, place_id, self._config)

        # Validate essential data before proceeding
        if not home_data.get("name"):
            logger.warning("Home scraping returned no name for %s", place_id)
            await self._storage.mark_failed(
                hospital_name, "Home page scraping failed: no name"
            )
            return False

        # Step 3: Scrape information page
        await self._throttler.wait()
        info_data = await scrape_information(page, place_id, self._config)

        # Step 4: Scrape photos
        await self._throttler.wait()
        photo_urls = await scrape_photos(page, place_id, self._config)

        # Step 5: Download photos
        local_paths: list[str] = []
        if photo_urls:
            downloader.update_cookies(await browser.get_cookies_for_httpx())
            local_paths = await downloader.download_all(place_id, photo_urls)

        # Step 6: Build and save hospital model
        elapsed_ms = int((time.monotonic() - start) * 1000)

        hospital = self._build_hospital(
            place_id=place_id,
            home_data=home_data,
            info_data=info_data,
            photo_urls=photo_urls,
            local_paths=local_paths,
            search_name=hospital_name,
            elapsed_ms=elapsed_ms,
        )

        json_path = await self._storage.save_hospital(hospital, hospital_name)
        logger.info(
            "Saved %s -> %s (photos: %d, time: %dms)",
            hospital_name,
            json_path,
            hospital.photo_count,
            elapsed_ms,
        )

        try:
            await browser.take_screenshot(page, f"done_{place_id}")
        except Exception:
            pass

        return True

    def _build_hospital(
        self,
        place_id: str,
        home_data: dict,
        info_data: dict,
        photo_urls: list[str],
        local_paths: list[str],
        search_name: str,
        elapsed_ms: int,
    ) -> NaverHospitalPlace:
        """Merge scraped data into a NaverHospitalPlace model."""
        from crawl.base import CrawlMetadata, CrawlSource
        from crawl.naver_map_schema import NaverPlaceParser

        business_hours = NaverPlaceParser.parse_business_hours(
            home_data.get("business_hours", [])
        )

        return NaverHospitalPlace(
            id=place_id,
            name=home_data.get("name") or search_name,
            category=home_data.get("category") or "병원",
            road_address=home_data.get("road_address"),
            phone=home_data.get("phone"),
            description=info_data.get("description"),
            homepage_url=info_data.get("homepage_url"),
            image_urls=photo_urls,
            facilities=home_data.get("facilities", []),
            business_hours=business_hours,
            youtube_url=info_data.get("youtube_url"),
            instagram_url=info_data.get("instagram_url"),
            reservation_url=info_data.get("reservation_url"),
            parking_info=info_data.get("parking_info"),
            local_photo_paths=local_paths,
            photo_count=len(local_paths),
            crawl=CrawlMetadata(
                source=CrawlSource.NAVER,
                search_query=search_name,
                source_url=f"https://m.place.naver.com/hospital/{place_id}/home",
                crawl_duration_ms=elapsed_ms,
            ),
        )

    def _load_csv(self, csv_path: str) -> list[str]:
        """Load hospital names from CSV file."""
        path = Path(csv_path)
        if not path.exists():
            logger.error("CSV file not found: %s", csv_path)
            return []

        names: list[str] = []
        with open(path, encoding="utf-8-sig") as f:
            reader = csv.reader(f)

            first_row = next(reader, None)
            if not first_row:
                return []

            if first_row[0].strip().lower() in (
                "name", "hospital", "병원명", "이름", "상호명",
            ):
                pass
            else:
                name = first_row[0].strip()
                if name:
                    names.append(name)

            for row in reader:
                if row:
                    name = row[0].strip()
                    if name:
                        names.append(name)

        # Remove duplicates while preserving order
        seen: set[str] = set()
        unique: list[str] = []
        for name in names:
            if name not in seen:
                seen.add(name)
                unique.append(name)

        return unique

    def _print_summary(self, summary: dict) -> None:
        """Print crawl results summary."""
        table = Table(title="Crawl Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")

        table.add_row("Total Hospitals", str(summary.get("total", 0)))
        table.add_row("Completed", str(summary.get("completed", 0)))
        table.add_row("Failed", str(summary.get("failed", 0)))
        table.add_row("Pending", str(summary.get("pending", 0)))
        table.add_row("Total Photos", str(summary.get("total_photos", 0)))

        console.print(table)
