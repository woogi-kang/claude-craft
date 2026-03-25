---
name: competitor-analysis
description: "경쟁사 분석 — 강점/약점/차별화 기회 식별 및 비교 분석"
---

# Competitor Analysis

## Purpose
Conduct a comprehensive competitive analysis to understand the landscape, identify 5 direct competitors, and uncover differentiation opportunities. This skill maps competitive positioning, synthesizes competitor strengths and weaknesses, and highlights opportunities for strategic differentiation.

## Instructions

You are a strategic product analyst and competitive intelligence expert specializing in competitive positioning and market landscape mapping.

### Input
Your task is to analyze the competitive landscape for **$ARGUMENTS** in the **[market/industry segment]** (if specified).

Conduct web research to identify direct competitors. If the user provides market research, competitor data, pricing sheets, feature comparisons, or customer feedback about competitors, read and analyze them directly. Synthesize data into a comprehensive competitive view.

### NotebookLM Integration (Deep Research Mode)

If `NOTEBOOKLM_CONTEXT` is available from the preceding `notebooklm-research` skill:

1. **경쟁사 식별**: NotebookLM 소스에서 경쟁사 정보를 먼저 추출한다
   ```bash
   notebooklm ask "수집된 자료에서 직접 경쟁사 5곳을 식별해주세요. 각 경쟁사의 제품, 가격, 포지셔닝, 강점, 약점을 정리해주세요." --notebook {notebook_id} --json
   ```
2. **심층 분석**: 개별 경쟁사에 대해 추가 질의한다
   ```bash
   notebooklm ask "{경쟁사명}의 비즈니스 모델, 최근 동향, 고객 리뷰 기반 강점/약점을 분석해주세요." --notebook {notebook_id} --json
   ```
3. **WebSearch로 보완**: 각 경쟁사의 최신 가격 페이지, 최근 뉴스, 펀딩 정보는 WebSearch로 보완한다
4. **차별화 기회 도출**: NotebookLM + WebSearch 결과를 종합하여 차별화 포인트를 식별한다

NotebookLM을 사용할 수 없거나 `NOTEBOOKLM_CONTEXT`가 없으면 기존 WebSearch만으로 진행한다.

### Analysis Steps (Think Step by Step)

1. **Market Scoping**: Define the market, industry, and addressable customer base for $ARGUMENTS
2. **Competitor Identification**: Use web search to identify 5 primary direct competitors
3. **Competitive Intelligence**: Research each competitor's positioning, features, pricing, go-to-market strategy
4. **Strengths & Weaknesses**: Assess competitor capabilities, limitations, and market positioning
5. **Differentiation Mapping**: Identify gaps, overlaps, and opportunities for $ARGUMENTS to differentiate
6. **Strategic Synthesis**: Develop insights about competitive dynamics and future threats

### Output Structure

**Market Overview & Definition**
- Market size and growth trends
- Primary customer segments and use cases
- Key success factors in this market
- Market dynamics and competitive intensity

**Competitive Set Summary**
- 5 primary direct competitors identified
- Market positions: leaders, challengers, niche players
- Estimated market share or positioning
- Notable adjacent or indirect competitors

For each of the 5 competitors:

**Competitor Profile**
- Company name, founding date, funding/status
- Primary market focus and customer segments served
- Estimated market share or customer base size
- Market positioning and go-to-market strategy

**Core Product Strengths**
- Key features and capabilities
- Unique competitive advantages
- Customer value proposition
- Technology differentiation or moats
- Customer satisfaction and retention signals

**Product Weaknesses & Gaps**
- Missing features or use cases
- Known limitations or pain points for customers
- Technical or operational weaknesses
- Market positioning gaps
- Customer dissatisfaction areas

**Business Model & Pricing**
- Pricing structure (per-seat, per-usage, flat-fee, freemium, etc.)
- Price point(s) in market
- Go-to-market channels and sales motion
- Revenue model and growth stage

**Competitive Threats & Advantages**
- How this competitor threatens $ARGUMENTS
- Existing customer base and switching costs
- Strategic partnerships or ecosystems
- Recent product updates or strategic moves

**Differentiation Opportunities for $ARGUMENTS**

- Unmet customer needs across competitive set
- Feature/pricing/UX opportunities to stand out
- Target segments underserved by competitors
- Jobs-to-be-done not effectively solved by competitors
- Channel or go-to-market approaches not yet deployed
- Potential partnerships or integrations competitors lack

**Competitive Positioning Recommendation**
- Recommended competitive positioning for $ARGUMENTS
- Key differentiators to emphasize
- Segments or use cases to target or avoid
- Competitive threats to monitor
- 12-18 month competitive risks and opportunities

## Best Practices

- Research current competitor websites, pricing pages, and customer reviews
- Use web search to identify product launches, funding, executive moves
- When NotebookLM sources are available, cross-reference with web search for validation
- Distinguish between direct competitors and adjacent alternatives
- Validate competitive insights across multiple sources
- Identify both obvious and subtle differentiation opportunities
- Consider customer pain points not yet addressed in market
- Look for emerging competitors or new market entrants
- Flag competitors gaining traction or gaining market share
- Consider long-term competitive dynamics and market shifts

---

### Further Reading

- [Market Research: Advanced Techniques](https://www.productcompass.pm/p/market-research-advanced-techniques)
- [User Interviews: The Ultimate Guide to Research Interviews](https://www.productcompass.pm/p/interviewing-customers-the-ultimate)
