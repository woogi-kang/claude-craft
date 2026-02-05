"""
Kakao Map Place Data Schema for FastAPI Crawling Project.

Production-ready Pydantic v2 models with:
- Field validation and range constraints
- JSON alias mapping for direct API response parsing
- Enum types for known categorical values
- Shared base models for Naver Map alignment
- Utility methods for data transformation
"""

from __future__ import annotations

import hashlib
import re
from datetime import date, datetime, timezone
from enum import StrEnum
from typing import Any, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)

from crawl.base import (
    Coordinates,
    CrawlMetadata,
    CrawlSource,
)


# ---------------------------------------------------------------------------
# Kakao-Specific Enums
# ---------------------------------------------------------------------------


class OpenStatus(StrEnum):
    """Known operating status values from Kakao Map API."""

    OPEN = "OPEN"
    CLOSE = "CLOSE"
    BREAKTIME = "BREAKTIME"
    NOT_AVAILABLE = "N/A"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value: object) -> OpenStatus:
        return cls.UNKNOWN


# ---------------------------------------------------------------------------
# Kakao Address Models
# ---------------------------------------------------------------------------


class RegionInfo(BaseModel):
    """Administrative region hierarchy (province > district > neighborhood)."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    province: Optional[str] = Field(
        None,
        alias="name1",
        description="Province or metropolitan city",
        examples=["서울"],
    )
    district: Optional[str] = Field(
        None,
        alias="name2",
        description="District (Gu/Gun)",
        examples=["마포구"],
    )
    neighborhood: Optional[str] = Field(
        None,
        alias="name3",
        description="Neighborhood (Dong)",
        examples=["서교동"],
    )

    @property
    def full_region(self) -> str:
        parts = [p for p in [self.province, self.district, self.neighborhood] if p]
        return " ".join(parts)


class KakaoAddressInfo(BaseModel):
    """Kakao Map address with road address, zipcode, and region details."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    road_address: Optional[str] = Field(
        None,
        alias="newaddrfull",
        description="Full road-name address",
        examples=["서울 마포구 홍익로 25"],
    )
    zipcode: Optional[str] = Field(
        None,
        alias="bsizonno",
        description="5-digit postal code",
        examples=["04039"],
    )
    region: Optional[RegionInfo] = Field(None)

    @field_validator("zipcode")
    @classmethod
    def validate_zipcode(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^\d{5}$", v):
            return None
        return v

    @property
    def display_address(self) -> str:
        if self.road_address:
            return self.road_address
        if self.region:
            return self.region.full_region
        return ""


# ---------------------------------------------------------------------------
# Feedback & Operations Models
# ---------------------------------------------------------------------------


class KakaoFeedbackInfo(BaseModel):
    """Aggregated user feedback and review counts from Kakao Map."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",
    )

    score: float = Field(
        0.0,
        ge=0.0,
        le=5.0,
        description="Average rating (0.0-5.0)",
        examples=[4.9],
    )
    review_count: int = Field(
        0,
        alias="comntcnt",
        ge=0,
        description="Total user review count",
        examples=[128],
    )
    blog_review_count: int = Field(
        0,
        alias="blogrvwcnt",
        ge=0,
        description="Blog post review count",
        examples=[862],
    )

    @property
    def total_mentions(self) -> int:
        return self.review_count + self.blog_review_count

    @property
    def has_reviews(self) -> bool:
        return self.review_count > 0


class OpenHourInfo(BaseModel):
    """Real-time operating status from Kakao Map."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    status: OpenStatus = Field(
        OpenStatus.UNKNOWN,
        description="Current operating status",
        examples=["OPEN"],
    )
    current_description: Optional[str] = Field(
        None,
        alias="datetime",
        description="Human-readable status text",
        examples=["진료중"],
    )


# ---------------------------------------------------------------------------
# Menu Models
# ---------------------------------------------------------------------------


class KakaoMenuItem(BaseModel):
    """Single menu item or service offered by a Kakao Map place."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    name: str = Field(
        ...,
        alias="menu",
        min_length=1,
        description="Menu item or service name",
        examples=["아메리카노"],
    )
    price_raw: Optional[str] = Field(
        None,
        alias="price",
        description="Price as displayed (Korean won format)",
        examples=["4,500"],
    )
    photo_url: Optional[str] = Field(
        None,
        alias="photo",
        description="Menu item photo URL",
    )
    is_recommended: bool = Field(
        False,
        alias="recommend",
        description="Whether this item is recommended",
    )

    @property
    def price_value(self) -> Optional[int]:
        """Parse Korean won price string to integer."""
        if not self.price_raw:
            return None
        cleaned = re.sub(r"[^\d]", "", self.price_raw)
        if not cleaned:
            return None
        return int(cleaned)


# ---------------------------------------------------------------------------
# Review Models
# ---------------------------------------------------------------------------


class KakaoReviewItem(BaseModel):
    """Individual user review from Kakao Map."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    content: Optional[str] = Field(
        None,
        alias="contents",
        description="Review text body",
        examples=["친절해요..."],
    )
    rating: int = Field(
        ...,
        alias="point",
        ge=1,
        le=5,
        description="User rating (1-5)",
        examples=[5],
    )
    username: Optional[str] = Field(
        None,
        description="Reviewer display name",
        examples=["라이언"],
    )
    review_date: Optional[str] = Field(
        None,
        alias="date",
        description="Date posted as raw string",
        examples=["2024.01.01"],
    )

    @property
    def parsed_date(self) -> Optional[date]:
        if not self.review_date:
            return None
        for fmt in ("%Y.%m.%d", "%Y-%m-%d", "%y.%m.%d"):
            try:
                return datetime.strptime(self.review_date, fmt).date()
            except ValueError:
                continue
        return None

    @property
    def has_content(self) -> bool:
        return bool(self.content and self.content.strip())


# ---------------------------------------------------------------------------
# Main Place Model
# ---------------------------------------------------------------------------


class PlaceBasicInfo(BaseModel):
    """Core identity and metadata for a Kakao Map place."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    place_id: str = Field(
        ...,
        alias="cid",
        min_length=1,
        description="Unique Kakao place identifier",
        examples=["1048722794"],
    )
    name: str = Field(
        ...,
        alias="placenamefull",
        min_length=1,
        description="Full place name",
        examples=["리즈온의원 홍대점"],
    )
    short_name: Optional[str] = Field(
        None,
        alias="placename",
        description="Abbreviated place name",
        examples=["리즈온의원"],
    )
    phone: Optional[str] = Field(
        None,
        alias="phonenum",
        description="Contact phone number",
        examples=["02-1234-5678"],
    )
    category: Optional[str] = Field(
        None,
        alias="cate1name",
        description="Top-level category",
        examples=["병원"],
    )
    subcategory: Optional[str] = Field(
        None,
        alias="catename",
        description="Specific subcategory",
        examples=["피부과"],
    )
    homepage: Optional[str] = Field(None)
    main_photo_url: Optional[str] = Field(
        None,
        alias="mainphotourl",
        description="Primary photo URL",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Place attribute tags",
        examples=[["주차가능", "반려동물 동반"]],
    )

    address: Optional[KakaoAddressInfo] = Field(None)
    coordinates: Optional[Coordinates] = Field(None)
    feedback: KakaoFeedbackInfo = Field(default_factory=KakaoFeedbackInfo)
    open_hour: Optional[OpenHourInfo] = Field(None)

    @field_validator("homepage")
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

    @property
    def category_path(self) -> str:
        parts = [p for p in [self.category, self.subcategory] if p]
        return " > ".join(parts) if parts else ""

    @property
    def display_address(self) -> str:
        if self.address:
            return self.address.display_address
        return ""


# ---------------------------------------------------------------------------
# Top-Level Aggregate Model
# ---------------------------------------------------------------------------


class KakaoPlaceData(BaseModel):
    """Complete Kakao Map place data aggregate."""

    model_config = ConfigDict(
        populate_by_name=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    basic_info: PlaceBasicInfo
    menus: list[KakaoMenuItem] = Field(default_factory=list)
    reviews: list[KakaoReviewItem] = Field(default_factory=list)
    crawl_metadata: CrawlMetadata = Field(
        default_factory=lambda: CrawlMetadata(source=CrawlSource.KAKAO),
    )

    @property
    def place_id(self) -> str:
        return self.basic_info.place_id

    @property
    def average_review_rating(self) -> Optional[float]:
        if not self.reviews:
            return None
        return sum(r.rating for r in self.reviews) / len(self.reviews)

    @property
    def recommended_menus(self) -> list[KakaoMenuItem]:
        return [m for m in self.menus if m.is_recommended]

    def content_hash(self) -> str:
        content = f"{self.basic_info.place_id}:{self.basic_info.name}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def __repr__(self) -> str:
        return (
            f"KakaoPlaceData(id={self.basic_info.place_id!r}, "
            f"name={self.basic_info.name!r}, "
            f"reviews={len(self.reviews)})"
        )


# ---------------------------------------------------------------------------
# Raw API Response Parser
# ---------------------------------------------------------------------------


class KakaoPlaceParser:
    """Parse raw Kakao Map API JSON into KakaoPlaceData models."""

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
    def parse_address(cls, basic_info: dict[str, Any]) -> Optional[KakaoAddressInfo]:
        address_data = cls._safe_get(basic_info, "address")
        if not address_data:
            return None
        new_addr = cls._safe_get(address_data, "newaddr") or {}
        region_data = cls._safe_get(address_data, "region")
        region = RegionInfo.model_validate(region_data) if region_data else None
        return KakaoAddressInfo(
            road_address=new_addr.get("newaddrfull"),
            zipcode=new_addr.get("bsizonno"),
            region=region,
        )

    @classmethod
    def parse_coordinates(cls, basic_info: dict[str, Any]) -> Optional[Coordinates]:
        x = basic_info.get("x")
        y = basic_info.get("y")
        if x is None or y is None:
            return None
        try:
            return Coordinates.from_kakao(x=float(x), y=float(y))
        except (ValueError, TypeError):
            return None

    @classmethod
    def parse_feedback(cls, basic_info: dict[str, Any]) -> KakaoFeedbackInfo:
        feedback_all = cls._safe_get(basic_info, "feedback", "all") or {}
        return KakaoFeedbackInfo(
            score=feedback_all.get("score", 0.0),
            review_count=feedback_all.get("comntcnt", 0),
            blog_review_count=feedback_all.get("blogrvwcnt", 0),
        )

    @classmethod
    def parse_open_hour(cls, basic_info: dict[str, Any]) -> Optional[OpenHourInfo]:
        realtime = cls._safe_get(basic_info, "openHour", "realtime")
        if not realtime:
            return None
        return OpenHourInfo.model_validate(realtime)

    @classmethod
    def parse_menus(cls, raw_data: dict[str, Any]) -> list[KakaoMenuItem]:
        menu_list = cls._safe_get(raw_data, "menuInfo", "menuList") or []
        items = []
        for item in menu_list:
            try:
                items.append(KakaoMenuItem.model_validate(item))
            except Exception:
                continue
        return items

    @classmethod
    def parse_reviews(cls, raw_data: dict[str, Any]) -> list[KakaoReviewItem]:
        review_list = cls._safe_get(raw_data, "comment", "list") or []
        items = []
        for item in review_list:
            try:
                items.append(KakaoReviewItem.model_validate(item))
            except Exception:
                continue
        return items

    @classmethod
    def parse(
        cls,
        raw_data: dict[str, Any],
        search_query: Optional[str] = None,
        source_url: Optional[str] = None,
    ) -> KakaoPlaceData:
        """Parse a complete raw Kakao Map API response into KakaoPlaceData."""
        basic_info = raw_data.get("basicInfo", {})

        cid = basic_info.get("cid")
        name = basic_info.get("placenamefull")
        if not cid or not name:
            raise ValueError(
                f"Missing required fields: cid={cid!r}, placenamefull={name!r}"
            )

        tags: list[str] = []
        tag_list = cls._safe_get(basic_info, "tags") or []
        if isinstance(tag_list, list):
            tags = [str(t) for t in tag_list if t]

        place_basic = PlaceBasicInfo(
            place_id=str(cid),
            name=name,
            short_name=basic_info.get("placename"),
            phone=basic_info.get("phonenum"),
            category=basic_info.get("cate1name"),
            subcategory=basic_info.get("catename"),
            homepage=basic_info.get("homepage"),
            main_photo_url=basic_info.get("mainphotourl"),
            tags=tags,
            address=cls.parse_address(basic_info),
            coordinates=cls.parse_coordinates(basic_info),
            feedback=cls.parse_feedback(basic_info),
            open_hour=cls.parse_open_hour(basic_info),
        )

        raw_json = str(raw_data)
        raw_hash = hashlib.sha256(raw_json.encode()).hexdigest()[:16]

        metadata = CrawlMetadata(
            source=CrawlSource.KAKAO,
            search_query=search_query,
            source_url=source_url,
            raw_data_hash=raw_hash,
        )

        return KakaoPlaceData(
            basic_info=place_basic,
            menus=cls.parse_menus(raw_data),
            reviews=cls.parse_reviews(raw_data),
            crawl_metadata=metadata,
        )
