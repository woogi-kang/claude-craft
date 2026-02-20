"""Data models for clinic information from hospitals.db."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DoctorInfo:
    """Doctor/staff record from the hospitals database."""

    name: str
    name_english: str | None = None
    role: str = "specialist"
    education: list[str] = field(default_factory=list)
    career: list[str] = field(default_factory=list)
    credentials: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ClinicInfo:
    """Aggregated clinic information for reservation contact."""

    hospital_no: int
    name: str
    kakao_url: str | None = None
    phone: str | None = None
    address: str | None = None
    website: str | None = None
    doctors: list[DoctorInfo] = field(default_factory=list)

    @property
    def has_kakao(self) -> bool:
        return self.kakao_url is not None

    @property
    def kakao_chat_url(self) -> str | None:
        """Return the direct chat URL for the KakaoTalk channel."""
        if not self.kakao_url:
            return None
        url = self.kakao_url.rstrip("/")
        # Strip fragment identifiers
        if "#" in url:
            url = url.split("#")[0]
        # Ensure /chat suffix for direct chat
        if not url.endswith("/chat"):
            url = f"{url}/chat"
        return url
