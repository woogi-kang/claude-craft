"""Tests for URL utility functions: classify_url, strip_tracking, normalize_url."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from clinic_crawler.url_utils import classify_url, normalize_url, strip_tracking

# ============================================================================
# classify_url
# ============================================================================

class TestClassifyUrl:
    # -- KakaoTalk --
    def test_kakao_pf(self):
        assert classify_url("https://pf.kakao.com/_abc123") == "KakaoTalk"

    def test_kakao_open(self):
        assert classify_url("https://open.kakao.com/o/xyz789") == "KakaoTalk"

    def test_kakao_talk(self):
        assert classify_url("https://talk.kakao.com/channel") == "KakaoTalk"

    # -- Naver --
    def test_naver_talk(self):
        assert classify_url("https://talk.naver.com/ct/abcdef") == "NaverTalk"

    def test_naver_shortlink(self):
        assert classify_url("https://naver.me/abc123") == "NaverShortlink"

    def test_naver_booking(self):
        assert classify_url("https://booking.naver.com/booking/6/bizes/12345") == "NaverBooking"

    def test_naver_blog(self):
        assert classify_url("https://blog.naver.com/clinic_name") == "NaverBlog"

    def test_naver_cafe(self):
        assert classify_url("https://cafe.naver.com/clinicname") == "NaverCafe"

    def test_naver_map(self):
        assert classify_url("https://map.naver.com/v5/entry/place/12345") == "NaverMap"

    # -- Other platforms --
    def test_line(self):
        assert classify_url("https://line.me/ti/p/@clinic") == "Line"

    def test_line_short(self):
        assert classify_url("https://lin.ee/abc123") == "Line"

    def test_whatsapp(self):
        assert classify_url("https://wa.me/821012345678") == "WhatsApp"

    def test_whatsapp_api(self):
        assert classify_url("https://api.whatsapp.com/send?phone=82") == "WhatsApp"

    def test_wechat(self):
        assert classify_url("https://u.wechat.com/abc") == "WeChat"

    def test_telegram(self):
        assert classify_url("https://t.me/clinicname") == "Telegram"

    def test_facebook_messenger(self):
        assert classify_url("https://m.me/clinicname") == "FacebookMessenger"

    def test_instagram(self):
        assert classify_url("https://www.instagram.com/clinic_name") == "Instagram"

    def test_facebook(self):
        assert classify_url("https://www.facebook.com/clinic.page") == "Facebook"

    # -- YouTube --
    def test_youtube_channel(self):
        assert classify_url("https://www.youtube.com/@clinic_channel") == "YouTube"

    def test_youtube_embed_excluded(self):
        assert classify_url("https://www.youtube.com/embed/videoId123") is None

    def test_youtube_watch_excluded(self):
        assert classify_url("https://www.youtube.com/watch?v=abc") is None

    def test_youtube_shorts_excluded(self):
        assert classify_url("https://www.youtube.com/shorts/abc") is None

    def test_youtu_be_short_excluded(self):
        assert classify_url("https://youtu.be/abc123") is None

    # -- Phone/SMS --
    def test_tel_link(self):
        assert classify_url("tel:+821012345678") == "Phone"

    def test_sms_link(self):
        assert classify_url("sms:+821012345678") == "SMS"

    # -- Edge cases --
    def test_empty_string(self):
        assert classify_url("") is None

    def test_none_input(self):
        assert classify_url(None) is None

    def test_unknown_url(self):
        assert classify_url("https://www.randomsite.com/page") is None

    def test_case_insensitive(self):
        assert classify_url("https://PF.KAKAO.COM/_test") == "KakaoTalk"


# ============================================================================
# strip_tracking
# ============================================================================

class TestStripTracking:
    def test_removes_utm_params(self):
        url = "https://example.com/page?utm_source=google&utm_medium=cpc&keep=1"
        result = strip_tracking(url)
        assert "utm_source" not in result
        assert "utm_medium" not in result
        assert "keep=1" in result

    def test_removes_fbclid(self):
        url = "https://example.com/?fbclid=abc123&real=value"
        result = strip_tracking(url)
        assert "fbclid" not in result
        assert "real=value" in result

    def test_removes_gclid(self):
        url = "https://example.com/?gclid=xyz"
        result = strip_tracking(url)
        assert "gclid" not in result

    def test_preserves_non_tracking_params(self):
        url = "https://example.com/?id=123&type=clinic"
        assert strip_tracking(url) == url

    def test_no_params(self):
        url = "https://example.com/page"
        assert strip_tracking(url) == url

    def test_malformed_url_returns_original(self):
        url = "not-a-valid-url"
        assert strip_tracking(url) == url

    def test_all_tracking_removed_leaves_clean_url(self):
        url = "https://example.com/?utm_source=a&utm_medium=b"
        result = strip_tracking(url)
        assert result == "https://example.com/"


# ============================================================================
# normalize_url
# ============================================================================

class TestNormalizeUrl:
    def test_strips_trailing_slash(self):
        result = normalize_url("https://example.com/page/")
        assert result == "https://example.com/page"

    def test_lowercases_host(self):
        result = normalize_url("https://EXAMPLE.COM/Page")
        assert "example.com" in result
        assert "/Page" in result  # path case preserved

    def test_root_path_kept(self):
        result = normalize_url("https://example.com/")
        assert result == "https://example.com/"

    def test_phone_normalization(self):
        result = normalize_url("tel:010-1234-5678")
        assert result == "tel:01012345678"

    def test_phone_with_spaces(self):
        result = normalize_url("tel:010 1234 5678")
        assert result == "tel:01012345678"

    def test_sms_normalization(self):
        result = normalize_url("sms:+82-10-1234-5678")
        assert result == "sms:821012345678"

    def test_youtube_strips_videos_suffix(self):
        result = normalize_url("https://www.youtube.com/@clinic/videos")
        assert result.endswith("/@clinic")

    def test_youtube_strips_featured_suffix(self):
        result = normalize_url("https://www.youtube.com/@clinic/featured")
        assert result.endswith("/@clinic")

    def test_youtube_strips_about_suffix(self):
        result = normalize_url("https://www.youtube.com/@clinic/about")
        assert result.endswith("/@clinic")

    def test_removes_tracking_params(self):
        result = normalize_url("https://example.com/?utm_source=test&id=1")
        assert "utm_source" not in result
        assert "id=1" in result

    def test_non_youtube_path_preserved(self):
        result = normalize_url("https://example.com/about")
        assert result == "https://example.com/about"
