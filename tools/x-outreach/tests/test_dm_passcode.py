"""Tests for DM encryption passcode handling.

The passcode page is an inline element (NOT a modal). Detection uses
``data-testid="pin-title"`` and inputs are inside
``data-testid="pin-code-input-container"``.  After all 4 digits are entered
the form auto-submits (no confirm button).  Success is verified by waiting
for the passcode title to become hidden via ``wait_for_selector(state="hidden")``.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from src.config import Settings
from src.pipeline.dm import (
    DmEncryptionPasscodeError,
    _handle_encryption_passcode,
)
from src.platform.selectors import DM_PASSCODE_TITLE

# =========================================================================
# Fixtures
# =========================================================================


def _make_page(
    *,
    has_passcode_page: bool = False,
    input_count: int = 4,
    passcode_accepted: bool = True,
) -> AsyncMock:
    """Create a mock Playwright Page with configurable passcode page state.

    Parameters
    ----------
    has_passcode_page:
        Whether the ``pin-title`` element is detected on initial load.
    input_count:
        Number of numeric input fields returned by ``query_selector_all``.
    passcode_accepted:
        If ``True``, ``wait_for_selector(state="hidden")`` succeeds after
        digit entry (title disappears).  If ``False``, it raises
        ``TimeoutError`` (wrong passcode).
    """
    page = AsyncMock()

    # wait_for_selector is called twice:
    #   1) Detection: DM_PASSCODE_TITLE (default state)
    #   2) Verification: DM_PASSCODE_TITLE with state="hidden"
    call_count = {"n": 0}

    def mock_wait_for_selector(selector: str, **kwargs: object) -> AsyncMock:
        call_count["n"] += 1
        state = kwargs.get("state")

        if selector == DM_PASSCODE_TITLE and state is None:
            # Detection call
            if has_passcode_page:
                return AsyncMock()
            raise TimeoutError("no passcode page")

        if selector == DM_PASSCODE_TITLE and state == "hidden":
            # Verification call after digit entry
            if passcode_accepted:
                return AsyncMock()
            raise TimeoutError("passcode title still visible")

        # Default: timeout for unknown selectors
        raise TimeoutError(f"unexpected wait_for_selector: {selector}")

    page.wait_for_selector = AsyncMock(side_effect=mock_wait_for_selector)

    # query_selector_all for passcode digit inputs
    inputs = [AsyncMock() for _ in range(input_count)]
    page.query_selector_all = AsyncMock(return_value=inputs)

    page.keyboard = AsyncMock()

    return page


# =========================================================================
# Settings.dm_passcode_digits
# =========================================================================


class TestDmPasscodeDigits:
    """Test the dm_passcode_digits property on Settings."""

    def test_empty_returns_none(self) -> None:
        s = Settings(x_dm_encryption_passcode="")
        assert s.dm_passcode_digits is None

    def test_valid_four_digits(self) -> None:
        s = Settings(x_dm_encryption_passcode="1234")
        assert s.dm_passcode_digits == ["1", "2", "3", "4"]

    def test_valid_with_whitespace(self) -> None:
        s = Settings(x_dm_encryption_passcode=" 5678 ")
        assert s.dm_passcode_digits == ["5", "6", "7", "8"]

    def test_invalid_non_digit(self) -> None:
        s = Settings(x_dm_encryption_passcode="12ab")
        with pytest.raises(ValueError, match="exactly 4 digits"):
            _ = s.dm_passcode_digits

    def test_invalid_wrong_length(self) -> None:
        s = Settings(x_dm_encryption_passcode="123")
        with pytest.raises(ValueError, match="exactly 4 digits"):
            _ = s.dm_passcode_digits


# =========================================================================
# _handle_encryption_passcode
# =========================================================================


class TestHandleEncryptionPasscode:
    """Test the inline passcode page handler function."""

    @pytest.mark.asyncio
    async def test_no_passcode_page_returns_false(self) -> None:
        """No passcode page detected -> return False."""
        page = _make_page(has_passcode_page=False)
        result = await _handle_encryption_passcode(page, None, timeout_ms=100)
        assert result is False

    @pytest.mark.asyncio
    async def test_no_passcode_configured_raises(self) -> None:
        """Passcode page shown but no passcode configured -> raise."""
        page = _make_page(has_passcode_page=True)

        with pytest.raises(DmEncryptionPasscodeError, match="X_DM_ENCRYPTION_PASSCODE"):
            await _handle_encryption_passcode(page, None, timeout_ms=100)

    @pytest.mark.asyncio
    async def test_passcode_accepted_title_hidden(self) -> None:
        """Passcode entered and title disappears -> success."""
        page = _make_page(has_passcode_page=True, passcode_accepted=True)
        digits = ["1", "2", "3", "4"]

        with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
            result = await _handle_encryption_passcode(page, digits, timeout_ms=100)

        assert result is True
        assert page.keyboard.type.call_count == 4

    @pytest.mark.asyncio
    async def test_insufficient_input_fields_raises(self) -> None:
        """Fewer than 4 input fields found -> raise."""
        page = _make_page(has_passcode_page=True, input_count=2)
        # Override both primary and fallback selectors to return only 2
        page.query_selector_all = AsyncMock(return_value=[AsyncMock(), AsyncMock()])

        with pytest.raises(DmEncryptionPasscodeError, match="Expected 4"):
            with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
                await _handle_encryption_passcode(page, ["1", "2", "3", "4"], timeout_ms=100)

    @pytest.mark.asyncio
    async def test_wrong_passcode_title_persists_raises(self) -> None:
        """Passcode title still visible after entry -> wrong passcode."""
        page = _make_page(has_passcode_page=True, passcode_accepted=False)

        with pytest.raises(DmEncryptionPasscodeError, match="passcode may be incorrect"):
            with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
                await _handle_encryption_passcode(page, ["1", "2", "3", "4"], timeout_ms=100)
