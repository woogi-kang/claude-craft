"""Social consultation channel models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from clinic_crawl.models.enums import ExtractionMethod, SocialPlatform


class SocialLink(BaseModel):
    """A single social consultation channel link."""

    model_config = ConfigDict(frozen=True)

    platform: SocialPlatform
    url: str
    extraction_method: ExtractionMethod
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)


class SocialChannels(BaseModel):
    """All social channels found for a hospital."""

    links: list[SocialLink] = Field(default_factory=list)
    chat_widget_detected: bool = False
    qr_image_urls: list[str] = Field(default_factory=list)

    @property
    def platforms_found(self) -> set[SocialPlatform]:
        return {link.platform for link in self.links}

    @property
    def has_kakao(self) -> bool:
        return SocialPlatform.KAKAO in self.platforms_found

    def deduplicated(self) -> SocialChannels:
        """Return a copy with duplicate URLs removed, keeping highest confidence."""
        best: dict[tuple[SocialPlatform, str], SocialLink] = {}
        for link in self.links:
            key = (link.platform, link.url)
            existing = best.get(key)
            if existing is None or link.confidence > existing.confidence:
                best[key] = link
        return SocialChannels(
            links=list(best.values()),
            chat_widget_detected=self.chat_widget_detected,
            qr_image_urls=self.qr_image_urls,
        )
