"""Review sentiment analyzer — keyword-based sentiment analysis for patient reviews."""

import re
from collections import Counter, defaultdict

from bs4 import BeautifulSoup

from .procedure_completeness import PROCEDURE_KEYWORDS, PROCEDURE_LABELS

# ── Sentiment keyword dictionaries (with weights) ────────────────────

POSITIVE_KEYWORDS: dict[str, dict[str, float]] = {
    "ko": {
        "만족": 1.0, "친절": 0.8, "추천": 1.0, "좋은": 0.7, "자연스러운": 0.9,
        "깔끔": 0.7, "통증없": 0.8, "효과": 0.8, "감사": 0.6, "재방문": 1.0,
        "최고": 0.9, "좋았": 0.7, "만족스러": 0.9, "편안": 0.7, "꼼꼼": 0.8,
    },
    "en": {
        "satisfied": 1.0, "recommend": 1.0, "excellent": 0.9, "natural": 0.8,
        "professional": 0.8, "painless": 0.7, "amazing": 0.9, "great": 0.7,
        "comfortable": 0.7, "happy": 0.8,
    },
    "ja": {
        "満足": 1.0, "自然": 0.8, "丁寧": 0.8, "おすすめ": 1.0, "痛くない": 0.7,
        "きれい": 0.7, "良い": 0.7,
    },
}

NEGATIVE_KEYWORDS: dict[str, dict[str, float]] = {
    "ko": {
        "불만": 1.0, "아프": 0.6, "대기시간": 0.7, "비싸": 0.6, "후회": 1.0,
        "효과없": 1.0, "재발": 0.8, "부작용": 0.7, "불친절": 0.9, "실망": 0.9,
        "아팠": 0.6, "비추": 1.0, "별로": 0.7,
    },
    "en": {
        "disappointed": 1.0, "painful": 0.6, "expensive": 0.6, "regret": 1.0,
        "no effect": 1.0, "rude": 0.9, "terrible": 1.0, "worst": 1.0,
        "waste": 0.8,
    },
    "ja": {
        "不満": 1.0, "痛い": 0.6, "高い": 0.5, "効果ない": 1.0, "後悔": 1.0,
    },
}

# ── Review page/section detection patterns ───────────────────────────

_REVIEW_URL_PATTERNS = re.compile(
    r"(review|후기|testimonial|口コミ|comment|voice|patients)", re.I,
)

_REVIEW_SECTION_KEYWORDS = re.compile(
    r"(후기|리뷰|환자\s*사례|치료\s*후기|이용\s*후기|고객\s*후기"
    r"|review|testimonial|patient\s*voice|口コミ|体験談|评价|患者の声)",
    re.I,
)

_REVIEW_CONTAINER_RE = re.compile(
    r"(review|comment|testimonial|voice|후기|리뷰)", re.I,
)

_STAR_PATTERNS = re.compile(r"(★|☆|⭐|star|rating|점|\bscore\b)", re.I)

_RATING_NUMBER_RE = re.compile(r"(\d(?:\.\d)?)\s*/\s*5")

# Precompiled patterns for sentiment keywords
_POSITIVE_PATTERNS: dict[str, list[tuple[re.Pattern, float]]] = {
    lang: [(re.compile(re.escape(kw), re.I), weight) for kw, weight in keywords.items()]
    for lang, keywords in POSITIVE_KEYWORDS.items()
}

_NEGATIVE_PATTERNS: dict[str, list[tuple[re.Pattern, float]]] = {
    lang: [(re.compile(re.escape(kw), re.I), weight) for kw, weight in keywords.items()]
    for lang, keywords in NEGATIVE_KEYWORDS.items()
}

# Precompiled procedure patterns for matching reviews to procedures
_PROCEDURE_PATTERNS: dict[str, re.Pattern] = {
    key: re.compile("|".join(re.escape(kw) for kw in keywords), re.I)
    for key, keywords in PROCEDURE_KEYWORDS.items()
}


def _extract_text(html: str) -> str:
    """Extract visible text from HTML, removing scripts and styles."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def _is_review_page(url: str, html: str) -> bool:
    """Check if a page is a review page based on URL and content."""
    if _REVIEW_URL_PATTERNS.search(url):
        return True
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    if title_tag and _REVIEW_SECTION_KEYWORDS.search(title_tag.get_text()):
        return True
    # Check headings
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if _REVIEW_SECTION_KEYWORDS.search(heading.get_text()):
            return True
    return False


def _has_review_section(html: str) -> bool:
    """Check if the page contains a review section."""
    soup = BeautifulSoup(html, "html.parser")
    # Check for review containers by class/id
    for el in soup.find_all(attrs={"class": _REVIEW_CONTAINER_RE}):
        return True
    for el in soup.find_all(attrs={"id": _REVIEW_CONTAINER_RE}):
        return True
    # Check headings for review keywords
    for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
        if _REVIEW_SECTION_KEYWORDS.search(heading.get_text()):
            return True
    return False


def _extract_review_texts(html: str) -> list[str]:
    """Extract individual review texts from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    reviews: list[str] = []

    # Strategy 1: Find review containers by class/id
    containers = soup.find_all(attrs={"class": _REVIEW_CONTAINER_RE})
    containers += soup.find_all(attrs={"id": _REVIEW_CONTAINER_RE})

    for container in containers:
        text = container.get_text(separator=" ", strip=True)
        if len(text) >= 10:
            reviews.append(text)

    # Strategy 2: If no containers found, find sections after review headings
    if not reviews:
        for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
            if _REVIEW_SECTION_KEYWORDS.search(heading.get_text()):
                # Collect text from siblings until next heading
                for sibling in heading.find_next_siblings():
                    if sibling.name in ("h1", "h2", "h3", "h4"):
                        break
                    text = sibling.get_text(separator=" ", strip=True)
                    if len(text) >= 10:
                        reviews.append(text)

    # Strategy 3: Check structured data (Review schema)
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            import json
            data = json.loads(script.string or "")
            if isinstance(data, list):
                for item in data:
                    _extract_schema_reviews(item, reviews)
            elif isinstance(data, dict):
                _extract_schema_reviews(data, reviews)
        except (json.JSONDecodeError, TypeError):
            pass

    return reviews


def _extract_schema_reviews(data: dict, reviews: list[str]) -> None:
    """Extract review text from structured data."""
    if not isinstance(data, dict):
        return
    # Direct Review type
    if data.get("@type") == "Review":
        body = data.get("reviewBody", "")
        if body and len(body) >= 10:
            reviews.append(body)
    # AggregateRating or Review list
    for review in data.get("review", []):
        if isinstance(review, dict):
            body = review.get("reviewBody", "")
            if body and len(body) >= 10:
                reviews.append(body)
    # @graph
    for item in data.get("@graph", []):
        _extract_schema_reviews(item, reviews)


def _detect_star_ratings(html: str) -> tuple[bool, float | None]:
    """Detect star ratings in HTML. Returns (has_ratings, average_rating)."""
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    has_stars = bool(_STAR_PATTERNS.search(text))

    # Try to extract numeric rating from structured data
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            import json
            data = json.loads(script.string or "")
            rating = _find_aggregate_rating(data)
            if rating is not None:
                return True, rating
        except (json.JSONDecodeError, TypeError):
            pass

    # Try to extract from text patterns like "4.5/5"
    matches = _RATING_NUMBER_RE.findall(text)
    if matches:
        ratings = [float(m) for m in matches if 0 <= float(m) <= 5]
        if ratings:
            return True, round(sum(ratings) / len(ratings), 1)

    return has_stars, None


def _find_aggregate_rating(data) -> float | None:
    """Recursively find AggregateRating in structured data."""
    if isinstance(data, list):
        for item in data:
            result = _find_aggregate_rating(item)
            if result is not None:
                return result
    elif isinstance(data, dict):
        if data.get("@type") == "AggregateRating":
            val = data.get("ratingValue")
            if val is not None:
                try:
                    return round(float(val), 1)
                except (ValueError, TypeError):
                    pass
        # Check nested
        for key in ("aggregateRating", "@graph", "review"):
            if key in data:
                result = _find_aggregate_rating(data[key])
                if result is not None:
                    return result
    return None


def _analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of a single review text. Returns scores and matched keywords."""
    positive_score = 0.0
    negative_score = 0.0
    positive_matches: list[str] = []
    negative_matches: list[str] = []

    for lang_patterns in _POSITIVE_PATTERNS.values():
        for pattern, weight in lang_patterns:
            if pattern.search(text):
                positive_score += weight
                positive_matches.append(pattern.pattern.replace("\\", ""))

    for lang_patterns in _NEGATIVE_PATTERNS.values():
        for pattern, weight in lang_patterns:
            if pattern.search(text):
                negative_score += weight
                negative_matches.append(pattern.pattern.replace("\\", ""))

    total = positive_score + negative_score
    if total == 0:
        return {"sentiment": "neutral", "positive_keywords": [], "negative_keywords": []}

    if positive_score > negative_score * 1.2:
        sentiment = "positive"
    elif negative_score > positive_score * 1.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "positive_keywords": positive_matches,
        "negative_keywords": negative_matches,
    }


def _match_procedures(text: str) -> list[str]:
    """Match review text to procedure types."""
    found = []
    for proc_key, pattern in _PROCEDURE_PATTERNS.items():
        if pattern.search(text):
            found.append(proc_key)
    return found


def analyze_review_sentiment(pages: list[dict]) -> dict:
    """Analyze patient review sentiment from crawled pages.

    Args:
        pages: List of crawled page dicts with keys: url, html

    Returns:
        Analysis result with sentiment scores, keywords, procedure breakdown, etc.
    """
    if not pages:
        return _empty_result()

    all_reviews: list[str] = []
    has_review_section = False
    has_star_ratings = False
    all_ratings: list[float] = []

    for page in pages:
        url = page.get("url", "")
        html = page.get("html", "")

        is_review = _is_review_page(url, html)
        has_section = _has_review_section(html)
        if is_review or has_section:
            has_review_section = True

        # Extract reviews from review pages/sections
        if is_review or has_section:
            reviews = _extract_review_texts(html)
            all_reviews.extend(reviews)

        # Detect star ratings
        stars, rating = _detect_star_ratings(html)
        if stars:
            has_star_ratings = True
        if rating is not None:
            all_ratings.append(rating)

    if not all_reviews:
        # Even without explicit reviews, check for review indicators
        return {
            "reviews_found": 0,
            "has_review_section": has_review_section,
            "has_star_ratings": has_star_ratings,
            "average_rating": round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else None,
            "overall_sentiment": {"positive": 0, "neutral": 0, "negative": 0},
            "top_positive_keywords": [],
            "top_negative_keywords": [],
            "by_procedure": {},
            "sentiment_score": 0,
            "recommendations": _generate_no_review_recommendations(has_review_section),
        }

    # Analyze each review
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    all_positive_keywords: list[str] = []
    all_negative_keywords: list[str] = []
    procedure_sentiments: dict[str, dict] = defaultdict(lambda: {
        "positive": 0, "neutral": 0, "negative": 0, "review_count": 0,
    })

    for review_text in all_reviews:
        result = _analyze_sentiment(review_text)
        sentiment = result["sentiment"]

        if sentiment == "positive":
            positive_count += 1
        elif sentiment == "negative":
            negative_count += 1
        else:
            neutral_count += 1

        all_positive_keywords.extend(result["positive_keywords"])
        all_negative_keywords.extend(result["negative_keywords"])

        # Match to procedures
        procs = _match_procedures(review_text)
        for proc in procs:
            procedure_sentiments[proc]["review_count"] += 1
            procedure_sentiments[proc][sentiment] += 1

    total_reviews = len(all_reviews)

    # Calculate percentages
    overall_sentiment = {
        "positive": round(positive_count / total_reviews * 100) if total_reviews else 0,
        "neutral": round(neutral_count / total_reviews * 100) if total_reviews else 0,
        "negative": round(negative_count / total_reviews * 100) if total_reviews else 0,
    }

    # Top keywords
    pos_counter = Counter(all_positive_keywords)
    neg_counter = Counter(all_negative_keywords)
    top_positive = [{"keyword": kw, "count": cnt} for kw, cnt in pos_counter.most_common(10)]
    top_negative = [{"keyword": kw, "count": cnt} for kw, cnt in neg_counter.most_common(10)]

    # Procedure breakdown with percentages
    by_procedure: dict[str, dict] = {}
    for proc_key, data in procedure_sentiments.items():
        rc = data["review_count"]
        if rc == 0:
            continue
        by_procedure[proc_key] = {
            "name": PROCEDURE_LABELS.get(proc_key, proc_key),
            "positive": round(data["positive"] / rc * 100),
            "neutral": round(data["neutral"] / rc * 100),
            "negative": round(data["negative"] / rc * 100),
            "review_count": rc,
        }

    # Overall sentiment score (0-100)
    sentiment_score = _calculate_sentiment_score(
        overall_sentiment, has_star_ratings, all_ratings, total_reviews,
    )

    # Recommendations
    recommendations = _generate_recommendations(
        overall_sentiment, by_procedure, top_negative, total_reviews,
        has_review_section, has_star_ratings,
    )

    return {
        "reviews_found": total_reviews,
        "has_review_section": has_review_section,
        "has_star_ratings": has_star_ratings,
        "average_rating": round(sum(all_ratings) / len(all_ratings), 1) if all_ratings else None,
        "overall_sentiment": overall_sentiment,
        "top_positive_keywords": top_positive,
        "top_negative_keywords": top_negative,
        "by_procedure": by_procedure,
        "sentiment_score": sentiment_score,
        "recommendations": recommendations,
    }


def _empty_result() -> dict:
    return {
        "reviews_found": 0,
        "has_review_section": False,
        "has_star_ratings": False,
        "average_rating": None,
        "overall_sentiment": {"positive": 0, "neutral": 0, "negative": 0},
        "top_positive_keywords": [],
        "top_negative_keywords": [],
        "by_procedure": {},
        "sentiment_score": 0,
        "recommendations": [],
    }


def _calculate_sentiment_score(
    overall_sentiment: dict,
    has_star_ratings: bool,
    all_ratings: list[float],
    total_reviews: int,
) -> int:
    """Calculate overall sentiment score (0-100)."""
    if total_reviews == 0:
        return 0

    # Base score from positive ratio
    base = overall_sentiment["positive"]

    # Bonus for star ratings
    if has_star_ratings and all_ratings:
        avg = sum(all_ratings) / len(all_ratings)
        rating_bonus = (avg / 5.0) * 20  # up to 20 points
        base = base * 0.7 + rating_bonus + 10  # weighted blend

    # Penalty for high negative ratio
    neg_ratio = overall_sentiment["negative"]
    if neg_ratio > 30:
        base -= (neg_ratio - 30) * 0.5

    return max(0, min(100, round(base)))


def _generate_no_review_recommendations(has_review_section: bool) -> list[dict]:
    """Generate recommendations when no reviews are found."""
    recs = []
    if not has_review_section:
        recs.append({
            "priority": "high",
            "message": "환자 후기/리뷰 섹션이 없습니다. 실제 치료 경험을 공유하는 리뷰 페이지를 추가하세요.",
        })
    recs.append({
        "priority": "medium",
        "message": "Review 구조화 데이터(Schema.org)를 추가하면 검색 결과에 별점이 표시됩니다.",
    })
    return recs


def _generate_recommendations(
    overall_sentiment: dict,
    by_procedure: dict,
    top_negative: list[dict],
    total_reviews: int,
    has_review_section: bool,
    has_star_ratings: bool,
) -> list[dict]:
    """Generate actionable recommendations based on sentiment analysis."""
    recs: list[dict] = []

    # High negative sentiment overall
    if overall_sentiment["negative"] > 30:
        recs.append({
            "priority": "high",
            "message": f"부정적 리뷰 비율이 {overall_sentiment['negative']}%로 높습니다. "
                       "주요 불만 요인을 파악하고 개선이 필요합니다.",
        })

    # Procedure-specific negative sentiment
    for proc_key, data in sorted(
        by_procedure.items(), key=lambda x: x[1]["negative"], reverse=True,
    ):
        if data["negative"] > 25 and data["review_count"] >= 3:
            recs.append({
                "priority": "high",
                "message": f"{data['name']} 시술 후기에서 부정적 감성이 {data['negative']}%로 높습니다. "
                           "불만 요인을 확인하세요.",
            })

    # Repeated negative keywords
    for kw_data in top_negative[:3]:
        if kw_data["count"] >= 3:
            recs.append({
                "priority": "medium",
                "message": f"'{kw_data['keyword']}' 관련 불만이 {kw_data['count']}회 반복됩니다.",
            })

    # Missing star ratings
    if not has_star_ratings and total_reviews > 0:
        recs.append({
            "priority": "medium",
            "message": "별점/평점 시스템을 도입하면 신뢰도가 향상됩니다.",
        })

    # Few reviews
    if 0 < total_reviews < 5:
        recs.append({
            "priority": "medium",
            "message": f"리뷰가 {total_reviews}개로 적습니다. 환자 후기를 적극적으로 수집하세요.",
        })

    # Missing review section
    if not has_review_section:
        recs.append({
            "priority": "high",
            "message": "환자 후기/리뷰 섹션이 없습니다. 리뷰 페이지를 추가하면 전환율이 향상됩니다.",
        })

    # Good sentiment encouragement
    if overall_sentiment["positive"] >= 70 and total_reviews >= 5:
        recs.append({
            "priority": "low",
            "message": f"긍정적 리뷰 비율이 {overall_sentiment['positive']}%로 우수합니다. "
                       "리뷰를 마케팅에 적극 활용하세요.",
        })

    return recs
