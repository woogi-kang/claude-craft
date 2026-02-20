"""Japanese keyword lists for pre-filtering tweets before LLM classification.

Provides include/exclude keyword matching to quickly route obvious tweets
to categories without an LLM call, and to reject spam/irrelevant content
at the code level.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KeywordMatch:
    """Result of keyword-based pre-filtering."""

    matched: bool
    category: str | None = None  # hospital/price/procedure/complaint/review
    keyword: str | None = None  # The keyword that triggered the match
    excluded: bool = False  # True if an exclude keyword matched


# ---------------------------------------------------------------------------
# Exclude keywords -- tweets matching these are immediately irrelevant.
# ---------------------------------------------------------------------------

EXCLUDE_KEYWORDS: list[str] = [
    # Clinic marketing / official accounts
    "公式アカウント",
    "公式サイト",
    "キャンペーン実施中",
    "モニター募集",
    "初回限定",
    "カウンセリング無料",
    "ご予約はDMまで",
    "ご予約はこちら",
    "期間限定",
    "LINE登録",
    "LINE予約",
    "PR",
    "プロモーション",
    "広告",
    "#ad",
    "#PR",
    "提供",
    # Bot / spam
    "フォロバ100",
    "相互フォロー",
    "固定ツイ見て",
    "プロフ見て",
    "リンク先",
    # Unrelated content
    "転売",
    "仮想通貨",
    "FX",
    "ビットコイン",
    "NFT",
    "投資",
]

# ---------------------------------------------------------------------------
# Category keywords -- tweets matching these get a keyword-based category.
# Order matters: first match wins.
# ---------------------------------------------------------------------------

# hospital: clinic recommendations, clinic search, clinic comparison
HOSPITAL_KEYWORDS: list[str] = [
    "クリニック おすすめ",
    "クリニック選び",
    "皮膚科 おすすめ",
    "皮膚科 どこ",
    "病院 おすすめ",
    "クリニック 比較",
    "クリニック 探し",
    "クリニック どこ",
    "皮膚科 選び",
    "皮膚科 比較",
    "どこのクリニック",
    "どこの皮膚科",
    "日本語対応",
    "日本語OK",
    "初めて行く",
    "初めての韓国",
    "初渡韓",
]

# price: cost sharing, price comparison, budget questions
PRICE_KEYWORDS: list[str] = [
    "円だった",
    "万円",
    "ウォン",
    "安い",
    "安かった",
    "高い",
    "高かった",
    "値段",
    "料金",
    "費用",
    "価格",
    "相場",
    "コスパ",
    "割引",
    "半額",
    "%OFF",
    "いくら",
    "予算",
]

# procedure: treatment experience, treatment questions
PROCEDURE_KEYWORDS: list[str] = [
    "ボトックス",
    "フィラー",
    "ヒアルロン酸",
    "ポテンツァ",
    "ピコレーザー",
    "ピコトーニング",
    "ダーマペン",
    "リジュラン",
    "水光注射",
    "ハイフ",
    "シュリンク",
    "ウルセラ",
    "レーザートーニング",
    "フラクショナル",
    "シミ取り",
    "肌管理",
    "エラボトックス",
    "涙袋",
    "糸リフト",
    "脂肪溶解",
    "スキンボトックス",
    "受けてきた",
    "打ってきた",
    "やってきた",
    "施術",
    "ダウンタイム",
    "効果",
    "仕上がり",
    "経過",
    "ビフォーアフター",
    "ビフォアフ",
    "BA写真",
]

# complaint: negative experiences, problems, warnings
COMPLAINT_KEYWORDS: list[str] = [
    "失敗",
    "後悔",
    "やばい",
    "ひどい",
    "最悪",
    "不自然",
    "腫れ",
    "痛い",
    "痛すぎ",
    "泣いた",
    "怖い",
    "トラブル",
    "クレーム",
    "返金",
    "やり直し",
    "対応が悪い",
    "不安",
    "心配",
    "ぼったくり",
    "アップセル",
    "追加料金",
    "騙された",
    "言語の壁",
]

# review: general reviews, experience sharing, opinions
REVIEW_KEYWORDS: list[str] = [
    "口コミ",
    "レビュー",
    "体験談",
    "レポ",
    "感想",
    "行ってきた",
    "行ってみた",
    "通ってる",
    "リピート",
    "おすすめ",
    "良かった",
    "よかった",
    "満足",
    "経験",
    "実体験",
]

# Mapping from category to keyword list
_CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "hospital": HOSPITAL_KEYWORDS,
    "price": PRICE_KEYWORDS,
    "procedure": PROCEDURE_KEYWORDS,
    "complaint": COMPLAINT_KEYWORDS,
    "review": REVIEW_KEYWORDS,
}


def check_exclude(text: str) -> KeywordMatch:
    """Check if text contains any exclude keywords.

    Parameters
    ----------
    text:
        Tweet content to check.

    Returns
    -------
    KeywordMatch
        With ``excluded=True`` if an exclude keyword was found.
    """
    text_lower = text.lower()
    for kw in EXCLUDE_KEYWORDS:
        if kw.lower() in text_lower:
            return KeywordMatch(matched=True, excluded=True, keyword=kw)
    return KeywordMatch(matched=False)


def match_category(text: str) -> KeywordMatch:
    """Match text against category keywords.

    Checks exclude list first, then tries each category in priority
    order.  Returns the first category match found.

    Parameters
    ----------
    text:
        Tweet content to classify.

    Returns
    -------
    KeywordMatch
        Category match result. ``matched=False`` means no keyword hit.
    """
    # Check excludes first
    exclude_result = check_exclude(text)
    if exclude_result.excluded:
        return exclude_result

    text_lower = text.lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return KeywordMatch(
                    matched=True,
                    category=category,
                    keyword=kw,
                )

    return KeywordMatch(matched=False)
