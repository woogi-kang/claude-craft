"""Weekly report generation for the X Outreach pipeline.

Generates a CSV export of daily statistics for the past 7 days and
prints a human-readable summary including totals, averages, and API
budget status.
"""

from __future__ import annotations

import csv
import io
from datetime import datetime, timedelta
from pathlib import Path

from outreach_shared.utils.logger import get_logger
from outreach_shared.utils.rate_limiter import MonthlyBudgetTracker
from outreach_shared.utils.time_utils import now_jst

from src.config import Settings
from src.db.repository import Repository

logger = get_logger("report")

# CSV columns for the weekly report
_CSV_COLUMNS = [
    "date",
    "tweets_searched",
    "tweets_collected",
    "tweets_analyzed",
    "replies_sent",
    "dms_sent",
    "dms_skipped",
    "dm_responses",
    "errors",
    "api_tweets_used",
]


def _date_range_7_days() -> tuple[str, str]:
    """Return the start and end dates for a 7-day report window.

    Uses JST as the canonical timezone, ending on today.

    Returns
    -------
    tuple[str, str]
        ``(start_date, end_date)`` as ``YYYY-MM-DD`` strings.
    """
    today = now_jst().date()
    start = today - timedelta(days=6)
    return start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


def generate_csv(
    rows: list[dict],
    start_date: str,
    end_date: str,
) -> str:
    """Generate a CSV string from daily stats rows.

    Fills in missing dates with zero values so the report always
    contains exactly 7 rows.

    Parameters
    ----------
    rows:
        Daily stats rows from the database.
    start_date:
        Start of the reporting period.
    end_date:
        End of the reporting period.

    Returns
    -------
    str
        CSV-formatted string.
    """
    # Build a lookup by date
    by_date: dict[str, dict] = {}
    for row in rows:
        by_date[row["date"]] = row

    # Generate all dates in the range
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=_CSV_COLUMNS)
    writer.writeheader()

    current = start
    while current <= end:
        date_str = current.strftime("%Y-%m-%d")
        row_data = by_date.get(date_str)

        if row_data:
            csv_row = {col: row_data.get(col, 0) for col in _CSV_COLUMNS}
            csv_row["date"] = date_str
        else:
            csv_row = {col: 0 for col in _CSV_COLUMNS}
            csv_row["date"] = date_str

        writer.writerow(csv_row)
        current += timedelta(days=1)

    return output.getvalue()


def generate_summary(
    rows: list[dict],
    budget_remaining: int,
    budget_limit: int,
) -> str:
    """Generate a human-readable summary of the weekly report.

    Parameters
    ----------
    rows:
        Daily stats rows from the database.
    budget_remaining:
        Remaining monthly API budget.
    budget_limit:
        Total monthly API budget.

    Returns
    -------
    str
        Multi-line formatted summary.
    """
    num_days = max(len(rows), 1)

    # Calculate totals
    totals: dict[str, int] = {}
    for col in _CSV_COLUMNS:
        if col == "date":
            continue
        totals[col] = sum(row.get(col, 0) or 0 for row in rows)

    lines: list[str] = []
    lines.append("=" * 50)
    lines.append("  Weekly Report Summary")
    lines.append("=" * 50)
    lines.append("")

    lines.append("  Totals (last 7 days)")
    lines.append(f"    Searched:     {totals.get('tweets_searched', 0)}")
    lines.append(f"    Collected:    {totals.get('tweets_collected', 0)}")
    lines.append(f"    Analyzed:     {totals.get('tweets_analyzed', 0)}")
    lines.append(f"    Replied:      {totals.get('replies_sent', 0)}")
    lines.append(f"    DMs sent:     {totals.get('dms_sent', 0)}")
    lines.append(f"    DMs skipped:  {totals.get('dms_skipped', 0)}")
    lines.append(f"    DM responses: {totals.get('dm_responses', 0)}")
    lines.append(f"    Errors:       {totals.get('errors', 0)}")
    lines.append(f"    API used:     {totals.get('api_tweets_used', 0)}")
    lines.append("")

    lines.append("  Averages (per day)")
    for col in _CSV_COLUMNS:
        if col == "date":
            continue
        avg = totals.get(col, 0) / num_days
        label = col.replace("_", " ").title()
        lines.append(f"    {label:18s} {avg:.1f}")
    lines.append("")

    budget_pct = (budget_remaining / budget_limit * 100) if budget_limit > 0 else 0
    conservation = " [CONSERVATION]" if budget_pct <= 20 else ""
    lines.append("  API Budget")
    lines.append(
        f"    Remaining: {budget_remaining} / {budget_limit} ({budget_pct:.0f}%){conservation}"
    )
    lines.append("")
    lines.append("=" * 50)

    return "\n".join(lines)


def write_csv_file(csv_content: str, output_dir: Path | None = None) -> Path:
    """Write the CSV report to a file.

    Parameters
    ----------
    csv_content:
        CSV string to write.
    output_dir:
        Directory for report files.  Defaults to
        ``<project_root>/data/reports/``.

    Returns
    -------
    Path
        Path to the written CSV file.
    """
    if output_dir is None:
        output_dir = Path(__file__).resolve().parent.parent.parent / "data" / "reports"

    output_dir.mkdir(parents=True, exist_ok=True)

    today = now_jst().strftime("%Y-%m-%d")
    filename = f"weekly_{today}.csv"
    filepath = output_dir / filename

    filepath.write_text(csv_content, encoding="utf-8")
    logger.info("report_csv_written", path=str(filepath))
    return filepath


def run_report(settings: Settings) -> str:
    """Execute the report command and return formatted output.

    Generates a weekly CSV report, writes it to disk, and returns
    a summary string for terminal display.

    Parameters
    ----------
    settings:
        Application settings for database path.

    Returns
    -------
    str
        Formatted report summary with the CSV file path.
    """
    db_url = settings.database_url or settings.database.url
    repo = Repository(db_url)
    repo.init_db()

    try:
        start_date, end_date = _date_range_7_days()
        rows = repo.get_daily_stats_range(start_date, end_date)

        # Generate CSV
        csv_content = generate_csv(rows, start_date, end_date)
        csv_path = write_csv_file(csv_content)

        # Budget tracking (simplified -- no raw SQL)
        budget = MonthlyBudgetTracker(monthly_limit=1500)

        # Generate summary
        summary = generate_summary(
            rows,
            budget_remaining=budget.remaining,
            budget_limit=budget.monthly_limit,
        )

        output_lines = [
            summary,
            "",
            f"  CSV report: {csv_path}",
            f"  Period: {start_date} to {end_date}",
        ]
        return "\n".join(output_lines)
    finally:
        repo.close()
