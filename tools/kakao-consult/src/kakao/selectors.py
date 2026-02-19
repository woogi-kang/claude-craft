"""Centralized KakaoTalk UI element selectors.

All uiautomator2 resource-ids and XPath patterns are defined here
so that a KakaoTalk UI update requires changes in only one file.
"""

# Package
KAKAO_PACKAGE = "com.kakao.talk"
KAKAO_MAIN_ACTIVITY = "com.kakao.talk.activity.main.MainActivity"

# Chat list screen
CHAT_LIST_TAB = "com.kakao.talk:id/tab_chat"
CHAT_LIST_RECYCLER = "com.kakao.talk:id/recyclerView"
CHAT_ITEM_TITLE = "com.kakao.talk:id/title"
CHAT_ITEM_MESSAGE = "com.kakao.talk:id/message"
CHAT_ITEM_BADGE = "com.kakao.talk:id/badge"
CHAT_ITEM_TIME = "com.kakao.talk:id/time"

# Chat room screen
CHATROOM_TITLE = "com.kakao.talk:id/toolbar_title"
MESSAGE_RECYCLER = "com.kakao.talk:id/recyclerView_chat"
MESSAGE_TEXT = "com.kakao.talk:id/message_text"
MESSAGE_SENDER = "com.kakao.talk:id/profile_name"
MESSAGE_TIME = "com.kakao.talk:id/time_text"
MESSAGE_INPUT = "com.kakao.talk:id/message_edit_text"
SEND_BUTTON = "com.kakao.talk:id/send"
BACK_BUTTON = "com.kakao.talk:id/toolbar_back"

# Navigation
BOTTOM_TAB_CHAT = "com.kakao.talk:id/tab_chat"
BOTTOM_TAB_FRIENDS = "com.kakao.talk:id/tab_friend"
