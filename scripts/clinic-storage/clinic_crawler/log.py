"""Logging utility for the clinic crawler."""

import sys


def log(msg: str) -> None:
    """Log to stderr (stdout reserved for JSON output)."""
    print(f"[crawl] {msg}", file=sys.stderr, flush=True)
