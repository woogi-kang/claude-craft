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

export type AuditItemStatus = "pass" | "warn" | "fail" | "info";

export type Priority = "critical" | "high" | "medium" | "low";

export type AuditSource = "web" | "api" | "batch";

export type ProjectStatus =
  | "planning"
  | "in_progress"
  | "completed"
  | "cancelled";
