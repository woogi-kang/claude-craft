"""Central hospital crawl result model."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from clinic_crawl.models.doctor import DoctorPage
from clinic_crawl.models.enums import CrawlCategory, CrawlPhase
from clinic_crawl.models.social import SocialChannels


class ClinicWebsite(BaseModel):
    """Metadata about a clinic's website after initial probe."""

    final_url: str | None = None
    redirected_from: str | None = None
    status_code: int | None = None
    server_header: str | None = None
    platform_detected: str | None = None  # e.g. "imweb", "mobidoc", "wordpress"
    has_javascript_rendering: bool = False


class HospitalCrawlResult(BaseModel):
    """Complete crawl result for a single hospital."""

    hospital_no: int
    name: str
    category: CrawlCategory = CrawlCategory.NO_URL
    phase: CrawlPhase = CrawlPhase.PENDING
    chain_domain: str | None = None

    website: ClinicWebsite | None = None
    social_channels: SocialChannels = Field(default_factory=SocialChannels)
    doctor_page: DoctorPage | None = None

    crawled_at: datetime | None = None
    errors: list[str] = Field(default_factory=list)

    def mark_complete(self) -> None:
        self.crawled_at = datetime.now(UTC)

    @property
    def has_social(self) -> bool:
        return len(self.social_channels.links) > 0

    @property
    def has_doctors(self) -> bool:
        return self.doctor_page is not None and self.doctor_page.doctor_count > 0
