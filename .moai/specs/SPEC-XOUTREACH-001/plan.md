# SPEC-XOUTREACH-001: Implementation Plan

## Traceability

| Tag | Reference |
|-----|-----------|
| SPEC ID | SPEC-XOUTREACH-001 |
| Spec Document | `.moai/specs/SPEC-XOUTREACH-001/spec.md` |
| Acceptance Criteria | `.moai/specs/SPEC-XOUTREACH-001/acceptance.md` |

---

## Technical Approach

### Architecture Pattern

The system follows a **Pipeline Architecture** with six sequential stages: Search -> Collect -> Analyze -> Reply -> DM -> Track. Each stage is an independent module that reads from and writes to the shared SQLite database, enabling:

- **Stage isolation**: Each stage can be tested, debugged, and restarted independently
- **State persistence**: SQLite ensures no work is lost on crash/restart
- **Rate limit compliance**: Each stage manages its own rate limits independently
- **Audit trail**: Every action is recorded for debugging and compliance

### Dual-Account Strategy

The system uses two distinct accounts with clear separation of concerns:

1. **Burner Account** (Playwright only): Used exclusively for search and crawl. Disposable. No brand risk.
2. **@ask.nandemo Account** (X API + Playwright): Used for replies (via API) and DMs (via Playwright). Brand account. Must be protected.

This separation ensures that aggressive search behavior on the burner account cannot trigger restrictions on the brand account.

### AI Integration Strategy

Claude API is used in two capacities:

1. **Classification** (structured output): Each tweet is classified with category, confidence, and rationale. Uses system prompt with korean-derm-expert domain knowledge for accurate Japanese tweet understanding.
2. **Content Generation** (creative output): Reply and DM content is generated based on tweet context, template guidelines, and @ask.nandemo voice guide. Uses template rotation constraints and uniqueness requirements.

### Anti-Detection Architecture

Anti-detection is built as a cross-cutting concern, not bolted on:

- **`browser/stealth.py`**: Playwright stealth configuration (webdriver flag removal, navigator override, WebGL fingerprint randomization)
- **`browser/session.py`**: Cookie persistence, session health checks, re-login on expiry
- **`browser/human_sim.py`**: Randomized delays, mouse movements, scroll patterns, typing simulation
- **`utils/rate_limiter.py`**: Token bucket and sliding window implementations for all rate limits

---

## Milestones

### Primary Goal: Core Pipeline (Search -> Collect -> Analyze)

**Scope**: Build the foundation that finds and classifies target tweets.

**Deliverables**:
- Project scaffolding (`tools/x-outreach/` directory structure, pyproject.toml, config.yaml)
- SQLite database schema and repository layer
- Playwright stealth browser setup with session persistence
- Search module: keyword search on X with burner account
- Collect module: tweet data extraction and deduplication
- Analyze module: Claude API classification with korean-derm-expert context
- Structured logging infrastructure
- Unit tests for all core modules

**Dependencies**: None (foundational)

**Risks**:
- Playwright stealth may need tuning if X detects automation
- Claude API classification prompt may need iteration for accuracy

**Verification**: Run search cycle, verify tweets are collected, classified, and stored in SQLite with correct schema.

### Secondary Goal: Reply and DM Automation

**Scope**: Build the outreach modules that engage with classified tweets.

**Deliverables**:
- Reply module: X API Free tier integration via tweepy with rate limiting
- DM module: Playwright-based DM sending with human simulation
- Content generation: Claude API reply/DM content with template rotation
- Rate limiter: Token bucket for API limits, sliding window for DM limits
- Template manager: Load and rotate templates from strategy documents
- Anti-detection: Human behavior simulation, delay randomization
- Integration tests for full pipeline flow

**Dependencies**: Primary Goal complete

**Risks**:
- X API Free tier rate limits may be more restrictive than documented
- DM automation detection is the highest-risk component
- @ask.nandemo account restriction would impact brand

**Verification**: Full pipeline execution: search -> collect -> analyze -> reply -> DM -> track, with all rate limits enforced.

### Final Goal: Scheduling, Monitoring, and Daemon

**Scope**: Make the system run autonomously as a macOS daemon.

**Deliverables**:
- APScheduler integration with 2-hour cycle during active hours (08:00-23:00 JST)
- launchd plist configuration for macOS daemon
- CLI status command (current stats, API budget, last run)
- Daily stats aggregation and reporting
- Monthly API budget tracking with conservation mode
- Emergency halt protocols (account restriction detection)
- Setup script for first-time installation
- End-to-end integration tests

**Dependencies**: Secondary Goal complete

**Risks**:
- launchd daemon may not handle Playwright browser instances cleanly
- Long-running Playwright sessions may leak memory

**Verification**: System runs unattended for 24 hours, respecting all rate limits, with correct daily stats.

### Optional Goal: Warmup Mode and Advanced Features

**Scope**: Implement the 14-day warmup period and operational refinements.

**Deliverables**:
- Warmup mode: 50% volume limits for first 14 days of operation
- Conservation mode: Automatic when API budget reaches 80%
- User blocklist management (CLI command to add/remove)
- DM response tracking (detect if user replied to DM)
- Weekly report generation (CSV export of stats)
- Configuration hot-reload (update config.yaml without restart)

**Dependencies**: Final Goal complete

**Risks**: Low risk - these are refinements on a working system.

**Verification**: Warmup mode correctly limits volume; conservation mode activates at threshold.

---

## Risks and Mitigation

### Risk 1: Burner Account Suspension

**Likelihood**: High (expected within 1-3 months)
**Impact**: Search operations halt
**Mitigation**:
- Accept as operational cost (per user's risk acceptance)
- Document burner account setup process for quick replacement
- Store search keywords and config separately from account credentials
- Implement account-agnostic search module (swap credentials in `.env`)

### Risk 2: @ask.nandemo DM Restriction

**Likelihood**: Medium
**Impact**: DM outreach halted, potential temporary account restriction
**Mitigation**:
- Conservative default DM limits (20/day vs strategy max of 30)
- 24-hour automatic halt on any restriction signal
- 50% volume reduction on resumption
- Human-like behavior simulation reduces detection risk
- Consider X Premium subscription for higher limits and lower spam sensitivity

### Risk 3: Claude API Classification Accuracy

**Likelihood**: Medium (initial accuracy may be lower)
**Impact**: False positives waste API budget; false negatives miss opportunities
**Mitigation**:
- 0.7 confidence threshold filters low-confidence classifications
- Include rich domain context from korean-derm-expert in prompts
- Log all classifications for human review and prompt iteration
- Start with manual review of first 100 classifications to calibrate

### Risk 4: X API Free Tier Changes

**Likelihood**: Low-Medium (X has changed API tiers multiple times)
**Impact**: Reply volume may be reduced or API access revoked
**Mitigation**:
- Monthly budget tracking with conservation mode
- DM operations are Playwright-based (independent of API)
- Search operations are Playwright-based (independent of API)
- Only reply phase depends on X API; could theoretically fall back to Playwright

### Risk 5: Playwright Detection by X

**Likelihood**: Medium
**Impact**: Browser sessions blocked, automation detected
**Mitigation**:
- Stealth mode with webdriver flag removal
- Session cookie persistence (reduce login frequency)
- Human behavior simulation (delays, scrolls, mouse movements)
- User-Agent rotation
- Gradual volume increase during warmup period

### Risk 6: Data Privacy and Legal

**Likelihood**: Low
**Impact**: Legal exposure from collecting user data
**Mitigation**:
- Only collect publicly available tweet data
- Do not store private information beyond what is publicly visible
- Implement data retention policy (delete records older than 90 days)
- No PII in logs

---

## Technology Decisions

### Why Playwright over Selenium

- Better stealth capabilities (Playwright context isolation)
- Built-in session persistence via persistent browser contexts
- Superior async support (native Python async)
- More reliable element selection and waiting

### Why tweepy for X API

- Most mature Python X API client
- Good support for API v2 endpoints
- Built-in rate limit handling
- Active maintenance

### Why APScheduler over cron

- In-process scheduling (no external dependencies)
- Supports missed job handling (important for daemon restarts)
- Easy dynamic schedule modification
- Built-in job persistence

### Why SQLite over PostgreSQL

- Zero infrastructure (single file database)
- Sufficient for expected data volume (<100K rows/year)
- Built into Python standard library
- Simple backup (copy single file)
- Local-only operation aligns with macOS daemon architecture

---

## Expert Consultation Recommendations

### Backend Architecture Review

This SPEC contains significant backend architecture decisions (pipeline pattern, database schema, rate limiting, credential management). Consultation with **expert-backend** is recommended for:
- Pipeline error handling and retry strategy
- SQLite schema optimization for query patterns
- Rate limiter implementation (token bucket vs leaky bucket)
- Async architecture decisions (asyncio patterns for Playwright + API)

### Security Review

This SPEC involves credential management, browser automation, and outreach that could be considered spam. Consultation with **expert-security** is recommended for:
- Credential storage best practices (.env handling)
- Session cookie security (encryption at rest)
- Compliance with X Terms of Service
- Data retention and privacy considerations
