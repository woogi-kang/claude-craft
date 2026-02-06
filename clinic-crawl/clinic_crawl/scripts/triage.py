"""Classify hospital URLs by category and identify chain hospitals."""

from __future__ import annotations

import asyncio
import logging
import re
from collections import Counter
from pathlib import Path

import tldextract
from rich.console import Console
from rich.table import Table

from clinic_crawl.config import ClinicCrawlConfig
from clinic_crawl.models.csv_row import SkinClinicRow
from clinic_crawl.models.enums import CrawlCategory, CrawlPhase
from clinic_crawl.scripts.clean_csv import load_csv
from clinic_crawl.storage import ClinicStorageManager

logger = logging.getLogger(__name__)
console = Console()

# Platform detection patterns
PLATFORM_PATTERNS: list[tuple[str, CrawlCategory]] = [
    (r"blog\.naver\.com", CrawlCategory.BLOG_NAVER),
    (r"pf\.kakao\.com", CrawlCategory.KAKAO_CHANNEL),
    (r"instagram\.com", CrawlCategory.INSTAGRAM),
    (r"youtube\.com|youtu\.be", CrawlCategory.YOUTUBE),
    (r"\.imweb\.me", CrawlCategory.IMWEB),
    (r"mobidoc\.co\.kr", CrawlCategory.MOBIDOC),
    (r"sites\.google\.com", CrawlCategory.GOOGLE_SITES),
]


def classify_url(url: str | None) -> CrawlCategory:
    """Classify a single URL into a crawl category."""
    if not url:
        return CrawlCategory.NO_URL

    for pattern, category in PLATFORM_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return category

    return CrawlCategory.CUSTOM_DOMAIN


def extract_domain(url: str) -> str | None:
    """Extract registered domain from URL using tldextract."""
    try:
        result = tldextract.extract(url)
        if result.domain and result.suffix:
            return f"{result.domain}.{result.suffix}"
    except Exception:
        pass
    return None


def find_chain_hospitals(
    rows: list[SkinClinicRow],
    threshold: int = 3,
) -> dict[str, list[int]]:
    """Find chain hospitals that share the same domain.

    Returns mapping of domain -> list of hospital_no values.
    """
    domain_hospitals: dict[str, list[int]] = {}

    for row in rows:
        for url in row.urls:
            domain = extract_domain(url)
            if domain:
                domain_hospitals.setdefault(domain, []).append(row.no)

    # Filter to chains (threshold+ hospitals on same domain)
    return {
        domain: hospitals
        for domain, hospitals in domain_hospitals.items()
        if len(hospitals) >= threshold
    }


async def run_triage(
    config: ClinicCrawlConfig,
    rows: list[SkinClinicRow],
) -> None:
    """Classify all hospitals and update database."""
    chains = find_chain_hospitals(rows, config.triage.chain_threshold)

    # Build reverse lookup: hospital_no -> chain_domain
    hospital_chain: dict[int, str] = {}
    for domain, hospitals in chains.items():
        for h_no in hospitals:
            hospital_chain[h_no] = domain

    category_counts: Counter[CrawlCategory] = Counter()

    async with ClinicStorageManager(config) as storage:
        for row in rows:
            # Use the best available URL for classification
            best_url = row.urls[0] if row.urls else None
            category = classify_url(best_url)
            chain_domain = hospital_chain.get(row.no)
            category_counts[category] += 1

            await storage.upsert_hospital(
                hospital_no=row.no,
                name=row.name,
                phase=CrawlPhase.TRIAGE_DONE,
                category=category,
                chain_domain=chain_domain,
            )

    # Print results
    table = Table(title="Triage Results")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right", style="green")
    for cat in CrawlCategory:
        count = category_counts.get(cat, 0)
        if count > 0:
            table.add_row(cat.value, str(count))
    console.print(table)

    # Chain summary
    if chains:
        chain_table = Table(title=f"Chain Hospitals ({len(chains)} chains)")
        chain_table.add_column("Domain", style="cyan")
        chain_table.add_column("Branches", justify="right", style="green")
        for domain, hospitals in sorted(chains.items(), key=lambda x: -len(x[1]))[:20]:
            chain_table.add_row(domain, str(len(hospitals)))
        console.print(chain_table)

    total_chain = sum(len(h) for h in chains.values())
    console.print(f"\n[green]Triage complete: {len(rows)} hospitals classified[/green]")
    console.print(f"[green]Chain hospitals: {total_chain} across {len(chains)} domains[/green]")


async def main() -> None:
    config = ClinicCrawlConfig()
    csv_path = Path(config.csv_path)
    rows = load_csv(csv_path)
    await run_triage(config, rows)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
