"""Common fixtures for CheckYourHospital Worker tests."""

import os
from unittest.mock import MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

# Set env vars before importing app modules
os.environ["WORKER_API_KEY"] = "test-key"
os.environ["SUPABASE_URL"] = ""
os.environ["SUPABASE_SECRET_KEY"] = ""


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-key"}


@pytest.fixture
def good_html():
    return """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>서울 강남 미소클리닉 - 피부과 전문</title>
    <meta name="description" content="서울 강남에 위치한 미소클리닉은 피부과 전문 클리닉입니다. 전문의가 직접 진료합니다.">
    <meta property="og:title" content="미소클리닉 - 피부과 전문">
    <meta property="og:description" content="서울 강남 피부과 전문 클리닉">
    <meta property="og:image" content="https://example.com/og.jpg">
    <link rel="canonical" href="https://example.com/">
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "MedicalClinic",
        "name": "미소클리닉",
        "address": {"@type": "PostalAddress", "addressLocality": "서울 강남"}
    }
    </script>
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": "진료시간은?", "acceptedAnswer": {"@type": "Answer", "text": "09-18시"}}
        ]
    }
    </script>
</head>
<body>
    <h1>미소클리닉 피부과</h1>
    <h2>진료 안내</h2>
    <h3>진료 시간</h3>
    <p>서울 강남에 위치한 미소클리닉은 피부과 전문 의료기관입니다. 대표원장 김미소 전문의가 직접 진료합니다.</p>
    <p>자격증: 피부과 전문의 면허 보유. 경력 15년. 대한피부과학회 정회원.</p>
    <p>연락처: 02-1234-5678. 주소: 서울 강남구 역삼동 123-45.</p>
    <p>후기: 환자 경험이 매우 좋습니다. 치료 사례가 많습니다.</p>
    <img src="/images/clinic.jpg" alt="미소클리닉 전경 사진">
    <img src="/images/doctor.jpg" alt="김미소 원장 프로필">
    <ul>
        <li>피부과 진료</li>
        <li>레이저 시술</li>
        <li>보톡스/필러</li>
    </ul>
    <table><tr><td>월-금</td><td>09:00-18:00</td></tr></table>
    <details><summary>자주 묻는 질문</summary><p>Q. 예약은 어떻게 하나요?</p></details>
    <p>어떻게 예약하나요? 전화 또는 온라인으로 예약 가능합니다.</p>
    <a href="/about">의료진 소개</a>
    <a href="/services">진료 안내</a>
    <a href="/contact">찾아오시는 길</a>
</body>
</html>"""


@pytest.fixture
def bad_html():
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
</head>
<body>
    <div>Some content</div>
    <img src="/img_001.jpg">
    <img src="/dsc_photo.jpg">
</body>
</html>"""


@pytest.fixture
def mock_supabase():
    mock_client = MagicMock()
    mock_client.table.return_value = mock_client
    mock_client.select.return_value = mock_client
    mock_client.insert.return_value = mock_client
    mock_client.update.return_value = mock_client
    mock_client.eq.return_value = mock_client
    mock_client.not_.return_value = mock_client
    mock_client.is_.return_value = mock_client
    mock_client.like.return_value = mock_client
    mock_client.lt.return_value = mock_client
    mock_client.order.return_value = mock_client
    mock_client.limit.return_value = mock_client
    mock_client.single.return_value = mock_client
    mock_client.execute.return_value = MagicMock(data=[])
    return mock_client


@pytest.fixture
def test_client():
    from app.main import app

    from httpx import ASGITransport, AsyncClient

    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")
