"""Navigate between KakaoTalk screens.

Provides high-level navigation helpers to move between the chat list,
individual chatrooms, and ensure KakaoTalk is in the foreground.
"""

from __future__ import annotations

import time

from src.kakao import selectors
from src.utils.logger import get_logger

logger = get_logger("navigator")

# Maximum retries for navigation actions
_MAX_BACK_PRESSES = 5
_NAVIGATION_WAIT_S = 1.0


class Navigator:
    """Navigate the KakaoTalk application screens.

    Parameters
    ----------
    device:
        Connected uiautomator2 device instance.
    """

    def __init__(self, device: object) -> None:
        self._device = device

    def go_to_chat_list(self) -> bool:
        """Navigate back to the chat list screen.

        Tries pressing the back button repeatedly until the chat list
        tab is detected. Falls back to tapping the chat tab directly.

        Returns
        -------
        bool
            ``True`` if the chat list screen is reached.
        """
        # Already on chat list
        if self.is_in_chat_list():
            return True

        # Try pressing back to exit the current chatroom
        for attempt in range(_MAX_BACK_PRESSES):
            try:
                back_btn = self._device.resourceId(selectors.BACK_BUTTON)  # type: ignore[attr-defined]
                if back_btn.exists:
                    back_btn.click()
                else:
                    self._device.press("back")  # type: ignore[attr-defined]

                time.sleep(_NAVIGATION_WAIT_S)

                if self.is_in_chat_list():
                    logger.info("navigated_to_chat_list", method="back", attempts=attempt + 1)
                    return True

            except Exception as exc:
                logger.warning("go_to_chat_list_back_error", attempt=attempt, error=str(exc))

        # Fallback: tap the chat tab directly
        try:
            chat_tab = self._device.resourceId(selectors.BOTTOM_TAB_CHAT)  # type: ignore[attr-defined]
            if chat_tab.exists:
                chat_tab.click()
                time.sleep(_NAVIGATION_WAIT_S)
                if self.is_in_chat_list():
                    logger.info("navigated_to_chat_list", method="tab_click")
                    return True
        except Exception as exc:
            logger.warning("go_to_chat_list_tab_error", error=str(exc))

        logger.error("go_to_chat_list_failed")
        return False

    def enter_chatroom(self, chatroom_name: str) -> bool:
        """Find and tap a chatroom in the chat list to enter it.

        The chat list must be visible before calling this method.

        Parameters
        ----------
        chatroom_name:
            Display name of the chatroom to open.

        Returns
        -------
        bool
            ``True`` if the chatroom was entered successfully.
        """
        try:
            # Find the chatroom by title text
            chat_item = self._device.resourceId(selectors.CHAT_ITEM_TITLE).text(chatroom_name)  # type: ignore[attr-defined]

            if not chat_item.exists:
                logger.warning("chatroom_not_found", chatroom=chatroom_name)
                return False

            chat_item.click()
            time.sleep(_NAVIGATION_WAIT_S)

            # Verify we entered the chatroom
            if self.is_in_chatroom():
                logger.info("entered_chatroom", chatroom=chatroom_name)
                return True

            logger.warning("enter_chatroom_verify_failed", chatroom=chatroom_name)
            return False

        except Exception as exc:
            logger.error("enter_chatroom_error", chatroom=chatroom_name, error=str(exc))
            return False

    def go_back(self) -> bool:
        """Press the back button to return to the previous screen.

        Returns
        -------
        bool
            ``True`` if the back action was performed.
        """
        try:
            back_btn = self._device.resourceId(selectors.BACK_BUTTON)  # type: ignore[attr-defined]
            if back_btn.exists:
                back_btn.click()
            else:
                self._device.press("back")  # type: ignore[attr-defined]

            time.sleep(_NAVIGATION_WAIT_S)
            logger.debug("go_back_pressed")
            return True

        except Exception as exc:
            logger.error("go_back_error", error=str(exc))
            return False

    def is_in_chatroom(self) -> bool:
        """Check whether the chatroom screen is currently displayed.

        Returns
        -------
        bool
            ``True`` if the chatroom title bar is visible.
        """
        try:
            title = self._device.resourceId(selectors.CHATROOM_TITLE)  # type: ignore[attr-defined]
            return title.exists
        except Exception:
            return False

    def is_in_chat_list(self) -> bool:
        """Check whether the chat list screen is currently displayed.

        Returns
        -------
        bool
            ``True`` if the chat list tab is visible and the chatroom
            title is *not* visible (i.e. we are not inside a chatroom).
        """
        try:
            chat_tab = self._device.resourceId(selectors.CHAT_LIST_TAB)  # type: ignore[attr-defined]
            chatroom_title = self._device.resourceId(selectors.CHATROOM_TITLE)  # type: ignore[attr-defined]
            return chat_tab.exists and not chatroom_title.exists
        except Exception:
            return False

    def ensure_kakao_foreground(self) -> bool:
        """Ensure KakaoTalk is the foreground application.

        If KakaoTalk is not currently active, launches it and waits
        for the main activity to appear.

        Returns
        -------
        bool
            ``True`` if KakaoTalk is in the foreground after this call.
        """
        try:
            current_app = self._device.app_current()  # type: ignore[attr-defined]
            current_package = current_app.get("package", "")

            if current_package == selectors.KAKAO_PACKAGE:
                logger.debug("kakao_already_foreground")
                return True

            # Launch KakaoTalk
            logger.info("launching_kakao", current_package=current_package)
            self._device.app_start(  # type: ignore[attr-defined]
                selectors.KAKAO_PACKAGE,
                selectors.KAKAO_MAIN_ACTIVITY,
            )

            # Wait for the app to appear (up to 10 seconds)
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                time.sleep(1.0)
                try:
                    current_app = self._device.app_current()  # type: ignore[attr-defined]
                    if current_app.get("package", "") == selectors.KAKAO_PACKAGE:
                        logger.info("kakao_launched")
                        return True
                except Exception:
                    continue

            logger.error("kakao_launch_timeout")
            return False

        except Exception as exc:
            logger.error("ensure_kakao_foreground_error", error=str(exc))
            return False
