"""Tests for utility modules, knowledge base, templates, and tracking."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from outreach_shared.utils.rate_limiter import (
    MonthlyBudgetTracker,
    SlidingWindowLimiter,
    TokenBucketLimiter,
)
from outreach_shared.utils.time_utils import (
    now_jst,
)
from outreach_shared.utils.time_utils import (
    parse_post_timestamp as parse_tweet_timestamp,
)
from outreach_shared.utils.time_utils import (
    post_age_hours as tweet_age_hours,
)

from src.ai.prompts import (
    build_classification_system_prompt,
    build_classification_user_prompt,
)
from src.db.repository import Repository
from src.knowledge.templates import TemplateSelector
from src.knowledge.treatments import (
    CONCERN_TO_PROCEDURES,
    JAPANESE_TO_KOREAN,
    TreatmentKnowledgeBase,
)
from src.pipeline.track import ActionTracker

# =========================================================================
# Time utilities
# =========================================================================


class TestTimeUtils:
    """Test JST time utilities."""

    def test_now_jst_timezone(self) -> None:
        dt = now_jst()
        assert dt.tzinfo is not None
        assert dt.utcoffset() == timedelta(hours=9)

    def test_parse_tweet_timestamp_iso(self) -> None:
        ts = "2026-02-19T10:30:00.000Z"
        dt = parse_tweet_timestamp(ts)
        assert dt.year == 2026
        assert dt.month == 2
        assert dt.day == 19
        assert dt.tzinfo is not None

    def test_parse_tweet_timestamp_no_millis(self) -> None:
        ts = "2026-02-19T10:30:00Z"
        dt = parse_tweet_timestamp(ts)
        assert dt.year == 2026

    def test_parse_tweet_timestamp_with_tz(self) -> None:
        ts = "2026-02-19T10:30:00+09:00"
        dt = parse_tweet_timestamp(ts)
        assert dt.year == 2026

    def test_parse_tweet_timestamp_twitter_format(self) -> None:
        ts = "Wed Feb 19 10:30:00 +0000 2026"
        dt = parse_tweet_timestamp(ts)
        assert dt.year == 2026

    def test_parse_tweet_timestamp_invalid(self) -> None:
        with pytest.raises(ValueError):
            parse_tweet_timestamp("not a date")

    def test_tweet_age_hours(self) -> None:
        recent = datetime.now(tz=UTC) - timedelta(hours=2)
        age = tweet_age_hours(recent)
        assert 1.9 < age < 2.1

    def test_tweet_age_hours_old(self) -> None:
        old = datetime.now(tz=UTC) - timedelta(days=3)
        age = tweet_age_hours(old)
        assert age > 70


# =========================================================================
# Rate limiters
# =========================================================================


class TestTokenBucketLimiter:
    """Test the token-bucket rate limiter."""

    def test_initial_tokens(self) -> None:
        limiter = TokenBucketLimiter(max_tokens=10, refill_seconds=60)
        assert limiter.available_tokens == 10.0

    @pytest.mark.asyncio
    async def test_acquire_decrements(self) -> None:
        limiter = TokenBucketLimiter(max_tokens=5, refill_seconds=60)
        await limiter.acquire()
        assert limiter.available_tokens < 5.0


class TestSlidingWindowLimiter:
    """Test the sliding-window rate limiter."""

    def test_can_act_initially(self) -> None:
        limiter = SlidingWindowLimiter(max_actions=10)
        assert limiter.can_act() is True
        assert limiter.remaining == 10

    def test_record_reduces_remaining(self) -> None:
        limiter = SlidingWindowLimiter(max_actions=3)
        limiter.record()
        limiter.record()
        assert limiter.remaining == 1
        assert limiter.actions_used == 2

    def test_max_actions_reached(self) -> None:
        limiter = SlidingWindowLimiter(max_actions=2)
        limiter.record()
        limiter.record()
        assert limiter.can_act() is False
        assert limiter.remaining == 0


class TestMonthlyBudgetTracker:
    """Test the monthly budget tracker."""

    def test_initial_state(self) -> None:
        tracker = MonthlyBudgetTracker(monthly_limit=100)
        assert tracker.remaining == 100
        assert tracker.used == 0

    def test_use_decrements(self) -> None:
        tracker = MonthlyBudgetTracker(monthly_limit=100)
        tracker.use(10)
        assert tracker.remaining == 90
        assert tracker.used == 10

    def test_can_use(self) -> None:
        tracker = MonthlyBudgetTracker(monthly_limit=5)
        assert tracker.can_use(5) is True
        assert tracker.can_use(6) is False

    def test_budget_exhausted(self) -> None:
        tracker = MonthlyBudgetTracker(monthly_limit=3)
        tracker.use(3)
        assert tracker.can_use() is False
        assert tracker.remaining == 0


# =========================================================================
# Knowledge base
# =========================================================================


class TestTreatmentKnowledgeBase:
    """Test the treatment knowledge base."""

    def test_load_from_json(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        assert knowledge_base.is_loaded is True
        assert knowledge_base.count == 2

    def test_lookup_by_name(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        info = knowledge_base.lookup_by_name("보톡스")
        assert info is not None
        assert info.procedure_id == 1

    def test_lookup_by_alias(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        info = knowledge_base.lookup_by_name("Potenza")
        assert info is not None
        assert info.procedure_id == 2

    def test_lookup_case_insensitive(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        info = knowledge_base.lookup_by_name("POTENZA")
        assert info is not None

    def test_lookup_nonexistent(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        assert knowledge_base.lookup_by_name("없는시술") is None

    def test_japanese_to_korean_mapping(self) -> None:
        assert "ボトックス" in JAPANESE_TO_KOREAN
        assert JAPANESE_TO_KOREAN["ボトックス"] == "보톡스"
        assert "ポテンツァ" in JAPANESE_TO_KOREAN

    def test_concern_to_procedures_mapping(self) -> None:
        assert "毛穴" in CONCERN_TO_PROCEDURES
        procs = CONCERN_TO_PROCEDURES["毛穴"]
        assert "ポテンツァ" in procs
        assert "ダーマペン" in procs

    def test_get_classification_context(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        ctx = knowledge_base.get_classification_context()
        assert "ボトックス" in ctx
        assert "보톡스" in ctx
        assert "毛穴" in ctx

    def test_load_nonexistent_file(self, tmp_path: Path) -> None:
        kb = TreatmentKnowledgeBase()
        count = kb.load(tmp_path / "missing.json")
        assert count == 0
        assert kb.is_loaded is True


# =========================================================================
# Templates
# =========================================================================


class TestTemplateSelector:
    """Test template selection and rotation."""

    def test_get_reply_template(self) -> None:
        selector = TemplateSelector()
        template = selector.get_reply_template("hospital")
        assert template is not None
        assert template.category == "hospital"
        assert len(template.text) > 0

    def test_get_reply_template_unknown_returns_none(self) -> None:
        selector = TemplateSelector()
        assert selector.get_reply_template("Z") is None

    def test_get_reply_template_unknown_category(self) -> None:
        selector = TemplateSelector()
        assert selector.get_reply_template("nonexistent") is None

    def test_get_dm_template(self) -> None:
        selector = TemplateSelector()
        template = selector.get_dm_template("procedure")
        assert template is not None
        assert template.category == "procedure"
        assert "{施術名}" in template.text

    def test_rotation_increments_count(self) -> None:
        selector = TemplateSelector()
        t1 = selector.get_reply_template("hospital")
        assert t1 is not None
        assert t1.use_count == 1
        t2 = selector.get_reply_template("hospital")
        assert t2 is not None
        # With 2 templates in hospital, rotation should pick the other first
        assert t1.use_count + t2.use_count >= 2

    def test_get_categories(self) -> None:
        selector = TemplateSelector()
        reply_cats = selector.get_categories("reply")
        assert "hospital" in reply_cats
        assert "review" in reply_cats
        dm_cats = selector.get_categories("dm")
        assert "hospital" in dm_cats
        assert "complaint" in dm_cats


# =========================================================================
# Prompts
# =========================================================================


class TestPrompts:
    """Test prompt building functions."""

    def test_system_prompt_includes_context(self) -> None:
        prompt = build_classification_system_prompt("Test domain context here")
        assert "Test domain context here" in prompt
        assert "intent_type" in prompt
        assert "llm_decision" in prompt
        assert "hospital" in prompt

    def test_user_prompt_includes_data(self) -> None:
        prompt = build_classification_user_prompt(
            tweet_content="テスト",
            author_username="test_user",
            author_bio="test bio",
            follower_count=100,
            following_count=200,
            likes=5,
            retweets=1,
            replies=2,
        )
        assert "テスト" in prompt
        assert "test_user" in prompt
        assert "100" in prompt

    def test_user_prompt_no_bio(self) -> None:
        prompt = build_classification_user_prompt(
            tweet_content="test",
            author_username="user",
            author_bio="",
            follower_count=0,
            following_count=0,
            likes=0,
            retweets=0,
            replies=0,
        )
        assert "(no bio)" in prompt


# =========================================================================
# Action tracker
# =========================================================================


class TestActionTracker:
    """Test the action tracking module with mocked repository."""

    def _make_mock_repo(self) -> MagicMock:
        repo = MagicMock(spec=Repository)
        repo.record_action.return_value = 1
        repo.update_daily_stats.return_value = None
        repo.get_daily_stats.return_value = {
            "tweets_searched": 5,
            "tweets_collected": 10,
            "tweets_analyzed": 1,
            "replies_sent": 1,
            "dms_sent": 1,
            "dms_skipped": 1,
            "errors": 1,
        }
        return repo

    def test_record_search(self) -> None:
        repo = self._make_mock_repo()
        tracker = ActionTracker(repo)
        tracker.record_search("テスト", 5)
        repo.record_action.assert_called_once()
        repo.update_daily_stats.assert_called_once()

    def test_record_collect(self) -> None:
        repo = self._make_mock_repo()
        tracker = ActionTracker(repo)
        tracker.record_collect(stored=10, rejected=3)
        repo.record_action.assert_called_once()

    def test_record_error(self) -> None:
        repo = self._make_mock_repo()
        tracker = ActionTracker(repo)
        tracker.record_error("test", "Something broke")
        repo.record_action.assert_called_once_with(
            action_type="test",
            tweet_id=None,
            username=None,
            details=None,
            status="error",
            error_message="Something broke",
        )

    def test_log_summary_no_crash(self) -> None:
        repo = self._make_mock_repo()
        repo.get_daily_stats.return_value = None
        tracker = ActionTracker(repo)
        tracker.log_summary()  # Should not raise even with no data

    def test_record_analyze(self) -> None:
        repo = self._make_mock_repo()
        tracker = ActionTracker(repo)
        tracker.record_analyze("t1", "hospital", 0.9)
        repo.record_action.assert_called_once()

    def test_record_reply(self) -> None:
        repo = self._make_mock_repo()
        tracker = ActionTracker(repo)
        tracker.record_reply("t1", "user1")
        repo.record_action.assert_called_once()

    def test_record_dm(self) -> None:
        repo = self._make_mock_repo()
        tracker = ActionTracker(repo)
        tracker.record_dm("user1", "hospital")
        repo.record_action.assert_called_once()

    def test_record_dm_skip(self) -> None:
        repo = self._make_mock_repo()
        tracker = ActionTracker(repo)
        tracker.record_dm_skip("user1", "DM closed")
        repo.record_action.assert_called_once()

    def test_log_summary_with_data(self) -> None:
        repo = self._make_mock_repo()
        tracker = ActionTracker(repo)
        tracker.record_search("テスト", 3)
        tracker.record_collect(stored=2, rejected=1)
        tracker.log_summary()  # Should not raise


# =========================================================================
# Logger
# =========================================================================


class TestLogger:
    """Test the logger setup."""

    def test_setup_logging(self, tmp_path: Path) -> None:
        from outreach_shared.utils.logger import setup_logging

        log = setup_logging(
            level="DEBUG",
            log_dir=str(tmp_path / "logs"),
            project_root=tmp_path,
        )
        assert log is not None

    def test_get_logger_with_module(self) -> None:
        from outreach_shared.utils.logger import get_logger

        log = get_logger("test_module")
        assert log is not None

    def test_get_logger_without_module(self) -> None:
        from outreach_shared.utils.logger import get_logger

        log = get_logger()
        assert log is not None


# =========================================================================
# Time utils additional tests
# =========================================================================


class TestIsActiveHours:
    """Test the is_active_hours function."""

    def test_returns_bool(self) -> None:
        from outreach_shared.utils.time_utils import is_active_hours

        result = is_active_hours(0, 23)
        assert result is True  # Any hour between 0-23 is active

    def test_narrow_window(self) -> None:
        from outreach_shared.utils.time_utils import is_active_hours

        # This may or may not be true depending on current JST hour
        result = is_active_hours(0, 23)
        assert isinstance(result, bool)


class TestRandomDelay:
    """Test the random_delay async function."""

    @pytest.mark.asyncio
    async def test_returns_delay_value(self) -> None:
        from outreach_shared.utils.time_utils import random_delay

        delay = await random_delay(0.01, 0.02)
        assert 0.01 <= delay <= 0.02


# =========================================================================
# Knowledge base additional tests
# =========================================================================


class TestKnowledgeBaseEdgeCases:
    """Test knowledge base edge cases."""

    def test_lookup_by_japanese_known(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        info = knowledge_base.lookup_by_japanese("ボトックス")
        assert info is not None
        assert info.korean_name == "보톡스"

    def test_lookup_by_japanese_unknown(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        result = knowledge_base.lookup_by_japanese("存在しない施術")
        assert result is None

    def test_get_procedures_for_concern(self, knowledge_base: TreatmentKnowledgeBase) -> None:
        procs = knowledge_base.get_procedures_for_concern("毛穴")
        assert len(procs) > 0

    def test_get_procedures_for_unknown_concern(
        self, knowledge_base: TreatmentKnowledgeBase
    ) -> None:
        procs = knowledge_base.get_procedures_for_concern("不明")
        assert procs == []
