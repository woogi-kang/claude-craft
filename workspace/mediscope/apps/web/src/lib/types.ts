export type AuditStatus = "pending" | "scanning" | "completed" | "failed";
export type LeadStatus =
  | "new"
  | "contacted"
  | "consulting"
  | "proposal_sent"
  | "contracted"
  | "active"
  | "churned";
export type Grade = "A" | "B" | "C" | "D" | "F";
export type Category =
  | "technical_seo"
  | "performance"
  | "geo_aeo"
  | "multilingual"
  | "competitiveness";

export interface AuditScores {
  technical_seo: number;
  performance: number;
  geo_aeo: number;
  multilingual: number;
  competitiveness: number;
}

export interface Audit {
  id: string;
  hospital_id: string | null;
  url: string;
  status: AuditStatus;
  total_score: number | null;
  grade: Grade | null;
  scores: AuditScores;
  details: Record<string, unknown>;
  report_url: string | null;
  scan_duration_ms: number | null;
  created_at: string;
  updated_at: string;
}

export interface Lead {
  id: string;
  audit_id: string | null;
  email: string;
  name: string;
  hospital_name: string | null;
  phone: string | null;
  specialty: string | null;
  status: LeadStatus;
  notes: Array<{ date: string; content: string; author: string }>;
  emails_sent: number;
  created_at: string;
  updated_at: string;
}

export interface CreateAuditRequest {
  url: string;
  specialty?: string;
}

export interface CreateAuditResponse {
  id: string;
  status: AuditStatus;
  estimated_time_seconds: number;
}

export interface CreateLeadRequest {
  audit_id: string;
  email: string;
  name: string;
  hospital_name?: string;
  phone?: string;
  specialty?: string;
}

export const CATEGORY_LABELS: Record<Category, string> = {
  technical_seo: "기술 SEO",
  performance: "성능",
  geo_aeo: "GEO/AEO",
  multilingual: "다국어",
  competitiveness: "경쟁력",
};

export const GRADE_COLORS: Record<Grade, string> = {
  A: "text-green-600",
  B: "text-blue-600",
  C: "text-yellow-600",
  D: "text-orange-600",
  F: "text-red-600",
};

export function getGrade(score: number): Grade {
  if (score >= 80) return "A";
  if (score >= 60) return "B";
  if (score >= 40) return "C";
  if (score >= 20) return "D";
  return "F";
}
