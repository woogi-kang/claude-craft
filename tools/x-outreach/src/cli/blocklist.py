"""User blocklist management via the ``config`` table.

Blocked users are stored as a JSON array under the ``blocked_users``
key in the database config table.  The :class:`BlocklistManager`
provides a simple interface for add/remove/query operations, and the
module-level functions implement the CLI subcommand handlers.
"""

from __future__ import annotations

import json

from outreach_shared.utils.logger import get_logger

from src.db.repository import Repository

logger = get_logger("blocklist")

# Config table key for the blocked users list
_CONFIG_KEY_BLOCKED = "blocked_users"


class BlocklistManager:
    """Manage a blocklist of usernames stored in the config table.

    Parameters
    ----------
    repository:
        Database repository with an initialised schema.
    """

    def __init__(self, repository: Repository) -> None:
        self._repo = repository

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load(self) -> list[str]:
        """Load the current blocklist from the config table."""
        raw = self._repo.get_config(_CONFIG_KEY_BLOCKED)
        if raw is None:
            return []
        try:
            data = json.loads(raw)
            if isinstance(data, list):
                return [str(u) for u in data]
        except (json.JSONDecodeError, TypeError):
            pass
        return []

    def _save(self, usernames: list[str]) -> None:
        """Persist the blocklist to the config table."""
        self._repo.set_config(_CONFIG_KEY_BLOCKED, json.dumps(usernames))

    @staticmethod
    def _normalise(username: str) -> str:
        """Strip a leading ``@`` and lowercase the username."""
        return username.lstrip("@").lower()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, username: str) -> bool:
        """Add a username to the blocklist.

        Returns ``True`` if the user was added, ``False`` if already
        blocked.
        """
        normalised = self._normalise(username)
        current = self._load()
        if normalised in current:
            return False
        current.append(normalised)
        self._save(current)
        logger.info("blocklist_add", username=normalised)
        return True

    def remove(self, username: str) -> bool:
        """Remove a username from the blocklist.

        Returns ``True`` if the user was removed, ``False`` if not
        found.
        """
        normalised = self._normalise(username)
        current = self._load()
        if normalised not in current:
            return False
        current.remove(normalised)
        self._save(current)
        logger.info("blocklist_remove", username=normalised)
        return True

    def is_blocked(self, username: str) -> bool:
        """Return ``True`` if the username is on the blocklist."""
        normalised = self._normalise(username)
        return normalised in self._load()

    def list_all(self) -> list[str]:
        """Return all blocked usernames."""
        return self._load()


# ---------------------------------------------------------------------------
# CLI handlers
# ---------------------------------------------------------------------------

_DEFAULT_DB_URL = "postgresql://localhost:5432/outreach"


def run_blocklist_add(username: str, db_url: str = _DEFAULT_DB_URL) -> str:
    """Add a user to the blocklist and return a status message."""
    repo = Repository(db_url)
    repo.init_db()
    try:
        mgr = BlocklistManager(repo)
        normalised = BlocklistManager._normalise(username)
        if mgr.add(username):
            return f"Added @{normalised} to blocklist."
        return f"@{normalised} is already blocked."
    finally:
        repo.close()


def run_blocklist_remove(username: str, db_url: str = _DEFAULT_DB_URL) -> str:
    """Remove a user from the blocklist and return a status message."""
    repo = Repository(db_url)
    repo.init_db()
    try:
        mgr = BlocklistManager(repo)
        normalised = BlocklistManager._normalise(username)
        if mgr.remove(username):
            return f"Removed @{normalised} from blocklist."
        return f"@{normalised} is not blocked."
    finally:
        repo.close()


def run_blocklist_list(db_url: str = _DEFAULT_DB_URL) -> str:
    """List all blocked users and return formatted output."""
    repo = Repository(db_url)
    repo.init_db()
    try:
        mgr = BlocklistManager(repo)
        blocked = mgr.list_all()
        if not blocked:
            return "Blocklist is empty."
        lines = ["Blocked users:"]
        for username in sorted(blocked):
            lines.append(f"  @{username}")
        lines.append(f"\nTotal: {len(blocked)}")
        return "\n".join(lines)
    finally:
        repo.close()
