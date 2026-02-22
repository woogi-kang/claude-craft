"""Search pipeline -- discover tweets matching configured keywords.

Navigates X's search page for each keyword, extracts raw tweet data
from the DOM, and returns unfiltered results for the collect stage.
"""

from __future__ import annotations

import random
import urllib.parse
from dataclasses import dataclass

from outreach_shared.browser.human_sim import human_scroll, random_mouse_move, random_pause
from outreach_shared.utils.logger import get_logger
from outreach_shared.utils.time_utils import random_delay
from playwright.async_api import BrowserContext, Page

from src.platform.selectors import (
    METRICS_GROUP,
    TWEET_ARTICLE,
    TWEET_TEXT,
    USER_NAME_CONTAINER,
)

logger = get_logger("search")


@dataclass
class RawTweet:
    """Raw tweet data extracted from the X DOM before filtering."""

    tweet_id: str = ""
    content: str = ""
    author_username: str = ""
    author_display_name: str = ""
    author_bio: str = ""
    author_follower_count: int = 0
    author_following_count: int = 0
    author_has_profile_pic: bool = True
    tweet_url: str = ""
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    tweet_timestamp: str = ""
    search_keyword: str = ""
    raw_html: str = ""


class SearchPipeline:
    """Execute keyword-based tweet discovery on X.

    Parameters
    ----------
    min_delay:
        Minimum seconds between keyword searches.
    max_delay:
        Maximum seconds between keyword searches.
    """

    def __init__(
        self,
        *,
        min_delay: float = 30.0,
        max_delay: float = 300.0,
    ) -> None:
        self._min_delay = min_delay
        self._max_delay = max_delay

    async def run(
        self,
        keywords: list[str],
        context: BrowserContext,
    ) -> list[RawTweet]:
        """Search for each keyword and return aggregated raw tweets.

        Parameters
        ----------
        keywords:
            Japanese search terms or hashtags.
        context:
            An authenticated Playwright browser context.

        Returns
        -------
        list[RawTweet]
            Unfiltered tweet data from all keyword searches.
        """
        all_tweets: list[RawTweet] = []
        page = context.pages[0] if context.pages else await context.new_page()

        # Randomize keyword order each run for natural-looking search patterns
        keywords = list(keywords)  # copy to avoid mutating caller's list
        random.shuffle(keywords)

        for idx, keyword in enumerate(keywords):
            logger.info("search_keyword_start", keyword=keyword, index=idx + 1, total=len(keywords))
            try:
                tweets = await self._search_keyword(page, keyword)
                all_tweets.extend(tweets)
                logger.info(
                    "search_keyword_done",
                    keyword=keyword,
                    found=len(tweets),
                )
            except Exception as exc:
                logger.error("search_keyword_error", keyword=keyword, error=str(exc))

            # Human-like delay between searches
            if idx < len(keywords) - 1:
                await random_delay(self._min_delay, self._max_delay)

        # Deduplicate by tweet_id
        seen: set[str] = set()
        unique: list[RawTweet] = []
        for tweet in all_tweets:
            if tweet.tweet_id and tweet.tweet_id not in seen:
                seen.add(tweet.tweet_id)
                unique.append(tweet)

        logger.info("search_complete", total_unique=len(unique), total_raw=len(all_tweets))
        return unique

    async def _search_keyword(self, page: Page, keyword: str) -> list[RawTweet]:
        """Navigate to X search and extract tweets for a single keyword."""
        encoded = urllib.parse.quote(keyword)
        url = f"https://x.com/search?q={encoded}&src=typed_query&f=live"

        await page.goto(url, wait_until="domcontentloaded", timeout=30_000)
        await random_pause(3.0, 5.0)
        await random_mouse_move(page)

        # Scroll a few times to load more results
        for _ in range(3):
            await human_scroll(page, direction="down")
            await random_pause(1.0, 2.0)

        # Extract tweet articles
        tweet_elements = await page.query_selector_all(TWEET_ARTICLE)
        logger.info("search_elements_found", keyword=keyword, count=len(tweet_elements))

        tweets: list[RawTweet] = []
        for el in tweet_elements:
            try:
                tweet = await self._extract_tweet(el, keyword)
                if tweet.tweet_id:
                    tweets.append(tweet)
            except Exception as exc:
                logger.warning("tweet_extract_error", keyword=keyword, error=str(exc))

        return tweets

    async def _extract_tweet(self, element: object, keyword: str) -> RawTweet:
        """Extract structured data from a tweet DOM element.

        Uses ``data-testid`` selectors that are relatively stable on X.
        """
        tweet = RawTweet(search_keyword=keyword)

        # The element is a Playwright ElementHandle
        el = element  # type: ignore[assignment]

        # Extract tweet URL and ID from the timestamp link
        time_link = await el.query_selector("time")
        if time_link:
            parent_a = await time_link.evaluate_handle("el => el.closest('a')")
            href = await parent_a.get_attribute("href") if parent_a else None
            if href:
                tweet.tweet_url = f"https://x.com{href}"
                # URL format: /{username}/status/{tweet_id}
                parts = href.strip("/").split("/")
                if len(parts) >= 3 and parts[-2] == "status":
                    tweet.tweet_id = parts[-1]

            datetime_attr = await time_link.get_attribute("datetime")
            if datetime_attr:
                tweet.tweet_timestamp = datetime_attr

        # Extract tweet text
        text_el = await el.query_selector(TWEET_TEXT)
        if text_el:
            tweet.content = (await text_el.inner_text()).strip()

        # Extract author username from the user link
        user_links = await el.query_selector_all('a[role="link"]')
        for link in user_links:
            href = await link.get_attribute("href")
            if href and href.startswith("/") and "/status/" not in href:
                username = href.strip("/")
                if username and not username.startswith("i/"):
                    tweet.author_username = username
                    break

        # Extract display name
        display_name_el = await el.query_selector(f"{USER_NAME_CONTAINER} span")
        if display_name_el:
            tweet.author_display_name = (await display_name_el.inner_text()).strip()

        # Extract engagement metrics from aria-labels on group buttons
        metrics_el = await el.query_selector(METRICS_GROUP)
        if metrics_el:
            buttons = await metrics_el.query_selector_all("button")
            # Typical order: reply, retweet, like, bookmark, share
            for i, btn in enumerate(buttons):
                aria = await btn.get_attribute("aria-label") or ""
                count = self._parse_metric(aria)
                if i == 0:
                    tweet.replies = count
                elif i == 1:
                    tweet.retweets = count
                elif i == 2:
                    tweet.likes = count

        return tweet

    @staticmethod
    def _parse_metric(aria_label: str) -> int:
        """Parse a count from an aria-label like '5 Likes' or '12 replies'."""
        if not aria_label:
            return 0
        parts = aria_label.split()
        for part in parts:
            cleaned = part.replace(",", "").replace(".", "")
            if cleaned.isdigit():
                return int(cleaned)
        return 0
