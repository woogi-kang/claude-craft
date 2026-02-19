"""DM response tracking -- detect whether users replied to our DMs.

After the DM pipeline sends messages, this module periodically checks
each conversation for new incoming messages.  When a response is
detected the user record is updated with ``dm_response_received=1``
and a timestamp, and the daily ``dm_responses`` counter is incremented.

The check is performed via Playwright by navigating to the X messages
interface and inspecting the conversation list for unread indicators.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from src.db.repository import Repository
from src.utils.logger import get_logger

logger = get_logger("dm_track")


@dataclass
class DmTrackResult:
    """Summary of a DM response tracking run."""

    users_checked: int = 0
    responses_detected: int = 0
    errors: int = 0


class DmResponseTracker:
    """Track whether users have responded to our DMs.

    Parameters
    ----------
    repository:
        Database repository for user and stats updates.
    """

    def __init__(self, repository: Repository) -> None:
        self._repo = repository

    def get_pending_users(self) -> list[dict]:
        """Return users who received a DM but have not responded yet.

        Queries the ``users`` table for rows where:
        - ``contact_count > 0`` (we sent them a DM)
        - ``dm_response_received = 0`` (no response recorded yet)

        Returns
        -------
        list[dict]
            User rows eligible for response checking.
        """
        conn = self._repo._get_conn()
        cursor = conn.execute(
            "SELECT * FROM users "
            "WHERE contact_count > 0 AND dm_response_received = 0 "
            "ORDER BY last_contacted ASC",
        )
        return [dict(row) for row in cursor.fetchall()]

    def mark_response(self, username: str) -> bool:
        """Record that a user has responded to our DM.

        Updates the user record and increments the daily
        ``dm_responses`` counter.

        Parameters
        ----------
        username:
            The responding user's username.

        Returns
        -------
        bool
            ``True`` if the user record was updated.
        """
        now_iso = datetime.now(tz=timezone.utc).isoformat()
        updated = self._repo.update_user(
            username,
            dm_response_received=1,
            dm_response_at=now_iso,
        )

        if updated:
            today = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d")
            self._repo.update_daily_stats(today, dm_responses=1)
            logger.info("dm_response_detected", username=username)

        return updated

    async def check_responses_playwright(
        self,
        context: object,
    ) -> DmTrackResult:
        """Check for DM responses using Playwright browser automation.

        Navigates to X's messaging interface and checks each pending
        user's conversation for new incoming messages.

        Parameters
        ----------
        context:
            Authenticated Playwright browser context.

        Returns
        -------
        DmTrackResult
            Summary statistics.
        """
        from playwright.async_api import BrowserContext

        result = DmTrackResult()
        pending = self.get_pending_users()
        if not pending:
            logger.info("dm_track_no_pending")
            return result

        assert isinstance(context, BrowserContext)
        page = context.pages[0] if context.pages else await context.new_page()

        for user in pending:
            username = user["username"]
            result.users_checked += 1

            try:
                has_response = await self._check_single_user(page, username)
                if has_response:
                    self.mark_response(username)
                    result.responses_detected += 1
            except Exception as exc:
                result.errors += 1
                logger.error(
                    "dm_track_error",
                    username=username,
                    error=str(exc),
                )

        logger.info(
            "dm_track_complete",
            checked=result.users_checked,
            responses=result.responses_detected,
            errors=result.errors,
        )
        return result

    @staticmethod
    async def _check_single_user(page: object, username: str) -> bool:
        """Check a single user's DM conversation for responses.

        Parameters
        ----------
        page:
            Playwright page object.
        username:
            Target username to check.

        Returns
        -------
        bool
            ``True`` if a response was detected.
        """
        from playwright.async_api import Page

        assert isinstance(page, Page)

        # Navigate to the direct conversation with the user
        await page.goto(
            f"https://x.com/messages",
            wait_until="domcontentloaded",
            timeout=30_000,
        )

        # Search for the user in conversations
        search_input = await page.query_selector(
            'input[data-testid="searchPeople"], input[placeholder]'
        )
        if search_input:
            await search_input.fill(username)
            await page.wait_for_timeout(2000)

        # Look for conversation with this user
        conversation = await page.query_selector(
            f'[data-testid="conversation"] >> text=@{username}'
        )

        if conversation is None:
            return False

        await conversation.click()
        await page.wait_for_timeout(2000)

        # Check if there are messages from the other user
        # (messages not sent by us -- identified by message alignment/style)
        incoming_messages = await page.query_selector_all(
            '[data-testid="messageEntry"][class*="incoming"], '
            '[data-testid="tweetText"]'
        )

        # Simple heuristic: if there are more messages in the conversation
        # than just ours, the user likely responded.
        return len(incoming_messages) > 0
