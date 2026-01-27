---
description: "Monthly financial report - Generate P&L, balance sheet, and cash flow"
argument-hint: "[YYYY-MM]"
type: utility
allowed-tools: AskUserQuestion, Bash, Read, Write, Glob, Grep, Task
model: opus
---

## Pre-execution Context

!ls -la operations/finance/ 2>/dev/null || echo "Finance directory not found"
!cat operations/finance/ledger.json 2>/dev/null | head -50 || echo "Ledger not found"

---

# /financial-report - Monthly Financial Report Command

## Core Principle

Generate comprehensive monthly financial reports using Multi-LLM strategy:
- **Gemini CLI**: OCR for any pending receipts (free tier)
- **Claude**: Analysis, classification, and report generation
- **Cost Target**: <$5/month for full automation

## Command Flow

```
START: Verify target month
  ↓
Collect pending receipts (if any)
  ↓
Run OCR with Gemini CLI
  ↓
Classify expenses with Claude
  ↓
Generate financial statements
  ↓
Create PDF reports
  ↓
Distribute (Notion + Slack)
```

## Step 1: Parameter Validation

```bash
# Default to previous month if not specified (cross-platform)
TARGET_MONTH="${1:-$(date -d 'last month' +%Y-%m 2>/dev/null || date -v-1m +%Y-%m)}"
echo "Generating report for: $TARGET_MONTH"
```

## Step 2: Process Pending Receipts

```bash
# Check for unprocessed receipts
PENDING=$(ls operations/finance/receipts/$TARGET_MONTH/*.{jpg,png,pdf} 2>/dev/null | wc -l)

if [ "$PENDING" -gt 0 ]; then
  echo "Processing $PENDING pending receipts with Gemini CLI..."

  for img in operations/finance/receipts/$TARGET_MONTH/*.{jpg,png,pdf}; do
    [ -f "$img" ] || continue

    # Skip if already processed
    json_file="${img%.*}.json"
    [ -f "$json_file" ] && continue

    gemini "영수증 JSON 추출: vendor, date, items, total, vat, category" \
      --image "$img" > "$json_file"

    sleep 1  # Rate limit prevention
  done
fi
```

## Step 3: Aggregate Ledger Data

```bash
# Extract transactions for target month
cat operations/finance/ledger.json | \
  jq --arg month "$TARGET_MONTH" \
  '.transactions | map(select(.date | startswith($month)))'
```

## Step 4: Generate Financial Statements

Using Claude to generate:

1. **손익계산서 (P&L)**
   - Revenue breakdown
   - Cost of goods sold
   - Operating expenses by category
   - Net income

2. **대차대조표 (Balance Sheet)**
   - Current assets (cash, receivables)
   - Fixed assets
   - Liabilities
   - Equity

3. **현금흐름표 (Cash Flow)**
   - Operating activities
   - Investing activities
   - Financing activities

## Step 5: Generate PDF Reports

```bash
# Use Playwright to render Markdown to PDF
npx playwright pdf \
  operations/finance/statements/$TARGET_MONTH/pnl.md \
  operations/finance/statements/$TARGET_MONTH/pnl.pdf
```

## Step 6: Distribution

```bash
# Git commit
git add operations/finance/statements/$TARGET_MONTH/
git commit -m "chore(finance): add $TARGET_MONTH financial statements"

# Notion upload (via MCP)
# notion_upload "Finance/$TARGET_MONTH" statements/

# Slack notification
# slack_notify "#finance" "📊 $TARGET_MONTH 재무 리포트가 생성되었습니다."
```

## Output Format

```markdown
## 📊 Financial Report Complete

**Period**: 2026-01

### Summary

| Metric | Amount | vs Previous |
|--------|--------|-------------|
| Revenue | ₩50,000,000 | +15% |
| Expenses | ₩35,000,000 | +8% |
| Net Income | ₩13,617,000 | +25% |
| Runway | 18 months | - |

### Generated Files

- `statements/2026-01/pnl.pdf` - 손익계산서
- `statements/2026-01/balance.pdf` - 대차대조표
- `statements/2026-01/cashflow.pdf` - 현금흐름표
- `statements/2026-01/summary.md` - 경영진 요약

### Key Insights

1. **매출 성장**: 전월 대비 15% 증가
2. **비용 효율**: 마케팅비 10% 절감
3. **주의 필요**: 서버비 20% 증가 (트래픽 증가로 인한 정상적 증가)

### Alerts

⚠️ 서버/인프라 예산 80% 도달 (₩8M / ₩10M)
```

---

## EXECUTION DIRECTIVE

1. Parse target month from argument (default: previous month)

2. Check for pending receipts in `operations/finance/receipts/$TARGET_MONTH/`
   - If found, process with Gemini CLI OCR
   - Save JSON results alongside images

3. Read ledger data: `operations/finance/ledger.json`
   - Filter transactions for target month
   - Validate: no missing required fields

4. Generate financial statements:
   - Use finance-orchestrator-agent or direct Claude prompts
   - Create Markdown files in `operations/finance/statements/$TARGET_MONTH/`

5. Generate PDF reports (if Playwright available):
   - Render each Markdown to PDF

6. Create summary with:
   - Key metrics table
   - Month-over-month comparison
   - Insights and alerts

7. Distribute:
   - Git commit the new statements
   - (Optional) Notion upload
   - (Optional) Slack notification

8. Present summary to user in conversation

---

Version: 1.0.0
Last Updated: 2026-01-27
Core: Multi-LLM financial reporting automation
