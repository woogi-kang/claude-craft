# SPEC-XOUTREACH-001: X Outreach Agent

## Metadata

| Field | Value |
|-------|-------|
| SPEC ID | SPEC-XOUTREACH-001 |
| Title | X Outreach Agent - Automated Twitter/X Outreach System |
| Created | 2026-02-19 |
| Status | Planned |
| Priority | High |
| Brand | @ask.nandemo |
| Project Location | `tools/x-outreach/` |
| Related Agents | korean-derm-expert |
| Related Strategies | ask-nandemo-dm-outreach-strategy.md, ask-nandemo-reply-strategy.md |

---

## Environment

### System Context

The @ask.nandemo brand provides Korean dermatology information to Japanese audiences on X (Twitter). Currently, all outreach activities (searching for target tweets, replying, sending DMs) are performed manually, consuming 60-80 minutes daily. This system automates the outreach pipeline while preserving the natural, human-like engagement patterns defined in the existing strategy documents.

### External Dependencies

| Dependency | Description | Constraint |
|------------|-------------|------------|
| X API Free Tier | Tweet posting (replies) | 1,500 tweets/month (17 writes + 100 reads per 15 min) |
| Playwright | Browser automation for search and DM | Stealth mode required; session persistence |
| Claude API | Tweet classification and DM generation | anthropic SDK; cost per classification call |
| SQLite | Local state management | Single-file database at `tools/x-outreach/data/outreach.db` |
| APScheduler | Task scheduling | ~2 hour intervals; macOS launchd for daemon |
| Burner X Account | Search and crawl operations | Disposable; suspension accepted as operational cost |
| @ask.nandemo Account | Reply and DM operations | Primary brand account; must be protected |

### Existing Data Sources

| Source | Path | Integration |
|--------|------|-------------|
| Clinic Database | `data/clinic-results/hospitals.db` | Treatment data for reply/DM content enrichment |
| Procedure Details | `data/dermatology/dermatology_procedure_details_complete.json` | Treatment knowledge base |
| DM Templates | `work-social/strategy/ask-nandemo-dm-outreach-strategy.md` | 5 DM templates (A-E) with variation rules |
| Reply Templates | `work-social/strategy/ask-nandemo-reply-strategy.md` | Post-type-specific reply strategies |
| Concern Mapping | `.claude/agents/.../korean-derm-expert/references/concern-mapping.md` | Japanese concern to procedure mapping |

### Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Runtime | Python | 3.13+ |
| Browser Automation | Playwright | latest stable |
| X API Client | tweepy | latest stable |
| AI SDK | anthropic | latest stable |
| Scheduler | APScheduler | 3.x |
| Database | SQLite | built-in |
| Daemon | launchd | macOS built-in |

---

## Assumptions

1. **A-ASM-001**: The burner X account is pre-created and warmed up (14+ days old, profile complete, engagement history established) before the system begins automated search operations.

2. **A-ASM-002**: The @ask.nandemo account has been active for at least 2 weeks with organic engagement before automated DM outreach begins, per the warmup schedule in the DM outreach strategy.

3. **A-ASM-003**: X API Free tier rate limits (1,500 tweets/month, 17 writes/15 min, 100 reads/15 min) remain stable and are sufficient for the reply phase volume.

4. **A-ASM-004**: Playwright stealth mode (with User-Agent rotation, session cookie reuse, and human-like delays) is sufficient to avoid automated detection for search and DM operations at the planned volume.

5. **A-ASM-005**: Claude API classification accuracy for Japanese tweets about Korean dermatology is 85%+ without fine-tuning, using prompt engineering with the existing korean-derm-expert domain knowledge.

6. **A-ASM-006**: The macOS host machine is available 24/7 with stable internet connectivity for the launchd daemon.

7. **A-ASM-007**: Session cookies for Playwright can persist across restarts, reducing login frequency to once per session expiration (typically 30-90 days).

---

## Requirements

### R1: Search Phase (Playwright + Burner Account)

**R1.1** - WHEN the scheduler triggers a search cycle, THEN the system shall log into X using the burner account's persisted session cookies via Playwright in stealth mode.

**R1.2** - IF the persisted session is expired or invalid, THEN the system shall perform a fresh login with the burner account credentials and persist the new session cookies.

**R1.3** - WHEN a search cycle begins, THEN the system shall execute keyword searches for the following Japanese terms: 韓国皮膚科, 韓国美容, 韓国美容皮膚科, レーザー治療, ピコレーザー, 韓国クリニック, 韓国整形, 美容皮膚科 韓国, 韓国 シミ取り, 韓国 ニキビ跡, 韓国 毛穴, フラクショナルレーザー, 韓国 ボトックス, 韓国 ヒアルロン酸, 韓国 美肌.

**R1.4** - WHEN search results are returned, THEN the system shall filter tweets to only those posted within the last 24 hours that have not been previously processed (checked against SQLite).

**R1.5** - The system shall apply random delays between 30 seconds and 5 minutes between consecutive search queries to simulate human browsing behavior.

**R1.6** - The system shall rotate User-Agent strings from a pool of at least 10 common browser User-Agents per search session.

### R2: Collect Phase (Data Extraction)

**R2.1** - WHEN a tweet passes the recency and deduplication filter, THEN the system shall extract: tweet ID, tweet content (full text), author username, author display name, author follower count, author following count, author bio, tweet timestamp, engagement metrics (likes, retweets, replies), and tweet URL.

**R2.2** - WHEN tweet data is extracted, THEN the system shall store all fields in the SQLite `tweets` table with status `collected`.

**R2.3** - The system shall not collect tweets from accounts with 10,000+ followers (influencer exclusion per DM strategy).

**R2.4** - The system shall not collect tweets from accounts without a profile picture or bio (bot/throwaway exclusion).

**R2.5** - The system shall not collect tweets from accounts that appear to be clinic marketing accounts (heuristic: bio contains clinic URL, all posts promote a single clinic).

### R3: Analyze Phase (Claude API Classification)

**R3.1** - WHEN a collected tweet is ready for analysis, THEN the system shall send the tweet content and author context to the Claude API for classification into one of three categories: `needs_help` (user is seeking assistance with Korean dermatology), `seeking_info` (user is looking for information about Korean dermatology), or `irrelevant` (not a valid outreach target).

**R3.2** - WHEN the Claude API returns a classification, THEN the system shall also receive a confidence score (0.0-1.0) and a brief rationale explaining the classification.

**R3.3** - IF the confidence score is below 0.7, THEN the system shall classify the tweet as `irrelevant` to avoid false-positive outreach.

**R3.4** - WHEN a tweet is classified as `needs_help` or `seeking_info`, THEN the system shall also determine the appropriate reply template category based on the reply strategy (A: experience report, B: question/concern, C: price sharing, D: trouble report, E: planning/preparation, F: before/after, G: education/info).

**R3.5** - The system shall include korean-derm-expert domain knowledge (treatment names, price ranges, concern mapping) in the Claude API prompt context to improve classification accuracy.

**R3.6** - WHEN analysis is complete, THEN the system shall update the tweet record in SQLite with classification, confidence, rationale, and template category, setting status to `analyzed`.

### R4: Reply Phase (X API Free Tier + @ask.nandemo)

**R4.1** - WHEN a tweet is classified as `needs_help` or `seeking_info` with confidence >= 0.7, THEN the system shall generate a reply using the @ask.nandemo account via the X API Free tier (tweepy).

**R4.2** - WHEN generating a reply, THEN the system shall select a reply template from the reply strategy based on the classified template category and customize it with tweet-specific context using the Claude API.

**R4.3** - The system shall enforce the X API Free tier rate limits: maximum 17 write operations per 15-minute window, maximum 1,500 tweets per month.

**R4.4** - IF the monthly tweet count approaches 80% of the 1,500 limit (1,200 tweets), THEN the system shall switch to a conservation mode that only replies to `needs_help` tweets (skipping `seeking_info`).

**R4.5** - The system shall not reply to more than 3 tweets in the same conversation thread (anti-spam per reply strategy).

**R4.6** - The system shall not reply between 23:00-08:00 JST (anti-bot detection per strategy).

**R4.7** - WHEN a reply is posted, THEN the system shall update the tweet record in SQLite with reply content, reply tweet ID, and timestamp, setting status to `replied`.

**R4.8** - The system shall ensure reply content is in natural casual Japanese (plain form base with occasional desu/masu softening) matching the @ask.nandemo voice guide.

### R5: DM Phase (Playwright + @ask.nandemo)

**R5.1** - WHEN a tweet has been replied to, THEN the system shall schedule a DM to the tweet author after a random delay of 10-30 minutes.

**R5.2** - WHEN the DM delay has elapsed, THEN the system shall use Playwright to log into the @ask.nandemo account (using persisted session cookies) and send a personalized DM to the tweet author.

**R5.3** - WHEN generating DM content, THEN the system shall use the Claude API to create a personalized message based on: the original tweet content, the template rotation schedule (templates A-E), and the user's apparent concern/interest.

**R5.4** - The system shall enforce a daily DM limit of 20-30 DMs per day (configurable, default 20).

**R5.5** - The system shall enforce a minimum interval of 20-30 minutes between consecutive DMs (configurable, default 25 minutes).

**R5.6** - The system shall rotate DM templates (A-E) such that the same template is never used consecutively.

**R5.7** - The system shall ensure each DM has at least 30 characters of unique content compared to the previous DM sent (anti-pattern detection per DM strategy).

**R5.8** - The system shall not include links in initial DMs (per DM strategy anti-spam rule).

**R5.9** - The system shall not send DMs between 23:00-08:00 JST.

**R5.10** - IF the target user's DMs are closed (not accepting DMs from non-followers), THEN the system shall skip the DM phase and log the reason.

**R5.11** - WHEN a DM is sent, THEN the system shall update the tweet record in SQLite with DM content, DM timestamp, and template used, setting status to `dm_sent`.

**R5.12** - IF a DM send fails due to rate limiting or account restriction, THEN the system shall immediately halt all DM operations for 24 hours and log the incident as a critical alert.

### R6: Track Phase (SQLite State Management)

**R6.1** - The system shall maintain a SQLite database with the following tables: `tweets` (processed tweets and their status), `users` (target user profiles and interaction history), `actions` (all outreach actions with timestamps), `config` (runtime configuration and rate limit state), `daily_stats` (aggregated daily metrics).

**R6.2** - The system shall prevent duplicate outreach by checking the `users` table before any reply or DM action. A user who has been contacted once shall not be contacted again for the same tweet.

**R6.3** - The system shall record all actions (search, collect, analyze, reply, DM) with timestamps, enabling full audit trail reconstruction.

**R6.4** - WHEN a new day begins (00:00 JST), THEN the system shall reset daily counters (DM count, reply count) and aggregate the previous day's stats into `daily_stats`.

**R6.5** - The system shall track monthly tweet count against the 1,500 API limit and expose the remaining budget via a status endpoint or log output.

### R7: Anti-Detection Measures

**R7.1** - The system shall reuse session cookies across Playwright sessions for both the burner account and @ask.nandemo account to minimize login frequency.

**R7.2** - The system shall apply random delays between all automated actions: 30s-5min between searches, 20-30min between DMs, 1-5min between replies.

**R7.3** - The system shall rotate User-Agent strings from a predefined pool of at least 10 entries per browsing session.

**R7.4** - WHILE the system is in its first 14 days of operation (warmup period), THEN the system shall operate at 50% of normal volume limits for all actions.

**R7.5** - The system shall simulate human-like behavior in Playwright: randomized mouse movements, scroll patterns, and typing delays when composing DMs.

**R7.6** - IF the burner account is suspended, THEN the system shall halt all search operations, log the event, and notify the operator. Search operations shall resume only after a new burner account is configured.

**R7.7** - IF the @ask.nandemo account receives a DM restriction warning, THEN the system shall immediately halt all DM operations, reduce DM volume to 50% of current level upon resumption after 24 hours, and log the incident.

### R8: Scheduling and Runtime

**R8.1** - The system shall use APScheduler to execute the full pipeline (search -> collect -> analyze -> reply -> DM) approximately every 2 hours during active hours (08:00-23:00 JST).

**R8.2** - The system shall be configured as a macOS launchd daemon for 24/7 operation with automatic restart on failure.

**R8.3** - WHEN the system starts, THEN it shall verify all dependencies (Playwright browsers installed, API keys configured, SQLite database accessible) before beginning operations.

**R8.4** - The system shall log all operations with structured logging (JSON format) to both console and rotating log files at `tools/x-outreach/logs/`.

**R8.5** - The system shall expose runtime status (last run time, tweets processed, daily counts, API budget remaining) via a simple CLI status command.

### R9: Configuration Management

**R9.1** - The system shall store all configurable parameters in a YAML configuration file at `tools/x-outreach/config.yaml` including: API keys (reference to env vars), keyword lists, volume limits, delay ranges, template paths, and schedule intervals.

**R9.2** - The system shall not store API keys, passwords, or session tokens directly in configuration files. All secrets shall be loaded from environment variables or a `.env` file excluded from version control.

**R9.3** - The system shall support runtime configuration updates without restart for: keyword lists, volume limits, and delay ranges.

### R10: Integration with korean-derm-expert

**R10.1** - WHEN generating replies or DMs, THEN the system shall have access to the korean-derm-expert knowledge base (treatment translations, price comparisons, concern mappings) for content enrichment.

**R10.2** - WHEN classifying tweets, THEN the Claude API prompt shall include treatment terminology mapping (Japanese to Korean) from the korean-derm-expert references to improve classification accuracy.

**R10.3** - WHERE the system identifies a tweet about a specific treatment, THEN it shall include relevant price comparison data (Korea vs Japan) in the generated reply content.

---

## Specifications

### Architecture Overview

```
                    +------------------+
                    |   APScheduler    |
                    |  (every ~2hrs)   |
                    +--------+---------+
                             |
                    +--------v---------+
                    |  Pipeline Runner |
                    +--------+---------+
                             |
          +------------------+------------------+
          |                  |                  |
+---------v------+  +--------v-------+  +-------v--------+
| Search Phase   |  | Analyze Phase  |  | Reply Phase    |
| (Playwright)   |  | (Claude API)   |  | (X API/tweepy) |
| Burner Account |  |                |  | @ask.nandemo   |
+-------+--------+  +--------+-------+  +-------+--------+
        |                     |                  |
        |            +--------v-------+          |
        |            | DM Phase       |          |
        |            | (Playwright)   |          |
        |            | @ask.nandemo   |          |
        |            +--------+-------+          |
        |                     |                  |
        +----------+----------+------------------+
                   |
          +--------v---------+
          |   SQLite DB      |
          | (State Tracking) |
          +------------------+
```

### Project Directory Structure

```
tools/x-outreach/
+-- pyproject.toml
+-- config.yaml
+-- .env.example
+-- README.md
+-- src/
|   +-- __init__.py
|   +-- main.py                 # Entry point, pipeline orchestration
|   +-- config.py               # Configuration loader
|   +-- scheduler.py            # APScheduler setup
|   +-- pipeline/
|   |   +-- __init__.py
|   |   +-- search.py           # Playwright search with burner account
|   |   +-- collect.py          # Tweet data extraction
|   |   +-- analyze.py          # Claude API classification
|   |   +-- reply.py            # X API reply via tweepy
|   |   +-- dm.py               # Playwright DM automation
|   |   +-- track.py            # SQLite state management
|   +-- browser/
|   |   +-- __init__.py
|   |   +-- stealth.py          # Playwright stealth configuration
|   |   +-- session.py          # Cookie/session persistence
|   |   +-- human_sim.py        # Human behavior simulation
|   +-- ai/
|   |   +-- __init__.py
|   |   +-- classifier.py       # Tweet classification
|   |   +-- content_gen.py      # Reply/DM content generation
|   |   +-- prompts.py          # Prompt templates
|   +-- db/
|   |   +-- __init__.py
|   |   +-- models.py           # SQLite schema/models
|   |   +-- repository.py       # Database operations
|   +-- knowledge/
|   |   +-- __init__.py
|   |   +-- treatments.py       # Treatment data loader
|   |   +-- templates.py        # Reply/DM template manager
|   +-- utils/
|       +-- __init__.py
|       +-- rate_limiter.py     # Rate limit tracking
|       +-- logger.py           # Structured logging
|       +-- time_utils.py       # JST time utilities
+-- data/
|   +-- outreach.db             # SQLite database
|   +-- sessions/               # Playwright session storage
|   +-- user_agents.json        # User-Agent pool
+-- logs/                       # Rotating log files
+-- scripts/
|   +-- setup.sh                # Initial setup script
|   +-- status.py               # CLI status checker
+-- launchd/
|   +-- com.asknandemo.xoutreach.plist  # launchd daemon config
+-- tests/
    +-- __init__.py
    +-- test_search.py
    +-- test_analyze.py
    +-- test_reply.py
    +-- test_dm.py
    +-- test_track.py
    +-- conftest.py
```

### SQLite Schema

```sql
CREATE TABLE tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id TEXT UNIQUE NOT NULL,
    content TEXT NOT NULL,
    author_username TEXT NOT NULL,
    author_display_name TEXT,
    author_follower_count INTEGER,
    author_following_count INTEGER,
    author_bio TEXT,
    tweet_timestamp DATETIME NOT NULL,
    likes INTEGER DEFAULT 0,
    retweets INTEGER DEFAULT 0,
    replies INTEGER DEFAULT 0,
    tweet_url TEXT,
    search_keyword TEXT,
    status TEXT NOT NULL DEFAULT 'collected',  -- collected, analyzed, replied, dm_sent, skipped
    classification TEXT,                        -- needs_help, seeking_info, irrelevant
    confidence REAL,
    classification_rationale TEXT,
    template_category TEXT,                     -- A, B, C, D, E, F, G
    reply_content TEXT,
    reply_tweet_id TEXT,
    reply_timestamp DATETIME,
    dm_content TEXT,
    dm_template_used TEXT,                      -- A, B, C, D, E
    dm_timestamp DATETIME,
    dm_skip_reason TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    display_name TEXT,
    follower_count INTEGER,
    following_count INTEGER,
    bio TEXT,
    is_blocked INTEGER DEFAULT 0,              -- manual block list
    first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_contacted DATETIME,
    contact_count INTEGER DEFAULT 0,
    dm_open INTEGER DEFAULT 1,                 -- whether DMs are open
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,                 -- search, collect, analyze, reply, dm, error
    tweet_id TEXT,
    username TEXT,
    details TEXT,                              -- JSON blob with action-specific data
    status TEXT NOT NULL,                      -- success, failed, skipped
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE daily_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE NOT NULL,                 -- YYYY-MM-DD
    tweets_searched INTEGER DEFAULT 0,
    tweets_collected INTEGER DEFAULT 0,
    tweets_analyzed INTEGER DEFAULT 0,
    tweets_needs_help INTEGER DEFAULT 0,
    tweets_seeking_info INTEGER DEFAULT 0,
    tweets_irrelevant INTEGER DEFAULT 0,
    replies_sent INTEGER DEFAULT 0,
    dms_sent INTEGER DEFAULT 0,
    dms_skipped INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    api_tweets_used INTEGER DEFAULT 0,         -- monthly running total
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tweets_status ON tweets(status);
CREATE INDEX idx_tweets_tweet_id ON tweets(tweet_id);
CREATE INDEX idx_tweets_author ON tweets(author_username);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_actions_type ON actions(action_type);
CREATE INDEX idx_actions_created ON actions(created_at);
CREATE INDEX idx_daily_stats_date ON daily_stats(date);
```

### Rate Limiting Strategy

| Operation | Limit | Window | Strategy |
|-----------|-------|--------|----------|
| Search queries | 15 keywords | per cycle | Sequential with 30s-5min random delays |
| X API writes (replies) | 17 | 15 minutes | Token bucket with backoff |
| X API writes (monthly) | 1,500 | 30 days | Daily budget allocation (~50/day) |
| DMs sent | 20-30 | per day | Counter with 20-30min intervals |
| DM send attempts | 4-5 | per hour | Sliding window |
| Active hours | 08:00-23:00 JST | daily | Scheduler constraint |

### Credential Management

| Credential | Storage | Access |
|------------|---------|--------|
| Burner X username/password | `.env` file | Environment variable |
| @ask.nandemo X API keys | `.env` file | Environment variable |
| @ask.nandemo X session cookies | `data/sessions/` | Playwright persistent context |
| Burner X session cookies | `data/sessions/` | Playwright persistent context |
| Claude API key | `.env` file | Environment variable |

### Traceability

| Tag | Requirement | Component |
|-----|-------------|-----------|
| SPEC-XOUTREACH-001-R1 | Search Phase | `pipeline/search.py`, `browser/stealth.py` |
| SPEC-XOUTREACH-001-R2 | Collect Phase | `pipeline/collect.py` |
| SPEC-XOUTREACH-001-R3 | Analyze Phase | `pipeline/analyze.py`, `ai/classifier.py` |
| SPEC-XOUTREACH-001-R4 | Reply Phase | `pipeline/reply.py`, `ai/content_gen.py` |
| SPEC-XOUTREACH-001-R5 | DM Phase | `pipeline/dm.py`, `browser/human_sim.py` |
| SPEC-XOUTREACH-001-R6 | Track Phase | `pipeline/track.py`, `db/repository.py` |
| SPEC-XOUTREACH-001-R7 | Anti-Detection | `browser/stealth.py`, `utils/rate_limiter.py` |
| SPEC-XOUTREACH-001-R8 | Scheduling | `scheduler.py`, `launchd/` |
| SPEC-XOUTREACH-001-R9 | Configuration | `config.py`, `config.yaml` |
| SPEC-XOUTREACH-001-R10 | Knowledge Integration | `knowledge/`, `ai/prompts.py` |
