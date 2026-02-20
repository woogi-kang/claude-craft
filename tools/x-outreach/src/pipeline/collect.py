"""Collect pipeline -- filter and store raw tweets.

Applies qualification filters (follower count, profile completeness,
marketing account detection) and persists passing tweets to the
database with status ``collected``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from outreach_shared.utils.logger import get_logger
from outreach_shared.utils.time_utils import parse_post_timestamp as parse_tweet_timestamp
from outreach_shared.utils.time_utils import post_age_hours as tweet_age_hours

from src.db.repository import Repository
from src.pipeline.search import RawTweet

logger = get_logger("collect")


# Keywords that indicate a clinic marketing account
_CLINIC_MARKETING_KEYWORDS = [
    "クリニック",
    "clinic",
    "美容外科",
    "美容皮膚科",
    "カウンセリング予約",
    "モニター募集",
    "キャンペーン",
    "公式",
    "official",
    "症例",
    "ご予約",
]

# URL pattern in bio text
_URL_PATTERN = re.compile(r"https?://\S+|[\w.-]+\.(com|jp|co\.jp|net|org)")


@dataclass
class CollectResult:
    """Summary of the collect pipeline run."""

    total_input: int = 0
    passed_filters: int = 0
    rejected_followers: int = 0
    rejected_no_profile_pic: int = 0
    rejected_no_bio: int = 0
    rejected_marketing: int = 0
    rejected_duplicate: int = 0
    rejected_too_old: int = 0
    stored: int = 0


class CollectPipeline:
    """Filter raw tweets and store qualifying ones.

    Parameters
    ----------
    max_follower_count:
        Exclude accounts with more than this many followers.
    require_profile_pic:
        Exclude accounts without a profile picture.
    require_bio:
        Exclude accounts without a bio.
    max_tweet_age_hours:
        Exclude tweets older than this many hours.
    """

    def __init__(
        self,
        *,
        max_follower_count: int = 10_000,
        require_profile_pic: bool = True,
        require_bio: bool = True,
        max_tweet_age_hours: int = 24,
    ) -> None:
        self._max_followers = max_follower_count
        self._require_pic = require_profile_pic
        self._require_bio = require_bio
        self._max_age_hours = max_tweet_age_hours

    def run(
        self,
        raw_tweets: list[RawTweet],
        repository: Repository,
    ) -> CollectResult:
        """Apply filters and store passing tweets.

        Parameters
        ----------
        raw_tweets:
            Unfiltered output from the search pipeline.
        repository:
            Database repository for persistence.

        Returns
        -------
        CollectResult
            Statistics about the filtering outcome.
        """
        result = CollectResult(total_input=len(raw_tweets))

        for raw in raw_tweets:
            # --- Filter: follower count ---
            if raw.author_follower_count > self._max_followers:
                result.rejected_followers += 1
                logger.debug(
                    "collect_reject_followers",
                    username=raw.author_username,
                    followers=raw.author_follower_count,
                )
                continue

            # --- Filter: profile picture ---
            if self._require_pic and not raw.author_has_profile_pic:
                result.rejected_no_profile_pic += 1
                continue

            # --- Filter: bio ---
            if self._require_bio and not raw.author_bio:
                result.rejected_no_bio += 1
                continue

            # --- Filter: clinic marketing account ---
            if self._is_marketing_account(raw.author_bio, raw.author_username):
                result.rejected_marketing += 1
                logger.debug(
                    "collect_reject_marketing",
                    username=raw.author_username,
                )
                continue

            # --- Filter: tweet age ---
            if raw.tweet_timestamp:
                try:
                    parsed_ts = parse_tweet_timestamp(raw.tweet_timestamp)
                    age_h = tweet_age_hours(parsed_ts)
                    if age_h > self._max_age_hours:
                        result.rejected_too_old += 1
                        continue
                except ValueError:
                    pass  # Keep tweets with unparseable timestamps

            result.passed_filters += 1

            # --- Store tweet ---
            tweet_data = {
                "tweet_id": raw.tweet_id,
                "content": raw.content,
                "author_username": raw.author_username,
                "author_display_name": raw.author_display_name,
                "author_follower_count": raw.author_follower_count,
                "author_following_count": raw.author_following_count,
                "author_bio": raw.author_bio,
                "tweet_timestamp": raw.tweet_timestamp,
                "likes": raw.likes,
                "retweets": raw.retweets,
                "replies": raw.replies,
                "tweet_url": raw.tweet_url,
                "search_keyword": raw.search_keyword,
                "status": "collected",
            }

            inserted = repository.insert_tweet(tweet_data)
            if inserted:
                result.stored += 1
                # Also store/update the user record
                self._upsert_user(repository, raw)
            else:
                result.rejected_duplicate += 1

        logger.info(
            "collect_complete",
            total=result.total_input,
            stored=result.stored,
            duplicates=result.rejected_duplicate,
            rejected_followers=result.rejected_followers,
            rejected_marketing=result.rejected_marketing,
        )
        return result

    def _is_marketing_account(self, bio: str, username: str) -> bool:
        """Heuristic check for clinic marketing accounts.

        An account is flagged if its bio contains both a URL and at
        least one clinic-related keyword.
        """
        if not bio:
            return False

        bio_lower = bio.lower()
        has_url = bool(_URL_PATTERN.search(bio))
        has_keyword = any(kw.lower() in bio_lower for kw in _CLINIC_MARKETING_KEYWORDS)

        return has_url and has_keyword

    @staticmethod
    def _upsert_user(repository: Repository, raw: RawTweet) -> None:
        """Insert or update the user record."""
        existing = repository.get_user(raw.author_username)
        if existing is None:
            repository.insert_user(
                {
                    "username": raw.author_username,
                    "display_name": raw.author_display_name,
                    "follower_count": raw.author_follower_count,
                    "following_count": raw.author_following_count,
                    "bio": raw.author_bio,
                }
            )
        else:
            # Update counts if changed
            repository.update_user(
                raw.author_username,
                follower_count=raw.author_follower_count,
                following_count=raw.author_following_count,
                bio=raw.author_bio,
            )
