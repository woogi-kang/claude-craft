-- MediScope Initial Schema
-- 001_initial_schema.sql

-- ============================================================
-- 1. hospitals
-- ============================================================
CREATE TABLE hospitals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    specialty TEXT,
    region TEXT,
    phone TEXT,
    is_registered BOOLEAN DEFAULT false,
    latest_score INTEGER,
    latest_audit_id UUID,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_hospitals_specialty ON hospitals(specialty);
CREATE INDEX idx_hospitals_region ON hospitals(region);
CREATE INDEX idx_hospitals_score ON hospitals(latest_score);

-- ============================================================
-- 2. audits
-- ============================================================
CREATE TABLE audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hospital_id UUID REFERENCES hospitals(id),
    url TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    total_score INTEGER CHECK (total_score >= 0 AND total_score <= 100),
    grade TEXT CHECK (grade IN ('A', 'B', 'C', 'D', 'F')),
    scores JSONB NOT NULL DEFAULT '{}',
    details JSONB NOT NULL DEFAULT '{}',
    benchmark JSONB,
    report_url TEXT,
    screenshots JSONB,
    scan_duration_ms INTEGER,
    source TEXT DEFAULT 'web',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_audits_hospital ON audits(hospital_id);
CREATE INDEX idx_audits_status ON audits(status);
CREATE INDEX idx_audits_created ON audits(created_at DESC);

-- ============================================================
-- 3. audit_items
-- ============================================================
CREATE TABLE audit_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audit_id UUID REFERENCES audits(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    item_key TEXT NOT NULL,
    status TEXT NOT NULL,
    score REAL CHECK (score >= 0 AND score <= 1),
    weight REAL CHECK (weight >= 0 AND weight <= 1),
    details JSONB,
    suggestion TEXT,
    priority TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_audit_items_audit ON audit_items(audit_id);
CREATE INDEX idx_audit_items_category ON audit_items(category);

-- ============================================================
-- 4. leads
-- ============================================================
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    audit_id UUID REFERENCES audits(id),
    email TEXT NOT NULL,
    name TEXT NOT NULL,
    hospital_name TEXT,
    phone TEXT,
    specialty TEXT,
    status TEXT DEFAULT 'new',
    notes JSONB DEFAULT '[]',
    emails_sent INTEGER DEFAULT 0,
    last_email_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_email ON leads(email);

-- ============================================================
-- 5. email_logs
-- ============================================================
CREATE TABLE email_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    template TEXT NOT NULL,
    sent_at TIMESTAMPTZ DEFAULT now(),
    opened_at TIMESTAMPTZ,
    clicked_at TIMESTAMPTZ
);

CREATE INDEX idx_email_logs_lead ON email_logs(lead_id);

-- ============================================================
-- 6. projects
-- ============================================================
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    hospital_id UUID REFERENCES hospitals(id),
    status TEXT NOT NULL DEFAULT 'planning',
    plan JSONB,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_hospital ON projects(hospital_id);

-- ============================================================
-- FK: hospitals.latest_audit_id -> audits.id (deferred)
-- ============================================================
ALTER TABLE hospitals
    ADD CONSTRAINT fk_hospitals_latest_audit
    FOREIGN KEY (latest_audit_id) REFERENCES audits(id);

-- ============================================================
-- updated_at trigger
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_hospitals_updated_at BEFORE UPDATE ON hospitals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_audits_updated_at BEFORE UPDATE ON audits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_leads_updated_at BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trg_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- RLS (Row Level Security)
-- ============================================================
ALTER TABLE hospitals ENABLE ROW LEVEL SECURITY;
ALTER TABLE audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- anon: audit 조회는 JWT audit_claims 기반 (단기 토큰)
CREATE POLICY "anon_view_own_audit" ON audits
    FOR SELECT TO anon USING (
        id = (auth.jwt() -> 'audit_claims' ->> 'audit_id')::uuid
    );

-- anon: audit_items 조회도 audit_claims 기반
CREATE POLICY "anon_view_own_audit_items" ON audit_items
    FOR SELECT TO anon USING (
        audit_id = (auth.jwt() -> 'audit_claims' ->> 'audit_id')::uuid
    );

-- anon INSERT 직접 차단: 모든 쓰기는 Edge Function (service_role) 경유
-- (RLS 활성화 + 별도 INSERT 정책 없음 = 기본 차단)

-- admin: app_metadata.role = 'admin' 기반 전체 접근
CREATE POLICY "admin_full_hospitals" ON hospitals
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

CREATE POLICY "admin_full_audits" ON audits
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

CREATE POLICY "admin_full_audit_items" ON audit_items
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

CREATE POLICY "admin_full_leads" ON leads
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

CREATE POLICY "admin_full_email_logs" ON email_logs
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

CREATE POLICY "admin_full_projects" ON projects
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );
