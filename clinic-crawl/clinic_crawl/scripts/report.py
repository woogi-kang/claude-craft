"""Coverage report generation with Rich tables."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

from rich.console import Console
from rich.table import Table

from clinic_crawl.config import ClinicCrawlConfig
from clinic_crawl.storage import ClinicStorageManager

logger = logging.getLogger(__name__)
console = Console()


async def generate_report(config: ClinicCrawlConfig) -> dict:
    """Generate a comprehensive coverage report."""
    report: dict = {}

    async with ClinicStorageManager(config) as storage:
        report["phase_counts"] = await storage.get_phase_counts()
        report["categories"] = await storage.get_category_counts()
        report["social_platforms"] = await storage.get_social_platform_counts()
        report["hospitals_with_social"] = await storage.get_hospitals_with_social_count()

        hospitals_with_doctors, total_doctors = await storage.get_doctor_stats()
        report["hospitals_with_doctors"] = hospitals_with_doctors
        report["total_doctors"] = total_doctors

        report["chain_domains"] = await storage.get_chain_domain_count()
        report["top_chains"] = await storage.get_top_chains()
        report["extraction_methods"] = await storage.get_extraction_method_counts()
        report["total_hospitals"] = await storage.get_total_hospitals()

    return report


def print_report(report: dict) -> None:
    """Print report as Rich tables."""
    total = report.get("total_hospitals", 0)

    # Phase summary
    table = Table(title="Pipeline Phase Summary")
    table.add_column("Phase", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_column("Percentage", justify="right")
    for phase, count in sorted(report.get("phase_counts", {}).items()):
        pct = f"{count / total * 100:.1f}%" if total else "0%"
        table.add_row(phase, str(count), pct)
    console.print(table)

    # Category distribution
    table = Table(title="URL Category Distribution")
    table.add_column("Category", style="cyan")
    table.add_column("Count", justify="right", style="green")
    for cat, count in report.get("categories", {}).items():
        table.add_row(str(cat), str(count))
    console.print(table)

    # Social platforms
    social_total = report.get("hospitals_with_social", 0)
    table = Table(title=f"Social Channels ({social_total} hospitals)")
    table.add_column("Platform", style="cyan")
    table.add_column("Links Found", justify="right", style="green")
    for platform, count in report.get("social_platforms", {}).items():
        table.add_row(platform, str(count))
    console.print(table)

    # Doctor stats
    console.print("\n[cyan]Doctor Information:[/cyan]")
    console.print(f"  Hospitals with doctors: {report.get('hospitals_with_doctors', 0)}")
    console.print(f"  Total doctors found: {report.get('total_doctors', 0)}")

    # Chain stats
    if report.get("top_chains"):
        table = Table(title=f"Top Chain Hospitals ({report.get('chain_domains', 0)} domains)")
        table.add_column("Domain", style="cyan")
        table.add_column("Branches", justify="right", style="green")
        for domain, count in report.get("top_chains", {}).items():
            table.add_row(domain, str(count))
        console.print(table)

    # Extraction methods
    if report.get("extraction_methods"):
        table = Table(title="Extraction Methods")
        table.add_column("Method", style="cyan")
        table.add_column("Count", justify="right", style="green")
        for method, count in report.get("extraction_methods", {}).items():
            table.add_row(method, str(count))
        console.print(table)

    # Coverage summary
    console.print("\n[bold cyan]Coverage Summary:[/bold cyan]")
    console.print(f"  Total hospitals: {total}")
    social_pct = f"{social_total / total * 100:.1f}%" if total else "0%"
    doctor_pct = f"{report.get('hospitals_with_doctors', 0) / total * 100:.1f}%" if total else "0%"
    console.print(f"  Social channel coverage: {social_pct}")
    console.print(f"  Doctor info coverage: {doctor_pct}")


async def main() -> None:
    config = ClinicCrawlConfig()
    report = await generate_report(config)
    print_report(report)

    # Save report as JSON
    report_path = Path("clinic-crawl/data/report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    console.print(f"\n[green]Report saved to {report_path}[/green]")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
