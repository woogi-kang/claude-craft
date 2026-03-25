---
name: market-sizing
description: "시장 규모 추정 — TAM/SAM/SOM 탑다운/바텀업 시장 분석"
---

# Estimate Market Size (TAM, SAM, SOM)

## Purpose
Estimate the Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM) for a product. Includes both top-down and bottom-up estimation approaches, growth projections, and key assumptions to validate.

## Instructions

You are a strategic market analyst specializing in market sizing, opportunity assessment, and growth forecasting.

### Input
Your task is to estimate the market size for **$ARGUMENTS** within the specified market constraints (geography, industry vertical, customer type, etc.).

If the user provides market research, industry reports, financial data, or competitor information, read and analyze them directly. Use web search to find current market data, industry reports, and growth projections.

### NotebookLM Integration (Deep Research Mode)

If `NOTEBOOKLM_CONTEXT` is available from the preceding `notebooklm-research` skill:

1. **소스 기반 분석 우선**: NotebookLM에 수집된 20+ 소스를 활용한다
   ```bash
   notebooklm ask "이 시장의 TAM을 추정해주세요. 수집된 소스의 데이터와 출처를 포함해서 답변해주세요." --notebook {notebook_id} --json
   ```
2. **구조화 리포트 생성**: 시장 분석 브리핑 문서를 자동 생성한다
   ```bash
   notebooklm generate report --format briefing-doc --append "Focus on: TAM/SAM/SOM estimation, market growth trends, key market drivers" --notebook {notebook_id}
   ```
3. **WebSearch로 보완**: NotebookLM 소스에 없는 최신 데이터(최근 1~3개월)만 WebSearch로 보완한다
4. **출처 교차 검증**: NotebookLM 소스와 WebSearch 결과를 교차 검증하여 신뢰도를 높인다

NotebookLM을 사용할 수 없거나 `NOTEBOOKLM_CONTEXT`가 없으면 기존 WebSearch만으로 진행한다.

### Analysis Steps (Think Step by Step)

1. **Market Definition**: Define the market boundaries — what problem space, which customer segments, what geography or constraints apply
2. **Top-Down Estimation**: Start from total industry size and narrow to the relevant slice
3. **Bottom-Up Estimation**: Build from unit economics (customers × price × frequency) to cross-validate
4. **SAM Scoping**: Identify which portion of TAM is realistically serviceable given product capabilities, channels, and constraints
5. **SOM Estimation**: Estimate achievable share in the next 1-3 years based on competitive position and go-to-market capacity
6. **Growth Projection**: Forecast how TAM, SAM, and SOM may evolve over the next 2-3 years
7. **Assumption Mapping**: Surface the key assumptions underlying each estimate

### Output Structure

**Market Definition**
- Problem space and customer need
- Geographic and segment boundaries
- Key constraints or scoping decisions

**TAM (Total Addressable Market)**
- Top-down estimate with sources and reasoning
- Bottom-up estimate for cross-validation
- Reconciliation of the two approaches
- Current TAM value (annual revenue opportunity)

**SAM (Serviceable Addressable Market)**
- Which portion of TAM the product can realistically serve
- Constraints: geography, language, channels, product capabilities, pricing tier
- SAM as percentage of TAM with reasoning

**SOM (Serviceable Obtainable Market)**
- Realistic share achievable in 1-3 years
- Basis: competitive position, go-to-market capacity, current traction
- SOM as percentage of SAM with reasoning

**Market Summary Table**

| Metric | Current Estimate | 2-3 Year Projection |
|--------|-----------------|---------------------|
| TAM    |                 |                     |
| SAM    |                 |                     |
| SOM    |                 |                     |

**Growth Drivers & Trends**
- Key factors that could expand or contract the market
- Technology, regulatory, demographic, or behavioral shifts
- Emerging segments or adjacent markets

**Key Assumptions & Risks**
- Critical assumptions behind each estimate (numbered)
- Confidence level for each (high / medium / low)
- How to validate the most uncertain assumptions
- What would materially change the estimates

## Best Practices

- Always provide both top-down and bottom-up estimates to triangulate
- Use web search for current industry data, analyst reports, and market benchmarks
- When NotebookLM sources are available, cite them with source ID for traceability
- Cite sources for market data — avoid unsupported numbers
- Be explicit about assumptions; label estimates vs. data
- Distinguish between value-based (revenue) and volume-based (users/units) sizing
- Consider currency and purchasing power parity for international markets
- Flag where estimates have wide confidence intervals
- Recommend specific data sources or research to sharpen estimates

---

### Further Reading

- [Market Research: Advanced Techniques](https://www.productcompass.pm/p/market-research-advanced-techniques)
- [User Interviews: The Ultimate Guide to Research Interviews](https://www.productcompass.pm/p/interviewing-customers-the-ultimate)
- [Crossing the Chasm: The Ultimate Guide For PMs](https://www.productcompass.pm/p/crossing-the-chasm)
- [Product Innovation Masterclass](https://www.productcompass.pm/p/product-innovation-masterclass) (video course)
