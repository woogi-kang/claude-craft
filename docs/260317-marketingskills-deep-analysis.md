# Deep Analysis: coreyhaines31/marketingskills (33 Skills)

*Analyzed: 2026-03-17*
*Repository: https://github.com/coreyhaines31/marketingskills*
*Creator: Corey Haines | License: MIT | All skills at v1.2.0 (except lead-magnets at v1.0.0)*

---

## Executive Summary

This repository is a comprehensive marketing skill library built on the [Agent Skills specification](https://agentskills.io/specification.md). It contains 33 skills, 51 zero-dependency CLI tools, 72 integration guides, and a Composio MCP integration layer. The skills are designed for AI agent consumption (Claude Code, Gemini CLI, Codex CLI, OpenCode) and cover the full SaaS marketing lifecycle: from positioning and content strategy through acquisition, conversion, retention, and revenue operations.

**Key architectural patterns:**
- Every skill reads `product-marketing-context` as shared context before asking questions
- Skills cross-reference each other with clear scope boundaries
- Reference files (`references/`) keep main SKILL.md under 500 lines
- 197 evals across all skills for automated quality testing
- Tool integrations map skills to specific CLI tools and integration guides

---

## Summary Table: All 33 Skills

| # | Skill | Category | Quality | Key Strength | Refs | Evals |
|---|-------|----------|---------|-------------|:----:|:-----:|
| 1 | ab-test-setup | Experimentation | A | Sample size tables, hypothesis framework | Yes | Yes |
| 2 | ad-creative | Paid Media | A+ | Platform specs, iteration from performance data, bulk CSV output | Yes | Yes |
| 3 | ai-seo | SEO | A+ | Princeton GEO research data, AI bot audit, platform-specific optimization | Yes | Yes |
| 4 | analytics-tracking | Analytics | A | Tracking plan framework, event naming conventions, GTM patterns | Yes | Yes |
| 5 | churn-prevention | Retention | A+ | Cancel flow UI patterns, dynamic save offers, dunning playbook | Yes | Yes |
| 6 | cold-email | Outbound | A | Voice/tone calibration, 4-level personalization system | Yes | Yes |
| 7 | competitor-alternatives | SEO/Sales | A | 4 page formats, centralized competitor data architecture | Yes | Yes |
| 8 | content-strategy | Content | A | Searchable vs shareable framework, 6 ideation sources | Yes | Yes |
| 9 | copy-editing | Writing | A+ | Seven Sweeps framework (unique methodology) | Yes | Yes |
| 10 | copywriting | Writing | A | Page structure framework, CTA copy guidelines | Yes | Yes |
| 11 | email-sequence | Email | A | 4 sequence types with full templates, email type catalog | Yes | Yes |
| 12 | form-cro | CRO | A | Field-by-field optimization, multi-step patterns | No | Yes |
| 13 | free-tool-strategy | Growth | A | Evaluation scorecard, gating options, build vs buy analysis | Yes | Yes |
| 14 | launch-strategy | GTM | A+ | ORB framework (Owned/Rented/Borrowed), 5-phase launch, Product Hunt playbook | No | Yes |
| 15 | lead-magnets | Lead Gen | A | Type matrix by buyer stage, gating strategy, distribution plan | Yes | No |
| 16 | marketing-ideas | Strategy | A | 139 categorized ideas with stage/budget mapping | Yes | Yes |
| 17 | marketing-psychology | Psychology | A+ | 39+ mental models with marketing applications | No | Yes |
| 18 | onboarding-cro | Activation | A | Aha moment framework, activation metrics, flow design patterns | Yes | Yes |
| 19 | page-cro | CRO | A | CRO analysis framework with priority ordering | Yes | Yes |
| 20 | paid-ads | Paid Media | A | Platform selection guide, campaign structure, naming conventions | Yes | Yes |
| 21 | paywall-upgrade-cro | Monetization | A | Trigger points taxonomy, paywall component design | Yes | Yes |
| 22 | popup-cro | CRO | A | Trigger strategies, frequency management, format selection | No | Yes |
| 23 | pricing-strategy | Monetization | A+ | Van Westendorp, Good-Better-Best, value metric selection | Yes | Yes |
| 24 | product-marketing-context | Foundation | A+ | 12-section positioning document, auto-draft from codebase | No | Yes |
| 25 | programmatic-seo | SEO | A | 12 playbooks, data defensibility hierarchy, URL structure rules | Yes | Yes |
| 26 | referral-program | Growth | A | Referral loop design, trigger moments, incentive structure | Yes | Yes |
| 27 | revops | Operations | A+ | Lead lifecycle framework, MQL definition, lead scoring model | Yes | Yes |
| 28 | sales-enablement | Sales | A | 10-12 slide deck framework, one-pagers, objection docs, demo scripts | Yes | Yes |
| 29 | schema-markup | Technical SEO | A | JSON-LD examples for all major types, validation workflow | Yes | Yes |
| 30 | seo-audit | SEO | A | 5-priority audit framework, schema detection limitations documented | Yes | Yes |
| 31 | signup-flow-cro | CRO | A | Field-by-field optimization, progressive profiling | No | Yes |
| 32 | site-architecture | IA | A | Site type templates, 3-click rule, flat vs deep analysis | Yes | Yes |
| 33 | social-content | Social | A | Platform quick reference, hook formulas, reverse engineering framework | Yes | Yes |

---

## Detailed Skill Analysis

### 1. ab-test-setup

- **Core capabilities:**
  - Design statistically valid A/B tests
  - Calculate sample sizes with quick-reference tables
  - Structure hypotheses with structured template
  - Select primary/secondary/guardrail metrics
  - Analyze and interpret results
- **Frameworks:** Hypothesis Framework ("Because [observation], we believe [change] will cause [outcome] for [audience]. We'll know when [metrics].")
- **Quality:** Highly detailed. Includes sample size lookup table (baseline x lift), traffic allocation strategies, implementation approaches (client-side vs server-side), common mistakes.
- **Outputs:** Hypothesis documents, test plans, analysis checklists
- **Cross-references:** page-cro, analytics-tracking, copywriting
- **Unique value:** The sample size quick-reference table and structured hypothesis template are immediately actionable. The "peeking problem" warning is a critical best practice often missed.
- **Reference files:** `references/sample-size-guide.md`, `references/test-templates.md`

---

### 2. ad-creative

- **Core capabilities:**
  - Generate ad copy at scale across Google, Meta, LinkedIn, TikTok, Twitter/X
  - Iterate from performance data (analyze winners/losers, generate new variations)
  - Validate against platform character limits
  - Produce bulk CSV output for direct upload
  - Guide AI-generated ad visuals and video
- **Frameworks:** Angle-based generation (8 angle categories), Iteration Log, Batch Generation Workflow (3 waves)
- **Quality:** Exceptional. Includes exact character limits per platform per element, organized output format with character counts, performance-driven iteration process.
- **Outputs:** Ad headlines/descriptions with character counts, bulk CSV for upload, iteration reports with performance analysis
- **Cross-references:** paid-ads, copywriting, ab-test-setup, marketing-psychology, copy-editing
- **Unique value:** The two-mode approach (generate from scratch vs. iterate from data) with CLI tool integration for pulling live performance data. The generative tools reference covering image/video/voice AI tools is cutting-edge.
- **Reference files:** `references/platform-specs.md`, `references/generative-tools.md`

---

### 3. ai-seo

- **Core capabilities:**
  - Optimize content for AI search engines (Google AI Overviews, ChatGPT, Perplexity, Claude, Gemini, Copilot)
  - Conduct AI visibility audits across platforms
  - Implement the 3-pillar strategy (Structure, Authority, Presence)
  - Check AI bot access (robots.txt)
  - Monitor AI citation rates
- **Frameworks:** 3 Pillars (Structure/Authority/Presence), Princeton GEO research (9 optimization methods ranked by visibility boost), AI Visibility Audit (4-step)
- **Quality:** Outstanding. Cites the Princeton KDD 2024 study with specific visibility boost percentages. Includes a complete AI bot list, content extractability checklist, and monitoring tool comparison.
- **Outputs:** AI visibility audit reports, content optimization recommendations, robots.txt configuration, monitoring setup
- **Cross-references:** seo-audit, schema-markup, content-strategy, competitor-alternatives, programmatic-seo, copywriting
- **Unique value:** The most comprehensive AI SEO guide available. The Princeton GEO data (citations +40%, statistics +37%, keyword stuffing -10%) is original research rarely compiled this clearly. The AI bot access check is a critical but overlooked audit step.
- **Reference files:** `references/platform-ranking-factors.md`, `references/content-patterns.md`

---

### 4. analytics-tracking

- **Core capabilities:**
  - Design tracking plans with event naming conventions
  - Implement GA4 custom events
  - Set up Google Tag Manager (tags, triggers, variables, data layer)
  - Design UTM parameter strategies
  - Debug and validate tracking implementations
- **Frameworks:** Object-Action event naming (`signup_completed`, `cta_hero_clicked`), Tracking Plan Framework
- **Quality:** Very detailed. Includes specific code examples for gtag.js and data layer pushes, essential event lists by site type, debugging tool recommendations.
- **Outputs:** Complete tracking plan documents, event schemas, UTM naming conventions
- **Cross-references:** ab-test-setup, seo-audit, page-cro, revops
- **Unique value:** The Object-Action naming convention and the essential events tables for marketing sites vs. product apps provide instant structure. Privacy/compliance section covers consent mode.
- **Reference files:** `references/event-library.md`, `references/ga4-implementation.md`, `references/gtm-implementation.md`

---

### 5. churn-prevention

- **Core capabilities:**
  - Design cancel flows with exit surveys and dynamic save offers
  - Build churn prediction models (health scoring)
  - Implement dunning strategies for failed payment recovery
  - Create proactive retention interventions
  - Run cancel flow A/B tests
- **Frameworks:** Cancel Flow Structure (Trigger -> Survey -> Dynamic Offer -> Confirmation -> Post-Cancel), Health Score Model (5-dimension weighted), Dunning Stack (Pre-dunning -> Smart Retry -> Dunning Emails -> Grace Period -> Hard Cancel)
- **Quality:** Exceptional. Includes ASCII UI wireframes for cancel flows, offer-to-reason mapping tables, retry strategies by decline type (soft vs hard), recovery benchmarks, and retention platform comparisons (Churnkey, ProsperStack, Raaft).
- **Outputs:** Cancel flow designs with UI patterns, save offer configurations, dunning email sequences, health score models, churn metric dashboards
- **Cross-references:** email-sequence, paywall-upgrade-cro, pricing-strategy, onboarding-cro, analytics-tracking, ab-test-setup
- **Unique value:** The dynamic offer mapping (discount for "too expensive," pause for "not using enough," roadmap for "missing feature") is sophisticated. The distinction between voluntary and involuntary churn with separate strategies for each is critical knowledge often missed.
- **Reference files:** `references/cancel-flow-patterns.md`, `references/dunning-playbook.md`

---

### 6. cold-email

- **Core capabilities:**
  - Write cold emails that sound human, not templated
  - Craft subject lines optimized for open rates
  - Design multi-touch follow-up sequences (3-5 emails)
  - Calibrate voice by audience (C-suite vs mid-level vs technical)
  - Personalize connected to the problem (not surface-level)
- **Frameworks:** Multiple structural frameworks (Observation -> Problem -> Proof -> Ask; Question -> Value -> Ask; Trigger -> Insight -> Ask; Story -> Bridge -> Ask), 4-level personalization system
- **Quality:** Excellent. The writing principles are sophisticated ("write like a peer, not a vendor," "every sentence must earn its place"). The anti-pattern list ("I hope this email finds you well") is practical.
- **Outputs:** Cold email drafts, follow-up sequences with angle rotation, subject lines, breakup emails
- **Cross-references:** copywriting, email-sequence, social-content, product-marketing-context, revops
- **Unique value:** The philosophy of "personalization must connect to the problem" elevates this beyond template-based cold email tools. The emphasis on voice calibration by seniority level is a rare find.
- **Reference files:** `references/personalization.md`, `references/subject-lines.md`, `references/follow-up-sequences.md`, `references/frameworks.md`, `references/benchmarks.md`

---

### 7. competitor-alternatives

- **Core capabilities:**
  - Create 4 types of competitive pages (singular alternative, plural alternatives, you vs competitor, competitor A vs B)
  - Build centralized competitor data architecture
  - Research competitors systematically (product, pricing, review mining)
  - Optimize competitive pages for SEO
- **Frameworks:** 4 Page Formats with URL patterns and page structures, Centralized Competitor Data model
- **Quality:** Very detailed. Each page format includes target keywords, URL patterns, and complete page structure outlines. The honesty-first approach ("acknowledge competitor strengths") is strategically sound.
- **Outputs:** Competitor data files (YAML), full page content by section, page set plans with priority
- **Cross-references:** programmatic-seo, copywriting, seo-audit, schema-markup, sales-enablement
- **Unique value:** The 4-format taxonomy is comprehensive. The "Competitor A vs B" format (positioning yourself as a third option) is an underutilized strategy. Centralized competitor data architecture enables consistency across pages.
- **Reference files:** `references/templates.md`, `references/content-architecture.md`

---

### 8. content-strategy

- **Core capabilities:**
  - Plan content strategies around 3-5 pillars
  - Prioritize content using a 4-factor scoring model
  - Map content to buyer journey stages with keyword modifiers
  - Ideate from 6 sources (keywords, calls, surveys, forums, competitors, sales/support)
  - Design hub-and-spoke topic clusters
- **Frameworks:** Searchable vs Shareable content distinction, 4-Factor Prioritization (Customer Impact 40%, Content-Market Fit 30%, Search Potential 20%, Resources 10%), Buyer Stage Keyword Modifiers
- **Quality:** Excellent. The searchable vs shareable framework is a clean mental model. The 6 ideation sources with specific extraction methods are immediately useful. The buyer stage keyword modifiers are practical.
- **Outputs:** Content pillars with rationale, prioritized topic lists with scoring, topic cluster maps
- **Cross-references:** copywriting, seo-audit, ai-seo, programmatic-seo, site-architecture, email-sequence, social-content
- **Unique value:** The weighted scoring template and the note on when to use hub/spoke URL structures vs. simple `/blog` is pragmatic advice rarely found.
- **Reference files:** `references/headless-cms.md` (Sanity, Contentful, Strapi comparison)

---

### 9. copy-editing

- **Core capabilities:**
  - Systematically improve existing copy through 7 sequential passes
  - Run quick-pass editing checks for word/sentence/paragraph level issues
  - Provide structured copy editing checklists
  - Diagnose and fix 8 common copy problems
- **Frameworks:** Seven Sweeps Framework (Clarity -> Voice & Tone -> So What -> Prove It -> Specificity -> Heightened Emotion -> Zero Risk) -- a unique, proprietary methodology
- **Quality:** Outstanding. Each sweep includes what to check, common issues, a process, and a verification step. The "loop back" instruction after each sweep is methodologically rigorous.
- **Outputs:** Annotated copy with issue identification, specific edit recommendations, editing checklists
- **Cross-references:** copywriting, page-cro, marketing-psychology, ab-test-setup
- **Unique value:** The Seven Sweeps Framework is the most distinctive methodology in the entire repository. The word-level replacement table (utilize -> use, leverage -> use, seamless -> smooth) is immediately applicable.
- **Reference files:** `references/plain-english-alternatives.md`

---

### 10. copywriting

- **Core capabilities:**
  - Write conversion-focused copy for all page types (homepage, landing, pricing, feature, about)
  - Structure pages with above-the-fold framework
  - Create effective CTAs with action + outcome formula
  - Establish brand voice and tone
  - Provide page-specific guidance
- **Frameworks:** Above-the-Fold framework (Headline + Subheadline + CTA), CTA Formula ([Action Verb] + [What They Get] + [Qualifier]), Page Structure Framework with core section types
- **Quality:** Very good. Includes headline formula examples, CTA strength comparisons, page-type-specific guidance. The "clarity over cleverness" principle is well-supported.
- **Outputs:** Page copy organized by section, annotated alternatives with rationale, meta content
- **Cross-references:** copy-editing, page-cro, email-sequence, popup-cro, ab-test-setup
- **Unique value:** The Slack example (showing bad vs good copy) is concrete. The page-specific guidance (homepage serves multiple audiences, landing page single CTA) is sound.
- **Reference files:** `references/copy-frameworks.md`, `references/natural-transitions.md`

---

### 11. email-sequence

- **Core capabilities:**
  - Design 4 main sequence types (welcome, nurture, re-engagement, onboarding)
  - Plan timing, delays, and cadence
  - Write email copy with hook-context-value-CTA structure
  - Catalog email types by category (onboarding, retention, billing, usage, win-back, campaign)
  - Define measurement plans with benchmarks
- **Frameworks:** Sequence types with email-by-email structure, Email Copy Structure (Hook -> Context -> Value -> CTA -> Sign-off)
- **Quality:** Excellent. Each sequence type includes length, timing, trigger, and key emails with specific purposes. The email types catalog is comprehensive.
- **Outputs:** Complete sequence designs with subject lines, preview text, body copy, and CTAs for each email
- **Cross-references:** lead-magnets, churn-prevention, onboarding-cro, copywriting, ab-test-setup, popup-cro, revops
- **Unique value:** The email types catalog (onboarding, retention, billing, usage, win-back, campaign) is a rare comprehensive reference. Subject line patterns with specific formulas are actionable.
- **Reference files:** `references/sequence-templates.md`, `references/email-types.md`, `references/copy-guidelines.md`

---

### 12. form-cro

- **Core capabilities:**
  - Optimize form fields individually (email, name, phone, dropdowns, checkboxes)
  - Design multi-step forms with progressive commitment
  - Handle errors with inline validation
  - Optimize submit buttons (copy, placement, post-submit states)
  - Add trust elements and reduce friction
  - Provide form-type-specific guidance (lead capture, contact, demo, quote, survey)
- **Frameworks:** Progressive Commitment Pattern (low friction -> more detail -> qualifying questions -> contact preferences), Field Cost Rule (each field reduces completion 10-25%)
- **Quality:** Very detailed. The field-by-field optimization is granular (e.g., email typo detection for gmial.com). Mobile optimization with 44px touch targets is specific.
- **Outputs:** Form audits with issue/impact/fix/priority, recommended form designs, test hypotheses
- **Cross-references:** signup-flow-cro, popup-cro, page-cro, ab-test-setup
- **Unique value:** The "labels vs placeholders" distinction (placeholders disappear when typing) and the field cost quantification are practical. The experiment ideas section is extensive.
- **Reference files:** None (evals only)

---

### 13. free-tool-strategy

- **Core capabilities:**
  - Evaluate free tool ideas with a scoring framework
  - Choose between gating strategies
  - Plan SEO and link-building for tools
  - Decide build vs buy vs embed
  - Scope MVPs
- **Frameworks:** Evaluation Scorecard (25+ = Strong, 15-24 = Promising, <15 = Reconsider), Build vs Buy decision framework
- **Quality:** Good. The 4 core principles (solve real problem, adjacent to product, simple, worth the investment) are sound. The lead capture strategy section provides concrete gating options.
- **Outputs:** Tool strategy recommendations, evaluation scorecards, MVP scope documents
- **Cross-references:** lead-magnets, page-cro, seo-audit, analytics-tracking, email-sequence
- **Unique value:** The "engineering as marketing" framing and the evaluation scorecard quantify what is usually a gut-feel decision. The build vs buy analysis is practical.
- **Reference files:** `references/tool-types.md`

---

### 14. launch-strategy

- **Core capabilities:**
  - Plan launches using the ORB channel framework (Owned, Rented, Borrowed)
  - Execute a 5-phase launch approach (Internal -> Alpha -> Beta -> Early Access -> Full Launch)
  - Run Product Hunt launches with preparation checklist
  - Create pre-launch, launch day, and post-launch checklists
- **Frameworks:** ORB Framework (Owned/Rented/Borrowed channels), 5-Phase Launch Approach, Product Hunt Launch Strategy
- **Quality:** Excellent. The ORB framework with real examples (Superhuman, Notion, TRMNL) is memorable and actionable. The 5-phase approach is methodical. The Product Hunt section is detailed.
- **Outputs:** Launch plans with phase timelines, channel strategies, checklists for pre-launch/launch/post-launch
- **Cross-references:** marketing-ideas, email-sequence, page-cro, marketing-psychology, programmatic-seo, sales-enablement
- **Unique value:** The ORB framework is distinctive and well-illustrated. The TRMNL case study ($500K from a single YouTuber review) is compelling. The emphasis on "launch again and again" is a key mindset shift.
- **Reference files:** None (evals only)

---

### 15. lead-magnets

- **Core capabilities:**
  - Select lead magnet format by buyer stage (awareness, consideration, decision)
  - Design gating strategies with conversion trade-offs
  - Plan landing page structure for lead magnets
  - Create distribution and promotion plans (blog CTAs, exit-intent, social, paid, partners)
  - Measure success with benchmarks
- **Frameworks:** Lead Magnet Type Matrix (format x effort x time), Buyer Stage Matching, Gating Strategy Options (full gate, partial gate, ungated + optional, content upgrade)
- **Quality:** Very good. The format-to-stage matching table and the gating options with trade-offs are well-structured. The thank-you page optimization section is an often-overlooked detail.
- **Outputs:** Lead magnet recommendations, content outlines, gating/capture plans, distribution plans, measurement plans
- **Cross-references:** free-tool-strategy, copywriting, email-sequence, page-cro, popup-cro, form-cro, content-strategy, analytics-tracking, paid-ads, social-content
- **Unique value:** The observation that "content upgrades convert 2-5x better than generic sidebar CTAs" and the thank-you page optimization advice are high-value insights. This is the newest skill (v1.0.0).
- **Reference files:** `references/format-guide.md`, `references/benchmarks.md`

---

### 16. marketing-ideas

- **Core capabilities:**
  - Provide 139 categorized marketing ideas
  - Match ideas to stage (pre-launch, early, growth, scale)
  - Match ideas to budget (free, low, medium, high)
  - Provide implementation guidance for each chosen idea
- **Frameworks:** 139 Ideas organized into 17 categories, Stage-Based and Budget-Based filtering
- **Quality:** Very good as an ideation tool. Functions as a curated index pointing to specific skills for execution. The category breakdown and cross-referencing is well-organized.
- **Outputs:** 3-5 recommended ideas with fit rationale, implementation steps, expected outcomes, resource requirements
- **Cross-references:** programmatic-seo, competitor-alternatives, email-sequence, free-tool-strategy, referral-program
- **Unique value:** The 139-idea library is the largest curated marketing tactics collection designed for AI agent consumption. Functions as a routing hub to other skills.
- **Reference files:** `references/ideas-by-category.md`

---

### 17. marketing-psychology

- **Core capabilities:**
  - Apply 39+ psychological principles and mental models to marketing
  - Foundational thinking models (First Principles, JTBD, Pareto, Theory of Constraints)
  - Cognitive biases applied to marketing (Anchoring, Endowment Effect, Loss Aversion)
  - Decision-making models (Hick's Law, Paradox of Choice, Default Effect)
  - Persuasion principles (Reciprocity, Social Proof, Authority, Scarcity)
- **Frameworks:** 39+ named mental models including First Principles, Jobs to Be Done, Circle of Competence, Inversion, Occam's Razor, Pareto, Theory of Constraints, Opportunity Cost, Diminishing Returns, Second-Order Thinking, Mere Exposure, Availability Heuristic, Confirmation Bias, Mimetic Desire, Sunk Cost Fallacy, Endowment Effect, IKEA Effect, Zero-Price Effect, Hyperbolic Discounting, Status-Quo Bias, Default Effect, Paradox of Choice, Goal-Gradient Effect, Peak-End Rule, Zeigarnik Effect, Pratfall Effect, Mental Accounting, Regret Aversion, Bandwagon/Social Proof, Reciprocity, Commitment & Consistency, Authority Bias, Liking/Similarity Bias, and more
- **Quality:** Outstanding. Each model includes a clear explanation and specific marketing applications. The challenge-to-model mapping table at the end is extremely useful for quick lookup.
- **Outputs:** Relevant mental model recommendations, specific marketing applications, ethical implementation guidance
- **Cross-references:** page-cro, copywriting, popup-cro, ab-test-setup
- **Unique value:** This is the most comprehensive behavioral science reference for marketing practitioners I've seen in an AI-consumable format. The 39+ models with marketing-specific applications make it an encyclopedia of persuasion science.
- **Reference files:** None (evals only)

---

### 18. onboarding-cro

- **Core capabilities:**
  - Define activation metrics and "aha moments"
  - Design post-signup onboarding flows (first 30 seconds)
  - Implement onboarding checklists and progress patterns
  - Handle empty states
  - Balance product-first vs guided setup vs value-first approaches
- **Frameworks:** Aha Moment Framework (correlating actions with retention), Onboarding Flow Design (3 approaches: product-first, guided setup, value-first)
- **Quality:** Very good. The "time to value is everything" principle and "do, don't show" philosophy are well-supported. The approach selection table (best for / risk) is practical.
- **Outputs:** Activation metric definitions, onboarding flow designs, checklist patterns, experiment recommendations
- **Cross-references:** signup-flow-cro, email-sequence, paywall-upgrade-cro, ab-test-setup
- **Unique value:** The correlation between activation actions and retention is the right analytical approach. The 3 onboarding approaches with risk trade-offs help make the right choice.
- **Reference files:** `references/experiments.md`

---

### 19. page-cro

- **Core capabilities:**
  - Analyze any marketing page across 5 dimensions (value prop clarity, headline effectiveness, CTA hierarchy, visual hierarchy, trust signals)
  - Provide page-type-specific recommendations (homepage, landing, pricing, feature, blog)
  - Generate experiment ideas organized by page section
  - Prioritize recommendations by impact
- **Frameworks:** CRO Analysis Framework (5 dimensions in order of impact), Page-type-specific analysis
- **Quality:** Excellent. The 5-dimension analysis in priority order gives structure to CRO reviews. The emphasis on "5-second clarity test" for value propositions is a proven technique.
- **Outputs:** Page audits with prioritized recommendations, experiment ideas by page type
- **Cross-references:** signup-flow-cro, form-cro, popup-cro, copywriting, ab-test-setup
- **Unique value:** The priority ordering of CRO dimensions (value prop clarity is highest impact) prevents practitioners from wasting time on low-impact changes. Integrates well with the CRO skill family.
- **Reference files:** `references/experiments.md`

---

### 20. paid-ads

- **Core capabilities:**
  - Select platforms based on product/audience fit
  - Structure campaigns with consistent naming conventions
  - Set up targeting, bidding, and budget strategies
  - Plan retargeting and remarketing
  - Optimize campaigns based on performance data
- **Frameworks:** Platform Selection Guide (5 platforms with decision criteria), Campaign Structure hierarchy (Account -> Campaign -> Ad Set -> Ad), Naming Convention template
- **Quality:** Very good. The platform comparison table and naming convention template are immediately actionable. The budget allocation guidance is practical.
- **Outputs:** Campaign strategies, targeting plans, budget allocations, naming conventions, optimization recommendations
- **Cross-references:** ad-creative, copywriting, analytics-tracking, ab-test-setup, page-cro
- **Unique value:** The separation of strategy (paid-ads) from creative (ad-creative) is smart. The naming convention template prevents the chaos that typically plagues ad accounts.
- **Reference files:** `references/` directory present

---

### 21. paywall-upgrade-cro

- **Core capabilities:**
  - Design in-app paywalls for feature gates, usage limits, trial expiration, and time-based prompts
  - Build paywall screen components
  - Apply "value before ask" principle
  - Balance conversion pressure with user respect
- **Frameworks:** 4 Trigger Points (Feature Gates, Usage Limits, Trial Expiration, Time-Based), "Value Before Ask" principle, "Respect the No" principle
- **Quality:** Good. The trigger point taxonomy is useful. The principles (value before ask, show don't tell, respect the no) set the right constraints. Distinct from public pricing page optimization.
- **Outputs:** Paywall designs, trigger configurations, upgrade screen copy
- **Cross-references:** churn-prevention, page-cro, onboarding-cro, ab-test-setup
- **Unique value:** The clear distinction between in-app paywalls (this skill) and public pricing pages (page-cro) prevents scope confusion. The "respect the no" principle prevents dark patterns.
- **Reference files:** `references/` directory present

---

### 22. popup-cro

- **Core capabilities:**
  - Select popup formats (modal, slide-in, banner, full-screen, notification bar)
  - Configure triggers (time, scroll, exit intent, click, page count)
  - Optimize popup copy, design, and CTA
  - Manage frequency and suppression rules
  - Handle mobile popup UX
- **Frameworks:** Trigger Strategies (time-based, scroll-based, exit intent, click-triggered, page count), Format Selection by use case
- **Quality:** Good. The trigger strategy comparisons with "best for" recommendations are practical. The "timing is everything" principle is well-explained with specific thresholds.
- **Outputs:** Popup designs, trigger configurations, frequency rules, experiment ideas
- **Cross-references:** lead-magnets, form-cro, page-cro, email-sequence, ab-test-setup
- **Unique value:** The "respect the user" principle with specific rules (easy to dismiss, remember preferences) prevents the common mistake of over-aggressive popups.
- **Reference files:** None (evals only)

---

### 23. pricing-strategy

- **Core capabilities:**
  - Design pricing tiers and packaging
  - Select value metrics (per seat, usage, feature, flat fee)
  - Conduct pricing research (Van Westendorp, Gabor-Granger, conjoint)
  - Plan price increases
  - Choose between freemium, free trial, and paid-only models
- **Frameworks:** Van Westendorp Price Sensitivity Meter, Good-Better-Best Framework, Three Pricing Axes (Packaging, Pricing Metric, Price Point), Value-Based Pricing model
- **Quality:** Excellent. The value metric selection framework ("does more usage = more value?") is clean. The Van Westendorp method explanation is actionable.
- **Outputs:** Pricing tier recommendations, value metric analysis, pricing research plans, price change strategies
- **Cross-references:** churn-prevention, page-cro, copywriting, marketing-psychology, ab-test-setup, revops, sales-enablement
- **Unique value:** Named pricing research methodologies (Van Westendorp, Good-Better-Best) with implementation guidance are hard to find in a concise, actionable format.
- **Reference files:** `references/` directory present

---

### 24. product-marketing-context

- **Core capabilities:**
  - Create and maintain a shared product marketing context document
  - Auto-draft positioning from codebase analysis (README, landing pages, package.json)
  - Capture 12 sections: product overview, target audience, personas, problems, competitive landscape, differentiation, objections, switching dynamics (JTBD Four Forces), customer language, brand voice, proof points, goals
  - Serve as shared context consumed by all other 32 skills
- **Frameworks:** JTBD Four Forces (Push, Pull, Habit, Anxiety) for switching dynamics, 12-Section Positioning Document
- **Quality:** Outstanding. This is the architectural foundation of the entire skill system. The auto-draft-from-codebase approach is clever -- the agent reads the repo to pre-populate the context doc. The emphasis on verbatim customer language is a best practice.
- **Outputs:** `.agents/product-marketing-context.md` -- a structured positioning document
- **Cross-references:** All 32 other skills reference this skill
- **Unique value:** The shared context pattern is the most innovative architectural decision in this repository. It prevents repetitive questioning across skills and ensures consistency. The JTBD Four Forces for switching dynamics is sophisticated.
- **Reference files:** None (evals only)

---

### 25. programmatic-seo

- **Core capabilities:**
  - Build SEO pages at scale using templates and data
  - Execute 12 playbooks (templates, curation, conversions, comparisons, examples, locations, personas, and 5 more)
  - Assess data defensibility (proprietary > product-derived > user-generated > licensed > public)
  - Design URL structures (subfolders over subdomains)
  - Avoid thin content penalties
- **Frameworks:** 12 Playbooks (Templates, Curation, Conversions, Comparisons, Examples, Locations, Personas, + 5 more), Data Defensibility Hierarchy (5 levels)
- **Quality:** Excellent. The data defensibility hierarchy is a strategic insight. The "subfolders consolidate domain authority, subdomains split it" rule is important. The "quality over quantity" principle with specific warnings about doorway pages is responsible.
- **Outputs:** Strategy documents, page templates, URL structures, content guidelines, schema markup recommendations
- **Cross-references:** seo-audit, schema-markup, site-architecture, competitor-alternatives
- **Unique value:** The 12 playbooks provide a complete taxonomy of programmatic SEO approaches. The data defensibility hierarchy helps prioritize data sources strategically.
- **Reference files:** `references/` directory present

---

### 26. referral-program

- **Core capabilities:**
  - Design customer referral programs and affiliate programs
  - Identify trigger moments for referral prompts
  - Structure incentives (double-sided, tiered, milestone-based)
  - Select and configure referral platforms
  - Measure program performance
- **Frameworks:** Referral Loop (Trigger -> Share -> Convert -> Reward -> Loop), Referral vs Affiliate decision framework, Trigger Moment identification
- **Quality:** Very good. The referral loop visualization and trigger moment identification are actionable. The tool integration section with specific platform recommendations (Rewardful, Tolt, Mention Me, Dub.co) is practical.
- **Outputs:** Program designs, incentive structures, platform configurations, measurement plans
- **Cross-references:** launch-strategy, email-sequence, marketing-psychology, analytics-tracking
- **Unique value:** The referral vs affiliate distinction with specific use cases helps avoid the common mistake of building the wrong type of program.
- **Reference files:** `references/` directory present

---

### 27. revops

- **Core capabilities:**
  - Design lead lifecycle stages (Subscriber -> Lead -> MQL -> SQL -> Opportunity -> Customer -> Evangelist)
  - Build lead scoring models (explicit fit + implicit engagement + negative signals)
  - Define MQL criteria and handoff SLAs
  - Route leads to appropriate sales reps
  - Set up pipeline management and forecasting
  - Align marketing, sales, and CS teams
- **Frameworks:** Lead Lifecycle Framework (7 stages with entry/exit criteria), Lead Scoring Model (3 dimensions: explicit/implicit/negative), MQL-to-SQL Handoff SLA, Revenue Team Alignment
- **Quality:** Excellent. The lifecycle stage definitions with entry/exit criteria and owners are immediately implementable. The MQL definition requiring both fit AND engagement is the right approach. The 4-hour SLA standard is specific.
- **Outputs:** Lifecycle definitions, lead scoring models, handoff SLAs, pipeline stage configurations, CRM automation rules
- **Cross-references:** cold-email, email-sequence, pricing-strategy, analytics-tracking, launch-strategy, sales-enablement
- **Unique value:** The principle "define before automate" prevents the common mistake of automating broken processes. The lead scoring model with negative signals (competitor domains, student emails) is sophisticated.
- **Reference files:** `references/lifecycle-definitions.md`

---

### 28. sales-enablement

- **Core capabilities:**
  - Create sales decks (10-12 slide framework)
  - Build one-pagers and leave-behinds
  - Write objection handling documents
  - Design demo scripts with timing and talk tracks
  - Create ROI calculators, proposal templates, and sales playbooks
- **Frameworks:** 10-12 Slide Deck Framework (Problem -> Cost -> Shift -> Approach -> Product -> Proof -> Case Study -> Implementation -> ROI -> Pricing -> Next Steps), Customization by Buyer Type (Technical, Economic, Champion)
- **Quality:** Very good. The deck framework with buyer-type customization is practical. The "sales uses what sales trusts" principle is a critical insight. The "scannable over comprehensive" principle prevents the common mistake of overloaded decks.
- **Outputs:** Sales decks, one-pagers, objection docs, demo scripts, ROI calculators, proposal templates, persona cards, playbooks
- **Cross-references:** competitor-alternatives, copywriting, cold-email, revops, pricing-strategy, product-marketing-context
- **Unique value:** The buyer-type customization table (technical vs economic vs champion -- what to emphasize and de-emphasize) is immediately actionable. The comprehensive output format list covers all major sales assets.
- **Reference files:** `references/deck-frameworks.md`

---

### 29. schema-markup

- **Core capabilities:**
  - Implement JSON-LD structured data for 10+ schema types
  - Choose appropriate schema types by page content
  - Generate complete JSON-LD code blocks
  - Validate with Google Rich Results Test
  - Monitor Schema health in Search Console
- **Frameworks:** Schema Type Selection Guide (10 types with required/recommended properties), JSON-LD best practices
- **Quality:** Very good. The quick-reference table matching page types to schema types is useful. The emphasis on validation and accuracy prevents common implementation mistakes.
- **Outputs:** JSON-LD code blocks, validation checklists, testing procedures
- **Cross-references:** seo-audit, ai-seo, programmatic-seo, site-architecture
- **Unique value:** The direct connection to AI SEO (schema helps AI understand content, 30-40% higher AI visibility) elevates this beyond basic technical SEO.
- **Reference files:** `references/schema-examples.md`

---

### 30. seo-audit

- **Core capabilities:**
  - Conduct full SEO audits in priority order (crawlability, technical, on-page, content, authority)
  - Check robots.txt, XML sitemaps, site architecture
  - Evaluate core web vitals and page speed
  - Analyze on-page optimization (title tags, meta, headings, content)
  - Document schema markup detection limitations
- **Frameworks:** 5-Priority Audit Framework (Crawlability -> Technical -> On-Page -> Content -> Authority), Schema Markup Detection Limitation warning
- **Quality:** Excellent. The priority ordering prevents wasting time on content optimization when crawlability is broken. The schema detection limitation warning (web_fetch cannot see JS-injected JSON-LD) is a critical note for AI agents.
- **Outputs:** Audit reports with prioritized findings, technical issue lists, optimization recommendations
- **Cross-references:** ai-seo, programmatic-seo, site-architecture, schema-markup, page-cro, analytics-tracking
- **Unique value:** The honest documentation of schema detection limitations for AI agents is uniquely self-aware. The audit priority ordering is based on impact, not effort.
- **Reference files:** `references/` directory present

---

### 31. signup-flow-cro

- **Core capabilities:**
  - Optimize signup/registration flows field by field
  - Implement progressive profiling (collect data over time)
  - Design social login and SSO options
  - Reduce perceived effort (progress indicators, smart defaults)
  - Plan post-submit experiences
- **Frameworks:** Field Priority Hierarchy (Essential -> Often Needed -> Usually Deferrable), "Value Before Commitment" principle
- **Quality:** Good. The field-by-field optimization and the "can we infer this?" question for each field are practical. The progressive profiling concept is well-explained.
- **Outputs:** Signup flow recommendations, field reduction plans, experiment ideas
- **Cross-references:** onboarding-cro, form-cro, page-cro, ab-test-setup
- **Unique value:** The field priority hierarchy (email/password essential, company/role usually deferrable) provides a clear decision framework. The password UX recommendations (show toggle, requirements upfront) are practical.
- **Reference files:** None (evals only)

---

### 32. site-architecture

- **Core capabilities:**
  - Plan website page hierarchy by site type
  - Design navigation (primary, secondary, footer, sidebar)
  - Structure URLs for SEO and usability
  - Plan internal linking strategies
  - Implement breadcrumbs
- **Frameworks:** 3-Click Rule, Flat vs Deep analysis with tradeoffs, Site Type Templates (6 types: SaaS, content/blog, e-commerce, docs, hybrid, small business), Hierarchy Levels (L0-L3)
- **Quality:** Very good. The site type table with typical depth, key sections, and URL patterns provides instant starting points. The flat vs deep tradeoff analysis is practical.
- **Outputs:** Page hierarchy maps, navigation designs, URL structures, internal linking plans, breadcrumb configurations
- **Cross-references:** content-strategy, programmatic-seo, seo-audit, page-cro, schema-markup, competitor-alternatives
- **Unique value:** The 6 site type templates provide starting points for any website project. The distinction from XML sitemaps (technical SEO) is a helpful scope clarification.
- **Reference files:** `references/site-type-templates.md`

---

### 33. social-content

- **Core capabilities:**
  - Create platform-specific social content (LinkedIn, Twitter/X, Instagram, TikTok, Facebook)
  - Build content pillar frameworks (3-5 pillars with percentage allocation)
  - Write hooks using proven formulas
  - Plan content calendars
  - Reverse-engineer successful competitor content
- **Frameworks:** Content Pillars Framework (with percentage allocation), Platform Quick Reference, Hook Formulas, Reverse Engineering Framework (6 steps)
- **Quality:** Very good. The platform quick reference table and the content pillar percentage allocation are immediately actionable. The reverse engineering framework is a sophisticated approach.
- **Outputs:** Social posts, content calendars, pillar strategies, hook formulas, competitor analysis
- **Cross-references:** copywriting, launch-strategy, email-sequence, marketing-psychology
- **Unique value:** The reverse engineering framework (find creators -> collect 500+ posts -> analyze patterns -> codify playbook -> layer voice -> convert) is a systematic approach to social content strategy rarely documented this clearly.
- **Reference files:** `references/platforms.md`, `references/reverse-engineering.md`

---

## Cross-Cutting Analysis

### The product-marketing-context Shared Context Pattern

The most architecturally significant feature of this repository. Every skill begins with:

```
If `.agents/product-marketing-context.md` exists, read it before asking questions.
Use that context and only ask for information not already covered.
```

This creates a "write once, use everywhere" pattern where foundational positioning (product, audience, competitors, voice) is captured once and consumed by all 33 skills. Benefits:
- Eliminates repetitive questioning across skills
- Ensures consistent positioning across all outputs
- Supports auto-generation from codebase analysis
- Follows the JTBD Four Forces model for switching dynamics

### Skill Dependency Graph

The skills form a clear dependency network:

**Foundation layer:** product-marketing-context (consumed by all)

**Strategy layer:** content-strategy, pricing-strategy, marketing-ideas, launch-strategy

**Execution layer:** copywriting, email-sequence, cold-email, paid-ads, ad-creative, social-content, programmatic-seo

**Optimization layer:** page-cro, signup-flow-cro, form-cro, popup-cro, onboarding-cro, paywall-upgrade-cro, ab-test-setup

**Retention layer:** churn-prevention, referral-program

**Operations layer:** analytics-tracking, revops, sales-enablement

**Technical SEO layer:** seo-audit, ai-seo, schema-markup, site-architecture

**Knowledge layer:** marketing-psychology, competitor-alternatives, copy-editing

**Growth layer:** free-tool-strategy, lead-magnets

### CRO Skill Family (6 skills with clear scope boundaries)

| Skill | Scope |
|-------|-------|
| page-cro | Any marketing page (homepage, landing, pricing, feature) |
| signup-flow-cro | Signup/registration flows |
| form-cro | Non-signup forms (lead capture, contact, demo, quote) |
| popup-cro | Popups, modals, overlays, banners |
| onboarding-cro | Post-signup activation and first-run experience |
| paywall-upgrade-cro | In-app upgrade moments (feature gates, trial expiration) |

The scope boundaries are well-documented in each skill's description with explicit "for X, see Y" cross-references.

---

## Tools Ecosystem

### CLI Tools (51 tools)

All zero-dependency Node.js scripts (Node 18+) following a consistent pattern:
- `{tool} <resource> <action> [options]`
- Env var auth (`{TOOL}_API_KEY`)
- JSON output for piping
- `--dry-run` for safe preview

Categories: Analytics (7), SEO (5), Data Enrichment (4), CRM (3), Payments (2), Referral/Links (5), Email (11), Ads (4), Automation (1), CRO/Testing (2), Scheduling (2), Forms (1), Messaging (1), Sales/Partners/Reviews/Push/Webinar/Social/Video/Content (various)

### Integration Guides (72 guides)

Detailed markdown guides in `tools/integrations/` covering:
- API endpoints and authentication
- Common operations and examples
- MCP configuration (where available)

### Composio Integration

Provides MCP access to OAuth-heavy tools without native MCP servers:
- HubSpot, Salesforce, Meta Ads, LinkedIn Ads, Google Sheets, Slack, Notion
- Single MCP server via `npx @composio/mcp@latest setup`
- 500+ tool connectors

### MCP-Enabled Tools (12)

GA4, Stripe, Mailchimp, Google Ads, Resend, Zapier, ZoomInfo, Clay, Supermetrics, Coupler, Outreach, Crossbeam

---

## Configuration Patterns

### CLAUDE.md Architecture

The repo's CLAUDE.md serves triple duty:
1. **Repository overview** -- structure, skill spec, writing guidelines
2. **Agent instructions** -- build/lint commands, git workflow, PR checklist
3. **Update checking** -- version comparison via VERSIONS.md with non-blocking notifications

Notable patterns:
- Auto-update checking: fetch VERSIONS.md once per session, notify if 2+ skills updated or any major version bump
- Claude Code plugin marketplace via `.claude-plugin/marketplace.json`
- Symlinked as AGENTS.md for cross-agent compatibility

### VERSIONS.md

Simple version tracking table with all 33 skills, versions, and last-updated dates. Enables the session-based update check pattern described in CLAUDE.md.

### Version History

- **v1.0.0** (2026-01-27): Initial release with 29 skills, tool registry
- **v1.1.0** (2026-02-27): Migration from `.claude/` to `.agents/`, all skills bumped
- **v1.2.0** (2026-03-14): Added lead-magnets, Composio, headless CMS guides, 197 evals, 10 new CLIs, 13 new integration guides, all descriptions optimized

---

## Quality Assessment Summary

### Strengths

1. **Architectural coherence** -- The shared context pattern + clear scope boundaries + cross-references create a well-integrated system, not just a collection of documents
2. **Actionable over abstract** -- Every skill produces concrete outputs (documents, code, configurations), not just advice
3. **Research-backed** -- Multiple skills cite specific studies (Princeton GEO, sample size calculations) rather than relying on conventional wisdom
4. **Honest about limitations** -- The seo-audit skill documents its own schema detection limitations. The churn-prevention skill warns against guilt-trip copy
5. **Practical tool integration** -- 51 CLI tools + 72 integration guides + Composio make skills executable, not just theoretical
6. **Comprehensive CRO family** -- 6 CRO skills with clean scope boundaries cover every conversion touchpoint

### Areas for Improvement

1. **lead-magnets** is still at v1.0.0 while all others are at v1.2.0 -- may lack the same level of polish
2. **marketing-psychology** and **popup-cro** lack reference files -- all content is in SKILL.md
3. Some skills (form-cro, signup-flow-cro) lack reference directories, keeping all content in the main file
4. The 139 marketing ideas in marketing-ideas are only accessible via the references file, not inline

### Standout Skills (Top 5)

1. **ai-seo** -- Most forward-looking, backed by Princeton research, covers an emerging category
2. **churn-prevention** -- Most comprehensive, with cancel flow wireframes, dunning strategies, and health scoring
3. **marketing-psychology** -- Deepest knowledge base with 39+ mental models
4. **copy-editing** -- Most unique methodology (Seven Sweeps framework)
5. **product-marketing-context** -- Most architecturally innovative (shared context pattern)
