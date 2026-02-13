# Korean Dermatology Market Research

Cross-country analysis of how foreign nationals discover, evaluate, and book Korean dermatology/beauty clinics.

## Purpose

Identify pain points, optimal content platforms, and market opportunities for a "Korean Dermatology Guide" targeting each country's audience.

## Directory Structure

```
data/market-research/
├── README.md                        # This file
├── index.json                       # Master metadata & research status
├── schema/
│   ├── platforms.schema.json        # JSON schema for platform data
│   └── templates/
│       └── country-report.md        # Markdown report template
├── countries/
│   ├── japan/
│   │   ├── report.md               # Qualitative analysis (Korean)
│   │   ├── platforms.json           # Platform rankings & metrics
│   │   ├── pain-points.json        # Pain points with severity scores
│   │   ├── influencers.json        # Key influencers & reach
│   │   ├── market.json             # Market size, trends, demographics
│   │   └── competitors.json        # Competing services & agencies
│   ├── taiwan/                      # Same structure (template)
│   └── malaysia/                    # Same structure (template)
└── comparisons/
    └── cross-country-summary.md     # Auto-generated comparison
```

## Data Schema

### JSON Files (Structured, Comparable)
- `platforms.json` — Ranked list with scores across 7 dimensions
- `pain-points.json` — Categorized pain points with severity/frequency
- `influencers.json` — Influencers with platform, reach, engagement
- `market.json` — Visitor stats, growth rates, demographics, trends
- `competitors.json` — Intermediary services, agencies, apps

### Markdown Files (Qualitative)
- `report.md` — Full narrative analysis with sources

## Adding a New Country

1. Copy template: `cp -r schema/templates/ countries/{country}/`
2. Fill JSON files following the schema
3. Write qualitative report in `report.md`
4. Update `index.json` with new country entry
5. Regenerate `comparisons/cross-country-summary.md`

## Comparison Axes

| Axis | JSON File | Key Metrics |
|------|-----------|-------------|
| Platforms | platforms.json | rank, score, organic_reach, seo_value, engagement |
| Pain Points | pain-points.json | severity (1-5), frequency, resolution_difficulty |
| Influencers | influencers.json | platform, followers, engagement_rate, content_type |
| Market | market.json | visitors_per_year, growth_rate, avg_spend, demographics |
| Competitors | competitors.json | type, coverage, pricing, language_support |

## Research Status

| Country | Status | Last Updated | Researcher |
|---------|--------|-------------|------------|
| Japan | Complete | 2026-02-13 | Claude + 8 sub-agents |
| Taiwan | Planned | - | - |
| Malaysia | Planned | - | - |
