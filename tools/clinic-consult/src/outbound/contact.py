"""Outbound contact via messenger deep links.

Opens a clinic's messenger channel chat (KakaoTalk, LINE, etc.) using
ADB deep links, which is more reliable than navigating the UI manually.
"""

from __future__ import annotations

import asyncio
import subprocess

from src.clinic.models import ClinicInfo
from src.utils.logger import get_logger

logger = get_logger("contact")

# Wait time after opening deep link for the messenger to load
_DEEP_LINK_WAIT_S = 3.0


class ClinicContactor:
    """Opens messenger channel chats via ADB deep links.

    Parameters
    ----------
    device:
        Connected uiautomator2 device instance.
    navigator:
        Messenger navigator for screen verification.
    serial:
        ADB device serial (e.g. "127.0.0.1:5555").
    platform:
        Messenger platform (``"kakao"`` or ``"line"``).
    """

    def __init__(
        self,
        device: object,
        navigator: object,
        serial: str = "127.0.0.1:5555",
        platform: str = "kakao",
    ) -> None:
        self._device = device
        self._navigator = navigator
        self._serial = serial
        self._platform = platform

    @property
    def platform(self) -> str:
        return self._platform

    async def open_clinic_chat(self, clinic: ClinicInfo) -> bool:
        """Open a chat with the clinic via deep link.

        Parameters
        ----------
        clinic:
            Clinic info containing the messenger channel URL.

        Returns
        -------
        bool
            True if the chat window was opened successfully.
        """
        chat_url = clinic.get_chat_url(self._platform)
        if not chat_url:
            logger.error(
                "no_contact_url", clinic=clinic.name, platform=self._platform,
            )
            return False

        logger.info(
            "opening_clinic_chat",
            clinic=clinic.name,
            url=chat_url,
            platform=self._platform,
        )

        # Ensure messenger is running
        self._navigator.ensure_foreground()  # type: ignore[attr-defined]
        await asyncio.sleep(1.0)

        # Open deep link via ADB
        success = await self._open_deep_link(chat_url)
        if not success:
            logger.error("deep_link_failed", clinic=clinic.name)
            return False

        await asyncio.sleep(_DEEP_LINK_WAIT_S)

        # Verify chatroom opened
        if self._navigator.is_in_chatroom():  # type: ignore[attr-defined]
            logger.info("clinic_chat_opened", clinic=clinic.name)
            return True

        # Retry once
        logger.warning("chatroom_not_detected_retrying", clinic=clinic.name)
        await asyncio.sleep(2.0)
        if self._navigator.is_in_chatroom():  # type: ignore[attr-defined]
            logger.info("clinic_chat_opened_retry", clinic=clinic.name)
            return True

        logger.error("clinic_chat_open_failed", clinic=clinic.name)
        return False

    async def _open_deep_link(self, url: str) -> bool:
        """Send an ADB intent to open a URL."""
        cmd = [
            "adb", "-s", self._serial,
            "shell", "am", "start",
            "-a", "android.intent.action.VIEW",
            "-d", url,
        ]
        try:
            result = await asyncio.to_thread(
                subprocess.run,
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode == 0:
                logger.debug("adb_deep_link_sent", url=url)
                return True
            logger.error("adb_deep_link_error", stderr=result.stderr.strip())
            return False
        except subprocess.TimeoutExpired:
            logger.error("adb_deep_link_timeout")
            return False
        except FileNotFoundError:
            logger.error("adb_not_found")
            return False

    async def return_to_chat_list(self) -> bool:
        """Navigate back to the chat list."""
        return self._navigator.go_to_chat_list()  # type: ignore[attr-defined]
