"""Status dashboard for the X Outreach pipeline.

Displays current stats, last run information, and aggregate counts
formatted for terminal output.
"""

from __future__ import annotations

from outreach_shared.utils.time_utils import now_jst

from src.config import Settings
from src.db.repository import Repository
from src.pipeline.halt import HaltManager


def _today_jst() -> str:
    """Return today's date in JST as ``YYYY-MM-DD``."""
    return now_jst().strftime("%Y-%m-%d")


def get_last_run_time(repo: Repository) -> str | None:
    """Return the last run time. Currently returns None (no actions table in PG)."""
    return None


def get_total_counts(repo: Repository) -> dict[str, int]:
    """Return aggregate counts from the posts/outreach tables."""
    stats = repo.get_daily_stats(_today_jst())
    if stats:
        return {
            "tweets_collected": stats.get("tweets_collected", 0),
            "tweets_analyzed": 0,
            "replies_sent": 0,
            "dms_sent": 0,
        }
    return {
        "tweets_collected": 0,
        "tweets_analyzed": 0,
        "replies_sent": 0,
        "dms_sent": 0,
    }


def format_status_output(
    *,
    today_stats: dict[str, int] | None,
    totals: dict[str, int],
    last_run: str | None,
    is_halted: bool,
    halt_info: dict[str, str] | None,
) -> str:
    """Build the formatted status output string.

    Parameters
    ----------
    today_stats:
        Today's stats (may be ``None``).
    totals:
        Aggregate counts across all time.
    last_run:
        ISO timestamp of the last pipeline action.
    is_halted:
        Whether the pipeline is in emergency halt.
    halt_info:
        Halt metadata if halted.

    Returns
    -------
    str
        Multi-line formatted status report.
    """
    lines: list[str] = []
    lines.append("=" * 50)
    lines.append("  X Outreach Pipeline Status")
    lines.append("=" * 50)
    lines.append("")

    # Halt status
    if is_halted:
        lines.append("  !! EMERGENCY HALT ACTIVE !!")
        if halt_info:
            lines.append(f"  Reason:  {halt_info.get('reason', 'unknown')}")
            lines.append(f"  Source:  {halt_info.get('source', 'unknown')}")
            lines.append(f"  Since:   {halt_info.get('timestamp', 'unknown')}")
        lines.append("")

    # Last run
    if last_run:
        lines.append(f"  Last run:  {last_run}")
    else:
        lines.append("  Last run:  (no runs recorded)")
    lines.append("")

    # Today's stats
    lines.append(f"  Today ({_today_jst()})")
    if today_stats:
        lines.append(f"    Searched:   {today_stats.get('tweets_searched', 0)}")
        lines.append(f"    Collected:  {today_stats.get('tweets_collected', 0)}")
        lines.append(f"    Analyzed:   {today_stats.get('tweets_analyzed', 0)}")
        lines.append(f"    Replied:    {today_stats.get('replies_sent', 0)}")
        lines.append(f"    DMs sent:   {today_stats.get('dms_sent', 0)}")
    else:
        lines.append("    (no activity today)")
    lines.append("")

    # All-time totals
    lines.append("  All Time")
    lines.append(f"    Collected:  {totals.get('tweets_collected', 0)}")
    lines.append(f"    Analyzed:   {totals.get('tweets_analyzed', 0)}")
    lines.append(f"    Replied:    {totals.get('replies_sent', 0)}")
    lines.append(f"    DMs sent:   {totals.get('dms_sent', 0)}")
    lines.append("")
    lines.append("=" * 50)

    return "\n".join(lines)


def run_status(settings: Settings) -> str:
    """Execute the status command and return the formatted output.

    Parameters
    ----------
    settings:
        Application settings for database URL and budget config.

    Returns
    -------
    str
        Formatted status report.
    """
    db_url = settings.database_url or settings.database.url
    repo = Repository(db_url)
    repo.init_db()

    try:
        today = _today_jst()
        today_stats = repo.get_daily_stats(today)
        totals = get_total_counts(repo)
        last_run = get_last_run_time(repo)

        halt_mgr = HaltManager()
        is_halted = halt_mgr.is_halted()
        halt_info = halt_mgr.get_halt_info() if is_halted else None

        return format_status_output(
            today_stats=dict(today_stats) if today_stats else None,
            totals=totals,
            last_run=last_run,
            is_halted=is_halted,
            halt_info=halt_info,
        )
    finally:
        repo.close()
