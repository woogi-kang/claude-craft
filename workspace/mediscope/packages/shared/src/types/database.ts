import type {
  AuditItemStatus,
  AuditSource,
  AuditStatus,
  Category,
  Grade,
  LeadStatus,
  Priority,
  ProjectStatus,
} from "./enums";

// ============================================================
// hospitals
// ============================================================
export interface HospitalRow {
  id: string;
  name: string;
  url: string;
  specialty: string | null;
  region: string | null;
  phone: string | null;
  is_registered: boolean;
  latest_score: number | null;
  latest_audit_id: string | null;
  metadata: Record<string, unknown> | null;
  created_at: string;
  updated_at: string;
}

export interface HospitalInsert {
  id?: string;
  name: string;
  url: string;
  specialty?: string | null;
  region?: string | null;
  phone?: string | null;
  is_registered?: boolean;
  latest_score?: number | null;
  latest_audit_id?: string | null;
  metadata?: Record<string, unknown> | null;
}

export interface HospitalUpdate {
  name?: string;
  url?: string;
  specialty?: string | null;
  region?: string | null;
  phone?: string | null;
  is_registered?: boolean;
  latest_score?: number | null;
  latest_audit_id?: string | null;
  metadata?: Record<string, unknown> | null;
}

// ============================================================
// audits
// ============================================================
export interface AuditScores {
  technical_seo?: number;
  performance?: number;
  geo_aeo?: number;
  multilingual?: number;
  competitiveness?: number;
}

export interface AuditRow {
  id: string;
  hospital_id: string | null;
  url: string;
  status: AuditStatus;
  total_score: number | null;
  grade: Grade | null;
  scores: AuditScores;
  details: Record<string, unknown>;
  benchmark: Record<string, unknown> | null;
  report_url: string | null;
  screenshots: string[] | null;
  scan_duration_ms: number | null;
  source: AuditSource;
  created_at: string;
  updated_at: string;
}

export interface AuditInsert {
  id?: string;
  hospital_id?: string | null;
  url: string;
  status?: AuditStatus;
  total_score?: number | null;
  grade?: Grade | null;
  scores?: AuditScores;
  details?: Record<string, unknown>;
  benchmark?: Record<string, unknown> | null;
  report_url?: string | null;
  screenshots?: string[] | null;
  scan_duration_ms?: number | null;
  source?: AuditSource;
}

export interface AuditUpdate {
  hospital_id?: string | null;
  url?: string;
  status?: AuditStatus;
  total_score?: number | null;
  grade?: Grade | null;
  scores?: AuditScores;
  details?: Record<string, unknown>;
  benchmark?: Record<string, unknown> | null;
  report_url?: string | null;
  screenshots?: string[] | null;
  scan_duration_ms?: number | null;
  source?: AuditSource;
}

// ============================================================
// audit_items
// ============================================================
export interface AuditItemRow {
  id: string;
  audit_id: string;
  category: Category;
  item_key: string;
  status: AuditItemStatus;
  score: number | null;
  weight: number | null;
  details: Record<string, unknown> | null;
  suggestion: string | null;
  priority: Priority | null;
  created_at: string;
}

export interface AuditItemInsert {
  id?: string;
  audit_id: string;
  category: Category;
  item_key: string;
  status: AuditItemStatus;
  score?: number | null;
  weight?: number | null;
  details?: Record<string, unknown> | null;
  suggestion?: string | null;
  priority?: Priority | null;
}

export interface AuditItemUpdate {
  status?: AuditItemStatus;
  score?: number | null;
  weight?: number | null;
  details?: Record<string, unknown> | null;
  suggestion?: string | null;
  priority?: Priority | null;
}

// ============================================================
// leads
// ============================================================
export interface LeadNote {
  date: string;
  content: string;
  author: string;
}

export interface LeadRow {
  id: string;
  audit_id: string | null;
  email: string;
  name: string;
  hospital_name: string | null;
  phone: string | null;
  specialty: string | null;
  status: LeadStatus;
  notes: LeadNote[];
  emails_sent: number;
  last_email_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface LeadInsert {
  id?: string;
  audit_id?: string | null;
  email: string;
  name: string;
  hospital_name?: string | null;
  phone?: string | null;
  specialty?: string | null;
  status?: LeadStatus;
  notes?: LeadNote[];
  emails_sent?: number;
  last_email_at?: string | null;
}

export interface LeadUpdate {
  audit_id?: string | null;
  email?: string;
  name?: string;
  hospital_name?: string | null;
  phone?: string | null;
  specialty?: string | null;
  status?: LeadStatus;
  notes?: LeadNote[];
  emails_sent?: number;
  last_email_at?: string | null;
}

// ============================================================
// email_logs
// ============================================================
export interface EmailLogRow {
  id: string;
  lead_id: string | null;
  template: string;
  sent_at: string;
  opened_at: string | null;
  clicked_at: string | null;
}

export interface EmailLogInsert {
  id?: string;
  lead_id?: string | null;
  template: string;
  sent_at?: string;
  opened_at?: string | null;
  clicked_at?: string | null;
}

export interface EmailLogUpdate {
  opened_at?: string | null;
  clicked_at?: string | null;
}

// ============================================================
// projects
// ============================================================
export interface ProjectRow {
  id: string;
  lead_id: string | null;
  hospital_id: string | null;
  status: ProjectStatus;
  plan: Record<string, unknown> | null;
  start_date: string | null;
  end_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectInsert {
  id?: string;
  lead_id?: string | null;
  hospital_id?: string | null;
  status?: ProjectStatus;
  plan?: Record<string, unknown> | null;
  start_date?: string | null;
  end_date?: string | null;
}

export interface ProjectUpdate {
  lead_id?: string | null;
  hospital_id?: string | null;
  status?: ProjectStatus;
  plan?: Record<string, unknown> | null;
  start_date?: string | null;
  end_date?: string | null;
}

// ============================================================
// Database schema (Supabase-style aggregate)
// ============================================================
export interface Database {
  public: {
    Tables: {
      hospitals: {
        Row: HospitalRow;
        Insert: HospitalInsert;
        Update: HospitalUpdate;
      };
      audits: { Row: AuditRow; Insert: AuditInsert; Update: AuditUpdate };
      audit_items: {
        Row: AuditItemRow;
        Insert: AuditItemInsert;
        Update: AuditItemUpdate;
      };
      leads: { Row: LeadRow; Insert: LeadInsert; Update: LeadUpdate };
      email_logs: {
        Row: EmailLogRow;
        Insert: EmailLogInsert;
        Update: EmailLogUpdate;
      };
      projects: {
        Row: ProjectRow;
        Insert: ProjectInsert;
        Update: ProjectUpdate;
      };
    };
  };
}
