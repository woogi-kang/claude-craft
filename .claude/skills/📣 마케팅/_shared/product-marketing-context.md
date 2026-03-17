# Product Marketing Context Bridge

This file bridges the two context systems used by marketing skills:

## Context File Locations

All marketing skills should check for product/brand context in this order:

1. `.agents/product-marketing-context.md` (Agent Skills spec standard)
2. `context/{project}-context.md` (Local convention)

If neither exists, invoke `1-context-intake` skill to generate context.

## For Skill Authors

When writing or importing marketing skills:
- Local pipeline skills (1-15) use `context/{project}-context.md`
- Imported skills (CRO, Growth, Sales) use `.agents/product-marketing-context.md`
- The `1-context-intake` skill outputs to BOTH locations

## Cross-Reference Map

| Remote Skill Reference | Local Equivalent |
|----------------------|-----------------|
| product-marketing-context | 1-context-intake |
| copywriting | 9-copywriting |
| copy-editing | copy-editing (standalone) |
| email-sequence | 11-email-sequence |
| ab-test-setup | 13-ab-testing |
| analytics-tracking | 14-analytics-kpi |
| social-content | social-media-agent-skills (12 skills) |
| content-strategy | content-strategy (standalone) |
| page-cro | cro-skills/page-cro |
| cold-email | sales-skills/cold-email |
