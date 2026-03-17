# Marketing Skills Overlap & Gap Analysis

**Local**: `claude-craft/.claude/skills/` (marketing-agent-skills + social-media-agent-skills)
**Remote**: `coreyhaines31/marketingskills` (GitHub)
**Date**: 2026-03-17

---

## Executive Summary

The local skills suite is a **structured, framework-heavy Korean-language system** designed as a sequential marketing workflow (1-15 numbered pipeline). The remote repo is an **English-language, SaaS-focused, practitioner-oriented toolkit** built around real-world execution with deep references and case studies. They have fundamentally different philosophies: local emphasizes templates and frameworks; remote emphasizes principles, decision-making, and actionable guidance.

**Key findings:**
- Remote is clearly superior in **CRO** (6 specialized skills vs 1 local), **copywriting** (with dedicated copy-editing), **content strategy**, **RevOps**, and **launch strategy**
- Local is stronger in **social media operations** (12 dedicated skills vs 1 remote), **visual design guidance**, and **sequential workflow connectivity**
- 13 remote skills have NO local equivalent at all
- Local's `2-market-research`, `3-persona`, `8-customer-journey`, and `15-review` have no direct remote equivalents

---

## Pair-by-Pair Detailed Comparison

### 1. Context: local `1-context-intake` vs remote `product-marketing-context`

**What local does better:**
- Tiered collection (Must Have / Should Have / Nice to Have) with clear prioritization
- Interview question templates (Quick Start 5min + Deep Dive 15min) for live user sessions
- Minimum viable context concept for starting with limited info
- Progressive collection workflow (collect, confirm, refine iteratively)
- Output path convention for file storage (`context/{project}-context.md`)

**What remote does better:**
- **Auto-draft from codebase** feature: scans README, landing pages, package.json to pre-fill the context document -- a killer feature for developer users
- **JTBD Four Forces** (Push/Pull/Habit/Anxiety) for switching dynamics -- sophisticated buying psychology absent from local
- **Anti-personas** section (who is NOT a good fit) -- prevents wasted effort
- **Customer Language** section emphasizing verbatim phrasing, not polished descriptions
- **Proof Points** section (metrics, logos, testimonials) structured for immediate reuse
- **Competitive landscape** taxonomy (direct/secondary/indirect) is more nuanced than local's simple direct/indirect split
- Persistent storage at `.agents/product-marketing-context.md` referenced by ALL other skills automatically

**Concrete gaps in local:**
- No auto-draft from codebase capability
- No switching dynamics / JTBD analysis
- No anti-persona concept
- No proof points / social proof collection
- No emphasis on verbatim customer language vs polished descriptions
- No cross-skill automatic reference mechanism

**Recommendation: MERGE** -- Local's interview templates and tiered collection are valuable UX. Remote's auto-draft, JTBD, anti-personas, and proof points add substantial depth. Combine both.

---

### 2. Market Research: local `2-market-research` vs remote (no direct match)

**What local provides:**
- Comprehensive 3C framework (Customer/Competitor/Company)
- TAM/SAM/SOM market sizing templates
- SWOT analysis structure
- Customer segment analysis with buying behavior
- Detailed competitor comparison tables
- Structured output template with executive summary

**Remote gap:**
- No dedicated market research skill. Competitor analysis is split across `competitor-alternatives` (comparison pages for SEO/sales) and `content-strategy` (competitive content analysis). Neither covers full 3C market research.
- Remote's `competitor-alternatives` is focused on creating web pages, not analytical research.

**Assessment:** Local's market research skill fills a genuine gap. The 3C framework and structured market analysis are foundational activities that the remote suite assumes the user has done elsewhere.

**Recommendation: KEEP** -- This is a strength of local with no remote equivalent. Consider enriching with remote's more practical competitor page creation approach as a downstream output.

---

### 3. Persona: local `3-persona` vs remote `product-marketing-context` (section)

**What local does better:**
- **Dedicated full skill** vs a brief section in remote's context document
- **Empathy Map** (Thinks/Feels, Sees, Hears, Says/Does, Pain/Gain) -- complete visual framework
- **Negative Persona** concept (non-target customers)
- **Daily routine** description for vivid persona portrayal
- **Objections with responses** built into persona
- **Marketing implications** section (effective message, channel, tone, CTA per persona)
- **Customer journey snapshot** embedded in each persona
- Concrete B2B SaaS example included

**What remote does better:**
- Remote's Personas section in `product-marketing-context` is more role-oriented (User, Champion, Decision Maker, Financial Buyer, Technical Influencer) -- better for B2B multi-stakeholder sales
- Captures "what each cares about, their challenge, and the value we promise" per role -- concise and actionable
- Connected to the switching dynamics framework

**Concrete gaps in local:**
- No B2B buying committee role mapping (User vs Champion vs Decision Maker)
- Personas are consumer-oriented; less structured for enterprise sales

**Recommendation: KEEP** -- Local's persona skill is significantly more comprehensive. Supplement with remote's B2B buying committee role framework.

---

### 4. Positioning: local `4-positioning` vs remote `product-marketing-context` (section)

**What local does better:**
- **Full STP framework** (Segmentation, Targeting, Positioning) as a dedicated skill
- **Positioning map** with visual axis diagram
- **Segment evaluation criteria** (MASD-A: Measurable, Accessible, Substantial, Differentiable, Actionable)
- **Four targeting strategies** explained (Undifferentiated, Differentiated, Concentrated, Micromarketing)
- **Five differentiation areas** (Product, Service, Channel, People, Image)
- **Messaging framework** with primary/supporting messages and words to use/avoid
- **Positioning formula**: "For [target], [brand] is [category] that provides [benefit] because [reason]"

**What remote does better:**
- Remote's Differentiation section is more concise and action-oriented
- "Why customers choose you over alternatives" is a sharper question than local's abstract framework
- Connected directly to proof points and customer language

**Concrete gaps in local:**
- No connection to proof points or evidence backing
- Positioning is theoretical rather than tied to real customer language

**Recommendation: KEEP** -- Local's positioning skill is comprehensive and well-structured. The framework depth exceeds what remote offers. Add remote's emphasis on evidence-backed claims.

---

### 5. Strategy: local `5-strategy` vs remote `content-strategy` + `marketing-ideas`

**What local does better:**
- **PESO framework** (Paid/Earned/Shared/Owned) with detailed channel breakdown
- **North Star Metric** concept with selection criteria
- **AI era strategy section (2025)** with short-form video prioritization (80/20 split), platform-specific recommendations, AI tool recommendations
- **Budget allocation** templates and ROI expectations
- **Risk & Mitigation** planning
- **Phased roadmap** (Foundation, Growth, Optimization) with weekly granularity
- **SMART objectives** table

**What remote does better:**
- `content-strategy`: **Searchable vs Shareable** framework -- a powerful, simple dichotomy that local lacks entirely
- `content-strategy`: **Hub and Spoke** content architecture, **Topic Clusters**, keyword research by buyer stage
- `content-strategy`: **Content ideation from multiple sources** (keyword data, call transcripts, survey responses, forum research, competitor analysis, sales/support input) -- deeply practical
- `content-strategy`: **Prioritization scoring** (Customer Impact 40%, Content-Market Fit 30%, Search Potential 20%, Resources 10%)
- `marketing-ideas`: **139 proven SaaS marketing ideas** categorized by stage, budget, and timeline -- an enormous tactical library
- `marketing-ideas`: Ideas organized by use case (Need Leads Fast, Building Authority, Low Budget Growth, Product-Led Growth, Enterprise Sales)

**Concrete gaps in local:**
- No searchable vs shareable content distinction
- No topic cluster / hub-and-spoke architecture
- No keyword research by buyer stage
- No content prioritization scoring model
- No tactical idea library (139 ideas)
- No content ideation from customer conversations/transcripts

**Recommendation: SUPPLEMENT** -- Local's PESO/NSM strategy is solid for overall marketing planning. Remote's `content-strategy` and `marketing-ideas` are complementary skills covering content planning and tactical ideation that local doesn't address. Add both as additional skills.

---

### 6. Campaign: local `6-campaign` vs remote `launch-strategy`

**What local does better:**
- **Campaign types taxonomy** (Awareness, Acquisition, Conversion, Retention, Advocacy) -- broader scope
- **SMART Goals** with detailed table format
- **Creative requirements** section (asset specs, design guidelines)
- **Team & Responsibilities** matrix
- **Risk & Contingency** planning
- **AI-era campaign additions**: challenge campaigns, community/fandom building, zero-budget viral strategies, AI content production pipeline
- **Message by funnel stage** mapping
- **Weekly optimization triggers** (if metric < threshold, then action)

**What remote does better:**
- **ORB Framework** (Owned/Rented/Borrowed channels) -- a clearer, more modern channel categorization than PESO
- **Five-phase launch approach** (Internal, Alpha, Beta, Early Access, Full Launch) -- granular phased rollout missing from local
- **Product Hunt launch strategy** with detailed preparation, execution, and case studies (SavvyCal, Reform)
- **Post-launch product marketing** with ongoing announcement strategy and update prioritization matrix
- **Real case studies** (Superhuman, Notion, TRMNL) providing concrete examples
- Focus on **momentum compounding** -- launches as an ongoing practice, not one-time events

**Concrete gaps in local:**
- No phased launch approach (Internal through Full Launch)
- No Product Hunt strategy
- No ORB channel framework
- No case studies with real company examples
- No post-launch momentum strategy

**Recommendation: MERGE** -- Local's campaign planning is broader (covers all campaign types, not just launches). Remote's launch-specific depth (phasing, Product Hunt, ORB) is superior for launch scenarios. Merge launch-specific remote content into local's campaign skill, or keep remote's `launch-strategy` as a supplementary launch-specific skill.

---

### 7. Funnel: local `7-funnel` vs remote `revops`

**What local does better:**
- **AARRR Pirate Metrics** as a clear, visual funnel framework
- **Typical conversion benchmarks** at each stage (e.g., Activation 20-40%)
- **Priority matrix** (Impact vs Difficulty quadrant)
- **Implementation roadmap** with weekly phases
- **Funnel visualization** with absolute numbers flowing through stages
- Simpler, more accessible for non-enterprise users

**What remote does better:**
- **Full RevOps system**: Lead Lifecycle Framework with 7 stages (Subscriber through Evangelist)
- **Lead Scoring**: Explicit (fit) + Implicit (engagement) + Negative scoring with detailed model building
- **Lead Routing**: Round-robin, territory-based, account-based, skill-based with routing rules
- **MQL/SQL definitions** with handoff SLAs (contact within 4 hours, qualify within 48 hours)
- **Pipeline Stage Management** with required fields per stage, stale deal alerts, stage skip detection
- **CRM Automation Workflows**: lifecycle stage updates, task creation on handoff, SLA alerts
- **Deal Desk Processes**: approval workflow tiers by deal size
- **Data Hygiene & Enrichment**: dedup strategy, enrichment tools (Clearbit, Apollo, ZoomInfo)
- **Speed-to-lead** research (5-minute response = 21x more likely to qualify)
- **RevOps Metrics Dashboard** with pipeline velocity, CAC, LTV:CAC formulas
- **Tool integrations** (HubSpot, Salesforce, Calendly, Zapier)

**Concrete gaps in local:**
- No lead scoring model
- No lead routing logic
- No MQL/SQL definitions or handoff SLAs
- No CRM automation workflows
- No deal desk processes
- No data hygiene practices
- No tool integration guidance
- Lacks the operational depth needed for B2B SaaS

**Recommendation: SUPPLEMENT** -- These skills serve different purposes. Local's AARRR funnel is a strategic planning tool. Remote's RevOps is an operational system for revenue teams. Add `revops` as a separate skill for B2B SaaS operations.

---

### 8. Customer Journey: local `8-customer-journey` vs remote (no direct match)

**What local provides:**
- 5-stage journey map (Awareness, Consideration, Decision, Purchase, Loyalty)
- Per-stage analysis: customer goals, questions, emotions, pain points
- Touchpoint mapping (online/offline)
- Content needs per stage
- Emotion curve visualization
- Gaps & Opportunities analysis
- Action items with timeline (This Week / This Month / This Quarter)

**Remote gap:**
- No dedicated customer journey skill. Journey concepts are distributed across `revops` (pipeline stages), `email-sequence` (lifecycle stages), and `page-cro` (visitor intent analysis), but none provide a unified customer journey map.

**Assessment:** This is a genuine gap in the remote suite. Customer journey mapping is a strategic exercise that ties together multiple execution skills.

**Recommendation: KEEP** -- Valuable standalone skill with no remote equivalent.

---

### 9. Copywriting: local `9-copywriting` vs remote `copywriting` + `copy-editing`

**What local does better:**
- **Five frameworks** (AIDA, PAS, BAB, FAB, 4P's) with full examples for each
- **Short-form video scripts (2025)**: Hook-Problem-Solution-CTA structure for 15-second videos, hook type templates (question, empathy, provocative, curiosity, trend), platform-specific optimization
- **Headline formulas**: 7 categories (question, how-to, number, comparison, proof, urgency, curiosity) with template patterns
- **CTA variations** by type (direct, benefit-focused, low commitment, urgency)
- **Korean-language examples** throughout

**What remote does better:**
- `copywriting`: **Writing style rules** as concrete principles (Simple > Complex, Specific > Vague, Active > Passive, Confident > Qualified, Show > Tell, Honest > Sensational)
- `copywriting`: **Page-specific guidance** for each page type (Homepage, Landing, Pricing, Feature, About)
- `copywriting`: **CTA formula**: [Action Verb] + [What They Get] + [Qualifier]
- `copywriting`: **Real brand examples** (Slack, etc.) showing before/after
- `copywriting`: Strong emphasis on **clarity over cleverness**, **customer language over company language**
- `copy-editing`: **Seven Sweeps Framework** -- a systematic 7-pass editing process:
  1. Clarity, 2. Voice/Tone, 3. So What, 4. Prove It, 5. Specificity, 6. Heightened Emotion, 7. Zero Risk
- `copy-editing`: **Word-level checks** with specific weak/strong word replacement table
- `copy-editing`: **Common problems & fixes** (Wall of Features, Corporate Speak, Weak Opening, Buried CTA, No Proof, Generic Claims, Mixed Audiences)
- `copy-editing`: Each sweep loops back to verify previous sweeps -- iterative quality control

**Concrete gaps in local:**
- No dedicated copy editing / review process
- No Seven Sweeps systematic editing framework
- No page-specific copywriting guidance
- No weak-word replacement lists
- No emphasis on customer language vs company language
- No writing style rules as principles

**Recommendation: MERGE** -- Local's framework variety (5 frameworks + short-form scripts) and remote's execution principles (writing rules + Seven Sweeps editing) are highly complementary. Merge remote's copywriting principles and add `copy-editing` as a supplementary skill.

---

### 10. Landing Page: local `10-landing-page` vs remote CRO cluster (6 skills)

**What local does better:**
- **Complete LP structure** with 11-section wireframe template (Hero through Footer)
- **Three output documents** per page: structure.md, copy.md, cro-checklist.md
- **Landing page types** taxonomy (Lead Gen, Click Through, Sales, Squeeze)
- **CRO checklist** organized by section (Hero, Trust, Form, Technical, Copy)
- **Wireframe** ASCII visualization

**What remote does better (6 specialized skills):**
- `page-cro`: Full CRO audit methodology with 10-point assessment, heatmap analysis guidance, framework for different page types, psychological principles integration
- `signup-flow-cro`: **Dedicated signup flow optimization** -- field reduction, social login, progressive profiling, post-signup activation. This granularity does not exist in local.
- `form-cro`: **Form-specific CRO** -- field optimization, error handling, multi-step forms, conditional logic, mobile optimization. Far more detailed than local's 5-line form checklist.
- `popup-cro`: **Popup/modal optimization** -- timing, trigger types, exit intent, scroll-based, A/B testing for popups. Entirely absent from local.
- `paywall-upgrade-cro`: **Upgrade/paywall screen optimization** -- pricing display, feature comparison, trial-to-paid conversion. Entirely absent from local.
- `onboarding-cro`: **Post-signup onboarding optimization** -- first-run experience, activation metrics, tooltip/tour design. Entirely absent from local.

**Concrete gaps in local:**
- No signup flow optimization
- No form-specific CRO (beyond basic checklist)
- No popup/modal strategy
- No paywall/upgrade screen optimization
- No onboarding flow optimization
- No psychological principles for conversion
- CRO is a checklist rather than an analytical methodology

**Recommendation: SUPPLEMENT** -- Local's LP skill provides a good starting template. Add all 6 remote CRO skills as a CRO cluster -- they cover the full conversion funnel from landing to onboarding, which local's single skill cannot match.

---

### 11. Email: local `11-email-sequence` vs remote `email-sequence` + `cold-email`

**What local does better:**
- **Six sequence types** with specifics: Welcome, Onboarding, Nurturing, Abandoned Cart, Reengagement, Upsell
- **Day-by-day sequence templates** for Welcome (Day 0-7), Onboarding (Day 0-14), Nurturing (Day 0-21)
- **Full email draft** template with subject, preview text, body, P.S. line
- **Branching rules** with visual flow (open/no-open logic)
- **Exit conditions** and **Segment rules** for automation
- **Technical setup** section (tags, triggers, UTM parameters)
- **Benchmark comparison** table per email

**What remote does better:**
- `email-sequence`: **Deeper principles**: "One Email, One Job," "Value Before Ask," "Relevance Over Volume"
- `email-sequence`: More emphasis on **sequence logic and decision trees**
- `cold-email`: **Entirely separate cold outreach skill** -- a whole domain local doesn't cover at all. Covers cold email frameworks, personalization at scale, follow-up cadences, deliverability, compliance (CAN-SPAM, GDPR)

**Concrete gaps in local:**
- No cold email / outbound prospecting skill
- No deliverability guidance
- No compliance/legal framework (CAN-SPAM, GDPR)

**Recommendation: MERGE + SUPPLEMENT** -- Merge remote's principles into local's already-strong email sequence skill. Add `cold-email` as a new supplementary skill (entirely new capability).

---

### 12. Ads: local `12-ads-creative` vs remote `ad-creative` + `paid-ads`

**What local does better:**
- **Three platform-specific output templates** (Google, Meta, LinkedIn) with complete copy structures
- **Exact character limits** per platform per element
- **Ad preview** mockup templates
- **Keyword strategy** with negative keywords
- **Audience targeting** specs (Core, Custom, Lookalike for Meta; Professional targeting for LinkedIn)
- **Platform-specific tone guidance** (Google: direct; Meta: conversational; LinkedIn: professional)

**What remote does better:**
- `ad-creative`: Focused on **creative strategy and iteration** rather than specs
- `paid-ads`: **Campaign architecture** (account structure, campaign types, ad group organization)
- `paid-ads`: **Budget optimization** (dayparting, bid strategies, ROAS targets)
- `paid-ads`: **Attribution modeling** and cross-channel measurement
- `paid-ads`: **Scaling framework** (when to increase spend, diminishing returns signals)
- `paid-ads`: **Platform algorithm understanding** (learning phase, audience signals)

**Concrete gaps in local:**
- No campaign architecture guidance
- No budget optimization / scaling framework
- No attribution modeling
- No algorithm/learning phase understanding
- No retargeting strategy

**Recommendation: MERGE** -- Local's detailed specs and templates are excellent for execution. Remote's strategic and optimization layers add the "why" and "when" that local misses. Merge both.

---

### 13. A/B Test: local `13-ab-testing` vs remote `ab-test-setup`

**What local does better:**
- **Sample size calculation table** (quick-reference by baseline conversion rate)
- **Test duration formula** with concrete example
- **Guardrail metrics** concept (metrics that shouldn't degrade)
- **Decision framework** with 4 scenarios (B wins, A wins, Inconclusive, B wins but guardrail violated)
- **Visual comparison** template (Control vs Variant side-by-side)
- **Results section** with raw data and statistical analysis templates

**What remote does better:**
- Similar overall structure and depth
- May include references to specific A/B testing tools and implementation guidance
- Emphasis on statistical rigor

**Concrete gaps in local:**
- Minor -- both are roughly equivalent in scope

**Recommendation: KEEP** -- Local's A/B testing skill is comprehensive and well-structured. Remote offers similar content. No significant advantage to switching.

---

### 14. Analytics: local `14-analytics-kpi` vs remote `analytics-tracking`

**What local does better:**
- **Full KPI dashboard template** organized by funnel stage (TOFU/MOFU/BOFU/Post-Funnel)
- **Channel-specific KPIs** for 6 channels (Paid Search, Paid Social, Organic, Email, Content, Social Organic)
- **Calculation formulas** for CAC, LTV, LTV:CAC, ROAS, ROI with Korean Won examples
- **Campaign performance** tracking table
- **Budget tracking** (planned vs actual vs remaining)
- **Trend visualization** templates (ASCII charts)
- **Reporting schedule** (Daily, Weekly, Monthly, Quarterly)
- **Industry benchmarks** by sector (SaaS, E-commerce, B2B)

**What remote does better:**
- `analytics-tracking`: Focused on **implementation** -- GA4 setup, event tracking, conversion tracking, UTM strategy
- **Data layer** specifications and tag management
- **Attribution model** selection guidance
- **Debugging** tracking issues
- More technically implementation-focused

**Concrete gaps in local:**
- No tracking implementation guidance (GA4, tag management)
- No data layer specifications
- No attribution model guidance
- No debugging/troubleshooting for tracking issues
- Dashboard is conceptual, not implementation-specific

**Recommendation: MERGE** -- Local excels at KPI framework and dashboard design. Remote excels at technical implementation. Combine both dimensions.

---

### 15. Social: local social-media-agent-skills (12 skills) vs remote `social-content` (1 skill)

**What local does better (overwhelmingly):**
- **12 specialized skills** covering the entire social media lifecycle:
  - `0-strategy`: Brand voice, audience persona, content pillars, platform selection
  - `1-research`: Trend monitoring, competitor watch, viral pattern analysis, topic clustering
  - `2-validation`: Brand consistency verification (not read but exists)
  - `3-compliance`: Legal/platform compliance (not read but exists)
  - `4-content`: Platform-specific content creation
  - `5-visual`: Image specs per platform, carousel design, video storyboard, AI image prompts
  - `6-hashtag`: Platform-specific hashtag strategy with mix ratios, banned tag monitoring
  - `7-approval`: Approval workflow (not read but exists)
  - `8-schedule`: Optimal posting times (KST and global), frequency guides, batching strategy, calendar templates
  - `9-repurpose`: Cross-platform content transformation with tone adaptation guides
  - `10-engagement`: Community management, DM templates, crisis protocol, outbound engagement
  - `11-analytics`: Platform-specific KPIs, engagement rate formulas, A/B testing, weekly/monthly reports

**What remote does better:**
- `social-content`: **Hook formulas** (Curiosity, Story, Value, Contrarian) are concise and actionable
- **Reverse engineering viral content** framework (Find creators, Collect data, Analyze patterns, Codify playbook)
- **Content pillars** with specific percentage allocation (Industry insights 30%, Behind-scenes 25%, Educational 25%, Personal 15%, Promotional 5%)
- **Engagement strategy** with daily routine (30 min breakdown)
- More focused on **LinkedIn and Twitter/X** which matters for SaaS B2B
- References to detailed platform strategies and post templates in separate reference files

**Concrete gaps in local:**
- No viral content reverse-engineering framework
- Less focused on B2B-relevant platforms (LinkedIn, Twitter/X)
- No TikTok strategy (though mentioned in marketing-agent-skills strategy)

**Recommendation: KEEP local + SUPPLEMENT selectively** -- Local's 12-skill social media suite is vastly more comprehensive. Add remote's hook formulas and viral reverse-engineering framework as enhancements. Remote's single skill cannot replace local's operational depth.

---

## Remote Skills with NO Local Equivalent

| Remote Skill | Description | Value Assessment |
|---|---|---|
| `ai-seo` | Optimize content for AI search engines (ChatGPT, Perplexity, Claude, Gemini) and AI Overviews | **HIGH** -- emerging critical capability, no local equivalent |
| `seo-audit` | Technical SEO audit, on-page optimization, ranking diagnosis | **HIGH** -- foundational SEO capability entirely absent from local |
| `programmatic-seo` | Build SEO-optimized pages at scale using templates and data | **MEDIUM** -- valuable for SaaS growth, specialized use case |
| `site-architecture` | Page hierarchy, navigation, URL structure, information architecture | **MEDIUM** -- important for website planning |
| `schema-markup` | Structured data / JSON-LD for rich search results | **MEDIUM** -- technical SEO enhancement |
| `cold-email` | Cold outreach email frameworks, personalization, deliverability, compliance | **HIGH** -- entire outbound channel missing from local |
| `copy-editing` | Seven Sweeps systematic copy editing framework | **HIGH** -- quality assurance layer missing from local |
| `competitor-alternatives` | Competitor comparison pages and alternative pages for SEO | **MEDIUM** -- SEO/sales enablement tool |
| `free-tool-strategy` | Engineering as marketing: build free tools for lead gen | **MEDIUM** -- creative growth tactic |
| `lead-magnets` | Gated content strategy (ebooks, checklists, templates) for email capture | **MEDIUM** -- lead generation tactic |
| `marketing-psychology` | Psychological principles and mental models for marketing | **HIGH** -- foundational knowledge missing from local |
| `pricing-strategy` | Pricing tiers, freemium, value metrics, willingness to pay | **HIGH** -- critical business decision with no local coverage |
| `churn-prevention` | Cancel flows, save offers, dunning, retention strategies | **HIGH** -- retention is critical for SaaS |
| `referral-program` | Referral, affiliate, ambassador, viral loop programs | **MEDIUM** -- growth channel |
| `sales-enablement` | Sales decks, one-pagers, objection handling, demo scripts | **HIGH** -- B2B sales support entirely absent |

---

## Local Skills with NO Remote Equivalent

| Local Skill | Description | Still Valuable? |
|---|---|---|
| `2-market-research` | 3C framework, TAM/SAM/SOM, SWOT analysis | **YES** -- foundational strategic analysis |
| `3-persona` | Full persona + empathy map creation | **YES** -- much deeper than remote's brief section |
| `4-positioning` | STP strategy with positioning map | **YES** -- comprehensive strategic framework |
| `8-customer-journey` | 5-stage journey map with touchpoints | **YES** -- unified customer view missing from remote |
| `15-review` | Marketing materials quality review | **YES** -- QA checkpoint before launch |
| Social: `2-validation` | Brand consistency verification | **YES** -- quality gate |
| Social: `3-compliance` | Legal/platform compliance | **YES** -- risk mitigation |
| Social: `5-visual` | Image specs, carousel design, AI prompts | **YES** -- operational necessity |
| Social: `6-hashtag` | Platform-specific hashtag strategy | **YES** -- platform optimization |
| Social: `7-approval` | Approval workflow | **YES** -- process governance |
| Social: `8-schedule` | Posting time optimization, batching | **YES** -- operational efficiency |
| Social: `9-repurpose` | Cross-platform content transformation | **YES** -- efficiency multiplier |
| Social: `10-engagement` | Community management, crisis protocol | **YES** -- reputation management |

All local-unique skills remain valuable. None should be removed.

---

## Priority Recommendations Summary

### Tier 1: ADD immediately (high-value gaps)

| Remote Skill | Action | Rationale |
|---|---|---|
| `copy-editing` | ADD as new skill | Seven Sweeps framework fills critical QA gap |
| `cold-email` | ADD as new skill | Entire outbound channel missing |
| `pricing-strategy` | ADD as new skill | Critical business decision with no coverage |
| `marketing-psychology` | ADD as new skill | Foundational knowledge applicable across all skills |
| `churn-prevention` | ADD as new skill | Retention is existential for SaaS |
| `sales-enablement` | ADD as new skill | B2B sales support entirely absent |

### Tier 2: ADD for SEO/technical capabilities

| Remote Skill | Action | Rationale |
|---|---|---|
| `ai-seo` | ADD as new skill | Emerging critical capability |
| `seo-audit` | ADD as new skill | Foundational SEO absent from local |
| `page-cro` | ADD as new skill | CRO methodology far deeper than local checklist |
| `signup-flow-cro` | ADD as new skill | Specialized conversion optimization |
| `onboarding-cro` | ADD as new skill | Post-signup activation |

### Tier 3: MERGE into existing local skills

| Comparison | Action | What to merge |
|---|---|---|
| Context (#1) | MERGE remote into local | Auto-draft, JTBD, anti-personas, proof points |
| Strategy (#5) | MERGE + ADD | Add `content-strategy` and `marketing-ideas` as new skills |
| Campaign (#6) | MERGE remote launch phases into local | ORB framework, 5-phase launch, Product Hunt strategy |
| Copywriting (#9) | MERGE remote principles into local | Writing style rules, page-specific guidance |
| Email (#11) | MERGE remote principles into local | "One Email One Job," deliverability |
| Ads (#12) | MERGE remote strategy into local | Campaign architecture, scaling framework |
| Analytics (#14) | MERGE remote implementation into local | GA4 setup, attribution models, data layer |

### Tier 4: KEEP as-is (local is adequate or better)

| Local Skill | Verdict |
|---|---|
| `2-market-research` | KEEP -- no remote equivalent |
| `3-persona` | KEEP -- superior to remote |
| `4-positioning` | KEEP -- comprehensive framework |
| `7-funnel` | KEEP + ADD `revops` separately |
| `8-customer-journey` | KEEP -- no remote equivalent |
| `13-ab-testing` | KEEP -- roughly equivalent |
| `15-review` | KEEP -- no remote equivalent |
| All 12 social-media skills | KEEP -- vastly superior to remote |

---

## Conclusion

The two skill suites are more **complementary than overlapping**. Local excels at structured frameworks, sequential workflows, social media operations, and Korean-market awareness. Remote excels at SaaS-specific execution, conversion optimization, SEO, sales enablement, and psychological principles. The optimal approach is to keep the local suite intact, merge remote's execution principles into matching local skills, and add 11-15 new skills from the remote suite to fill genuine capability gaps -- particularly in SEO, CRO, outbound sales, pricing, retention, and marketing psychology.
