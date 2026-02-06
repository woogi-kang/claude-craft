"""Pydantic model for skin_clinics.csv row input."""

from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SkinClinicRow(BaseModel):
    """One row from samples/skin_clinics.csv with Korean column aliases."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        populate_by_name=True,
    )

    no: int = Field(alias="NO")
    name: str = Field(alias="병원/약국명")
    hospital_type: str = Field(alias="병원/약국구분")
    phone: str | None = Field(default=None, alias="전화번호")
    zipcode: str | None = Field(default=None, alias="우편번호")
    address: str | None = Field(default=None, alias="소재지주소")
    homepage: str | None = Field(default=None, alias="홈페이지")
    source: str | None = Field(default=None, alias="출처")

    # Naver-matched fields
    naver_name: str | None = Field(default=None, alias="naver_name")
    naver_address: str | None = Field(default=None, alias="naver_address")
    naver_website: str | None = Field(default=None, alias="naver_website")
    naver_category: str | None = Field(default=None, alias="naver_category")
    naver_mapx: float | None = Field(default=None, alias="naver_mapx")
    naver_mapy: float | None = Field(default=None, alias="naver_mapy")
    naver_matched: bool | None = Field(default=None, alias="naver_matched")
    match_reason: str | None = Field(default=None, alias="match_reason")

    @field_validator("homepage", "naver_website", mode="before")
    @classmethod
    def clean_url(cls, v: str | None) -> str | None:
        """Normalize URLs: strip, add protocol, reject garbage values."""
        if v is None:
            return None
        v = str(v).strip()
        if not v or v in ("", "http://", "https://", "ㅇ", "-", "없음"):
            return None
        # Remove BOM and zero-width characters
        v = re.sub(r"[\ufeff\u200b\u200c\u200d]", "", v)
        # Add https:// if no protocol
        if not re.match(r"^https?://", v, re.IGNORECASE):
            v = f"https://{v}"
        return v

    @property
    def urls(self) -> list[str]:
        """All available URLs for this hospital, deduplicated."""
        seen: set[str] = set()
        result: list[str] = []
        for url in (self.homepage, self.naver_website):
            if url and url not in seen:
                seen.add(url)
                result.append(url)
        return result
