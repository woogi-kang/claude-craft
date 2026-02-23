"""Tests for DM encryption passcode handling."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from src.config import Settings
from src.pipeline.dm import (
    DmEncryptionPasscodeError,
    _handle_encryption_passcode,
)

# =========================================================================
# Fixtures
# =========================================================================


def _make_page(
    *,
    has_dialog: bool = False,
    dialog_text: str = "Enter Passcode recover encryption keys",
    input_count: int = 4,
    has_confirm: bool = True,
    has_dismiss: bool = False,
    dialog_persists: bool = False,
) -> AsyncMock:
    """Create a mock Playwright Page with configurable passcode dialog state."""
    page = AsyncMock()

    # wait_for_selector for the modal dialog
    if has_dialog:
        dialog_el = AsyncMock()
        page.wait_for_selector = AsyncMock(return_value=dialog_el)
    else:
        page.wait_for_selector = AsyncMock(side_effect=TimeoutError("no dialog"))

    # inner_text returns the dialog text
    page.inner_text = AsyncMock(return_value=dialog_text)

    # query_selector_all for passcode inputs
    inputs = [AsyncMock() for _ in range(input_count)]
    page.query_selector_all = AsyncMock(return_value=inputs)

    # query_selector for confirm/dismiss buttons and post-entry check
    def mock_query_selector(selector: str) -> AsyncMock | None:
        from src.platform.selectors import DM_PASSCODE_CONFIRM, DM_PASSCODE_DISMISS

        if selector == DM_PASSCODE_CONFIRM and has_confirm:
            return AsyncMock()
        if selector == DM_PASSCODE_DISMISS and has_dismiss:
            return AsyncMock()
        # After entry: check if dialog persists
        from src.platform.selectors import DM_ENCRYPTION_DIALOG

        if selector == DM_ENCRYPTION_DIALOG:
            if dialog_persists:
                return AsyncMock()
            return None
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
    """Test the passcode dialog handler function."""

    @pytest.mark.asyncio
    async def test_no_dialog_returns_false(self) -> None:
        page = _make_page(has_dialog=False)
        result = await _handle_encryption_passcode(page, None, timeout_ms=100)
        assert result is False

    @pytest.mark.asyncio
    async def test_non_passcode_modal_ignored(self) -> None:
        page = _make_page(has_dialog=True, dialog_text="Cookie consent dialog")
        result = await _handle_encryption_passcode(page, None, timeout_ms=100)
        assert result is False

    @pytest.mark.asyncio
    async def test_passcode_entered_successfully(self) -> None:
        page = _make_page(has_dialog=True, dialog_persists=False)
        digits = ["1", "2", "3", "4"]

        with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
            with patch("src.pipeline.dm.random_mouse_move", new_callable=AsyncMock):
                result = await _handle_encryption_passcode(page, digits, timeout_ms=100)

        assert result is True
        # Verify 4 digits were typed
        assert page.keyboard.type.call_count == 4

    @pytest.mark.asyncio
    async def test_no_passcode_dismiss_available(self) -> None:
        page = _make_page(has_dialog=True, has_dismiss=True)

        with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
            result = await _handle_encryption_passcode(page, None, timeout_ms=100)

        assert result is True

    @pytest.mark.asyncio
    async def test_no_passcode_no_dismiss_raises(self) -> None:
        page = _make_page(has_dialog=True, has_dismiss=False)

        with pytest.raises(DmEncryptionPasscodeError, match="X_DM_ENCRYPTION_PASSCODE"):
            await _handle_encryption_passcode(page, None, timeout_ms=100)

    @pytest.mark.asyncio
    async def test_insufficient_input_fields_raises(self) -> None:
        page = _make_page(has_dialog=True, input_count=2)
        # Override fallback query_selector_all to also return 2
        page.query_selector_all = AsyncMock(return_value=[AsyncMock(), AsyncMock()])

        with pytest.raises(DmEncryptionPasscodeError, match="Expected 4"):
            with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
                await _handle_encryption_passcode(page, ["1", "2", "3", "4"], timeout_ms=100)

    @pytest.mark.asyncio
    async def test_wrong_passcode_dialog_persists_raises(self) -> None:
        page = _make_page(has_dialog=True, dialog_persists=True)

        with pytest.raises(DmEncryptionPasscodeError, match="passcode may be incorrect"):
            with patch("src.pipeline.dm.random_pause", new_callable=AsyncMock):
                with patch("src.pipeline.dm.random_mouse_move", new_callable=AsyncMock):
                    await _handle_encryption_passcode(page, ["1", "2", "3", "4"], timeout_ms=100)
