"""Tests for review sentiment analyzer."""

import pytest

from app.services.review_sentiment import (
    _analyze_sentiment,
    _detect_star_ratings,
    _extract_review_texts,
    _has_review_section,
    _is_review_page,
    _match_procedures,
    analyze_review_sentiment,
)


# ── Review page detection ────────────────────────────────────────────


class TestIsReviewPage:
    def test_review_in_url(self):
        assert _is_review_page("https://example.com/review", "<html></html>") is True

    def test_korean_review_in_url(self):
        assert _is_review_page("https://example.com/후기", "<html></html>") is True

    def test_testimonial_in_url(self):
        assert _is_review_page("https://example.com/testimonial", "<html></html>") is True

    def test_japanese_review_in_url(self):
        assert _is_review_page("https://example.com/口コミ", "<html></html>") is True

    def test_review_in_title(self):
        html = "<html><head><title>환자 후기 - 병원</title></head></html>"
        assert _is_review_page("https://example.com/page", html) is True

    def test_review_in_heading(self):
        html = "<html><body><h2>치료 후기</h2></body></html>"
        assert _is_review_page("https://example.com/page", html) is True

    def test_no_review_indicators(self):
        html = "<html><body><h2>시술 안내</h2></body></html>"
        assert _is_review_page("https://example.com/about", html) is False


# ── Review section detection ─────────────────────────────────────────


class TestHasReviewSection:
    def test_review_class(self):
        html = '<div class="review-list"><p>Great!</p></div>'
        assert _has_review_section(html) is True

    def test_testimonial_id(self):
        html = '<div id="testimonial-section"><p>Good clinic</p></div>'
        assert _has_review_section(html) is True

    def test_review_heading(self):
        html = "<h3>환자 후기</h3><p>만족합니다</p>"
        assert _has_review_section(html) is True

    def test_no_review_section(self):
        html = "<div class='about'><p>We are a clinic</p></div>"
        assert _has_review_section(html) is False


# ── Review text extraction ───────────────────────────────────────────


class TestExtractReviewTexts:
    def test_extract_from_review_class(self):
        html = """
        <div class="review-item">
            <p>보톡스 시술 받았는데 정말 만족합니다. 친절하고 효과도 좋아요.</p>
        </div>
        <div class="review-item">
            <p>대기시간이 좀 길었지만 결과는 만족스러워요.</p>
        </div>
        """
        reviews = _extract_review_texts(html)
        assert len(reviews) == 2

    def test_extract_from_heading_section(self):
        html = """
        <h2>환자 후기</h2>
        <p>리프팅 시술 후 자연스러운 결과에 만족합니다. 추천합니다!</p>
        <p>필러 시술도 좋았어요. 깔끔한 시술이었습니다.</p>
        <h2>시술 안내</h2>
        <p>This should not be extracted</p>
        """
        reviews = _extract_review_texts(html)
        assert len(reviews) == 2

    def test_extract_from_schema(self):
        html = """
        <script type="application/ld+json">
        {"@type": "Product", "review": [
            {"@type": "Review", "reviewBody": "Excellent treatment, very professional and natural results."},
            {"@type": "Review", "reviewBody": "Good experience overall, would recommend to others."}
        ]}
        </script>
        """
        reviews = _extract_review_texts(html)
        assert len(reviews) == 2

    def test_short_text_excluded(self):
        html = '<div class="review-item"><p>Good</p></div>'
        reviews = _extract_review_texts(html)
        assert len(reviews) == 0

    def test_empty_html(self):
        reviews = _extract_review_texts("")
        assert len(reviews) == 0


# ── Star rating detection ────────────────────────────────────────────


class TestDetectStarRatings:
    def test_aggregate_rating_schema(self):
        html = """
        <script type="application/ld+json">
        {"@type": "LocalBusiness", "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.5", "reviewCount": "23"}}
        </script>
        """
        has_stars, rating = _detect_star_ratings(html)
        assert has_stars is True
        assert rating == 4.5

    def test_text_rating_pattern(self):
        html = "<p>평균 평점: 4.2 / 5</p>"
        has_stars, rating = _detect_star_ratings(html)
        assert has_stars is True  # "평점" contains "rating" pattern match
        assert rating == 4.2

    def test_star_symbols(self):
        html = "<p>★★★★☆ 4.0점</p>"
        has_stars, _ = _detect_star_ratings(html)
        assert has_stars is True

    def test_no_ratings(self):
        html = "<p>Just some text</p>"
        has_stars, rating = _detect_star_ratings(html)
        assert has_stars is False
        assert rating is None


# ── Sentiment analysis ───────────────────────────────────────────────


class TestAnalyzeSentiment:
    def test_positive_korean(self):
        result = _analyze_sentiment("보톡스 시술 정말 만족합니다. 친절하고 효과도 좋아요.")
        assert result["sentiment"] == "positive"
        assert len(result["positive_keywords"]) > 0

    def test_negative_korean(self):
        result = _analyze_sentiment("대기시간이 너무 길고 불친절해서 불만입니다. 후회합니다.")
        assert result["sentiment"] == "negative"
        assert len(result["negative_keywords"]) > 0

    def test_positive_english(self):
        result = _analyze_sentiment("I'm very satisfied with the results. Highly recommend this clinic!")
        assert result["sentiment"] == "positive"

    def test_negative_english(self):
        result = _analyze_sentiment("Very disappointed with the treatment. It was painful and rude staff.")
        assert result["sentiment"] == "negative"

    def test_neutral_text(self):
        result = _analyze_sentiment("시술을 받았습니다. 일반적인 경험이었습니다.")
        assert result["sentiment"] == "neutral"

    def test_japanese_positive(self):
        result = _analyze_sentiment("施術の結果にとても満足しています。丁寧な対応でした。")
        assert result["sentiment"] == "positive"

    def test_mixed_sentiment(self):
        result = _analyze_sentiment("효과는 만족스러웠지만 대기시간이 길고 비싸서 아쉬웠습니다.")
        # Should have both positive and negative keywords
        assert len(result["positive_keywords"]) > 0
        assert len(result["negative_keywords"]) > 0


# ── Procedure matching ───────────────────────────────────────────────


class TestMatchProcedures:
    def test_botox_korean(self):
        procs = _match_procedures("보톡스 시술 후기입니다")
        assert "botox" in procs

    def test_filler_english(self):
        procs = _match_procedures("My filler treatment review")
        assert "filler" in procs

    def test_multiple_procedures(self):
        procs = _match_procedures("보톡스와 필러를 함께 받았습니다")
        assert "botox" in procs
        assert "filler" in procs

    def test_no_procedure(self):
        procs = _match_procedures("일반적인 피부 관리 후기")
        assert len(procs) == 0


# ── Full analysis ────────────────────────────────────────────────────


class TestAnalyzeReviewSentiment:
    def test_empty_pages(self):
        result = analyze_review_sentiment([])
        assert result["reviews_found"] == 0
        assert result["sentiment_score"] == 0
        assert result["has_review_section"] is False
        assert result["recommendations"] == []

    def test_no_reviews_found(self):
        html = "<html><body><h2>시술 안내</h2><p>보톡스 안내</p></body></html>"
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_review_sentiment(pages)
        assert result["reviews_found"] == 0
        assert result["has_review_section"] is False

    def test_page_with_reviews(self):
        html = """<html><body>
        <h2>환자 후기</h2>
        <div class="review-item">
            <p>보톡스 시술 정말 만족합니다. 친절하고 자연스러운 결과였어요. 추천!</p>
        </div>
        <div class="review-item">
            <p>필러 시술 효과가 좋았습니다. 깔끔하고 만족스러운 시술이었습니다.</p>
        </div>
        <div class="review-item">
            <p>리프팅 시술 받았는데 대기시간이 길고 좀 아팠습니다. 효과는 있었지만.</p>
        </div>
        </body></html>"""
        pages = [{"url": "https://example.com/review", "html": html}]
        result = analyze_review_sentiment(pages)
        assert result["reviews_found"] == 3
        assert result["has_review_section"] is True
        assert result["overall_sentiment"]["positive"] > 0
        assert result["sentiment_score"] > 0
        assert len(result["top_positive_keywords"]) > 0

    def test_review_with_star_rating(self):
        html = """<html><head>
        <script type="application/ld+json">
        {"@type": "LocalBusiness", "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.3"}}
        </script>
        </head><body>
        <h2>리뷰</h2>
        <div class="review-item">
            <p>만족스러운 시술이었습니다. 친절하고 효과가 좋아요. 재방문 의사 있습니다.</p>
        </div>
        </body></html>"""
        pages = [{"url": "https://example.com/review", "html": html}]
        result = analyze_review_sentiment(pages)
        assert result["has_star_ratings"] is True
        assert result["average_rating"] == 4.3

    def test_procedure_breakdown(self):
        html = """<html><body>
        <h2>환자 후기</h2>
        <div class="review-item">
            <p>보톡스 시술 만족합니다. 친절하고 추천해요!</p>
        </div>
        <div class="review-item">
            <p>보톡스 받았는데 대기시간 길고 불만입니다.</p>
        </div>
        <div class="review-item">
            <p>필러 시술 자연스럽고 최고였어요!</p>
        </div>
        </body></html>"""
        pages = [{"url": "https://example.com/review", "html": html}]
        result = analyze_review_sentiment(pages)
        assert "botox" in result["by_procedure"]
        assert "filler" in result["by_procedure"]
        assert result["by_procedure"]["botox"]["review_count"] == 2
        assert result["by_procedure"]["filler"]["review_count"] == 1

    def test_multi_page_aggregation(self):
        page1 = """<html><body>
        <h2>후기</h2>
        <div class="review-item"><p>만족합니다. 친절한 상담이 좋았어요.</p></div>
        </body></html>"""

        page2 = """<html><body>
        <h2>리뷰</h2>
        <div class="review-item"><p>추천합니다! 효과가 좋아요.</p></div>
        </body></html>"""

        pages = [
            {"url": "https://example.com/review1", "html": page1},
            {"url": "https://example.com/review2", "html": page2},
        ]
        result = analyze_review_sentiment(pages)
        assert result["reviews_found"] == 2
        assert result["has_review_section"] is True

    def test_recommendations_for_no_reviews(self):
        html = "<html><body><p>시술 안내 페이지</p></body></html>"
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_review_sentiment(pages)
        # Should have recommendation about missing review section
        messages = [r["message"] for r in result["recommendations"]]
        assert any("후기" in m or "리뷰" in m for m in messages)

    def test_recommendations_for_high_negative(self):
        html = """<html><body>
        <h2>후기</h2>
        <div class="review-item"><p>불만입니다. 불친절하고 후회합니다. 실망스러운 경험.</p></div>
        <div class="review-item"><p>효과없고 비싸서 후회합니다. 별로였어요.</p></div>
        <div class="review-item"><p>대기시간 길고 아팠습니다. 불친절해요.</p></div>
        </body></html>"""
        pages = [{"url": "https://example.com/review", "html": html}]
        result = analyze_review_sentiment(pages)
        assert result["overall_sentiment"]["negative"] > 0
        priorities = [r["priority"] for r in result["recommendations"]]
        assert "high" in priorities

    def test_score_range(self):
        html = """<html><body>
        <h2>후기</h2>
        <div class="review-item"><p>만족합니다. 친절하고 효과 좋아요. 추천!</p></div>
        </body></html>"""
        pages = [{"url": "https://example.com/review", "html": html}]
        result = analyze_review_sentiment(pages)
        assert 0 <= result["sentiment_score"] <= 100
