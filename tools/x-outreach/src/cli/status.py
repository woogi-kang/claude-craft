"""Status dashboard for the X Outreach pipeline.

Displays current stats, API budget, last run information, and
aggregate counts formatted for terminal output.
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.config import Settings
from src.db.repository import Repository
from src.utils.rate_limiter import MonthlyBudgetTracker
from src.utils.time_utils import now_jst
from src.pipeline.halt import HaltManager


def _today_jst() -> str:
    """Return today's date in JST as ``YYYY-MM-DD``."""
    return now_jst().strftime("%Y-%m-%d")


def get_last_run_time(repo: Repository) -> str | None:
    """Query the most recent action timestamp from the actions table.

    Returns
    -------
    str | None
        ISO timestamp of the last action, or ``None`` if no actions.
    """
    conn = repo._get_conn()
    cursor = conn.execute(
        "SELECT created_at FROM actions ORDER BY id DESC LIMIT 1"
    )
    row = cursor.fetchone()
    if row is None:
        return None
    return row["created_at"]


def get_total_counts(repo: Repository) -> dict[str, int]:
    """Return aggregate counts across all daily_stats rows.

    Returns
    -------
    dict[str, int]
        Keys: tweets_collected, tweets_analyzed, replies_sent, dms_sent.
    """
    conn = repo._get_conn()
    cursor = conn.execute(
        """SELECT
            COALESCE(SUM(tweets_collected), 0) AS tweets_collected,
            COALESCE(SUM(tweets_analyzed), 0) AS tweets_analyzed,
            COALESCE(SUM(replies_sent), 0) AS replies_sent,
            COALESCE(SUM(dms_sent), 0) AS dms_sent
        FROM daily_stats"""
    )
    row = cursor.fetchone()
    return dict(row) if row else {
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
    budget_remaining: int,
    budget_limit: int,
    is_halted: bool,
    halt_info: dict[str, str] | None,
) -> str:
    """Build the formatted status output string.

    Parameters
    ----------
    today_stats:
        Today's daily_stats row (may be ``None``).
    totals:
        Aggregate counts across all time.
    last_run:
        ISO timestamp of the last pipeline action.
    budget_remaining:
        Remaining monthly API tweet budget.
    budget_limit:
        Total monthly API tweet budget.
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

    # API budget
    budget_pct = (budget_remaining / budget_limit * 100) if budget_limit > 0 else 0
    conservation = " [CONSERVATION MODE]" if budget_pct <= 20 else ""
    lines.append("  API Budget (Monthly)")
    lines.append(f"    Remaining: {budget_remaining} / {budget_limit} ({budget_pct:.0f}%){conservation}")
    lines.append("")

    # Today's stats
    lines.append(f"  Today ({_today_jst()})")
    if today_stats:
        lines.append(f"    Searched:   {today_stats.get('tweets_searched', 0)}")
        lines.append(f"    Collected:  {today_stats.get('tweets_collected', 0)}")
        lines.append(f"    Analyzed:   {today_stats.get('tweets_analyzed', 0)}")
        lines.append(f"    Replied:    {today_stats.get('replies_sent', 0)}")
        lines.append(f"    DMs sent:   {today_stats.get('dms_sent', 0)}")
        lines.append(f"    DMs skip:   {today_stats.get('dms_skipped', 0)}")
        lines.append(f"    Errors:     {today_stats.get('errors', 0)}")
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
        Application settings for database path and budget config.

    Returns
    -------
    str
        Formatted status report.
    """
    repo = Repository(settings.database.path)
    repo.init_db()

    try:
        today = _today_jst()
        today_stats = repo.get_daily_stats(today)
        totals = get_total_counts(repo)
        last_run = get_last_run_time(repo)

        # Monthly budget (default 1500 for free tier)
        budget = MonthlyBudgetTracker(monthly_limit=1500)
        # Load used count from daily_stats for current month
        conn = repo._get_conn()
        cursor = conn.execute(
            """SELECT COALESCE(SUM(api_tweets_used), 0) AS total_used
            FROM daily_stats
            WHERE date LIKE ?""",
            (now_jst().strftime("%Y-%m") + "%",),
        )
        row = cursor.fetchone()
        if row and row["total_used"]:
            budget.use(row["total_used"])

        halt_mgr = HaltManager()
        is_halted = halt_mgr.is_halted()
        halt_info = halt_mgr.get_halt_info() if is_halted else None

        output = format_status_output(
            today_stats=dict(today_stats) if today_stats else None,
            totals=totals,
            last_run=last_run,
            budget_remaining=budget.remaining,
            budget_limit=budget.monthly_limit,
            is_halted=is_halted,
            halt_info=halt_info,
        )
        return output
    finally:
        repo.close()
