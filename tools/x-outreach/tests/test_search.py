"""Tests for the search pipeline."""

from __future__ import annotations

from src.pipeline.search import RawTweet, SearchPipeline


class TestRawTweet:
    """Test the RawTweet dataclass."""

    def test_default_values(self) -> None:
        tweet = RawTweet()
        assert tweet.tweet_id == ""
        assert tweet.content == ""
        assert tweet.author_username == ""
        assert tweet.likes == 0
        assert tweet.author_has_profile_pic is True

    def test_with_values(self) -> None:
        tweet = RawTweet(
            tweet_id="123",
            content="hello",
            author_username="test",
            likes=5,
        )
        assert tweet.tweet_id == "123"
        assert tweet.likes == 5


class TestSearchPipeline:
    """Test SearchPipeline helper methods."""

    def test_parse_metric_with_number(self) -> None:
        assert SearchPipeline._parse_metric("5 Likes") == 5

    def test_parse_metric_with_comma(self) -> None:
        assert SearchPipeline._parse_metric("1,234 Retweets") == 1234

    def test_parse_metric_empty(self) -> None:
        assert SearchPipeline._parse_metric("") == 0

    def test_parse_metric_no_number(self) -> None:
        assert SearchPipeline._parse_metric("Likes") == 0

    def test_parse_metric_zero(self) -> None:
        assert SearchPipeline._parse_metric("0 replies") == 0

    def test_init_delays(self) -> None:
        pipeline = SearchPipeline(min_delay=5.0, max_delay=10.0)
        assert pipeline._min_delay == 5.0
        assert pipeline._max_delay == 10.0

    def test_init_network_optimization_defaults(self) -> None:
        pipeline = SearchPipeline()
        assert pipeline._block_media_resources is False
        assert pipeline._blocked_resource_types == {"image", "media", "font"}
        assert pipeline._log_network_usage is False

    def test_init_network_optimization_custom(self) -> None:
        pipeline = SearchPipeline(
            block_media_resources=True,
            blocked_resource_types=("image", "font"),
            log_network_usage=True,
        )
        assert pipeline._block_media_resources is True
        assert pipeline._blocked_resource_types == {"image", "font"}
        assert pipeline._log_network_usage is True
