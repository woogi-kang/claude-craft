"""
Map Place Crawling Schema Package.

Provides production-ready Pydantic v2 models for Kakao Map and Naver Map
place data crawling with shared base models and platform-specific extensions.
"""

from crawl.base import (
    BasePlace,
    BaseReviewStats,
    Coordinates,
    CrawlError,
    CrawlJob,
    CrawlJobStatus,
    CrawlMetadata,
    CrawlSource,
    PaginatedResponse,
    PlaceSummary,
)
from crawl.kakao_map_schema import (
    KakaoPlaceData,
    KakaoPlaceParser,
    PlaceBasicInfo as KakaoPlaceBasicInfo,
)
from crawl.hospital_schema import NaverHospitalPlace
from crawl.naver_map_schema import (
    NaverPlace,
    NaverPlaceParser,
)

__all__ = [
    # Base
    "BasePlace",
    "BaseReviewStats",
    "Coordinates",
    "CrawlError",
    "CrawlJob",
    "CrawlJobStatus",
    "CrawlMetadata",
    "CrawlSource",
    "PaginatedResponse",
    "PlaceSummary",
    # Kakao
    "KakaoPlaceData",
    "KakaoPlaceParser",
    "KakaoPlaceBasicInfo",
    # Naver
    "NaverPlace",
    "NaverPlaceParser",
    "NaverHospitalPlace",
]
