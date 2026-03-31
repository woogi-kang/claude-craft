"""Tech stack detector: identifies marketing/analytics technologies from HTML signatures."""

import re

TECH_SIGNATURES: dict[str, dict] = {
    # Analytics
    "google_analytics": {
        "patterns": [r"gtag\(", r"google-analytics\.com", r"googletagmanager\.com", r"GA_TRACKING_ID", r"ga\('create"],
        "category": "analytics",
        "label": "Google Analytics",
    },
    "ga4": {
        "patterns": [r"gtag.*G-[A-Z0-9]+", r"google.*gtag"],
        "category": "analytics",
        "label": "GA4",
    },
    "naver_analytics": {
        "patterns": [r"wcs_add", r"naver\.com/wcslog"],
        "category": "analytics",
        "label": "네이버 애널리틱스",
    },
    # Advertising
    "google_ads": {
        "patterns": [r"googleads\.g\.doubleclick", r"adsbygoogle", r"google_conversion"],
        "category": "ads",
        "label": "Google Ads",
    },
    "facebook_pixel": {
        "patterns": [r"fbq\(", r"facebook\.com/tr", r"connect\.facebook\.net.*fbevents"],
        "category": "ads",
        "label": "Facebook Pixel",
    },
    "kakao_pixel": {
        "patterns": [r"kakao.*pixel", r"kpixel"],
        "category": "ads",
        "label": "카카오 픽셀",
    },
    "naver_ads": {
        "patterns": [r"wcs_do", r"naver.*conversion"],
        "category": "ads",
        "label": "네이버 광고",
    },
    # Chat/CRM
    "channel_io": {
        "patterns": [r"channel\.io", r"ChannelIO"],
        "category": "chat",
        "label": "Channel.io",
    },
    "zendesk": {
        "patterns": [r"zendesk\.com", r"zdassets"],
        "category": "chat",
        "label": "Zendesk",
    },
    "kakao_chat": {
        "patterns": [r"kakao.*chat", r"plusfriend"],
        "category": "chat",
        "label": "카카오톡 채팅",
    },
    # CMS
    "wordpress": {
        "patterns": [r"wp-content", r"wp-includes", r"wordpress"],
        "category": "cms",
        "label": "WordPress",
    },
    "cafe24": {
        "patterns": [r"cafe24\.com", r"sim\.cafe24"],
        "category": "cms",
        "label": "카페24",
    },
    "gnuboard": {
        "patterns": [r"gnuboard", r"youngcart"],
        "category": "cms",
        "label": "그누보드",
    },
    "wix": {
        "patterns": [r"wix\.com", r"wixstatic"],
        "category": "cms",
        "label": "Wix",
    },
    # CDN
    "cloudflare": {
        "patterns": [r"cloudflare", r"cf-ray"],
        "category": "cdn",
        "label": "Cloudflare",
    },
    "aws_cloudfront": {
        "patterns": [r"cloudfront\.net"],
        "category": "cdn",
        "label": "AWS CloudFront",
    },
    # Booking
    "naver_booking": {
        "patterns": [r"booking\.naver", r"naver.*reservation"],
        "category": "booking",
        "label": "네이버 예약",
    },
    "goodoc": {
        "patterns": [r"goodoc", r"굿닥"],
        "category": "booking",
        "label": "굿닥",
    },
    # SEO
    "schema_org": {
        "patterns": [r"schema\.org", r"application/ld\+json"],
        "category": "seo",
        "label": "구조화 데이터",
    },
}

ALL_CATEGORIES = ["analytics", "ads", "chat", "cms", "cdn", "booking", "seo"]

RECOMMENDED_TECH: list[dict[str, str]] = [
    {"category": "analytics", "tech": "Google Analytics", "reason": "웹사이트 방문자 행동 분석 필수"},
    {"category": "ads", "tech": "광고 추적 픽셀", "reason": "마케팅 ROI 측정 및 리타겟팅"},
    {"category": "chat", "tech": "채팅 위젯", "reason": "실시간 상담으로 전환율 향상"},
    {"category": "cdn", "tech": "CDN", "reason": "해외 환자 접속 속도 개선"},
    {"category": "booking", "tech": "온라인 예약", "reason": "24시간 예약 접수로 이탈 방지"},
    {"category": "seo", "tech": "구조화 데이터", "reason": "검색엔진 리치 결과 노출"},
]


def _match_tech(html: str, tech_id: str, sig: dict) -> bool:
    """Check if any pattern in a signature matches the HTML."""
    for pattern in sig["patterns"]:
        if re.search(pattern, html, re.IGNORECASE):
            return True
    return False


def detect_tech_stack(pages: list[dict]) -> dict:
    """Detect marketing/analytics tech stack from crawled pages.

    Args:
        pages: list of dicts with "url" and "html" keys.

    Returns:
        Dict with detected techs, by_category breakdown, missing_recommended, and recommendations.
    """
    if not pages:
        return {
            "detected": {},
            "by_category": {cat: [] for cat in ALL_CATEGORIES},
            "missing_recommended": [],
            "total_detected": 0,
            "recommendations": [],
        }

    detected: dict[str, dict] = {}

    for page in pages:
        html = page.get("html", "")
        page_url = page.get("url", "")

        for tech_id, sig in TECH_SIGNATURES.items():
            if _match_tech(html, tech_id, sig):
                if tech_id not in detected:
                    detected[tech_id] = {
                        "label": sig["label"],
                        "category": sig["category"],
                        "found_on": [],
                    }
                if page_url not in detected[tech_id]["found_on"]:
                    detected[tech_id]["found_on"].append(page_url)

    # Build by_category
    by_category: dict[str, list[str]] = {cat: [] for cat in ALL_CATEGORIES}
    for tech_id, info in detected.items():
        cat = info["category"]
        if info["label"] not in by_category[cat]:
            by_category[cat].append(info["label"])

    # Find missing recommended tech
    detected_categories = {info["category"] for info in detected.values()}
    missing_recommended = [
        {"tech": rec["tech"], "reason": rec["reason"]}
        for rec in RECOMMENDED_TECH
        if rec["category"] not in detected_categories
    ]

    # Build recommendations
    recommendations = []
    if "analytics" not in detected_categories:
        recommendations.append({
            "priority": "high",
            "message": "웹 분석 도구(Google Analytics 등)가 감지되지 않았습니다. 방문자 행동 분석을 위해 설치를 권장합니다.",
        })
    if "ads" not in detected_categories:
        recommendations.append({
            "priority": "medium",
            "message": "광고 추적 픽셀이 없습니다. 마케팅 캠페인 성과 측정을 위해 Facebook Pixel 또는 Google Ads 전환 추적 설치를 권장합니다.",
        })
    if "chat" not in detected_categories:
        recommendations.append({
            "priority": "medium",
            "message": "실시간 채팅 위젯이 없습니다. Channel.io, 카카오톡 상담 등을 통해 환자 문의 전환율을 높일 수 있습니다.",
        })
    if "cdn" not in detected_categories:
        recommendations.append({
            "priority": "low",
            "message": "CDN이 감지되지 않았습니다. 해외 환자 대상 서비스 시 Cloudflare 등 CDN 적용으로 접속 속도를 개선할 수 있습니다.",
        })
    if "seo" not in detected_categories:
        recommendations.append({
            "priority": "high",
            "message": "구조화 데이터(Schema.org)가 감지되지 않았습니다. 검색엔진 리치 결과 노출을 위해 MedicalOrganization, FAQPage 등의 스키마를 추가하세요.",
        })
    if "booking" not in detected_categories:
        recommendations.append({
            "priority": "medium",
            "message": "온라인 예약 시스템이 감지되지 않았습니다. 네이버 예약, 굿닥 등을 통해 24시간 예약 접수를 지원하세요.",
        })

    return {
        "detected": detected,
        "by_category": by_category,
        "missing_recommended": missing_recommended,
        "total_detected": len(detected),
        "recommendations": recommendations,
    }
