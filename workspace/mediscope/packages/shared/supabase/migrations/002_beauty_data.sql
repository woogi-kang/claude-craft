-- CheckYourHospital: beauty-db integration
-- 002_beauty_data.sql
-- Imports dermatology clinic/procedure/price data for products

-- ============================================================
-- 1. beauty_clinics (from beauty-db hospitals)
-- ============================================================
CREATE TABLE beauty_clinics (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(500),
    website VARCHAR(500),
    phone VARCHAR(50),
    category VARCHAR(255),
    domain VARCHAR(255),
    region VARCHAR(100),
    is_foreign_patient_facilitator BOOLEAN DEFAULT false,
    ykiho VARCHAR(400),
    hira_name VARCHAR(255),
    sido VARCHAR(20),
    sggu VARCHAR(30),
    dr_count INTEGER,
    established_date VARCHAR(8),
    naver_place_id BIGINT,
    chain_group VARCHAR(50),
    clinic_final_url VARCHAR(500),
    google_lat NUMERIC(10,7),
    google_lng NUMERIC(10,7),
    dong VARCHAR,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_bc_sido ON beauty_clinics(sido);
CREATE INDEX idx_bc_sggu ON beauty_clinics(sggu);
CREATE INDEX idx_bc_foreign ON beauty_clinics(is_foreign_patient_facilitator);
CREATE INDEX idx_bc_website ON beauty_clinics(website);

-- ============================================================
-- 2. procedure_categories (from dermatology_categories)
-- ============================================================
CREATE TABLE procedure_categories (
    id INTEGER PRIMARY KEY,
    level INTEGER NOT NULL,
    parent_id INTEGER,
    name VARCHAR(50) NOT NULL,
    name_en VARCHAR(50),
    description TEXT,
    icon VARCHAR(30),
    display_order INTEGER DEFAULT 1,
    card_title TEXT,
    card_image_url VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 3. procedures (from dermatology_procedures)
-- ============================================================
CREATE TABLE procedures (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    grade INTEGER DEFAULT 2,
    primary_category_id INTEGER REFERENCES procedure_categories(id),
    thumbnail_url TEXT,
    is_leaf BOOLEAN DEFAULT true,
    thumbnail_alt VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_proc_category ON procedures(primary_category_id);

-- ============================================================
-- 4. procedure_details (from dermatology_procedure_details)
-- ============================================================
CREATE TABLE procedure_details (
    id INTEGER PRIMARY KEY,
    procedure_id INTEGER REFERENCES procedures(id),
    procedure_name VARCHAR(200) NOT NULL,
    alias TEXT,
    target TEXT,
    effect TEXT,
    principle TEXT NOT NULL,
    mechanism_detail TEXT NOT NULL,
    advantage TEXT,
    method TEXT NOT NULL,
    duration_of_procedure TEXT,
    golden_time TEXT,
    duration TEXT,
    recommended_cycle TEXT,
    result_expectation TEXT,
    not_recommended TEXT,
    side_effects TEXT,
    reverse_effects TEXT,
    pain_level INTEGER,
    pain_description TEXT,
    downtime TEXT,
    post_care TEXT,
    differences TEXT,
    hospital_caution TEXT,
    trend TEXT,
    comment_to_friend TEXT,
    price_reason TEXT,
    average_price TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pd_procedure ON procedure_details(procedure_id);

-- ============================================================
-- 5. procedure_intl (from procedure_translations)
-- ============================================================
CREATE TABLE procedure_intl (
    id INTEGER PRIMARY KEY,
    procedure_id INTEGER REFERENCES procedures(id),
    language_code VARCHAR(10) NOT NULL,
    translated_name TEXT,
    alias TEXT,
    principle TEXT,
    method TEXT,
    pain_description TEXT,
    downtime TEXT,
    duration TEXT,
    recommended_cycle TEXT,
    differences TEXT,
    golden_time TEXT,
    post_care TEXT,
    hospital_caution TEXT,
    trend TEXT,
    comment_to_friend TEXT,
    price_reason TEXT,
    average_price TEXT,
    not_recommended TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pi_procedure ON procedure_intl(procedure_id);
CREATE INDEX idx_pi_lang ON procedure_intl(language_code);

-- ============================================================
-- 6. std_procedures
-- ============================================================
CREATE TABLE beauty_std_procedures (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category_id INTEGER,
    subcategory_id INTEGER,
    aliases TEXT[],
    product_type VARCHAR(20),
    is_searchable BOOLEAN DEFAULT false,
    anesthesia_level VARCHAR(10) DEFAULT 'medium',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================================
-- 7. price_comparison (from market_price_by_county)
-- ============================================================
CREATE TABLE price_comparison (
    id INTEGER PRIMARY KEY,
    therapy_id INTEGER REFERENCES beauty_std_procedures(id),
    price_min NUMERIC(12,2),
    price_max NUMERIC(12,2),
    currency VARCHAR(3) NOT NULL,
    price_type VARCHAR(50) DEFAULT 'standard',
    condition_note TEXT,
    valid_month DATE NOT NULL,
    country VARCHAR(2) NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pc_therapy ON price_comparison(therapy_id);
CREATE INDEX idx_pc_country ON price_comparison(country);

-- ============================================================
-- 8. intl_prices (from international_prices)
-- ============================================================
CREATE TABLE intl_prices (
    id INTEGER PRIMARY KEY,
    top_procedure_id INTEGER,
    country_code VARCHAR(5) NOT NULL,
    currency VARCHAR(5) NOT NULL,
    price INTEGER DEFAULT 0,
    price_unit TEXT,
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================================
-- 9. search_dict (from search_dictionary)
-- ============================================================
CREATE TABLE search_dict (
    id INTEGER PRIMARY KEY,
    term VARCHAR(200) NOT NULL,
    canonical_term VARCHAR(200),
    language VARCHAR(10),
    category VARCHAR(50),
    procedure_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sd_term ON search_dict(term);
CREATE INDEX idx_sd_canonical ON search_dict(canonical_term);
CREATE INDEX idx_sd_lang ON search_dict(language);

-- ============================================================
-- 10. recommended_clinics (from recommended_hospitals)
-- ============================================================
CREATE TABLE recommended_clinics (
    id INTEGER PRIMARY KEY,
    hospital_id INTEGER REFERENCES beauty_clinics(id),
    region TEXT,
    target_procedures TEXT[],
    is_budget_friendly BOOLEAN DEFAULT false,
    interpreter_languages TEXT[],
    consultation_level SMALLINT DEFAULT 0,
    has_consultation_fee BOOLEAN DEFAULT false,
    is_doctor_selectable BOOLEAN DEFAULT false,
    has_equal_pricing BOOLEAN DEFAULT false,
    avg_wait_minutes INTEGER,
    deposit_amount INTEGER DEFAULT 0,
    tier SMALLINT DEFAULT 3,
    is_chat_target BOOLEAN DEFAULT false,
    anesthesia_options JSONB,
    consultation_fee INTEGER DEFAULT 0,
    doctor_info JSONB,
    specialist_counts JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- ============================================================
-- RLS: admin only (service_role for API, admin for dashboard)
-- ============================================================
ALTER TABLE beauty_clinics ENABLE ROW LEVEL SECURITY;
ALTER TABLE procedure_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE procedures ENABLE ROW LEVEL SECURITY;
ALTER TABLE procedure_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE procedure_intl ENABLE ROW LEVEL SECURITY;
ALTER TABLE beauty_std_procedures ENABLE ROW LEVEL SECURITY;
ALTER TABLE price_comparison ENABLE ROW LEVEL SECURITY;
ALTER TABLE intl_prices ENABLE ROW LEVEL SECURITY;
ALTER TABLE search_dict ENABLE ROW LEVEL SECURITY;
ALTER TABLE recommended_clinics ENABLE ROW LEVEL SECURITY;

-- Public read for procedures/prices (content hub needs this)
CREATE POLICY "public_read_procedures" ON procedures FOR SELECT TO anon USING (true);
CREATE POLICY "public_read_details" ON procedure_details FOR SELECT TO anon USING (true);
CREATE POLICY "public_read_intl" ON procedure_intl FOR SELECT TO anon USING (true);
CREATE POLICY "public_read_categories" ON procedure_categories FOR SELECT TO anon USING (true);
CREATE POLICY "public_read_prices" ON price_comparison FOR SELECT TO anon USING (true);
CREATE POLICY "public_read_intl_prices" ON intl_prices FOR SELECT TO anon USING (true);
CREATE POLICY "public_read_search" ON search_dict FOR SELECT TO anon USING (true);

-- Admin full access on all
CREATE POLICY "admin_beauty_clinics" ON beauty_clinics FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_recommended" ON recommended_clinics FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_procedures" ON procedures FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_proc_details" ON procedure_details FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_proc_intl" ON procedure_intl FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_categories" ON procedure_categories FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_std_proc" ON beauty_std_procedures FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_prices" ON price_comparison FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_intl_prices" ON intl_prices FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
CREATE POLICY "admin_search" ON search_dict FOR ALL TO authenticated
    USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'admin');
