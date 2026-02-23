# X-Outreach Pipeline

Automated X (Twitter) outreach pipeline for Korean dermatology expert targeting Japanese audience (@ask.nandemo brand).

## Architecture

```
src/                    Main application package
├── ai/                 LLM classification & two-phase content generation
├── browser/            Playwright session management (per-persona sessions)
├── cli/                CLI commands (status, report, blocklist, setup)
├── db/                 PostgreSQL data access layer
├── knowledge/          Treatment knowledge base & templates
├── pipeline/           Pipeline stages (search, collect, analyze, reply, dm, nurture, posting)
├── platform/           X login & DOM selectors
├── config.py           Pydantic settings (PROJECT_ROOT defined here)
├── daemon.py           Background daemon with scheduling
├── main.py             Pipeline orchestrator
└── persona.py          Multi-persona account system (5 personas)

packages/_shared/       Shared library (outreach_shared)
├── ai/                 LLM client abstraction (OpenAI, Gemini, Claude, Codex CLI)
├── browser/            Stealth browser & human simulation
├── daemon/             Daemon loop infrastructure
├── db/                 PostgreSQL models & connection pooling
├── account/            Account pool & health monitoring
└── utils/              Logger, rate limiter, time utilities

personas/               5 persona definitions
├── accounts.yaml       Account-to-persona mappings (master_a → p01_price, etc.)
├── p01_price.md        みく - Price analysis (master_a)
├── p02_beginner_guide.md  あや - Beginner guide (master_b)
├── p03_procedure_explainer.md  りこ - Procedure explanation (master_c)
├── p04_risk_care.md    なつみ - Risk & aftercare (master_d)
├── p05_lifestyle.md    ゆい - Lifestyle (master_e)
├── base_policy.md      Universal safety & expression policy
├── keyword_matrix.yaml Keyword profiles per persona
└── style_lexicon.yaml  Style preferences (endings, banned words)

data/
├── dermatology/        Treatment procedures (679 records, 30 categories)
├── clinic-results/     Hospital database (hospitals.db, skin_clinics.csv)
└── market-research/    Japan market data (prices, competitors, influencers)

docs/
├── strategy/           X launch strategy, 100-day plan, reply/DM strategy
└── drafts/             Content drafts
```

## Running

```bash
# Install dependencies
uv sync --all-extras

# Install Playwright browser
uv run playwright install chromium

# Dry run (no actual posting)
uv run python -m src run --account-id master_b --dry-run

# Full pipeline for a specific persona account
uv run python -m src run --account-id master_b

# Daemon mode (background scheduler, 2-4h intervals)
uv run python -m src daemon --account-id master_b

# Setup persona profile (pinned tweet)
uv run python scripts/setup_profiles.py --account master_b

# Pipeline status
uv run python -m src status
```

## Testing

```bash
# All 367 tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ --cov=src --cov-report=term-missing

# Linting
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

## Environment

Copy `.env.example` to `.env` and fill in credentials:

| Variable | Description |
|----------|-------------|
| `MASTER_A-E_USERNAME/PASSWORD` | 5 persona account credentials |
| `DATABASE_URL` | PostgreSQL connection string |

| `GEMINI_API_KEY` | Gemini API key (only for SDK provider, CLI needs no key) |

## Content Generation Pipeline

Two-phase content generation for reply, DM, and posting:

1. **Expert phase**: Korean derm expert prompt generates factually accurate base content
   - Uses treatment data (679 procedures, pricing, clinic info)
   - Output: accurate Japanese content with specific data points
2. **Persona phase**: Codex CLI (fallback: Gemini) adapts base content to persona voice
   - Applies persona's sentence endings, vocabulary, tone
   - Enforces banned words/phrases per persona
   - Preserves all factual data from expert phase

Casual daily posts skip the expert phase (not dermatology-related).

## Key Design Decisions

- **No burner/master split**: Each persona account (master_a~e) handles all stages (search + collect + analyze + reply + DM + posting)
- **LLM**: Codex CLI (gpt-5.1-codex-mini) as default, Gemini CLI (gemini-3-flash-preview) as fallback
- **Collection**: No follower count limit, no clinic marketing filter (collect all relevant tweets)
- **Browser sessions**: Per-persona persistent sessions at `data/sessions/{account_id}/`

## Key Paths

- `PROJECT_ROOT` is defined in `src/config.py` as `Path(__file__).resolve().parent.parent`
- Data files are at `PROJECT_ROOT / "data" / ...`
- Persona files are at `PROJECT_ROOT / "personas" / ...`
- Shared library is at `packages/_shared/` (editable install via pyproject.toml)

## Conventions

- Python 3.13+, ruff formatting, asyncio patterns
- `from src.` imports for app code
- `from outreach_shared.` imports for shared library
- All code comments in English
- Persona content output in Japanese
- X posting uses cookie injection + Playwright (NOT X API)
- Draft.js text input: use `execCommand('insertText')` + Enter key for newlines

## Agent Definitions

- `.claude/agents/x-outreach-agent.md` - Browser automation agent for search/reply/DM
- `.claude/agents/korean-derm-expert/` - Korean dermatology expert (treatment info, post generation, persona-aware content)
