"""Tests for international usability analysis."""

from app.services.international_usability import analyze_international_usability


def _make_page(html: str, url: str = "https://example.com") -> dict:
    return {"url": url, "html": html, "status_code": 200}


def _wrap_html(body: str, head: str = "") -> str:
    return f"<html><head><title>Test</title>{head}</head><body>{body}</body></html>"


_EMPTY_MULTILINGUAL = {"overall_score": 0, "readiness_scores": {}}


class TestLangSwitcher:
    def test_lang_switch_in_nav(self):
        html = _wrap_html('<nav><select class="lang-switch"><option>EN</option></select></nav>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["lang_switcher"]["status"] == "pass"

    def test_lang_link_in_nav(self):
        html = _wrap_html('<nav><a href="/en">English</a><a href="/ja">日本語</a></nav>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["lang_switcher"]["status"] == "pass"

    def test_flag_icon_in_nav(self):
        html = _wrap_html('<nav><span>🇺🇸</span><span>🇯🇵</span></nav>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["lang_switcher"]["status"] == "pass"

    def test_lang_switch_outside_nav(self):
        html = _wrap_html('<nav><a href="/">Home</a></nav><footer><a href="/en">EN</a></footer>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["lang_switcher"]["status"] == "warn"

    def test_no_lang_switch(self):
        html = _wrap_html('<nav><a href="/">Home</a></nav>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["lang_switcher"]["status"] == "fail"


class TestIntlPhone:
    def test_intl_phone_found(self):
        html = _wrap_html('<p>Call us: +82-2-1234-5678</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["intl_phone"]["status"] == "pass"

    def test_domestic_only(self):
        html = _wrap_html('<p>전화: 02-1234-5678</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["intl_phone"]["status"] == "warn"

    def test_no_phone(self):
        html = _wrap_html('<p>No phone</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["intl_phone"]["status"] == "fail"


class TestTimezone:
    def test_timezone_found(self):
        html = _wrap_html('<p>영업시간: 09:00-18:00 KST</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["timezone"]["status"] == "pass"

    def test_no_timezone(self):
        html = _wrap_html('<p>영업시간: 09:00-18:00</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["timezone"]["status"] == "fail"


class TestCurrency:
    def test_usd_found(self):
        html = _wrap_html('<p>Price: $500 USD</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["currency"]["status"] == "pass"

    def test_no_foreign_currency(self):
        html = _wrap_html('<p>가격: 50만원</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["currency"]["status"] == "fail"


class TestGoogleTranslate:
    def test_google_translate_widget(self):
        html = _wrap_html('<div id="google_translate_element"></div>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["google_translate"]["status"] == "pass"

    def test_no_translate(self):
        html = _wrap_html('<p>Normal content</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["google_translate"]["status"] == "fail"


class TestVisaInfo:
    def test_visa_info_found(self):
        html = _wrap_html('<p>의료관광 비자(C-3-3) 안내</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["visa_info"]["status"] == "pass"

    def test_no_visa_info(self):
        html = _wrap_html('<p>Welcome</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["visa_info"]["status"] == "fail"


class TestTravelSupport:
    def test_pickup_found(self):
        html = _wrap_html('<p>공항 픽업 서비스를 제공합니다</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["travel_support"]["status"] == "pass"

    def test_hotel_found(self):
        html = _wrap_html('<p>We provide hotel accommodation assistance</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["travel_support"]["status"] == "pass"

    def test_no_travel(self):
        html = _wrap_html('<p>Welcome to clinic</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["travel_support"]["status"] == "fail"


class TestPaymentMethods:
    def test_multiple_payments(self):
        html = _wrap_html('<p>We accept Alipay and PayPal</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["payment_methods"]["status"] == "pass"

    def test_single_payment(self):
        html = _wrap_html('<p>PayPal accepted</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["payment_methods"]["status"] == "warn"

    def test_no_intl_payment(self):
        html = _wrap_html('<p>카드 결제 가능</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["payment_methods"]["status"] == "fail"


class TestMultilingualFonts:
    def test_noto_sans_jp(self):
        html = _wrap_html('', '<link href="fonts.googleapis.com/css?family=Noto+Sans+JP">')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["multilingual_fonts"]["status"] == "pass"

    def test_no_cjk_font(self):
        html = _wrap_html('<p>Normal text</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["multilingual_fonts"]["status"] == "warn"


class TestAltMultilingual:
    def test_english_alt(self):
        html = _wrap_html('<img src="a.jpg" alt="Botox treatment before and after">')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["alt_multilingual"]["status"] in ("pass", "warn")

    def test_korean_only_alt(self):
        html = _wrap_html('<img src="a.jpg" alt="보톡스 시술 전후">')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["alt_multilingual"]["status"] == "fail"

    def test_no_alt(self):
        html = _wrap_html('<img src="a.jpg">')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["checks"]["alt_multilingual"]["status"] == "fail"


class TestOverallScoring:
    def test_empty_pages(self):
        result = analyze_international_usability([], _EMPTY_MULTILINGUAL)
        assert result["overall_score"] == 0
        assert result["pass_count"] == 0
        assert result["fail_count"] == 10

    def test_all_pass(self):
        html = _wrap_html(
            '''
            <nav>
                <select class="language-switch"><option>EN</option></select>
            </nav>
            <p>Call: +82-2-1234-5678</p>
            <p>Hours: 09:00-18:00 KST</p>
            <p>Price: $500 USD</p>
            <div id="google_translate_element"></div>
            <p>의료관광 비자 안내</p>
            <p>공항 픽업 서비스</p>
            <p>We accept Alipay and PayPal</p>
            <img src="a.jpg" alt="Botox treatment">
            <img src="b.jpg" alt="Filler injection">
            <img src="c.jpg" alt="Laser therapy">
            ''',
            '<link href="Noto Sans JP">',
        )
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert result["overall_score"] >= 90
        assert result["pass_count"] == 10
        assert result["fail_count"] == 0

    def test_partial_score(self):
        html = _wrap_html('''
            <nav><a href="/en">EN</a></nav>
            <p>Call: +82-2-1234-5678</p>
        ''')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert 20 <= result["overall_score"] <= 40
        assert result["pass_count"] == 2

    def test_multilingual_boost(self):
        html = _wrap_html('<nav><a href="/en">EN</a></nav>')
        result_low = analyze_international_usability(
            [_make_page(html)], {"overall_score": 0},
        )
        result_high = analyze_international_usability(
            [_make_page(html)], {"overall_score": 80},
        )
        assert result_high["overall_score"] >= result_low["overall_score"]

    def test_recommendations_generated(self):
        html = _wrap_html('<p>Simple page</p>')
        result = analyze_international_usability([_make_page(html)], _EMPTY_MULTILINGUAL)
        assert len(result["recommendations"]) > 0
        # High priority should be first
        priorities = [r["priority"] for r in result["recommendations"]]
        high_indices = [i for i, p in enumerate(priorities) if p == "high"]
        medium_indices = [i for i, p in enumerate(priorities) if p == "medium"]
        if high_indices and medium_indices:
            assert max(high_indices) < min(medium_indices)

    def test_multi_page_detection(self):
        main = _make_page(_wrap_html('<p>Main page</p>'))
        visa_page = _make_page(
            _wrap_html('<p>비자 안내 페이지입니다. 의료관광 비자(C-3-3)</p>'),
            url="https://example.com/visa",
        )
        result = analyze_international_usability([main, visa_page], _EMPTY_MULTILINGUAL)
        assert result["checks"]["visa_info"]["status"] == "pass"
