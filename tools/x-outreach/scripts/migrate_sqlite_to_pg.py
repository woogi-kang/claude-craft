"""One-time migration script: SQLite -> PostgreSQL.

Reads the existing SQLite database and inserts all data into the new
PostgreSQL schema.  Run once during the transition.

Usage:
    DATABASE_URL=postgresql://user:pass@localhost:5432/outreach \
    uv run python scripts/migrate_sqlite_to_pg.py [--sqlite-path data/outreach.db]
"""

from __future__ import annotations

import argparse
import asyncio
import sqlite3
from pathlib import Path

import asyncpg
from outreach_shared.db.models import ALL_DDL

_DEFAULT_SQLITE = Path(__file__).resolve().parent.parent / "data" / "outreach.db"


async def migrate(sqlite_path: Path, pg_dsn: str) -> None:
    """Migrate data from SQLite to PostgreSQL."""
    if not sqlite_path.exists():
        print(f"SQLite database not found: {sqlite_path}")
        return

    # Connect to both databases
    sqlite_conn = sqlite3.connect(str(sqlite_path))
    sqlite_conn.row_factory = sqlite3.Row
    pg_conn = await asyncpg.connect(pg_dsn)

    try:
        # Create schema
        for ddl in ALL_DDL:
            await pg_conn.execute(ddl)
        print("PostgreSQL schema created.")

        # Migrate tweets -> posts
        cursor = sqlite_conn.execute("SELECT * FROM tweets")
        rows = cursor.fetchall()
        migrated = 0
        for row in rows:
            try:
                await pg_conn.execute(
                    """\
                    INSERT INTO posts (
                        post_id, platform, user_id, username, contents,
                        intent_type, likes_count, comments_count, retweets_count,
                        post_url, author_bio, author_followers,
                        search_keyword, status
                    ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
                    ON CONFLICT (post_id) DO NOTHING
                    """,
                    str(row["tweet_id"]),
                    "x",
                    row["author_username"] or "unknown",
                    row["author_username"],
                    row["content"] or "",
                    row["classification"],
                    row["likes"] or 0,
                    row["replies"] or 0,
                    row["retweets"] or 0,
                    row["tweet_url"],
                    row["author_bio"],
                    row["follower_count"] or 0,
                    row["search_keyword"],
                    _map_status(row["status"]),
                )
                migrated += 1
            except Exception as exc:
                print(f"  Skip tweet {row['tweet_id']}: {exc}")
        print(f"Migrated {migrated}/{len(rows)} tweets -> posts")

        # Migrate actions -> outreach
        cursor = sqlite_conn.execute("SELECT * FROM actions")
        action_rows = cursor.fetchall()
        action_migrated = 0
        for row in action_rows:
            try:
                # Only migrate reply/dm actions
                action_type = row["action_type"]
                if action_type not in ("reply", "dm"):
                    continue
                await pg_conn.execute(
                    """\
                    INSERT INTO outreach (
                        post_id, user_id, platform,
                        outreach_type, message, status
                    ) VALUES ($1,$2,$3,$4,$5,$6)
                    """,
                    str(row["tweet_id"]) if row["tweet_id"] else None,
                    row["username"] or "unknown",
                    "x",
                    action_type,
                    row["status"] or "",
                    "sent" if row["status"] == "success" else "failed",
                )
                action_migrated += 1
            except Exception as exc:
                print(f"  Skip action: {exc}")
        print(f"Migrated {action_migrated}/{len(action_rows)} actions -> outreach")

    finally:
        sqlite_conn.close()
        await pg_conn.close()

    print("Migration complete.")


def _map_status(sqlite_status: str | None) -> str:
    """Map old SQLite status values to new unified statuses."""
    mapping = {
        "collected": "collected",
        "analyzed": "curated",
        "replied": "contacted",
        "dmed": "contacted",
        "skipped": "skipped",
    }
    return mapping.get(sqlite_status or "", "collected")


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate SQLite to PostgreSQL")
    parser.add_argument(
        "--sqlite-path",
        type=Path,
        default=_DEFAULT_SQLITE,
        help="Path to SQLite database",
    )
    parser.add_argument(
        "--database-url",
        type=str,
        default=None,
        help="PostgreSQL DSN (or set DATABASE_URL env var)",
    )
    args = parser.parse_args()

    import os

    dsn = args.database_url or os.environ.get("DATABASE_URL")
    if not dsn:
        print("Error: provide --database-url or set DATABASE_URL env var")
        return

    asyncio.run(migrate(args.sqlite_path, dsn))


if __name__ == "__main__":
    main()
