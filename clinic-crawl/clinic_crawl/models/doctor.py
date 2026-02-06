"""Doctor / medical staff information models."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from clinic_crawl.models.enums import DoctorRole


class DoctorCredential(BaseModel):
    """A single credential entry for a doctor."""

    model_config = ConfigDict(frozen=True)

    credential_type: str  # e.g. "전문의", "학위", "자격"
    value: str


class DoctorInfo(BaseModel):
    """Information about a single doctor or medical staff member."""

    name: str | None = None
    role: DoctorRole = DoctorRole.SPECIALIST
    photo_url: str | None = None
    credentials: list[DoctorCredential] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    career: list[str] = Field(default_factory=list)


class DoctorPage(BaseModel):
    """Extraction result from a hospital's doctor/staff page."""

    doctors: list[DoctorInfo] = Field(default_factory=list)
    page_url: str | None = None
    menu_label: str | None = None  # The actual menu text used (e.g. "의료진 소개")

    @property
    def doctor_count(self) -> int:
        return len(self.doctors)

    @property
    def has_photos(self) -> bool:
        return any(d.photo_url for d in self.doctors)
