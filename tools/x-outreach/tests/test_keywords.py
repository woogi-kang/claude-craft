"""Tests for the keyword pre-filter system."""

from __future__ import annotations

from src.ai.keywords import (
    EXCLUDE_KEYWORDS,
    KeywordMatch,
    check_exclude,
    match_category,
)


class TestCheckExclude:
    """Test the exclude keyword checker."""

    def test_no_match(self) -> None:
        result = check_exclude("韓国でボトックス打ってきた！")
        assert not result.matched
        assert not result.excluded

    def test_campaign_excluded(self) -> None:
        result = check_exclude("キャンペーン実施中！ボトックス50%OFF")
        assert result.matched
        assert result.excluded
        assert result.keyword == "キャンペーン実施中"

    def test_pr_excluded(self) -> None:
        result = check_exclude("この投稿は #PR です")
        assert result.matched
        assert result.excluded

    def test_bot_excluded(self) -> None:
        result = check_exclude("フォロバ100%します！プロフ見て")
        assert result.matched
        assert result.excluded

    def test_crypto_excluded(self) -> None:
        result = check_exclude("仮想通貨で稼ごう")
        assert result.matched
        assert result.excluded

    def test_case_insensitive(self) -> None:
        # Japanese keywords are case-insensitive (though most are kana)
        result = check_exclude("これは#ADです")
        assert result.matched
        assert result.excluded

    def test_exclude_keywords_not_empty(self) -> None:
        assert len(EXCLUDE_KEYWORDS) > 0


class TestMatchCategory:
    """Test the category keyword matcher."""

    def test_hospital_match(self) -> None:
        result = match_category("韓国の皮膚科 おすすめある？")
        assert result.matched
        assert result.category == "hospital"

    def test_price_match(self) -> None:
        result = match_category("ボトックス3000円だった")
        assert result.matched
        assert result.category == "price"

    def test_procedure_match(self) -> None:
        result = match_category("ポテンツァ受けてきた！効果すごい")
        assert result.matched
        assert result.category == "procedure"

    def test_complaint_match(self) -> None:
        result = match_category("失敗して後悔してる。最悪だった")
        assert result.matched
        assert result.category == "complaint"

    def test_review_match(self) -> None:
        result = match_category("韓国の皮膚科行ってきた口コミ")
        assert result.matched
        assert result.category == "review"

    def test_no_match(self) -> None:
        result = match_category("今日はいい天気だね")
        assert not result.matched
        assert result.category is None

    def test_exclude_takes_priority(self) -> None:
        result = match_category("キャンペーン実施中！ボトックス安い！")
        assert result.matched
        assert result.excluded
        assert result.category is None

    def test_first_category_wins(self) -> None:
        # "皮膚科 おすすめ" matches hospital, even though
        # "行ってきた" could match review
        result = match_category("皮膚科 おすすめの韓国クリニック行ってきた")
        assert result.matched
        assert result.category == "hospital"

    def test_pain_complaint(self) -> None:
        result = match_category("ポテンツァ受けてきたけど痛すぎて泣いた")
        assert result.matched
        # procedure comes first in priority order
        assert result.category == "procedure"

    def test_keyword_match_dataclass(self) -> None:
        m = KeywordMatch(matched=True, category="price", keyword="安い")
        assert m.matched
        assert m.category == "price"
        assert m.keyword == "安い"
        assert not m.excluded
