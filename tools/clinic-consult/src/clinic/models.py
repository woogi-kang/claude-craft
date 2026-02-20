"""Data models for clinic information from hospitals.db."""

from __future__ import annotations

from dataclasses import dataclass, field

from src.messenger.deep_link import build_chat_url


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
    contact_urls: dict[str, str] = field(default_factory=dict)
    phone: str | None = None
    address: str | None = None
    website: str | None = None
    doctors: list[DoctorInfo] = field(default_factory=list)

    # --- Backward-compatible properties ---

    @property
    def kakao_url(self) -> str | None:
        return self.contact_urls.get("kakao")

    @property
    def has_kakao(self) -> bool:
        return "kakao" in self.contact_urls

    @property
    def line_url(self) -> str | None:
        return self.contact_urls.get("line")

    @property
    def has_line(self) -> bool:
        return "line" in self.contact_urls

    # --- Platform-generic methods ---

    def has_platform(self, platform: str) -> bool:
        """Check if the clinic has a contact URL for the given platform."""
        from src.messenger import normalize_platform

        return normalize_platform(platform) in self.contact_urls

    def get_contact_url(self, platform: str) -> str | None:
        """Get the raw contact URL for a platform."""
        from src.messenger import normalize_platform

        return self.contact_urls.get(normalize_platform(platform))

    def get_chat_url(self, platform: str) -> str | None:
        """Get the direct chat URL for a platform."""
        raw = self.get_contact_url(platform)
        if not raw:
            return None
        return build_chat_url(platform, raw)

    @property
    def kakao_chat_url(self) -> str | None:
        """Backward-compatible: direct KakaoTalk chat URL."""
        return self.get_chat_url("kakao")
