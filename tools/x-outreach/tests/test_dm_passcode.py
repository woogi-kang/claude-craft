"""Tests for DM encryption passcode handling.

The passcode page is an inline element (NOT a modal). Detection uses
``data-testid="pin-title"`` and inputs are inside
``data-testid="pin-code-input-container"``.  After all 4 digits are entered
the form auto-submits (no confirm button).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from src.config import Settings
from src.pipeline.dm import (
    DmEncryptionPasscodeError,
    _handle_encryption_passcode,
)
from src.platform.selectors import (
    DM_PASSCODE_TITLE,
    NEW_DM_BUTTON,
)

# =========================================================================
# Fixtures
# =========================================================================


def _make_page(
    *,
    has_passcode_page: bool = False,
    input_count: int = 4,
    passcode_accepted: bool = True,
    new_dm_button_visible: bool = False,
) -> AsyncMock:
    """Create a mock Playwright Page with configurable passcode page state.

    Parameters
    ----------
    has_passcode_page:
        Whether the ``pin-title`` element is detected on initial load.
    input_count:
        Number of numeric input fields returned by ``query_selector_all``.
    passcode_accepted:
        If ``True``, the passcode title disappears after digit entry (success).
        If ``False``, it persists (wrong passcode).
    new_dm_button_visible:
        If ``True``, the ``NewDM_Button`` is found after passcode entry.
    """
    page = AsyncMock()

    # wait_for_selector for DM_PASSCODE_TITLE
    if has_passcode_page:
        title_el = AsyncMock()
        page.wait_for_selector = AsyncMock(return_value=title_el)
    else:
        page.wait_for_selector = AsyncMock(side_effect=TimeoutError("no passcode page"))

    # query_selector_all for passcode digit inputs
    inputs = [AsyncMock() for _ in range(input_count)]
    page.query_selector_all = AsyncMock(return_value=inputs)

    # query_selector for post-entry verification
    def mock_query_selector(selector: str) -> AsyncMock | None:
        if selector == NEW_DM_BUTTON:
            return AsyncMock() if new_dm_button_visible else None
        if selector == DM_PASSCODE_TITLE:
            # After entry: None = accepted, AsyncMock = still showing
            return None if passcode_accepted else AsyncMock()
        return None

    page.query_selector = AsyncMock(side_effect=mock_query_selector)
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
    async def test_passcode_entered_newdm_visible(self) -> None:
        """Passcode accepted: NewDM button appears (fast path)."""
        page = _make_page(
            has_passcode_page=True,
            passcode_accepted=True,
            new_dm_button_visible=True,
        )
        digits = ["1", "2", "3", "4"]

        with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
            result = await _handle_encryption_passcode(page, digits, timeout_ms=100)

        assert result is True
        assert page.keyboard.type.call_count == 4

    @pytest.mark.asyncio
    async def test_passcode_entered_no_newdm_but_accepted(self) -> None:
        """Passcode accepted: NewDM button absent but passcode page gone (fallback)."""
        page = _make_page(
            has_passcode_page=True,
            passcode_accepted=True,
            new_dm_button_visible=False,
        )
        digits = ["0", "8", "2", "6"]

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
    async def test_wrong_passcode_page_persists_raises(self) -> None:
        """Passcode page still visible after entry -> wrong passcode."""
        page = _make_page(
            has_passcode_page=True,
            passcode_accepted=False,
            new_dm_button_visible=False,
        )

        with pytest.raises(DmEncryptionPasscodeError, match="passcode may be incorrect"):
            with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
                await _handle_encryption_passcode(page, ["1", "2", "3", "4"], timeout_ms=100)
