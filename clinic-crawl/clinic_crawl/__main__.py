"""CLI entry point for clinic-crawl pipeline."""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="clinic-crawl",
        description="Korean skin clinic website crawler pipeline",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("triage", help="Classify URLs from CSV input")
    sub.add_parser("prescan", help="Fast HTTP scan for social links")
    sub.add_parser("resolve", help="Follow redirects and detect dead links")
    sub.add_parser("validate", help="Validate and deduplicate crawl results")
    sub.add_parser("report", help="Generate coverage report")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "triage":
        from clinic_crawl.scripts.triage import main as run
    elif args.command == "prescan":
        from clinic_crawl.scripts.prescan import main as run
    elif args.command == "resolve":
        from clinic_crawl.scripts.resolve_redirects import main as run
    elif args.command == "validate":
        from clinic_crawl.scripts.validate import main as run
    elif args.command == "report":
        from clinic_crawl.scripts.report import main as run
    else:
        parser.print_help()
        sys.exit(1)

    asyncio.run(run())


if __name__ == "__main__":
    main()
