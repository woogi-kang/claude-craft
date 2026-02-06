"""Load and clean skin_clinics.csv, insert into SQLite."""

from __future__ import annotations

import asyncio
import csv
import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from clinic_crawl.config import ClinicCrawlConfig
from clinic_crawl.models.csv_row import SkinClinicRow
from clinic_crawl.storage import ClinicStorageManager

logger = logging.getLogger(__name__)
console = Console()


def build_url_map(rows: list[SkinClinicRow]) -> dict[int, str]:
    """Build a mapping from hospital_no to first URL for rows that have URLs."""
    url_map: dict[int, str] = {}
    for row in rows:
        if row.urls:
            url_map[row.no] = row.urls[0]
    return url_map


def load_csv(csv_path: Path) -> list[SkinClinicRow]:
    """Load CSV with encoding fallback and validate rows."""
    rows: list[SkinClinicRow] = []
    errors: list[str] = []

    # Try UTF-8 with BOM first, then cp949
    raw_text = None
    for encoding in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            raw_text = csv_path.read_text(encoding=encoding)
            break
        except UnicodeDecodeError:
            continue

    if raw_text is None:
        console.print("[red]Failed to decode CSV with any encoding[/red]")
        sys.exit(1)

    reader = csv.DictReader(raw_text.splitlines())
    for i, raw_row in enumerate(reader, start=2):  # line 2 = first data row
        try:
            row = SkinClinicRow.model_validate(raw_row)
            rows.append(row)
        except Exception as e:
            errors.append(f"Row {i}: {e}")

    if errors:
        console.print(f"[yellow]{len(errors)} rows failed validation:[/yellow]")
        for err in errors[:10]:
            console.print(f"  {err}")
        if len(errors) > 10:
            console.print(f"  ... and {len(errors) - 10} more")

    return rows


async def insert_rows(
    storage: ClinicStorageManager,
    rows: list[SkinClinicRow],
) -> int:
    """Insert all rows into crawl_progress table."""
    count = 0
    for row in rows:
        await storage.upsert_hospital(
            hospital_no=row.no,
            name=row.name,
        )
        count += 1
    return count


async def main() -> None:
    config = ClinicCrawlConfig()
    csv_path = Path(config.csv_path)

    if not csv_path.exists():
        console.print(f"[red]CSV not found: {csv_path}[/red]")
        sys.exit(1)

    console.print(f"Loading CSV: {csv_path}")
    rows = load_csv(csv_path)

    # Summary statistics
    total = len(rows)
    with_homepage = sum(1 for r in rows if r.homepage)
    with_naver_web = sum(1 for r in rows if r.naver_website)
    with_any_url = sum(1 for r in rows if r.urls)
    no_url = total - with_any_url

    table = Table(title="CSV Summary")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_row("Total hospitals", str(total))
    table.add_row("With homepage URL", str(with_homepage))
    table.add_row("With Naver website", str(with_naver_web))
    table.add_row("With any URL", str(with_any_url))
    table.add_row("No URL at all", str(no_url))
    console.print(table)

    # Insert into storage
    async with ClinicStorageManager(config) as storage:
        inserted = await insert_rows(storage, rows)
        console.print(f"[green]Inserted {inserted} hospitals into database[/green]")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
