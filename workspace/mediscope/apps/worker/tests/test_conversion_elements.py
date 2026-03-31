"""Tests for conversion element detection."""

from app.checks.conversion_elements import check_conversion_elements


def _make_page(html: str, url: str = "https://example.com") -> dict:
    return {"url": url, "html": html, "status_code": 200}


def _wrap_html(body: str) -> str:
    return f"<html><head><title>Test</title></head><body>{body}</body></html>"


class TestCTADetection:
    def test_cta_button_found(self):
        html = _wrap_html('<button>예약하기</button>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["cta_main"] is True

    def test_cta_link_found(self):
        html = _wrap_html('<a href="/book">상담 문의</a>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["cta_main"] is True

    def test_cta_english_found(self):
        html = _wrap_html('<a href="/contact">Book Appointment</a>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["cta_main"] is True

    def test_no_cta_found(self):
        html = _wrap_html('<p>Welcome to our clinic</p>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["cta_main"] is False

    def test_cta_in_href(self):
        html = _wrap_html('<a href="/reserve">Click here</a>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["cta_main"] is True


class TestPhoneDetection:
    def test_tel_link_clickable(self):
        html = _wrap_html('<a href="tel:02-1234-5678">전화</a>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["phone_clickable"] is True

    def test_phone_text_only_not_clickable(self):
        html = _wrap_html('<p>전화: 02-1234-5678</p>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["phone_clickable"] is False
        assert result.details["phone_numbers_in_text"] > 0

    def test_no_phone(self):
        html = _wrap_html('<p>No phone here</p>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["phone_clickable"] is False


class TestMessengerDetection:
    def test_kakao_detected(self):
        html = _wrap_html('<a href="https://pf.kakao.com/abc">카카오톡</a>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["messengers"]["kakao"] is True

    def test_line_detected(self):
        html = _wrap_html('<a href="https://line.me/R/ti/p/@abc">LINE</a>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["messengers"]["line"] is True

    def test_wechat_detected(self):
        html = _wrap_html('<p>WeChat ID: hospital123</p>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["messengers"]["wechat"] is True

    def test_chat_widget_detected(self):
        html = _wrap_html('<script src="https://cdn.channel.io/plugin.js"></script>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["messengers"]["chat_widget"] is True

    def test_no_messenger(self):
        html = _wrap_html('<p>No messenger</p>')
        result = check_conversion_elements([_make_page(html)])
        assert all(v is False for v in result.details["messengers"].values())


class TestFormAnalysis:
    def test_form_detected(self):
        html = _wrap_html('''
            <form action="/submit">
                <input type="text" name="name" placeholder="이름">
                <input type="tel" name="phone" placeholder="전화번호">
                <button type="submit">문의</button>
            </form>
        ''')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["form_exists"] is True
        assert result.details["form_fields"] == 2

    def test_form_many_fields(self):
        fields = ''.join(f'<input type="text" name="f{i}">' for i in range(8))
        html = _wrap_html(f'<form>{fields}<button>문의</button></form>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["form_exists"] is True
        assert result.details["form_fields"] == 8

    def test_no_form(self):
        html = _wrap_html('<p>No form</p>')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["form_exists"] is False

    def test_form_multilingual(self):
        html = _wrap_html('''
            <form>
                <input type="text" placeholder="Name">
                <input type="email" placeholder="Email">
                <button type="submit">Submit</button>
            </form>
        ''')
        result = check_conversion_elements([_make_page(html)])
        assert result.details["form_multilingual"] is True


class TestScoring:
    def test_perfect_score(self):
        html = _wrap_html('''
            <a href="/book">예약하기</a>
            <a href="tel:02-1234-5678">전화</a>
            <a href="https://pf.kakao.com/abc">카카오</a>
            <a href="https://line.me/abc">LINE</a>
            <p>가격: 50만원</p>
            <form>
                <input type="text" name="name" placeholder="Name">
                <input type="tel" name="phone" placeholder="Phone">
                <button type="submit">Book</button>
            </form>
        ''')
        result = check_conversion_elements([_make_page(html)])
        # CTA(20) + no proc pages but has cta(8) + phone(10) + messenger(15) + line bonus(5) + form(15) + form simple(5) + price(10) + form multilingual(10) = 98
        assert result.score >= 0.9
        assert result.grade.value == "pass"

    def test_zero_score(self):
        html = _wrap_html('<p>Empty page</p>')
        result = check_conversion_elements([_make_page(html)])
        assert result.score == 0.0
        assert result.grade.value == "fail"

    def test_partial_score(self):
        html = _wrap_html('''
            <button>예약</button>
            <a href="tel:010-0000-0000">전화</a>
        ''')
        result = check_conversion_elements([_make_page(html)])
        # CTA(20) + no proc but has cta(8) + phone(10) = 38
        assert 0.3 <= result.score <= 0.5

    def test_empty_pages(self):
        result = check_conversion_elements([])
        assert result.score == 0.0
        assert result.grade.value == "fail"

    def test_procedure_page_cta_coverage(self):
        main = _make_page(_wrap_html('<button>예약</button>'))
        proc1 = _make_page(
            _wrap_html('<h1>보톡스 시술</h1><a href="/book">예약</a>'),
            url="https://example.com/botox",
        )
        proc2 = _make_page(
            _wrap_html('<h1>필러 시술</h1><p>No CTA</p>'),
            url="https://example.com/filler",
        )
        proc3 = _make_page(
            _wrap_html('<h1>레이저 치료</h1><button>상담</button>'),
            url="https://example.com/laser",
        )
        result = check_conversion_elements([main, proc1, proc2, proc3])
        assert result.details["cta_procedure_pages"]["total"] == 3
        assert result.details["cta_procedure_pages"]["with_cta"] == 2

    def test_elements_found_and_missing(self):
        html = _wrap_html('<button>예약</button>')
        result = check_conversion_elements([_make_page(html)])
        assert "cta_main" in result.details["elements_found"]
        assert "phone_clickable" in result.details["elements_missing"]

    def test_score_capped_at_100(self):
        # Even with all elements, score should not exceed 100
        html = _wrap_html('''
            <button>예약</button>
            <a href="tel:02-1234-5678">전화</a>
            <a href="https://pf.kakao.com/abc">카카오</a>
            <a href="https://line.me/abc">LINE</a>
            <a href="https://weixin.qq.com/abc">WeChat</a>
            <script src="https://cdn.channel.io/plugin.js"></script>
            <p>가격표</p>
            <form>
                <input type="text" placeholder="Name">
                <button>Book</button>
            </form>
        ''')
        result = check_conversion_elements([_make_page(html)])
        assert result.score <= 1.0
