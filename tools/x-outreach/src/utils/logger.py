"""Structured logging setup using structlog.

Provides JSON-formatted output to both console and a rotating log file.
Every log entry includes timestamp, level, module, and action fields.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import structlog


def setup_logging(
    *,
    level: str = "INFO",
    log_dir: str = "logs",
    log_file: str = "x-outreach.log",
    max_bytes: int = 10_485_760,
    backup_count: int = 5,
    project_root: Path | None = None,
) -> structlog.stdlib.BoundLogger:
    """Configure structlog with JSON output to console and file.

    Parameters
    ----------
    level:
        Python log level name (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    log_dir:
        Directory for log files, relative to *project_root*.
    log_file:
        Name of the rotating log file.
    max_bytes:
        Maximum size of a single log file before rotation.
    backup_count:
        Number of rotated backup files to keep.
    project_root:
        Base path for resolving *log_dir*.  Defaults to two levels up
        from this file (i.e. the ``tools/x-outreach/`` directory).

    Returns
    -------
    structlog.stdlib.BoundLogger
        A configured logger instance.
    """
    if project_root is None:
        project_root = Path(__file__).resolve().parent.parent.parent

    log_path = project_root / log_dir
    log_path.mkdir(parents=True, exist_ok=True)
    full_log_path = log_path / log_file

    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # --- Standard-library root logger ---
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove pre-existing handlers to avoid duplicates on re-init
    root_logger.handlers.clear()

    # Console handler (human-readable)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    root_logger.addHandler(console_handler)

    # Rotating file handler (JSON)
    file_handler = RotatingFileHandler(
        str(full_log_path),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(numeric_level)
    root_logger.addHandler(file_handler)

    # --- structlog configuration ---
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


def get_logger(module: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a bound logger, optionally pre-bound to a *module* name."""
    logger: structlog.stdlib.BoundLogger = structlog.get_logger()
    if module:
        logger = logger.bind(module=module)
    return logger
