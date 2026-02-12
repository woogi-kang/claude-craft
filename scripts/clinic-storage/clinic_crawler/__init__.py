"""clinic_crawler - Extracted pure modules from crawl_single.py."""

from clinic_crawler.constants import (
    DOCTOR_PRIMARY,
    DOCTOR_ROLES_EXCLUDE,
    DOCTOR_ROLES_KEEP,
    DOCTOR_SECONDARY,
    DOCTOR_SUBMENU_PARENTS,
    KOREAN_SURNAMES,
    PHONE_RE,
    PLATFORM_PATTERNS,
    ROLE_RE,
    TRACKING_PARAMS,
)
from clinic_crawler.korean_name import is_plausible_korean_name
from clinic_crawler.log import log
from clinic_crawler.url_utils import classify_url, normalize_url, strip_tracking

__all__ = [
    "PLATFORM_PATTERNS",
    "PHONE_RE",
    "TRACKING_PARAMS",
    "DOCTOR_PRIMARY",
    "DOCTOR_SECONDARY",
    "DOCTOR_SUBMENU_PARENTS",
    "DOCTOR_ROLES_KEEP",
    "DOCTOR_ROLES_EXCLUDE",
    "KOREAN_SURNAMES",
    "ROLE_RE",
    "classify_url",
    "strip_tracking",
    "normalize_url",
    "is_plausible_korean_name",
    "log",
]
