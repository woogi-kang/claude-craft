-- Phase A+: GEO/AEO + Benchmark + Subscriptions
-- 003_phase_aplus.sql

-- ============================================================
-- 1. beauty_clinics: add latest_score for benchmark
-- ============================================================
ALTER TABLE beauty_clinics ADD COLUMN IF NOT EXISTS latest_score INTEGER;
CREATE INDEX IF NOT EXISTS idx_beauty_clinics_score ON beauty_clinics(latest_score);
CREATE INDEX IF NOT EXISTS idx_beauty_clinics_sido ON beauty_clinics(sido);
CREATE INDEX IF NOT EXISTS idx_beauty_clinics_sggu ON beauty_clinics(sggu);

-- ============================================================
-- 2. subscriptions: hospital monitoring subscriptions
-- ============================================================
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hospital_id UUID REFERENCES hospitals(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    name TEXT,
    frequency TEXT DEFAULT 'monthly' CHECK (frequency IN ('weekly', 'biweekly', 'monthly')),
    is_active BOOLEAN DEFAULT true,
    last_scan_at TIMESTAMPTZ,
    next_scan_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_subscriptions_hospital ON subscriptions(hospital_id);
CREATE INDEX idx_subscriptions_next_scan ON subscriptions(next_scan_at) WHERE is_active = true;
CREATE INDEX idx_subscriptions_email ON subscriptions(email);

CREATE TRIGGER trg_subscriptions_updated_at BEFORE UPDATE ON subscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- 3. score_history: track score changes over time
-- ============================================================
CREATE TABLE IF NOT EXISTS score_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hospital_id UUID REFERENCES hospitals(id) ON DELETE CASCADE,
    audit_id UUID REFERENCES audits(id) ON DELETE CASCADE,
    total_score INTEGER CHECK (total_score >= 0 AND total_score <= 100),
    grade TEXT CHECK (grade IN ('A', 'B', 'C', 'D', 'F')),
    category_scores JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_score_history_hospital ON score_history(hospital_id);
CREATE INDEX idx_score_history_created ON score_history(created_at DESC);

-- ============================================================
-- 4. alerts: score change notifications
-- ============================================================
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID REFERENCES subscriptions(id) ON DELETE CASCADE,
    hospital_id UUID REFERENCES hospitals(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('score_drop', 'score_improve', 'new_issue', 'issue_resolved')),
    message TEXT NOT NULL,
    prev_score INTEGER,
    new_score INTEGER,
    is_read BOOLEAN DEFAULT false,
    sent_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_alerts_subscription ON alerts(subscription_id);
CREATE INDEX idx_alerts_hospital ON alerts(hospital_id);

-- ============================================================
-- 5. RLS for new tables
-- ============================================================
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE score_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

-- Public read for score_history (for benchmark charts)
CREATE POLICY "public_read_score_history" ON score_history
    FOR SELECT TO anon USING (true);

-- Admin full access
CREATE POLICY "admin_full_subscriptions" ON subscriptions
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

CREATE POLICY "admin_full_score_history" ON score_history
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

CREATE POLICY "admin_full_alerts" ON alerts
    FOR ALL TO authenticated USING (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

-- Service role bypasses RLS for backend operations
