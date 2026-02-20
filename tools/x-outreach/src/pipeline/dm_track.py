"""DM response tracking -- detect whether users replied to our DMs.

After the DM pipeline sends messages, this module periodically checks
each conversation for new incoming messages.  When a response is
detected the outreach record is updated with ``replied=True`` and the
daily stats counter is incremented.

The check is performed via Playwright by navigating to the X messages
interface and inspecting the conversation list for unread indicators.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from outreach_shared.utils.logger import get_logger

from src.db.repository import Repository

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

        Queries the outreach table for DMs with status ``sent`` and
        ``replied = FALSE``.

        Returns
        -------
        list[dict]
            User rows eligible for response checking.
        """
        return self._repo.get_dm_pending_users()

    def mark_response(self, username: str) -> bool:
        """Record that a user has responded to our DM.

        Updates the outreach record and increments the daily
        ``dm_responses`` counter.

        Parameters
        ----------
        username:
            The responding user's username.

        Returns
        -------
        bool
            ``True`` if the record was updated.
        """
        now_iso = datetime.now(tz=UTC).isoformat()
        self._repo.mark_dm_replied(username, replied_at=now_iso)

        today = datetime.now(tz=UTC).strftime("%Y-%m-%d")
        self._repo.update_daily_stats(today, dm_responses=1)
        logger.info("dm_response_detected", username=username)
        return True

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

        await page.goto(
            "https://x.com/messages",
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
        incoming_messages = await page.query_selector_all(
            '[data-testid="messageEntry"][class*="incoming"], [data-testid="tweetText"]'
        )

        return len(incoming_messages) > 0
