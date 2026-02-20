"""Tests for the collect pipeline."""

from __future__ import annotations

from unittest.mock import MagicMock

from src.db.repository import Repository
from src.pipeline.collect import CollectPipeline
from src.pipeline.search import RawTweet


def _make_mock_repo(*, duplicate_ids: set[str] | None = None) -> MagicMock:
    """Create a mock Repository that tracks inserted tweets.

    Parameters
    ----------
    duplicate_ids:
        Tweet IDs that should be treated as duplicates (insert returns False).
    """
    repo = MagicMock(spec=Repository)
    dupes = duplicate_ids or set()

    def _insert_tweet(data: dict) -> bool:
        return data.get("tweet_id") not in dupes

    repo.insert_tweet.side_effect = _insert_tweet
    repo.get_user.return_value = None
    repo.insert_user.return_value = True
    repo.update_user.return_value = True
    return repo


class TestCollectFilters:
    """Test the collect pipeline's filtering logic."""

    def test_passes_normal_user(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo()
        pipeline = CollectPipeline(max_tweet_age_hours=999)
        result = pipeline.run([sample_raw_tweets[0]], repo)
        assert result.stored == 1
        assert result.rejected_followers == 0

    def test_rejects_high_follower_count(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo()
        pipeline = CollectPipeline(max_tweet_age_hours=999)
        # tweet_004 has 50K followers
        result = pipeline.run([sample_raw_tweets[3]], repo)
        assert result.stored == 0
        assert result.rejected_followers == 1

    def test_rejects_no_bio(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo()
        pipeline = CollectPipeline(require_bio=True, max_tweet_age_hours=999)
        # tweet_005 has empty bio
        result = pipeline.run([sample_raw_tweets[4]], repo)
        assert result.stored == 0
        assert result.rejected_no_bio == 1

    def test_allows_no_bio_when_not_required(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo()
        pipeline = CollectPipeline(require_bio=False, max_tweet_age_hours=999)
        result = pipeline.run([sample_raw_tweets[4]], repo)
        assert result.stored == 1

    def test_rejects_marketing_account(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo()
        pipeline = CollectPipeline(max_tweet_age_hours=999)
        # tweet_003 is from clinic_official with URL + clinic keyword in bio
        result = pipeline.run([sample_raw_tweets[2]], repo)
        assert result.stored == 0
        assert result.rejected_marketing == 1

    def test_rejects_no_profile_pic(self) -> None:
        repo = _make_mock_repo()
        tweet = RawTweet(
            tweet_id="no_pic",
            content="test",
            author_username="nopic",
            author_bio="normal bio",
            author_has_profile_pic=False,
            tweet_timestamp="2026-02-19T10:00:00.000Z",
        )
        pipeline = CollectPipeline(require_profile_pic=True, max_tweet_age_hours=999)
        result = pipeline.run([tweet], repo)
        assert result.stored == 0
        assert result.rejected_no_profile_pic == 1

    def test_dedup_existing_tweets(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo(duplicate_ids={"tweet_001"})
        pipeline = CollectPipeline(max_tweet_age_hours=999)
        result = pipeline.run([sample_raw_tweets[0]], repo)
        assert result.rejected_duplicate == 1
        assert result.stored == 0

    def test_batch_mixed_tweets(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo()
        pipeline = CollectPipeline(max_tweet_age_hours=999)
        result = pipeline.run(sample_raw_tweets, repo)
        # tweet_001 and tweet_002 should pass (normal users with bio)
        # tweet_003 rejected (marketing)
        # tweet_004 rejected (50K followers)
        # tweet_005 rejected (no bio)
        assert result.stored == 2
        assert result.total_input == 5


class TestMarketingDetection:
    """Test the clinic marketing account heuristic."""

    def test_url_plus_keyword(self) -> None:
        pipeline = CollectPipeline()
        assert (
            pipeline._is_marketing_account("江南クリニック公式 https://example.com", "clinic")
            is True
        )

    def test_url_without_keyword(self) -> None:
        pipeline = CollectPipeline()
        assert pipeline._is_marketing_account("My blog https://myblog.com", "user") is False

    def test_keyword_without_url(self) -> None:
        pipeline = CollectPipeline()
        assert pipeline._is_marketing_account("美容皮膚科で働いてます", "user") is False

    def test_empty_bio(self) -> None:
        pipeline = CollectPipeline()
        assert pipeline._is_marketing_account("", "user") is False


class TestUserUpsert:
    """Test that collect creates/updates user records."""

    def test_creates_new_user(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo()
        repo.get_user.return_value = None  # No existing user
        pipeline = CollectPipeline(max_tweet_age_hours=999)
        pipeline.run([sample_raw_tweets[0]], repo)
        repo.insert_user.assert_called_once()
        call_data = repo.insert_user.call_args[0][0]
        assert call_data["username"] == "user_a"
        assert call_data["follower_count"] == 250

    def test_updates_existing_user(self, sample_raw_tweets: list[RawTweet]) -> None:
        repo = _make_mock_repo()
        repo.get_user.return_value = {"username": "user_a", "follower_count": 200}
        pipeline = CollectPipeline(max_tweet_age_hours=999)
        pipeline.run([sample_raw_tweets[0]], repo)
        repo.update_user.assert_called_once_with(
            "user_a",
            follower_count=250,
            following_count=300,
            bio="東京在住。美容好き。趣味はカフェ巡り",
        )
