"""
CLI entry point for Naver Hospital Crawler.

Usage:
    python -m crawl.naver_hospital hospitals.csv
    python -m crawl.naver_hospital hospitals.csv --max-places 10
    python -m crawl.naver_hospital hospitals.csv --delay-multiplier 2.0
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import signal
import sys
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

from crawl.config import CrawlerConfig
from crawl.naver_hospital.orchestrator import HospitalCrawlOrchestrator

console = Console()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Naver Map Hospital Crawler with anti-detection",
    )
    parser.add_argument(
        "csv_file",
        help="CSV file with hospital names (first column)",
    )
    parser.add_argument(
        "--max-places",
        type=int,
        default=None,
        help="Maximum number of hospitals to crawl",
    )
    parser.add_argument(
        "--delay-multiplier",
        type=float,
        default=1.0,
        help="Multiply all delays (>1 = slower but safer, minimum 0.1)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="crawl/output",
        help="Output directory for JSON files and database",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Run in headless mode (NOT recommended, risk of IP ban)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        default=False,
        help="Enable verbose logging",
    )
    return parser.parse_args()


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


async def run_crawl(args: argparse.Namespace) -> int:
    """Async crawl entry point."""
    config = CrawlerConfig(
        max_places=args.max_places,
        delay_multiplier=args.delay_multiplier,
    )

    if args.output_dir != "crawl/output":
        config.storage.output_dir = Path(args.output_dir)
        config.storage.db_path = Path(args.output_dir) / "naver_places.db"

    if args.headless:
        console.print(
            "[yellow]WARNING: Headless mode may trigger Naver IP bans.[/yellow]"
        )
        config.browser.headless = True

    console.print("[bold]Naver Hospital Crawler[/bold]")
    console.print(f"  CSV: {args.csv_file}")
    console.print(f"  Output: {config.storage.output_dir}")
    console.print(f"  Delay: {config.delay_multiplier}x")
    if config.max_places:
        console.print(f"  Max places: {config.max_places}")
    console.print()

    orchestrator = HospitalCrawlOrchestrator(config)

    # Register signal handler for graceful shutdown
    def handle_signal(sig, frame):
        console.print(
            f"\n[yellow]Received signal, finishing current hospital...[/yellow]"
        )
        orchestrator.request_shutdown()

    signal.signal(signal.SIGTERM, handle_signal)

    summary = await orchestrator.run(str(args.csv_file))

    if "error" in summary:
        return 1
    return 0 if summary.get("failed", 0) == 0 else 1


def main() -> int:
    """Synchronous CLI entry point."""
    args = parse_args()
    setup_logging(args.verbose)

    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        console.print(f"[red]CSV file not found: {csv_path}[/red]")
        return 1

    if args.delay_multiplier < 0.1:
        console.print("[red]--delay-multiplier must be >= 0.1[/red]")
        return 1

    try:
        return asyncio.run(run_crawl(args))
    except KeyboardInterrupt:
        console.print("\n[yellow]Crawl interrupted by user.[/yellow]")
        return 130


if __name__ == "__main__":
    sys.exit(main())
