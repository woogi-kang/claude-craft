"""
Naver Map Place Data Schema for FastAPI Crawling Project.

Production-ready Pydantic v2 models with:
- Structured business hours with DayOfWeek enum
- TAB/TEXT menu type discrimination with cross-field validation
- Coordinate support for map rendering
- Shared base models for Kakao Map alignment
- Naver-specific parsing utilities
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from enum import StrEnum
from typing import Annotated, Any, Optional, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    field_validator,
    model_validator,
)

from crawl.base import (
    BasePlace,
    BaseReviewStats,
    Coordinates,
    CrawlMetadata,
    CrawlSource,
    TimeStr,
)


# ---------------------------------------------------------------------------
# Naver-Specific Enums
# ---------------------------------------------------------------------------


class DayOfWeek(StrEnum):
    """Standardized day of week identifiers."""

    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"
    HOLIDAY = "HOLIDAY"

    @classmethod
    def from_korean(cls, value: str) -> DayOfWeek:
        """Parse Korean day names to enum values."""
        mapping = {
            "월": cls.MON,
            "월요일": cls.MON,
            "화": cls.TUE,
            "화요일": cls.TUE,
            "수": cls.WED,
            "수요일": cls.WED,
            "목": cls.THU,
            "목요일": cls.THU,
            "금": cls.FRI,
            "금요일": cls.FRI,
            "토": cls.SAT,
            "토요일": cls.SAT,
            "일": cls.SUN,
            "일요일": cls.SUN,
            "공휴일": cls.HOLIDAY,
        }
        result = mapping.get(value.strip())
        if result is None:
            raise ValueError(
                f"Unknown Korean day: '{value}'. "
                f"Expected one of: {list(mapping.keys())}"
            )
        return result


class NaverMenuType(StrEnum):
    """Menu data source type on Naver Map."""

    TAB = "TAB"
    TEXT = "TEXT"


NaverPlaceId = Annotated[
    str,
    Field(
        min_length=1,
        pattern=r"^\d+$",
        examples=["1612729816"],
        description="Naver Map unique numeric place ID",
    ),
]


# ---------------------------------------------------------------------------
# Value Objects
# ---------------------------------------------------------------------------


class NaverBusinessHour(BaseModel):
    """Operating hours for a single day."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    day_of_week: DayOfWeek
    open_time: Optional[str] = Field(
        default=None,
        description="Opening time (HH:MM)",
        examples=["09:30"],
    )
    close_time: Optional[str] = Field(
        default=None,
        description="Closing time (HH:MM)",
        examples=["18:00"],
    )
    break_start: Optional[str] = Field(
        default=None,
        description="Break period start time",
        examples=["13:00"],
    )
    break_end: Optional[str] = Field(
        default=None,
        description="Break period end time",
        examples=["14:00"],
    )
    is_day_off: bool = Field(
        default=False,
        description="True if closed for the entire day",
    )

    @model_validator(mode="after")
    def validate_hours_consistency(self) -> Self:
        if self.is_day_off and (self.open_time or self.close_time):
            raise ValueError(
                "open_time and close_time must be None when is_day_off is True"
            )
        if self.break_start and not self.break_end:
            raise ValueError("break_end is required when break_start is set")
        if self.break_end and not self.break_start:
            raise ValueError("break_start is required when break_end is set")
        return self


class NaverReviewStats(BaseReviewStats):
    """Naver-specific review statistics."""

    model_config = ConfigDict(frozen=True)

    visitor_reviews: NonNegativeInt = Field(
        default=0,
        description="Count of verified visitor reviews",
    )
    blog_reviews: NonNegativeInt = Field(
        default=0,
        description="Count of blog reviews",
    )

    @property
    def total_reviews(self) -> int:
        return self.visitor_reviews + self.blog_reviews

    @property
    def has_reviews(self) -> bool:
        return self.total_reviews > 0


class NaverMenuItem(BaseModel):
    """Individual menu item from Naver Map place."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, description="Menu item name")
    price: str = Field(
        min_length=1,
        description="Price as displayed (e.g., '15,000원')",
    )
    price_value: Optional[int] = Field(
        default=None,
        ge=0,
        description="Parsed numeric price in KRW",
    )
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_popular: bool = Field(
        default=False,
        description="Whether marked as popular/recommended",
    )

    @field_validator("price_value", mode="before")
    @classmethod
    def parse_price_from_string(cls, v: Optional[int], info) -> Optional[int]:
        if v is not None:
            return v
        price_str = info.data.get("price", "")
        if not price_str:
            return None
        digits = re.sub(r"[^\d]", "", price_str)
        return int(digits) if digits else None


class NaverMenuInfo(BaseModel):
    """Container for menu data, supporting both structured and text formats."""

    model_config = ConfigDict(frozen=True)

    menu_type: NaverMenuType
    items: list[NaverMenuItem] = Field(default_factory=list)
    price_text: Optional[str] = Field(
        default=None,
        description="Raw price/menu text (used when menu_type is TEXT)",
    )

    @model_validator(mode="after")
    def validate_menu_data(self) -> Self:
        if self.menu_type == NaverMenuType.TAB and not self.items:
            raise ValueError("items must be non-empty when menu_type is TAB")
        if self.menu_type == NaverMenuType.TEXT and not self.price_text:
            raise ValueError("price_text must be non-empty when menu_type is TEXT")
        return self


# ---------------------------------------------------------------------------
# Naver Place (Aggregate Root)
# ---------------------------------------------------------------------------


class NaverPlace(BasePlace):
    """Complete Naver Map place entity (aggregate root).

    Extends BasePlace with Naver-specific fields for business hours,
    menus, facilities, and review statistics.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
    )

    # --- Identity ---
    id: NaverPlaceId = Field(description="Unique Naver Place ID")

    # --- Content ---
    description: Optional[str] = Field(
        default=None,
        description="Place introduction / bio text",
    )
    homepage_url: Optional[str] = Field(
        default=None,
        description="Official website URL",
    )
    image_urls: list[str] = Field(
        default_factory=list,
        description="List of place image URLs",
    )
    facilities: list[str] = Field(
        default_factory=list,
        description="Available facilities (e.g., 'Parking', 'WiFi')",
    )

    # --- Structured Data ---
    business_hours: list[NaverBusinessHour] = Field(default_factory=list)
    review_stats: NaverReviewStats = Field(default_factory=NaverReviewStats)
    menu_info: Optional[NaverMenuInfo] = Field(
        default=None,
        description="Menu data (None for clinics/services without menu)",
    )

    # --- Crawl Metadata ---
    crawl: CrawlMetadata = Field(
        default_factory=lambda: CrawlMetadata(source=CrawlSource.NAVER),
    )

    @field_validator("business_hours")
    @classmethod
    def validate_unique_days(
        cls, v: list[NaverBusinessHour]
    ) -> list[NaverBusinessHour]:
        days = [bh.day_of_week for bh in v]
        if len(days) != len(set(days)):
            raise ValueError("Duplicate day_of_week entries found")
        return v

    @field_validator("image_urls")
    @classmethod
    def deduplicate_images(cls, v: list[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for url in v:
            if url not in seen:
                seen.add(url)
                result.append(url)
        return result

    @field_validator("homepage_url")
    @classmethod
    def validate_homepage(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if v.startswith("//"):
            v = f"https:{v}"
        if not v.startswith(("http://", "https://")):
            v = f"https://{v}"
        return v


# ---------------------------------------------------------------------------
# Raw API Response Parser
# ---------------------------------------------------------------------------


class NaverPlaceParser:
    """Parse raw Naver Map data into NaverPlace models.

    Handles inconsistent formats and missing fields from Naver Map responses.
    """

    @staticmethod
    def _safe_get(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
        current = data
        for key in keys:
            if not isinstance(current, dict):
                return default
            current = current.get(key, default)
            if current is None:
                return default
        return current

    @classmethod
    def parse_business_hours(
        cls, raw_hours: list[dict[str, Any]]
    ) -> list[NaverBusinessHour]:
        """Parse business hours from various Naver formats."""
        result = []
        for entry in raw_hours:
            day_str = entry.get("day", entry.get("day_of_week", ""))
            try:
                day = DayOfWeek(day_str.upper())
            except ValueError:
                try:
                    day = DayOfWeek.from_korean(day_str)
                except ValueError:
                    continue

            # Parse break time from combined string like "13:00 - 14:00"
            break_start = None
            break_end = None
            break_time = entry.get("break_time", entry.get("breakTime"))
            if break_time and isinstance(break_time, str):
                parts = [p.strip() for p in break_time.split("-")]
                if len(parts) == 2:
                    break_start = parts[0] if re.match(r"^\d{2}:\d{2}$", parts[0]) else None
                    break_end = parts[1] if re.match(r"^\d{2}:\d{2}$", parts[1]) else None

            try:
                result.append(
                    NaverBusinessHour(
                        day_of_week=day,
                        open_time=entry.get("open_time", entry.get("startTime")),
                        close_time=entry.get("close_time", entry.get("endTime")),
                        break_start=break_start,
                        break_end=break_end,
                        is_day_off=entry.get("is_day_off", entry.get("isDayOff", False)),
                    )
                )
            except ValueError:
                continue

        return result

    @classmethod
    def parse_menu_info(
        cls, raw_data: dict[str, Any]
    ) -> Optional[NaverMenuInfo]:
        """Parse menu info handling TAB vs TEXT types."""
        menu_data = cls._safe_get(raw_data, "menuInfo")
        if not menu_data:
            return None

        menu_type_str = menu_data.get("menu_type", menu_data.get("type", "TAB"))
        try:
            menu_type = NaverMenuType(menu_type_str.upper())
        except ValueError:
            menu_type = NaverMenuType.TAB

        items = []
        raw_items = menu_data.get("items", menu_data.get("menuList", []))
        for item in raw_items:
            try:
                items.append(NaverMenuItem.model_validate(item))
            except Exception:
                continue

        price_text = menu_data.get("price_text", menu_data.get("priceText"))

        # Adjust type based on actual data available
        if not items and price_text:
            menu_type = NaverMenuType.TEXT
        elif items and not price_text:
            menu_type = NaverMenuType.TAB

        try:
            return NaverMenuInfo(
                menu_type=menu_type,
                items=items,
                price_text=price_text,
            )
        except ValueError:
            return None

    @classmethod
    def parse_review_stats(
        cls, raw_data: dict[str, Any]
    ) -> NaverReviewStats:
        """Parse review statistics from various field names."""
        stats = cls._safe_get(raw_data, "review_stats") or {}
        return NaverReviewStats(
            visitor_reviews=stats.get("visitor_reviews", stats.get("visitorReviews", 0)),
            blog_reviews=stats.get("blog_reviews", stats.get("blogReviews", 0)),
            rating=stats.get("rating"),
        )

    @classmethod
    def parse_coordinates(
        cls, raw_data: dict[str, Any]
    ) -> Optional[Coordinates]:
        """Extract coordinates from raw data."""
        lat = raw_data.get("latitude", raw_data.get("y"))
        lng = raw_data.get("longitude", raw_data.get("x"))
        if lat is None or lng is None:
            return None
        try:
            return Coordinates(latitude=float(lat), longitude=float(lng))
        except (ValueError, TypeError):
            return None

    @classmethod
    def parse(
        cls,
        raw_data: dict[str, Any],
        search_query: Optional[str] = None,
        source_url: Optional[str] = None,
    ) -> NaverPlace:
        """Parse a complete raw Naver Map response into NaverPlace.

        Args:
            raw_data: Raw JSON data from Naver Map.
            search_query: The search query that led to this place.
            source_url: The URL from which data was fetched.

        Returns:
            Fully populated NaverPlace instance.

        Raises:
            ValueError: If essential fields (id, name) are missing.
        """
        place_id = raw_data.get("id", raw_data.get("place_id"))
        name = raw_data.get("name")
        category = raw_data.get("category", "")

        if not place_id or not name:
            raise ValueError(
                f"Missing required fields: id={place_id!r}, name={name!r}"
            )

        business_hours = cls.parse_business_hours(
            raw_data.get("business_hours", raw_data.get("businessHours", []))
        )

        metadata = CrawlMetadata(
            source=CrawlSource.NAVER,
            search_query=search_query,
            source_url=source_url,
        )

        return NaverPlace(
            id=str(place_id),
            name=name,
            category=category or "기타",
            road_address=raw_data.get("road_address", raw_data.get("address")),
            parcel_address=raw_data.get("parcel_address"),
            phone=raw_data.get("phone"),
            description=raw_data.get("description"),
            homepage_url=raw_data.get("homepage_url", raw_data.get("homepage")),
            image_urls=raw_data.get("image_urls", raw_data.get("images", [])),
            facilities=raw_data.get("facilities", []),
            coordinates=cls.parse_coordinates(raw_data),
            business_hours=business_hours,
            review_stats=cls.parse_review_stats(raw_data),
            menu_info=cls.parse_menu_info(raw_data),
            crawl=metadata,
        )
