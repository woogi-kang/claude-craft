"""X (Twitter) DOM selectors and constants.

Centralises all ``data-testid`` and other CSS selectors used by the
Playwright automation so changes to X's DOM only require updates here.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Navigation & Login
# ---------------------------------------------------------------------------

LOGIN_URL = "https://x.com/i/flow/login"
HOME_URL = "https://x.com/home"
SEARCH_URL_TEMPLATE = "https://x.com/search?q={query}&src=typed_query&f=live"
MESSAGES_URL = "https://x.com/messages"

# Login form
USERNAME_INPUT = 'input[autocomplete="username"]'
PASSWORD_INPUT = 'input[type="password"]'
LOGIN_BUTTON = '[data-testid="LoginForm_Login_Button"]'
NEXT_BUTTON_EN = 'text="Next"'
NEXT_BUTTON_JA = 'text="次へ"'

# Verification step (X sometimes asks for phone/email before password)
VERIFY_INPUT = 'input[data-testid="ocfEnterTextTextInput"]'

# Logged-in indicators
COMPOSE_TWEET_BUTTON = '[data-testid="SideNav_NewTweet_Button"]'
PROFILE_LINK = '[data-testid="AppTabBar_Profile_Link"]'

# ---------------------------------------------------------------------------
# Tweet elements
# ---------------------------------------------------------------------------

TWEET_ARTICLE = 'article[data-testid="tweet"]'
TWEET_TEXT = '[data-testid="tweetText"]'
USER_NAME_CONTAINER = '[data-testid="User-Name"]'
METRICS_GROUP = '[role="group"]'

# ---------------------------------------------------------------------------
# Reply (Playwright-based)
# ---------------------------------------------------------------------------

REPLY_BUTTON = '[data-testid="reply"]'
REPLY_TEXT_INPUT = '[data-testid="tweetTextarea_0"]'
REPLY_SUBMIT_BUTTON = '[data-testid="tweetButton"]'

# ---------------------------------------------------------------------------
# DM
# ---------------------------------------------------------------------------

NEW_DM_BUTTON = '[data-testid="NewDM_Button"]'
NEW_DM_LINK = 'a[href="/messages/compose"]'
DM_SEARCH_INPUT = '[data-testid="searchPeople"]'
DM_TYPEAHEAD_RESULT = '[data-testid="typeaheadResult"]'
DM_NEXT_BUTTON = '[data-testid="nextButton"]'
DM_COMPOSER_INPUT = '[data-testid="dmComposerTextInput"]'
DM_SEND_BUTTON = '[data-testid="dmComposerSendButton"]'
DM_CONVERSATION = '[data-testid="dmConversation"]'

# ---------------------------------------------------------------------------
# Restriction / rate limit page indicators
# ---------------------------------------------------------------------------

RESTRICTION_INDICATORS = [
    "rate limit",
    "temporarily restricted",
    "suspicious activity",
    "try again later",
    "limit exceeded",
    "something went wrong",
    "account suspended",
    "your account has been locked",
    "verify your identity",
    "unusual login activity",
    "caution: this account is temporarily limited",
]
