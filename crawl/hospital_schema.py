"""
Hospital-specific extension of NaverPlace.

Adds fields extracted from the /information page that are
specific to hospital/clinic place types on Naver Map.
"""

from __future__ import annotations

from typing import Optional, Self
from urllib.parse import urlparse

from pydantic import ConfigDict, Field, field_validator, model_validator

from crawl.naver_map_schema import NaverPlace


class NaverHospitalPlace(NaverPlace):
    """NaverPlace extended with hospital/clinic-specific fields."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="ignore",
    )

    # Hospital-specific fields from /information page
    youtube_url: Optional[str] = Field(
        default=None,
        description="YouTube channel URL",
    )
    instagram_url: Optional[str] = Field(
        default=None,
        description="Instagram profile URL",
    )
    reservation_url: Optional[str] = Field(
        default=None,
        description="Naver Booking URL",
        examples=["https://booking.naver.com/booking/13/bizes/1234567"],
    )
    parking_info: Optional[str] = Field(
        default=None,
        description="Parking availability description",
    )

    # Photo crawl results
    local_photo_paths: list[str] = Field(
        default_factory=list,
        description="Local filesystem paths of downloaded photos",
    )
    photo_count: int = Field(
        default=0,
        ge=0,
        description="Total photos downloaded",
    )

    @field_validator("reservation_url")
    @classmethod
    def validate_reservation_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        try:
            parsed = urlparse(v)
            if parsed.scheme != "https" or parsed.hostname != "booking.naver.com":
                return None
        except Exception:
            return None
        return v

    @field_validator("youtube_url")
    @classmethod
    def validate_youtube_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        try:
            parsed = urlparse(v)
            hostname = (parsed.hostname or "").lower()
            if hostname not in (
                "youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com",
            ):
                return None
        except Exception:
            return None
        return v

    @field_validator("instagram_url")
    @classmethod
    def validate_instagram_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        try:
            parsed = urlparse(v)
            hostname = (parsed.hostname or "").lower()
            if hostname not in ("instagram.com", "www.instagram.com"):
                return None
        except Exception:
            return None
        return v

    @model_validator(mode="after")
    def sync_photo_count(self) -> Self:
        """Keep photo_count consistent with local_photo_paths."""
        if self.local_photo_paths:
            object.__setattr__(self, "photo_count", len(self.local_photo_paths))
        return self
