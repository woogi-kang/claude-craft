"""Tests for video presence analyzer."""

import pytest

from app.services.video_presence import (
    SOCIAL_PATTERNS,
    VIDEO_EMBED_PATTERNS,
    _check_video_metadata,
    _detect_social_profiles,
    _extract_embedded_videos,
    analyze_video_presence,
)


# ── Embedded video detection ──────────────────────────────────────────────


class TestExtractEmbeddedVideos:
    def test_youtube_iframe(self):
        html = '<iframe src="https://www.youtube.com/embed/abc123" frameborder="0"></iframe>'
        result = _extract_embedded_videos(html)
        assert result["youtube"]["count"] == 1
        assert "youtube.com/embed/abc123" in result["youtube"]["urls"][0]

    def test_naver_tv_iframe(self):
        html = '<iframe src="https://tv.naver.com/embed/12345"></iframe>'
        result = _extract_embedded_videos(html)
        assert result["naver_tv"]["count"] == 1

    def test_vimeo_iframe(self):
        html = '<iframe src="https://player.vimeo.com/video/12345"></iframe>'
        result = _extract_embedded_videos(html)
        assert result["vimeo"]["count"] == 1

    def test_self_hosted_video(self):
        html = '<video src="/videos/surgery-intro.mp4" controls></video>'
        result = _extract_embedded_videos(html)
        assert result["self_hosted"]["count"] == 1
        assert "/videos/surgery-intro.mp4" in result["self_hosted"]["urls"][0]

    def test_self_hosted_video_with_source(self):
        html = '<video controls><source src="/media/clip.mp4" type="video/mp4"></video>'
        result = _extract_embedded_videos(html)
        assert result["self_hosted"]["count"] >= 1

    def test_no_videos(self):
        html = "<html><body><p>No videos here</p></body></html>"
        result = _extract_embedded_videos(html)
        for platform in VIDEO_EMBED_PATTERNS:
            assert result[platform]["count"] == 0

    def test_multiple_youtube_embeds(self):
        html = """
        <iframe src="https://www.youtube.com/embed/abc123"></iframe>
        <iframe src="https://www.youtube.com/embed/def456"></iframe>
        <iframe src="https://www.youtube.com/embed/ghi789"></iframe>
        """
        result = _extract_embedded_videos(html)
        assert result["youtube"]["count"] == 3


# ── Social profile detection ──────────────────────────────────────────────


class TestDetectSocialProfiles:
    def test_youtube_channel(self):
        html = '<a href="https://youtube.com/@hospital_clinic">YouTube</a>'
        result = _detect_social_profiles(html)
        assert result["youtube"]["found"] is True

    def test_instagram(self):
        html = '<a href="https://instagram.com/hospital_clinic">Instagram</a>'
        result = _detect_social_profiles(html)
        assert result["instagram"]["found"] is True

    def test_tiktok(self):
        html = '<a href="https://tiktok.com/@hospital_clinic">TikTok</a>'
        result = _detect_social_profiles(html)
        assert result["tiktok"]["found"] is True

    def test_facebook_profile(self):
        html = '<a href="https://facebook.com/hospitalclinic">Facebook</a>'
        result = _detect_social_profiles(html)
        assert result["facebook"]["found"] is True

    def test_facebook_share_excluded(self):
        html = '<a href="https://facebook.com/sharer/sharer.php?u=test">Share</a>'
        result = _detect_social_profiles(html)
        assert result["facebook"]["found"] is False

    def test_naver_blog(self):
        html = '<a href="https://blog.naver.com/hospital123">블로그</a>'
        result = _detect_social_profiles(html)
        assert result["naver_blog"]["found"] is True

    def test_xiaohongshu(self):
        html = '<a href="https://www.xiaohongshu.com/user/profile/12345">小红书</a>'
        result = _detect_social_profiles(html)
        assert result["xiaohongshu"]["found"] is True

    def test_xhslink(self):
        html = '<a href="https://xhslink.com/abc123">小红书</a>'
        result = _detect_social_profiles(html)
        assert result["xiaohongshu"]["found"] is True

    def test_twitter_x(self):
        html = '<a href="https://x.com/hospital">X</a>'
        result = _detect_social_profiles(html)
        assert result["twitter"]["found"] is True

    def test_twitter_intent_excluded(self):
        html = '<a href="https://twitter.com/intent/tweet?text=hello">Tweet</a>'
        result = _detect_social_profiles(html)
        assert result["twitter"]["found"] is False

    def test_no_social_profiles(self):
        html = "<html><body><a href='/about'>About</a></body></html>"
        result = _detect_social_profiles(html)
        for platform in SOCIAL_PATTERNS:
            assert result[platform]["found"] is False


# ── Metadata detection ────────────────────────────────────────────────────


class TestVideoMetadata:
    def test_og_video(self):
        html = '<meta property="og:video" content="https://example.com/video.mp4">'
        result = _check_video_metadata(html)
        assert result["has_og_video"] is True

    def test_video_schema(self):
        html = '{"@type": "VideoObject", "name": "test"}'
        result = _check_video_metadata(html)
        assert result["has_video_schema"] is True

    def test_no_metadata(self):
        html = "<html><body>plain</body></html>"
        result = _check_video_metadata(html)
        assert result["has_og_video"] is False
        assert result["has_video_schema"] is False


# ── Full analysis ─────────────────────────────────────────────────────────


class TestAnalyzeVideoPresence:
    def test_empty_pages(self):
        result = analyze_video_presence([])
        assert result["total_videos"] == 0
        assert result["social_count"] == 0
        assert result["video_score"] == 0
        assert result["social_score"] == 0
        assert result["overall_score"] == 0

    def test_full_video_presence(self):
        html = """
        <html>
        <head>
            <meta property="og:video" content="https://example.com/video.mp4">
        </head>
        <body>
            <iframe src="https://www.youtube.com/embed/abc123"></iframe>
            <iframe src="https://www.youtube.com/embed/def456"></iframe>
            <iframe src="https://www.youtube.com/embed/ghi789"></iframe>
            <video src="/videos/intro.mp4" controls></video>
            <a href="https://youtube.com/@hospital">YouTube</a>
            <a href="https://instagram.com/hospital">Instagram</a>
            <a href="https://tiktok.com/@hospital">TikTok</a>
            <a href="https://facebook.com/hospital">Facebook</a>
            <a href="https://blog.naver.com/hospital">블로그</a>
            <script type="application/ld+json">{"@type": "VideoObject"}</script>
        </body>
        </html>
        """
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        assert result["total_videos"] >= 4
        assert result["social_count"] >= 5
        assert result["video_score"] == 100
        assert result["social_score"] >= 75
        assert result["overall_score"] >= 80

    def test_no_video_no_social(self):
        html = "<html><body><p>Plain hospital website</p></body></html>"
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        assert result["total_videos"] == 0
        assert result["social_count"] == 0
        assert result["video_score"] == 0
        assert result["social_score"] == 0
        assert len(result["missing_platforms"]) > 0
        assert len(result["recommendations"]) > 0

    def test_scoring_video_exists(self):
        html = '<iframe src="https://www.youtube.com/embed/abc123"></iframe>'
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        # Video exists = 30 points minimum
        assert result["video_score"] >= 30

    def test_scoring_three_plus_videos(self):
        html = """
        <iframe src="https://www.youtube.com/embed/a"></iframe>
        <iframe src="https://www.youtube.com/embed/b"></iframe>
        <iframe src="https://www.youtube.com/embed/c"></iframe>
        """
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        # Video exists (30) + 3+ videos (15) = 45
        assert result["video_score"] >= 45

    def test_social_bonus_tiktok(self):
        html = """
        <a href="https://tiktok.com/@hospital">TikTok</a>
        <a href="https://instagram.com/hospital">Instagram</a>
        """
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        # 2 profiles * 15 = 30, plus TikTok bonus +10 = 40
        assert result["social_score"] == 40

    def test_social_bonus_xiaohongshu(self):
        html = '<a href="https://www.xiaohongshu.com/user/profile/123">小红书</a>'
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        # 1 profile * 15 = 15, plus Xiaohongshu bonus +10 = 25
        assert result["social_score"] == 25

    def test_overall_score_weighted(self):
        html = """
        <iframe src="https://www.youtube.com/embed/abc"></iframe>
        <a href="https://instagram.com/hospital">Instagram</a>
        """
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        expected_overall = round(result["video_score"] * 0.5 + result["social_score"] * 0.5)
        assert result["overall_score"] == expected_overall

    def test_missing_platforms_includes_tiktok(self):
        html = "<html><body>no social</body></html>"
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        platform_names = [p["platform"] for p in result["missing_platforms"]]
        assert "TikTok" in platform_names
        assert "小红书" in platform_names

    def test_recommendations_for_no_videos(self):
        html = "<html><body>plain</body></html>"
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        assert any("영상 콘텐츠가 없습니다" in r["message"] for r in result["recommendations"])

    def test_multiple_pages_aggregate(self):
        page1 = {
            "url": "https://example.com",
            "html": '<iframe src="https://www.youtube.com/embed/abc"></iframe>',
        }
        page2 = {
            "url": "https://example.com/about",
            "html": '<a href="https://instagram.com/hospital">IG</a><video src="/v.mp4"></video>',
        }
        result = analyze_video_presence([page1, page2])

        assert result["embedded_videos"]["youtube"]["count"] >= 1
        assert result["embedded_videos"]["self_hosted"]["count"] >= 1
        assert result["social_profiles"]["instagram"]["found"] is True

    def test_result_structure(self):
        pages = [{"url": "https://example.com", "html": "<html></html>"}]
        result = analyze_video_presence(pages)

        assert "embedded_videos" in result
        assert "total_videos" in result
        assert "social_profiles" in result
        assert "social_count" in result
        assert "has_video_schema" in result
        assert "has_og_video" in result
        assert "video_score" in result
        assert "social_score" in result
        assert "overall_score" in result
        assert "missing_platforms" in result
        assert "recommendations" in result

    def test_video_schema_recommendation(self):
        html = '<iframe src="https://www.youtube.com/embed/abc"></iframe>'
        pages = [{"url": "https://example.com", "html": html}]
        result = analyze_video_presence(pages)

        assert any("VideoObject Schema" in r["message"] for r in result["recommendations"])
