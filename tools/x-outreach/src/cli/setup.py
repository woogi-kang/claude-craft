"""First-time setup verification for the X Outreach pipeline.

Checks that all prerequisites are met before running the pipeline:
Python version, environment file, Playwright browsers, configuration
file, and database writability.
"""

from __future__ import annotations

import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

from src.config import PROJECT_ROOT


class SetupCheck:
    """Result of a single setup verification check.

    Parameters
    ----------
    name:
        Short name of the check.
    passed:
        Whether the check passed.
    message:
        Human-readable description of the result.
    """

    def __init__(self, name: str, passed: bool, message: str) -> None:
        self.name = name
        self.passed = passed
        self.message = message

    @property
    def status_icon(self) -> str:
        """Return a text indicator for pass/fail."""
        return "PASS" if self.passed else "FAIL"


def check_python_version(min_version: tuple[int, int] = (3, 13)) -> SetupCheck:
    """Verify that the Python version meets the minimum requirement.

    Parameters
    ----------
    min_version:
        Minimum ``(major, minor)`` version tuple.
    """
    current = sys.version_info[:2]
    passed = current >= min_version
    version_str = f"{current[0]}.{current[1]}"
    required_str = f"{min_version[0]}.{min_version[1]}"
    if passed:
        return SetupCheck(
            "python_version",
            True,
            f"Python {version_str} >= {required_str}",
        )
    return SetupCheck(
        "python_version",
        False,
        f"Python {version_str} < {required_str} (upgrade required)",
    )


def check_env_file(project_root: Path | None = None) -> SetupCheck:
    """Verify that the ``.env`` file exists and contains required keys.

    Required keys: ``ANTHROPIC_API_KEY``, ``BURNER_X_USERNAME``,
    ``BURNER_X_PASSWORD``.
    """
    root = project_root or PROJECT_ROOT
    env_path = root / ".env"

    if not env_path.exists():
        return SetupCheck(
            "env_file",
            False,
            f".env file not found at {env_path}",
        )

    content = env_path.read_text(encoding="utf-8")
    required_keys = [
        "ANTHROPIC_API_KEY",
        "BURNER_X_USERNAME",
        "BURNER_X_PASSWORD",
    ]
    missing = [k for k in required_keys if k not in content]

    if missing:
        return SetupCheck(
            "env_file",
            False,
            f".env missing keys: {', '.join(missing)}",
        )
    return SetupCheck("env_file", True, ".env file present with required keys")


def check_playwright_browsers() -> SetupCheck:
    """Verify that Playwright Chromium browser is installed."""
    # Playwright stores browsers in a known location.
    # The simplest check is whether the playwright CLI is available.
    playwright_bin = shutil.which("playwright")
    if playwright_bin is None:
        # Check via python module
        try:
            from playwright.sync_api import sync_playwright  # noqa: F401

            return SetupCheck(
                "playwright",
                True,
                "Playwright module available (run 'playwright install chromium' if browsers missing)",
            )
        except ImportError:
            return SetupCheck(
                "playwright",
                False,
                "Playwright not installed (run 'uv pip install playwright')",
            )

    return SetupCheck("playwright", True, "Playwright CLI found")


def check_config_yaml(project_root: Path | None = None) -> SetupCheck:
    """Verify that ``config.yaml`` exists and is valid YAML."""
    root = project_root or PROJECT_ROOT
    config_path = root / "config.yaml"

    if not config_path.exists():
        return SetupCheck(
            "config_yaml",
            False,
            f"config.yaml not found at {config_path}",
        )

    try:
        import yaml

        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            return SetupCheck(
                "config_yaml",
                False,
                "config.yaml does not contain a valid YAML mapping",
            )
        return SetupCheck("config_yaml", True, "config.yaml valid")
    except Exception as exc:
        return SetupCheck(
            "config_yaml",
            False,
            f"config.yaml parse error: {exc}",
        )


def check_database_writable(project_root: Path | None = None) -> SetupCheck:
    """Verify that the SQLite database directory is writable."""
    root = project_root or PROJECT_ROOT
    db_dir = root / "data"
    db_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Test by creating a temporary file in the data directory
        test_path = db_dir / ".write_test"
        test_path.write_text("test", encoding="utf-8")
        test_path.unlink()

        # Also verify SQLite can open a temp database there
        test_db = db_dir / ".test.db"
        conn = sqlite3.connect(str(test_db))
        conn.execute("CREATE TABLE IF NOT EXISTS _test (id INTEGER)")
        conn.close()
        test_db.unlink(missing_ok=True)

        return SetupCheck("database", True, f"Database directory writable: {db_dir}")
    except (OSError, sqlite3.Error) as exc:
        return SetupCheck(
            "database",
            False,
            f"Database directory not writable: {exc}",
        )


def run_all_checks(project_root: Path | None = None) -> list[SetupCheck]:
    """Execute all setup checks and return results.

    Parameters
    ----------
    project_root:
        Override the project root path for testing.
    """
    return [
        check_python_version(),
        check_env_file(project_root),
        check_playwright_browsers(),
        check_config_yaml(project_root),
        check_database_writable(project_root),
    ]


def format_setup_output(checks: list[SetupCheck]) -> str:
    """Format setup check results for terminal display.

    Parameters
    ----------
    checks:
        List of completed setup checks.

    Returns
    -------
    str
        Multi-line formatted report.
    """
    lines: list[str] = []
    lines.append("=" * 50)
    lines.append("  X Outreach Setup Verification")
    lines.append("=" * 50)
    lines.append("")

    all_passed = True
    for check in checks:
        status = f"[{check.status_icon}]"
        lines.append(f"  {status:8s} {check.message}")
        if not check.passed:
            all_passed = False

    lines.append("")

    if all_passed:
        lines.append("  All checks passed. Ready to run.")
    else:
        failed = sum(1 for c in checks if not c.passed)
        lines.append(f"  {failed} check(s) failed. Fix issues above before running.")

    lines.append("=" * 50)
    return "\n".join(lines)


def run_setup(project_root: Path | None = None) -> tuple[str, bool]:
    """Execute setup verification and return formatted output.

    Returns
    -------
    tuple[str, bool]
        The formatted output and whether all checks passed.
    """
    checks = run_all_checks(project_root)
    output = format_setup_output(checks)
    all_passed = all(c.passed for c in checks)
    return output, all_passed
