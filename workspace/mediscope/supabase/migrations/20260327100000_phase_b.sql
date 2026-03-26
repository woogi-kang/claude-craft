-- Phase B: Before/After Reports + Project Management
-- 20260327100000_phase_b.sql

ALTER TABLE projects ADD COLUMN IF NOT EXISTS name TEXT;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS contract_amount INTEGER;
ALTER TABLE projects ADD COLUMN IF NOT EXISTS before_audit_id UUID REFERENCES audits(id);
ALTER TABLE projects ADD COLUMN IF NOT EXISTS latest_audit_id UUID REFERENCES audits(id);
ALTER TABLE projects ADD COLUMN IF NOT EXISTS client_token TEXT UNIQUE;
CREATE INDEX IF NOT EXISTS idx_projects_client_token ON projects(client_token) WHERE client_token IS NOT NULL;
ALTER TABLE projects DROP CONSTRAINT IF EXISTS chk_projects_status;
ALTER TABLE projects ADD CONSTRAINT chk_projects_status CHECK (status IN ('planning', 'in_progress', 'completed', 'cancelled'));
