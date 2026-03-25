"""MediScope Pydantic v2 models for Worker API."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


# ============================================================
# Enums
# ============================================================
class AuditStatus(StrEnum):
    PENDING = "pending"
    SCANNING = "scanning"
    COMPLETED = "completed"
    FAILED = "failed"


class LeadStatus(StrEnum):
    NEW = "new"
    CONTACTED = "contacted"
    CONSULTING = "consulting"
    PROPOSAL_SENT = "proposal_sent"
    CONTRACTED = "contracted"
    ACTIVE = "active"
    CHURNED = "churned"


class Grade(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class Category(StrEnum):
    TECHNICAL_SEO = "technical_seo"
    PERFORMANCE = "performance"
    GEO_AEO = "geo_aeo"
    MULTILINGUAL = "multilingual"
    COMPETITIVENESS = "competitiveness"


class AuditItemStatus(StrEnum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    INFO = "info"


class Priority(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AuditSource(StrEnum):
    WEB = "web"
    API = "api"
    BATCH = "batch"


class ProjectStatus(StrEnum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ============================================================
# Hospital
# ============================================================
class Hospital(BaseModel):
    id: UUID
    name: str
    url: str
    specialty: str | None = None
    region: str | None = None
    phone: str | None = None
    is_registered: bool = False
    latest_score: int | None = None
    latest_audit_id: UUID | None = None
    metadata: dict | None = None
    created_at: datetime
    updated_at: datetime


class HospitalCreate(BaseModel):
    name: str
    url: str
    specialty: str | None = None
    region: str | None = None
    phone: str | None = None
    is_registered: bool = False
    metadata: dict | None = None


# ============================================================
# Audit
# ============================================================
class AuditScores(BaseModel):
    technical_seo: float | None = None
    performance: float | None = None
    geo_aeo: float | None = None
    multilingual: float | None = None
    competitiveness: float | None = None


class Audit(BaseModel):
    id: UUID
    hospital_id: UUID | None = None
    url: str
    status: AuditStatus = AuditStatus.PENDING
    total_score: int | None = Field(None, ge=0, le=100)
    grade: Grade | None = None
    scores: AuditScores = Field(default_factory=AuditScores)
    details: dict = Field(default_factory=dict)
    benchmark: dict | None = None
    report_url: str | None = None
    screenshots: list[str] | None = None
    scan_duration_ms: int | None = None
    source: AuditSource = AuditSource.WEB
    created_at: datetime
    updated_at: datetime


# ============================================================
# AuditItem
# ============================================================
class AuditItem(BaseModel):
    id: UUID
    audit_id: UUID
    category: Category
    item_key: str
    status: AuditItemStatus
    score: float | None = Field(None, ge=0, le=1)
    weight: float | None = Field(None, ge=0, le=1)
    details: dict | None = None
    suggestion: str | None = None
    priority: Priority | None = None
    created_at: datetime


class AuditItemCreate(BaseModel):
    category: Category
    item_key: str
    status: AuditItemStatus
    score: float | None = Field(None, ge=0, le=1)
    weight: float | None = Field(None, ge=0, le=1)
    details: dict | None = None
    suggestion: str | None = None
    priority: Priority | None = None


# ============================================================
# Lead
# ============================================================
class LeadNote(BaseModel):
    date: str
    content: str
    author: str


class Lead(BaseModel):
    id: UUID
    audit_id: UUID | None = None
    email: str
    name: str
    hospital_name: str | None = None
    phone: str | None = None
    specialty: str | None = None
    status: LeadStatus = LeadStatus.NEW
    notes: list[LeadNote] = Field(default_factory=list)
    emails_sent: int = 0
    last_email_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class LeadCreate(BaseModel):
    audit_id: UUID | None = None
    email: str
    name: str
    hospital_name: str | None = None
    phone: str | None = None
    specialty: str | None = None


# ============================================================
# EmailLog
# ============================================================
class EmailLog(BaseModel):
    id: UUID
    lead_id: UUID | None = None
    template: str
    sent_at: datetime
    opened_at: datetime | None = None
    clicked_at: datetime | None = None


# ============================================================
# Project
# ============================================================
class Project(BaseModel):
    id: UUID
    lead_id: UUID | None = None
    hospital_id: UUID | None = None
    status: ProjectStatus = ProjectStatus.PLANNING
    plan: dict | None = None
    start_date: str | None = None
    end_date: str | None = None
    created_at: datetime
    updated_at: datetime


# ============================================================
# Worker API models
# ============================================================
class ScanRequest(BaseModel):
    audit_id: UUID
    url: str
    specialty: str | None = None


class ScanCallbackPayload(BaseModel):
    audit_id: UUID
    status: AuditStatus
    total_score: int = Field(ge=0, le=100)
    grade: Grade
    scores: AuditScores
    details: dict
    items: list[AuditItemCreate]
    scan_duration_ms: int
