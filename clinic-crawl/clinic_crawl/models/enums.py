"""Core enumerations for clinic crawl pipeline."""

from __future__ import annotations

from enum import StrEnum


class CrawlCategory(StrEnum):
    """URL classification category determined during triage."""

    CUSTOM_DOMAIN = "custom_domain"
    BLOG_NAVER = "blog_naver"
    KAKAO_CHANNEL = "kakao_channel"
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    IMWEB = "imweb"
    MOBIDOC = "mobidoc"
    GOOGLE_SITES = "google_sites"
    NO_URL = "no_url"
    DEAD_LINK = "dead_link"
    INVALID_URL = "invalid_url"


class CrawlPhase(StrEnum):
    """Progress phase for each hospital in the pipeline."""

    PENDING = "pending"
    TRIAGE_DONE = "triage_done"
    RESOLVE_DONE = "resolve_done"
    PRESCAN_DONE = "prescan_done"
    DEEP_CRAWL_DONE = "deep_crawl_done"
    VALIDATED = "validated"
    FAILED = "failed"


class SocialPlatform(StrEnum):
    """Supported social consultation platforms."""

    KAKAO = "kakao"
    NAVER_TALK = "naver_talk"
    LINE = "line"
    WECHAT = "wechat"
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    FACEBOOK_MESSENGER = "facebook_messenger"


class DoctorRole(StrEnum):
    """Medical staff role classification."""

    DIRECTOR = "director"  # 원장
    SPECIALIST = "specialist"  # 전문의
    RESIDENT = "resident"  # 전공의
    NURSE = "nurse"  # 간호사
    STAFF = "staff"  # 스태프


class ExtractionMethod(StrEnum):
    """How a data point was extracted."""

    PRESCAN_REGEX = "prescan_regex"
    DOM_STATIC = "dom_static"
    DOM_DYNAMIC = "dom_dynamic"
    FLOATING_ELEMENT = "floating_element"
    QR_DECODE = "qr_decode"
    META_TAG = "meta_tag"
    IFRAME_WIDGET = "iframe_widget"
