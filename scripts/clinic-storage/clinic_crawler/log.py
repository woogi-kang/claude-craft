"""Logging utility for the clinic crawler."""

import sys
from datetime import datetime


def log(msg: str) -> None:
    """Log to stderr (stdout reserved for JSON output)."""
    print(f"[crawl] {msg}", file=sys.stderr, flush=True)


def batch_log(msg: str) -> None:
    """Log with timestamp to stderr (for batch/cycle scripts)."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", file=sys.stderr, flush=True)
