# MoAI Memory

## Clinic Crawler Agent
- Refactored from single file to directory structure with references/ (2026-02-09)
- clinic-crawl/ Python codebase removed - agent is fully self-contained
- Uses Playwright MCP only (single browser instance - NO parallel crawling)
- Gemini CLI 0.27.3 for OCR on image-based doctor pages
- Storage: `scripts/clinic-storage/storage_manager.py` (stdlib only, SQLite + CSV)
- CSV dataset preserved at `data/clinic-results/skin_clinics.csv`

## Key Lessons
- Playwright MCP shares single browser instance - parallel agent crawls cause page interference
- Always run clinic crawls sequentially (one hospital at a time)
- Image-based clinic sites need OCR fallback (Gemini CLI) for doctor info extraction
- Korean clinic popups often require checkbox-first-then-close pattern
