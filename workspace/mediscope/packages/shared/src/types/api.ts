import type { AuditRow, AuditItemRow, LeadRow } from "./database";
import type { AuditStatus, Grade } from "./enums";

// ============================================================
// Audit API
// ============================================================
export interface CreateAuditRequest {
  url: string;
  specialty?: string;
}

export interface CreateAuditResponse {
  id: string;
  status: AuditStatus;
  estimated_time_seconds: number;
}

export interface AuditSummaryResponse {
  id: string;
  url: string;
  status: AuditStatus;
  total_score: number | null;
  grade: Grade | null;
  scores: AuditRow["scores"];
  created_at: string;
}

export interface AuditDetailResponse extends AuditRow {
  items: AuditItemRow[];
}

// ============================================================
// Lead API
// ============================================================
export interface CreateLeadRequest {
  audit_id: string;
  email: string;
  name: string;
  hospital_name?: string;
  phone?: string;
  specialty?: string;
}

export interface CreateLeadResponse {
  id: string;
  status: string;
}

export interface LeadListResponse {
  data: LeadRow[];
  total: number;
  page: number;
  per_page: number;
}

// ============================================================
// Worker API (FastAPI internal)
// ============================================================
export interface ScanRequest {
  audit_id: string;
  url: string;
  specialty?: string;
}

export interface ScanCallbackPayload {
  audit_id: string;
  status: AuditStatus;
  total_score: number;
  grade: Grade;
  scores: AuditRow["scores"];
  details: Record<string, unknown>;
  items: Omit<AuditItemRow, "id" | "audit_id" | "created_at">[];
  scan_duration_ms: number;
}

// ============================================================
// Common
// ============================================================
export interface PaginationParams {
  page?: number;
  per_page?: number;
}

export interface ApiError {
  error: string;
  message: string;
  status_code: number;
}
