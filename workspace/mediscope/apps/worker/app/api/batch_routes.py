"""Batch scan routes: lightweight bulk crawling for beauty_clinics."""

import asyncio
import logging
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl

from ..config import settings
from ..db.supabase import get_supabase_client
from ..security.ssrf import SSRFError, validate_url

router = APIRouter()
logger = logging.getLogger("checkyourhospital.batch")

BATCH_CONCURRENCY = 10
SCAN_TIMEOUT = 15


class BatchScanRequest(BaseModel):
    urls: list[HttpUrl]
    update_db: bool = True


class LightScanResult(BaseModel):
    url: str
    has_robots_txt: bool = False
    has_sitemap: bool = False
    has_meta_description: bool = False
    has_meta_og_tags: bool = False
    is_https: bool = False
    has_canonical: bool = False
    score: int = 0
    error: str | None = None


class BatchScanResponse(BaseModel):
    total: int
    scanned: int
    failed: int
    results: list[LightScanResult]


async def _light_scan(client: httpx.AsyncClient, url: str) -> LightScanResult:
    """Lightweight scan: check 5 technical SEO items without Playwright/LLM."""
    result = LightScanResult(url=url)
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    result.is_https = parsed.scheme == "https"

    try:
        # Fetch main page
        resp = await client.get(url, follow_redirects=True, timeout=SCAN_TIMEOUT)
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        # Meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        result.has_meta_description = bool(meta_desc and meta_desc.get("content"))

        # OG tags
        og_title = soup.find("meta", attrs={"property": "og:title"})
        result.has_meta_og_tags = bool(og_title)

        # Canonical
        canonical = soup.find("link", attrs={"rel": "canonical"})
        result.has_canonical = bool(canonical and canonical.get("href"))

    except Exception as e:
        result.error = str(e)[:200]
        result.score = _calc_score(result)
        return result

    # robots.txt
    try:
        robots_resp = await client.get(
            f"{base}/robots.txt", follow_redirects=True, timeout=10
        )
        result.has_robots_txt = (
            robots_resp.status_code == 200
            and "user-agent" in robots_resp.text.lower()
        )
    except Exception:
        pass

    # sitemap.xml
    try:
        sitemap_resp = await client.get(
            f"{base}/sitemap.xml", follow_redirects=True, timeout=10
        )
        result.has_sitemap = (
            sitemap_resp.status_code == 200
            and "<urlset" in sitemap_resp.text.lower()
            or "sitemapindex" in sitemap_resp.text.lower()
        )
    except Exception:
        pass

    result.score = _calc_score(result)
    return result


def _calc_score(result: LightScanResult) -> int:
    """Calculate a 0-100 technical SEO score from 5 binary checks."""
    checks = [
        result.has_robots_txt,
        result.has_sitemap,
        result.has_meta_description,
        result.is_https,
        result.has_canonical,
    ]
    return int(sum(checks) / len(checks) * 100)


@router.post("/batch-scan", response_model=BatchScanResponse)
async def batch_scan(body: BatchScanRequest):
    """Scan multiple URLs with lightweight checks (no LLM, no Playwright)."""
    if len(body.urls) > 500:
        raise HTTPException(status_code=400, detail="Maximum 500 URLs per batch")

    sem = asyncio.Semaphore(BATCH_CONCURRENCY)
    results: list[LightScanResult] = []

    async def scan_with_sem(client: httpx.AsyncClient, url: str):
        async with sem:
            # Skip SSRF-blocked URLs silently
            try:
                validate_url(url)
            except SSRFError:
                return LightScanResult(url=url, error="SSRF blocked")
            return await _light_scan(client, url)

    async with httpx.AsyncClient(
        headers={"User-Agent": "CheckYourHospital-BatchScanner/1.0"},
    ) as client:
        tasks = [scan_with_sem(client, str(u)) for u in body.urls]
        results = await asyncio.gather(*tasks)

    # Update beauty_clinics if requested
    if body.update_db:
        sb = get_supabase_client()
        if sb:
            for r in results:
                if r.error:
                    continue
                # Match by website URL
                domain = urlparse(r.url).netloc
                try:
                    sb.table("beauty_clinics").update({
                        "latest_score": r.score,
                    }).like("website", f"%{domain}%").execute()
                except Exception as e:
                    logger.warning(f"DB update failed for {domain}: {e}")

    failed = sum(1 for r in results if r.error)
    return BatchScanResponse(
        total=len(results),
        scanned=len(results) - failed,
        failed=failed,
        results=results,
    )
