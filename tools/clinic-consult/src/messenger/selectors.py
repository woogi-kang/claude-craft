"""Platform-agnostic UI selector definitions for messenger apps.

Each messenger (KakaoTalk, LINE, etc.) has a different Android package name,
activity, and resource IDs. This module provides a unified dataclass so that
Navigator, Reader, Sender, and Monitor can work with any supported messenger.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MessengerSelectors:
    """Android UI resource IDs for a messenger application."""

    # App identity
    package: str
    main_activity: str

    # Chat list screen
    chat_list_tab: str
    chat_list_recycler: str
    chat_item_title: str
    chat_item_message: str
    chat_item_badge: str

    # Chat room screen
    chatroom_title: str
    message_text: str
    message_sender: str
    message_input: str
    send_button: str
    back_button: str

    # Bottom navigation
    bottom_tab_chat: str


# -----------------------------------------------------------------------
# KakaoTalk selectors (com.kakao.talk)
# -----------------------------------------------------------------------

KAKAO = MessengerSelectors(
    package="com.kakao.talk",
    main_activity="com.kakao.talk.activity.main.MainActivity",
    chat_list_tab="com.kakao.talk:id/tab_chat",
    chat_list_recycler="com.kakao.talk:id/recyclerView",
    chat_item_title="com.kakao.talk:id/title",
    chat_item_message="com.kakao.talk:id/message",
    chat_item_badge="com.kakao.talk:id/badge",
    chatroom_title="com.kakao.talk:id/toolbar_title",
    message_text="com.kakao.talk:id/message_text",
    message_sender="com.kakao.talk:id/profile_name",
    message_input="com.kakao.talk:id/message_edit_text",
    send_button="com.kakao.talk:id/send",
    back_button="com.kakao.talk:id/toolbar_back",
    bottom_tab_chat="com.kakao.talk:id/tab_chat",
)


# -----------------------------------------------------------------------
# LINE selectors (jp.naver.line.android)
# -----------------------------------------------------------------------

LINE = MessengerSelectors(
    package="jp.naver.line.android",
    main_activity="jp.naver.line.android.activity.SplashActivity",
    chat_list_tab="jp.naver.line.android:id/tab_chat",
    chat_list_recycler="jp.naver.line.android:id/chathistory_recyclerview",
    chat_item_title="jp.naver.line.android:id/chathistory_name",
    chat_item_message="jp.naver.line.android:id/chathistory_last_message",
    chat_item_badge="jp.naver.line.android:id/chathistory_badge",
    chatroom_title="jp.naver.line.android:id/chat_header_title",
    message_text="jp.naver.line.android:id/chat_message_text",
    message_sender="jp.naver.line.android:id/chat_message_name",
    message_input="jp.naver.line.android:id/chathistory_message_edit",
    send_button="jp.naver.line.android:id/chathistory_send_button",
    back_button="jp.naver.line.android:id/chat_header_back",
    bottom_tab_chat="jp.naver.line.android:id/tab_chat",
)


def get_selectors(platform: str) -> MessengerSelectors:
    """Return the selectors for a given platform name.

    Parameters
    ----------
    platform:
        One of ``"kakao"`` or ``"line"`` (case-insensitive).

    Raises
    ------
    ValueError
        If the platform is not supported.
    """
    from src.messenger import normalize_platform

    key = normalize_platform(platform)
    if key == "kakao":
        return KAKAO
    if key == "line":
        return LINE
    raise ValueError(f"Unsupported messenger platform: {platform!r}")
