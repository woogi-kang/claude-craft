#!/usr/bin/env bash
# Setup script for x-outreach development environment.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== X Outreach Setup ==="
echo "Project: $PROJECT_DIR"

cd "$PROJECT_DIR"

# Create virtual environment if not present
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -e ".[dev]"

# Install Playwright browsers
echo "Installing Playwright browsers..."
python -m playwright install chromium

# Create .env from example if not present
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "IMPORTANT: Edit .env and add your API keys before running."
fi

# Initialize database
echo "Initializing database..."
python -c "
from src.db.repository import Repository
from src.config import load_settings
settings = load_settings()
repo = Repository(settings.database.path)
repo.init_db()
repo.close()
print(f'Database created at {settings.database.path}')
"

echo ""
echo "=== Setup complete ==="
echo "Activate venv:  source .venv/bin/activate"
echo "Run tests:      pytest"
echo "Run pipeline:   python -m src.main --dry-run"
