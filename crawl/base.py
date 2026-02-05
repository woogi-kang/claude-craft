"""
Shared Base Models for Map Place Crawling.

Common types, enums, and base classes used by both
Kakao Map and Naver Map schema modules.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from typing import Annotated, Optional, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    model_validator,
)


# ---------------------------------------------------------------------------
# Shared Annotated Types
# ---------------------------------------------------------------------------

KoreanPhone = Annotated[
    str,
    Field(
        pattern=r"^0\d{1,2}-?\d{3,4}-?\d{4}$",
        examples=["02-1234-5678", "010-9876-5432"],
    ),
]

TimeStr = Annotated[
    str,
    Field(
        pattern=r"^([01]\d|2[0-3]):[0-5]\d$",
        examples=["09:30", "18:00"],
    ),
]


# ---------------------------------------------------------------------------
# Shared Enums
# ---------------------------------------------------------------------------


class CrawlSource(StrEnum):
    """Platform source identifier for multi-source crawling."""

    NAVER = "naver"
    KAKAO = "kakao"


class CrawlJobStatus(StrEnum):
    """Crawl job lifecycle states."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


# ---------------------------------------------------------------------------
# Shared Base Models
# ---------------------------------------------------------------------------


class Coordinates(BaseModel):
    """Geographic coordinates (WGS84)."""

    model_config = ConfigDict(frozen=True)

    latitude: float = Field(
        ...,
        ge=33.0,
        le=39.0,
        description="Latitude (South Korea: ~33-39)",
        examples=[37.5665],
    )
    longitude: float = Field(
        ...,
        ge=124.0,
        le=132.0,
        description="Longitude (South Korea: ~124-132)",
        examples=[126.9780],
    )

    @classmethod
    def from_kakao(cls, x: float, y: float) -> Coordinates:
        """Create from Kakao API x(longitude)/y(latitude) format."""
        return cls(latitude=y, longitude=x)

    def to_tuple(self) -> tuple[float, float]:
        return (self.latitude, self.longitude)


class CrawlMetadata(BaseModel):
    """Metadata about the crawl operation."""

    model_config = ConfigDict(frozen=True)

    source: CrawlSource
    crawled_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of crawl",
    )
    source_url: Optional[str] = Field(
        default=None,
        description="Original URL that was crawled",
    )
    search_query: Optional[str] = Field(
        default=None,
        description="Search query that found this place",
        examples=["홍대 피부과"],
    )
    raw_data_hash: Optional[str] = Field(
        default=None,
        description="SHA-256 hash prefix for deduplication",
    )
    crawl_duration_ms: Optional[int] = Field(
        default=None,
        ge=0,
        description="Crawl duration in milliseconds",
    )


class BaseReviewStats(BaseModel):
    """Common review statistics across platforms."""

    model_config = ConfigDict(frozen=True)

    rating: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=5.0,
        description="Average star rating (0.0-5.0)",
    )


class BasePlace(BaseModel):
    """Shared place fields across Naver and Kakao Map."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
    )

    name: str = Field(min_length=1, description="Business name")
    category: str = Field(min_length=1, description="Place category")
    road_address: Optional[str] = Field(
        default=None,
        description="Road name address",
    )
    parcel_address: Optional[str] = Field(
        default=None,
        description="Old parcel address",
    )
    phone: Optional[str] = Field(
        default=None,
        description="Contact phone number",
    )
    coordinates: Optional[Coordinates] = Field(
        default=None,
        description="Geographic location (WGS84)",
    )


# ---------------------------------------------------------------------------
# API Response Models
# ---------------------------------------------------------------------------


class PlaceSummary(BaseModel):
    """Lightweight place summary for list endpoints."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    category: str
    road_address: Optional[str] = None
    rating: Optional[float] = None
    total_reviews: int = 0
    source: CrawlSource
    coordinates: Optional[Coordinates] = None


class CrawlError(BaseModel):
    """Individual crawl error record."""

    model_config = ConfigDict(frozen=True)

    place_id: Optional[str] = None
    url: Optional[str] = None
    error_type: str = Field(description="Error class name")
    message: str = Field(description="Human-readable error message")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )


class CrawlJob(BaseModel):
    """Tracks a batch crawl operation."""

    job_id: str = Field(description="Unique crawl job identifier")
    source: CrawlSource
    status: CrawlJobStatus = CrawlJobStatus.PENDING
    query: Optional[str] = Field(default=None)
    region: Optional[str] = Field(default=None)
    total_places: NonNegativeInt = 0
    completed_places: NonNegativeInt = 0
    failed_places: NonNegativeInt = 0
    errors: list[CrawlError] = Field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    @property
    def progress_pct(self) -> float:
        if self.total_places == 0:
            return 0.0
        return (self.completed_places / self.total_places) * 100.0

    @property
    def success_rate(self) -> float:
        attempted = self.completed_places + self.failed_places
        if attempted == 0:
            return 0.0
        return (self.completed_places / attempted) * 100.0


class CrawlResult(BaseModel):
    """Result wrapper for a single place crawl attempt."""

    model_config = ConfigDict(frozen=True)

    success: bool
    place_data: Optional[dict] = None
    error: Optional[CrawlError] = None

    @model_validator(mode="after")
    def validate_result(self) -> Self:
        if self.success and self.place_data is None:
            raise ValueError("place_data is required when success is True")
        if not self.success and self.error is None:
            raise ValueError("error is required when success is False")
        return self


class PaginatedResponse(BaseModel):
    """Generic paginated API response."""

    model_config = ConfigDict(frozen=True)

    items: list[PlaceSummary]
    total: NonNegativeInt
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    has_next: bool

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size

    @classmethod
    def create(
        cls,
        items: list[PlaceSummary],
        total: int,
        page: int,
        page_size: int,
    ) -> PaginatedResponse:
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_next=page * page_size < total,
        )
