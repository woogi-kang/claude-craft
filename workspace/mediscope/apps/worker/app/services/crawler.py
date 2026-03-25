"""HTTP crawler with SSRF protection."""

from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from ..config import settings
from ..security.ssrf import SSRFError, validate_url


class CrawlResult:
    def __init__(self, url: str, html: str, status_code: int):
        self.url = url
        self.html = html
        self.status_code = status_code


class Crawler:
    def __init__(
        self,
        *,
        max_pages: int | None = None,
        max_depth: int | None = None,
        timeout: int | None = None,
    ):
        self.max_pages = max_pages or settings.crawler_max_pages
        self.max_depth = max_depth or settings.crawler_max_depth
        self.timeout = timeout or settings.crawler_timeout

    async def crawl(self, start_url: str) -> list[CrawlResult]:
        validate_url(start_url)

        results: list[CrawlResult] = []
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(start_url, 0)]
        base_domain = urlparse(start_url).netloc

        async with httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            headers={"User-Agent": "MediScope-Bot/1.0"},
        ) as client:
            while queue and len(results) < self.max_pages:
                url, depth = queue.pop(0)

                if url in visited:
                    continue
                visited.add(url)

                try:
                    validate_url(url)
                except SSRFError:
                    continue

                try:
                    resp = await client.get(url)
                except httpx.HTTPError:
                    continue

                content_type = resp.headers.get("content-type", "")
                if "text/html" not in content_type:
                    continue

                result = CrawlResult(url=url, html=resp.text, status_code=resp.status_code)
                results.append(result)

                # Extract links for next depth
                if depth < self.max_depth:
                    soup = BeautifulSoup(resp.text, "lxml")
                    for a in soup.find_all("a", href=True):
                        href = str(a["href"])
                        full = urljoin(url, href)
                        parsed = urlparse(full)
                        # Only follow same-domain, http(s) links
                        if (
                            parsed.netloc == base_domain
                            and parsed.scheme in ("http", "https")
                            and full not in visited
                        ):
                            # Strip fragments
                            clean = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                            if parsed.query:
                                clean += f"?{parsed.query}"
                            queue.append((clean, depth + 1))

        return results

    async def fetch_single(self, url: str) -> CrawlResult:
        validate_url(url)
        async with httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            headers={"User-Agent": "MediScope-Bot/1.0"},
        ) as client:
            resp = await client.get(url)
            return CrawlResult(url=url, html=resp.text, status_code=resp.status_code)
