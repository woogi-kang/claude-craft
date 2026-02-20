"""Shared fixtures for the x-outreach test suite."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.config import Settings, load_settings
from src.knowledge.treatments import TreatmentKnowledgeBase
from src.pipeline.search import RawTweet


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    """Provide a Settings instance with test-safe defaults."""
    config_yaml = tmp_path / "config.yaml"
    config_yaml.write_text(
        """\
search:
  keywords:
    - "テスト検索"
  max_post_age_hours: 24
classification:
  confidence_threshold: 0.7
  categories:
    - hospital
    - price
    - procedure
    - complaint
    - review
browser:
  headless: true
  viewport_width: 1280
  viewport_height: 720
delays:
  search_min_seconds: 1
  search_max_seconds: 2
  action_min_seconds: 1
  action_max_seconds: 2
logging:
  level: "DEBUG"
  log_dir: "logs"
database:
  url: "postgresql://localhost:5432/outreach_test"
llm:
  provider: gemini
  model: gemini-2.0-flash
""",
        encoding="utf-8",
    )
    return load_settings(config_path=config_yaml)


@pytest.fixture
def sample_raw_tweets() -> list[RawTweet]:
    """Provide a batch of sample raw tweets for testing."""
    return [
        RawTweet(
            tweet_id="tweet_001",
            content="韓国でボトックス打ってきた！めっちゃ安い！3000円だった",
            author_username="user_a",
            author_display_name="User A",
            author_bio="東京在住。美容好き。趣味はカフェ巡り",
            author_follower_count=250,
            author_following_count=300,
            author_has_profile_pic=True,
            tweet_url="https://x.com/user_a/status/tweet_001",
            likes=5,
            retweets=1,
            replies=2,
            tweet_timestamp="2026-02-19T10:00:00.000Z",
            search_keyword="韓国 ボトックス",
        ),
        RawTweet(
            tweet_id="tweet_002",
            content="韓国の皮膚科どこがいい？おすすめある？初めて行くから不安",
            author_username="user_b",
            author_display_name="User B",
            author_bio="大阪 / コスメ大好き",
            author_follower_count=180,
            author_following_count=200,
            author_has_profile_pic=True,
            tweet_url="https://x.com/user_b/status/tweet_002",
            likes=3,
            retweets=0,
            replies=4,
            tweet_timestamp="2026-02-19T12:00:00.000Z",
            search_keyword="韓国皮膚科",
        ),
        RawTweet(
            tweet_id="tweet_003",
            content="キャンペーン実施中！ボトックス50%OFF",
            author_username="clinic_official",
            author_display_name="Beauty Clinic Official",
            author_bio="江南クリニック公式アカウント https://clinic-example.com",
            author_follower_count=5000,
            author_following_count=100,
            author_has_profile_pic=True,
            tweet_url="https://x.com/clinic_official/status/tweet_003",
            likes=10,
            retweets=5,
            replies=1,
            tweet_timestamp="2026-02-19T09:00:00.000Z",
            search_keyword="韓国 ボトックス",
        ),
        RawTweet(
            tweet_id="tweet_004",
            content="韓国美容の情報共有します",
            author_username="influencer_big",
            author_display_name="Big Influencer",
            author_bio="Beauty influencer | PR",
            author_follower_count=50000,
            author_following_count=500,
            author_has_profile_pic=True,
            tweet_url="https://x.com/influencer_big/status/tweet_004",
            likes=200,
            retweets=50,
            replies=30,
            tweet_timestamp="2026-02-19T08:00:00.000Z",
            search_keyword="韓国美容",
        ),
        RawTweet(
            tweet_id="tweet_005",
            content="ポテンツァ受けてきたけど痛すぎて泣いた。でも効果すごい",
            author_username="user_c",
            author_display_name="User C",
            author_bio="",  # No bio
            author_follower_count=100,
            author_following_count=150,
            author_has_profile_pic=True,
            tweet_url="https://x.com/user_c/status/tweet_005",
            likes=8,
            retweets=2,
            replies=3,
            tweet_timestamp="2026-02-19T14:00:00.000Z",
            search_keyword="ポテンツァ",
        ),
    ]


@pytest.fixture
def knowledge_base(tmp_path: Path) -> TreatmentKnowledgeBase:
    """Provide a knowledge base loaded with minimal test data."""
    test_data = {
        "version": "1.0",
        "total_count": 2,
        "complete_count": 2,
        "details": [
            {
                "procedure_id": 1,
                "procedure_name": "보톡스",
                "alias": ["보툴리눔톡신"],
                "principle": "근육 이완",
                "average_price": "3만원~25만원",
                "downtime": "없음",
                "duration": "3-6개월",
                "recommended_cycle": "3-6개월 간격",
            },
            {
                "procedure_id": 2,
                "procedure_name": "포텐자",
                "alias": ["포텐짜", "Potenza"],
                "principle": "RF 고주파 에너지",
                "average_price": "15만원~25만원",
                "downtime": "2-3일",
                "duration": "6-12개월",
                "recommended_cycle": "1-3개월 간격",
            },
        ],
    }

    json_path = tmp_path / "treatments.json"
    json_path.write_text(json.dumps(test_data, ensure_ascii=False), encoding="utf-8")

    kb = TreatmentKnowledgeBase()
    kb.load(json_path)
    return kb
