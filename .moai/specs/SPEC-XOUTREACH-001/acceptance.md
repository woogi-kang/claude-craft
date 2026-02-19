# SPEC-XOUTREACH-001: Acceptance Criteria

## Traceability

| Tag | Reference |
|-----|-----------|
| SPEC ID | SPEC-XOUTREACH-001 |
| Spec Document | `.moai/specs/SPEC-XOUTREACH-001/spec.md` |
| Plan Document | `.moai/specs/SPEC-XOUTREACH-001/plan.md` |

---

## Test Scenarios

### TS-01: Search Phase (R1)

#### TS-01.1: Successful Keyword Search

```gherkin
Given the burner account has valid persisted session cookies
And the scheduler triggers a search cycle
When the system executes keyword searches for all 15 Japanese keywords
Then the system shall return tweets from the last 24 hours
And each tweet shall not exist in the SQLite tweets table
And random delays of 30s-5min shall be applied between queries
And the User-Agent shall be rotated from a pool of 10+ agents
```

#### TS-01.2: Session Expiry Handling

```gherkin
Given the burner account's persisted session cookies are expired
When the system attempts to load the session
Then the system shall detect the invalid session
And perform a fresh login with burner credentials
And persist the new session cookies for future use
And continue with the search cycle
```

#### TS-01.3: Search with No New Results

```gherkin
Given all tweets matching the keywords have already been processed
When the system executes keyword searches
Then the system shall find zero new tweets
And the pipeline shall proceed to the next cycle without errors
And the search action shall be logged as success with 0 results
```

---

### TS-02: Collect Phase (R2)

#### TS-02.1: Tweet Data Extraction

```gherkin
Given a tweet passes the recency (24h) and deduplication filter
When the system collects the tweet data
Then the following fields shall be extracted:
  | Field | Type |
  | tweet_id | text |
  | content | full text |
  | author_username | text |
  | author_display_name | text |
  | author_follower_count | integer |
  | author_following_count | integer |
  | author_bio | text |
  | tweet_timestamp | datetime |
  | likes | integer |
  | retweets | integer |
  | replies | integer |
  | tweet_url | text |
And the tweet shall be stored in SQLite with status "collected"
```

#### TS-02.2: Influencer Exclusion

```gherkin
Given a tweet is authored by a user with 10,000+ followers
When the collection filter evaluates the tweet
Then the tweet shall be excluded from collection
And the exclusion reason "influencer_follower_count" shall be logged
```

#### TS-02.3: Bot/Throwaway Exclusion

```gherkin
Given a tweet is authored by a user without a profile picture
Or a tweet is authored by a user without a bio
When the collection filter evaluates the tweet
Then the tweet shall be excluded from collection
And the exclusion reason "missing_profile" shall be logged
```

#### TS-02.4: Clinic Marketing Account Exclusion

```gherkin
Given a tweet is authored by a user whose bio contains a clinic URL
And all of the user's recent posts promote a single clinic
When the collection filter evaluates the tweet
Then the tweet shall be excluded from collection
And the exclusion reason "clinic_marketing_account" shall be logged
```

---

### TS-03: Analyze Phase (R3)

#### TS-03.1: Successful Classification

```gherkin
Given a collected tweet with content about seeking Korean dermatology advice
When the system sends the tweet to the Claude API for classification
Then the API shall return one of: "needs_help", "seeking_info", or "irrelevant"
And a confidence score between 0.0 and 1.0
And a brief rationale explaining the classification
And the tweet record shall be updated with classification data
And the tweet status shall be set to "analyzed"
```

#### TS-03.2: Low Confidence Threshold

```gherkin
Given the Claude API returns a classification with confidence below 0.7
When the system processes the classification result
Then the tweet shall be classified as "irrelevant" regardless of the returned category
And the original classification and confidence shall be preserved in the rationale
And the tweet shall not proceed to the reply phase
```

#### TS-03.3: Template Category Assignment

```gherkin
Given a tweet is classified as "needs_help" with confidence >= 0.7
And the tweet content is about a first-time Korean clinic visit
When the system determines the template category
Then the template category shall be set to "E" (planning/preparation)
And this category shall be stored in the tweet record
```

#### TS-03.4: Domain Knowledge Integration

```gherkin
Given a tweet mentions "ポテンツァ" (Potenza treatment)
When the system sends the tweet to the Claude API for classification
Then the prompt shall include treatment terminology from korean-derm-expert references
And the system shall correctly identify this as a dermatology treatment inquiry
And classify accordingly (not "irrelevant")
```

---

### TS-04: Reply Phase (R4)

#### TS-04.1: Successful Reply Posting

```gherkin
Given a tweet classified as "needs_help" with confidence >= 0.7
And the monthly tweet count is below 1,200 (80% of 1,500 limit)
And the current time is between 08:00-23:00 JST
When the system generates and posts a reply via X API
Then the reply shall be posted from the @ask.nandemo account
And the reply content shall be in casual Japanese matching the voice guide
And the reply shall reference context from the original tweet
And the tweet record shall be updated with reply content and tweet ID
And the tweet status shall be set to "replied"
```

#### TS-04.2: API Rate Limit Enforcement

```gherkin
Given 17 reply tweets have been posted in the last 15 minutes
When the system attempts to post another reply
Then the system shall wait until the 15-minute window resets
And log the rate limit pause
And resume posting after the window resets
```

#### TS-04.3: Monthly Budget Conservation Mode

```gherkin
Given 1,200 tweets have been posted this month (80% of 1,500 limit)
When a tweet classified as "seeking_info" enters the reply phase
Then the system shall skip the reply for "seeking_info" tweets
And only reply to "needs_help" tweets
And log the conservation mode activation
```

#### TS-04.4: Thread Limit Enforcement

```gherkin
Given 3 replies have already been posted in the same conversation thread
When a new tweet in that thread is classified for reply
Then the system shall skip the reply
And log the skip reason as "thread_limit_exceeded"
```

#### TS-04.5: Night Mode Restriction

```gherkin
Given the current time is 23:30 JST
When a tweet enters the reply phase
Then the system shall queue the reply for the next active window (08:00 JST)
And not post the reply until 08:00 JST
```

---

### TS-05: DM Phase (R5)

#### TS-05.1: Successful DM Sending

```gherkin
Given a tweet has been replied to
And 10-30 minutes have elapsed since the reply
And the daily DM count is below the configured limit (default 20)
And the target user's DMs are open
When the system sends a personalized DM via Playwright
Then the DM shall be sent from the @ask.nandemo account
And the DM content shall be personalized based on the original tweet
And the DM template shall differ from the previous DM sent
And the DM content shall have at least 30 unique characters vs the previous DM
And the DM shall not contain any links
And the tweet record shall be updated with DM content and timestamp
And the tweet status shall be set to "dm_sent"
```

#### TS-05.2: Template Rotation

```gherkin
Given the previous DM used template "A"
When the system selects a template for the next DM
Then the system shall select from templates B, C, D, or E
And not select template "A"
```

#### TS-05.3: Daily DM Limit

```gherkin
Given 20 DMs have been sent today (default daily limit)
When a new DM is scheduled
Then the system shall skip the DM
And log the skip reason as "daily_dm_limit_reached"
And the tweet status shall remain "replied"
```

#### TS-05.4: DM Interval Enforcement

```gherkin
Given the last DM was sent 10 minutes ago
And the configured minimum interval is 25 minutes
When a new DM is scheduled
Then the system shall wait until 25 minutes have elapsed since the last DM
And then send the DM
```

#### TS-05.5: Closed DM Handling

```gherkin
Given a target user's DMs are not open (non-followers cannot DM)
When the system attempts to send a DM
Then the system shall skip the DM
And log the skip reason as "dm_closed"
And update the user record with dm_open = 0
```

#### TS-05.6: DM Restriction Emergency Halt

```gherkin
Given the system detects a DM rate limit or restriction warning from X
When the warning is detected
Then the system shall immediately halt ALL DM operations
And log the incident as a critical alert
And not resume DM operations for 24 hours
And reduce DM volume to 50% of previous level upon resumption
```

#### TS-05.7: Night Mode DM Restriction

```gherkin
Given the current time is 01:00 JST
When a DM is scheduled for sending
Then the system shall queue the DM for the next active window (08:00 JST)
```

---

### TS-06: Track Phase (R6)

#### TS-06.1: Duplicate Prevention

```gherkin
Given a user "tanaka_beauty" has been contacted once for tweet "12345"
When a new tweet "67890" from "tanaka_beauty" is classified for outreach
Then the system shall check the users table for prior contact
And proceed with outreach (different tweet, same user is allowed)
But shall not contact the same user for the same tweet twice
```

#### TS-06.2: Daily Stats Aggregation

```gherkin
Given it is 00:00 JST on a new day
When the daily reset triggers
Then the system shall aggregate the previous day's stats into daily_stats
And reset all daily counters (DM count, reply count)
And the daily_stats record shall contain accurate counts for all metrics
```

#### TS-06.3: Action Audit Trail

```gherkin
Given the system performs a search action
When the action completes
Then an action record shall be created with:
  | Field | Value |
  | action_type | search |
  | status | success or failed |
  | details | JSON with search keywords and result count |
  | created_at | current timestamp |
```

#### TS-06.4: Monthly Budget Tracking

```gherkin
Given the system has used 1,450 tweets this month
When a status check is performed
Then the system shall report 50 remaining tweets for the month
And the conservation mode shall be active (since 1,450 > 1,200)
```

---

### TS-07: Anti-Detection (R7)

#### TS-07.1: Session Cookie Reuse

```gherkin
Given the system was shut down and restarted
When the system initializes Playwright for the burner account
Then the system shall load persisted session cookies from data/sessions/
And not perform a fresh login
And the search shall proceed with the existing session
```

#### TS-07.2: Warmup Period Volume Limits

```gherkin
Given the system has been operating for 7 days (within 14-day warmup)
When the system calculates volume limits for the current cycle
Then all limits shall be at 50% of normal:
  | Limit | Normal | Warmup |
  | Daily DMs | 20 | 10 |
  | Replies per cycle | normal | 50% |
  | Search keywords per cycle | 15 | 7-8 |
```

#### TS-07.3: Burner Account Suspension Handling

```gherkin
Given the burner account has been suspended by X
When the system attempts to load the burner account session
Then the system shall detect the suspension
And halt all search operations
And log the event as a critical alert with notification
And continue other operations (reply/DM) using existing analyzed tweets
And search shall not resume until a new burner account is configured
```

#### TS-07.4: Human-Like Behavior Simulation

```gherkin
Given the system is composing a DM via Playwright
When the DM content is being typed into the input field
Then the system shall simulate typing with randomized keystroke delays (50-200ms per character)
And include occasional pauses (500-2000ms) mid-sentence
And perform random scroll actions before and after typing
```

---

### TS-08: Scheduling and Runtime (R8)

#### TS-08.1: Pipeline Scheduling

```gherkin
Given the system is running as a launchd daemon
And the current time is within active hours (08:00-23:00 JST)
When approximately 2 hours have elapsed since the last pipeline run
Then the APScheduler shall trigger a new pipeline cycle
And execute: search -> collect -> analyze -> reply -> DM -> track
```

#### TS-08.2: Startup Dependency Verification

```gherkin
Given the system is starting up
When the initialization phase runs
Then the system shall verify:
  | Dependency | Check |
  | Playwright browsers | installed and executable |
  | X API keys | configured in environment |
  | Claude API key | configured in environment |
  | SQLite database | accessible and schema valid |
  | Burner account credentials | configured |
  | @ask.nandemo credentials | configured |
And if any dependency fails, the system shall log the error and exit with non-zero status
```

#### TS-08.3: Structured Logging

```gherkin
Given the system performs any operation
When the operation is logged
Then the log entry shall be in JSON format
And include: timestamp, level, module, action, details
And logs shall be written to both console and rotating files at tools/x-outreach/logs/
```

#### TS-08.4: CLI Status Command

```gherkin
Given the system has been running for 1 day
When the operator runs the status CLI command
Then the output shall display:
  | Metric | Example |
  | Last pipeline run | 2026-02-19 14:00 JST |
  | Tweets searched today | 45 |
  | Tweets collected today | 12 |
  | Tweets analyzed today | 12 |
  | Replies sent today | 8 |
  | DMs sent today | 6 |
  | Monthly API tweets used | 234 / 1,500 |
  | Monthly API budget remaining | 1,266 |
  | Conservation mode | inactive |
  | System status | healthy |
```

---

### TS-09: Configuration (R9)

#### TS-09.1: Secrets Not in Config File

```gherkin
Given the config.yaml file exists at tools/x-outreach/config.yaml
When the file is inspected
Then it shall not contain any API keys, passwords, or tokens
And all secret references shall point to environment variable names
And a .env.example file shall document required environment variables
```

#### TS-09.2: Runtime Configuration Update

```gherkin
Given the system is running
And the operator modifies the keyword list in config.yaml
When the next pipeline cycle begins
Then the system shall load the updated keyword list
And use the new keywords for the search phase
And no restart shall be required
```

---

### TS-10: Korean-Derm-Expert Integration (R10)

#### TS-10.1: Treatment-Enriched Reply

```gherkin
Given a tweet asks about "ポテンツァ" (Potenza) pricing in Korea
And the tweet is classified as "seeking_info"
When the system generates a reply
Then the reply shall include relevant price comparison data
  (e.g., Korea: 15,000-25,000 yen vs Japan: 50,000-80,000 yen)
And the data shall be sourced from the korean-derm-expert knowledge base
```

#### TS-10.2: Treatment Terminology in Classification

```gherkin
Given a tweet contains the term "ピコトーニング" (Pico Toning)
When the tweet is sent to the Claude API for classification
Then the prompt shall include the treatment mapping:
  ピコトーニング -> 피코토닝 (Pico Toning)
And the classifier shall recognize this as a Korean dermatology treatment query
```

---

## Quality Gates

### Definition of Done

- [ ] All 15 Japanese keywords produce search results via Playwright
- [ ] Tweet collection correctly filters influencers (10K+), bots (no profile), and clinic accounts
- [ ] Claude API classification returns valid categories with confidence scores for 100 test tweets
- [ ] Classification accuracy is 85%+ when manually reviewed against 50 sample tweets
- [ ] Replies are posted via X API within rate limits (17/15min, 1,500/month)
- [ ] DMs are sent via Playwright with template rotation and uniqueness enforcement
- [ ] All rate limits are enforced: search delays, reply limits, DM daily caps, DM intervals
- [ ] Night mode (23:00-08:00 JST) blocks all reply and DM operations
- [ ] Session cookies persist across system restarts for both accounts
- [ ] SQLite database correctly tracks all states and prevents duplicates
- [ ] Structured JSON logs are written to console and rotating files
- [ ] CLI status command displays accurate runtime metrics
- [ ] launchd daemon starts on boot and restarts on failure
- [ ] Warmup mode limits volume to 50% during first 14 days
- [ ] Conservation mode activates when monthly API budget reaches 80%
- [ ] Emergency halt activates on DM restriction detection
- [ ] No API keys, passwords, or tokens are stored in config files or committed to git
- [ ] All modules have unit tests with 85%+ coverage

### Verification Methods

| Method | Scope | Frequency |
|--------|-------|-----------|
| Unit Tests | Individual modules | Every code change |
| Integration Tests | Full pipeline flow | Before deployment |
| Manual Review | First 100 classifications | Initial deployment |
| Daily Stats Review | Operational metrics | Daily |
| Weekly Audit | Action logs and stats | Weekly |
| Monthly Review | API budget, detection signals | Monthly |
