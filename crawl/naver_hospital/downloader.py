"""
Async photo downloader using httpx with concurrency control.

Downloads photos to local folders organized by place ID,
using browser cookies for authenticated access.
"""

from __future__ import annotations

import asyncio
import logging
import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import httpx

from crawl.config import CrawlerConfig

logger = logging.getLogger(__name__)


class PhotoDownloader:
    """Downloads photos with concurrency limiting and retry."""

    def __init__(
        self,
        config: CrawlerConfig,
        cookies: Optional[dict[str, str]] = None,
    ) -> None:
        self._config = config
        self._photo_config = config.photos
        self._base_dir = config.storage.output_dir / "photos"
        self._semaphore: asyncio.Semaphore | None = None
        self._cookies = cookies or {}

    def _get_semaphore(self) -> asyncio.Semaphore:
        """Lazily create semaphore inside event loop."""
        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(
                self._photo_config.max_concurrent_downloads
            )
        return self._semaphore

    def update_cookies(self, cookies: dict[str, str]) -> None:
        """Update cookies for authenticated downloads."""
        self._cookies = cookies

    async def download_all(
        self,
        place_id: str,
        photo_urls: list[str],
    ) -> list[str]:
        """Download all photos for a place.

        Args:
            place_id: Naver Place ID for folder naming.
            photo_urls: List of photo URLs to download.

        Returns:
            List of local file paths for successfully downloaded photos.
        """
        if not photo_urls:
            return []

        place_dir = self._base_dir / place_id
        place_dir.mkdir(parents=True, exist_ok=True)

        async with httpx.AsyncClient(
            timeout=self._photo_config.download_timeout_seconds,
            cookies=self._cookies,
            headers={
                "User-Agent": self._config.browser.user_agent,
                "Referer": f"https://m.place.naver.com/hospital/{place_id}/photo",
            },
            follow_redirects=True,
        ) as client:
            tasks = []
            for idx, url in enumerate(photo_urls):
                if idx > 0:
                    await asyncio.sleep(0.2)  # Stagger initiation
                tasks.append(
                    asyncio.create_task(
                        self._download_one(client, url, place_dir, idx)
                    )
                )
            results = await asyncio.gather(*tasks, return_exceptions=True)

        paths = []
        for result in results:
            if isinstance(result, str):
                paths.append(result)
            elif isinstance(result, Exception):
                logger.debug("Download failed: %s", result)

        logger.info(
            "Downloaded %d/%d photos for place %s",
            len(paths),
            len(photo_urls),
            place_id,
        )
        return paths

    async def _download_one(
        self,
        client: httpx.AsyncClient,
        url: str,
        place_dir: Path,
        index: int,
    ) -> str:
        """Download a single photo with semaphore limiting and retry."""
        async with self._get_semaphore():
            ext = _guess_extension(url)
            filename = f"{index:04d}{ext}"
            filepath = place_dir / filename
            tmp_path = filepath.with_suffix(".tmp")

            # Skip if already downloaded
            if filepath.exists() and filepath.stat().st_size > 0:
                return str(filepath)

            last_error: Exception | None = None
            for attempt in range(3):
                try:
                    response = await client.get(url)
                    response.raise_for_status()

                    content_type = response.headers.get("content-type", "")
                    if not content_type.startswith("image/"):
                        raise ValueError(f"Not an image: {content_type}")

                    # Atomic write: temp file then rename
                    tmp_path.write_bytes(response.content)
                    tmp_path.rename(filepath)
                    return str(filepath)
                except (httpx.TransportError, httpx.HTTPStatusError, ValueError) as e:
                    last_error = e
                    tmp_path.unlink(missing_ok=True)
                    if attempt < 2:
                        await asyncio.sleep(1 * (2 ** attempt))

            raise last_error  # type: ignore[misc]


def _guess_extension(url: str) -> str:
    """Guess file extension from URL path."""
    path = urlparse(url).path
    match = re.search(r"\.(jpe?g|png|webp|gif|bmp)$", path, re.IGNORECASE)
    if match:
        ext = match.group(1).lower()
        return f".{ext}" if ext != "jpeg" else ".jpg"
    return ".jpg"
