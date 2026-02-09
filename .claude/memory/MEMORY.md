# MoAI Memory

## Clinic Crawler Agent
- Refactored from single file to directory structure with references/ (2026-02-09)
- clinic-crawl/ Python codebase removed - agent is fully self-contained
- Uses Playwright MCP only (single browser instance - NO parallel crawling)
- Gemini CLI 0.27.3 for OCR on image-based doctor pages
- Storage: `scripts/clinic-storage/storage_manager.py` (stdlib only, SQLite + CSV)
- CSV dataset preserved at `data/clinic-results/skin_clinics.csv`

## Gemini CLI OCR Critical Notes
- **NEVER use stdin** (`< image.png`) - causes heap out of memory crash
- **ALWAYS convert PNG to JPEG first** (`sips -s format jpeg -s formatOptions 85`)
- Correct invocation: `gemini -p "Read the image file at <path>..." -y 2>&1 | grep -A 200 '```'`
- `-y` flag (YOLO mode) needed to auto-approve read_file tool for image access
- Target JPEG under 500KB; resize to 1024px width if needed
- PNG files crash even with NODE_OPTIONS="--max-old-space-size=8192"
- Small files (<50KB) may work via stdin but JPEG path method is always safer

## Key Lessons
- Playwright MCP shares single browser instance - parallel agent crawls cause page interference
- Always run clinic crawls sequentially (one hospital at a time)
- Image-based clinic sites need OCR fallback (Gemini CLI) for doctor info extraction
- Korean clinic popups often require checkbox-first-then-close pattern
- When delegating to subagents, NEVER say "note that OCR is needed" - instruct them to EXECUTE OCR
