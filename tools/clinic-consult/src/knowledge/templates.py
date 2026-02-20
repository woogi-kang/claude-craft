"""Template engine for FAQ and greeting responses.

Loads templates from YAML files and tracks usage to ensure response
variety through least-used rotation.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import yaml

from src.utils.logger import get_logger

logger = get_logger("templates")


@dataclass
class Template:
    """A single response template."""

    id: str
    text: str
    category: str


class TemplateEngine:
    """Load and serve templates with usage-based rotation.

    Parameters
    ----------
    templates_dir:
        Directory containing YAML template files.
    """

    def __init__(self, templates_dir: Path) -> None:
        self._dir = templates_dir
        self._faq: dict[str, list[Template]] = {}
        self._greetings: dict[str, list[Template]] = {}
        self._usage: Counter[str] = Counter()

    def load(self) -> int:
        """Load templates from YAML files. Returns total template count."""
        total = 0

        faq_path = self._dir / "faq_templates.yaml"
        if faq_path.exists():
            with open(faq_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            for cat_name, cat_data in data.get("categories", {}).items():
                templates = []
                for resp in cat_data.get("responses", []):
                    templates.append(
                        Template(id=resp["id"], text=resp["text"], category=cat_name)
                    )
                self._faq[cat_name] = templates
                total += len(templates)

        greeting_path = self._dir / "greeting_templates.yaml"
        if greeting_path.exists():
            with open(greeting_path, encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            for cat_name, cat_data in data.get("greetings", {}).items():
                templates = []
                for resp in cat_data.get("responses", []):
                    templates.append(
                        Template(id=resp["id"], text=resp["text"], category=cat_name)
                    )
                self._greetings[cat_name] = templates
                total += len(templates)

        logger.info(
            "templates_loaded",
            faq_categories=len(self._faq),
            greeting_categories=len(self._greetings),
            total=total,
        )
        return total

    def get_faq_response(self, category: str) -> Template | None:
        """Get least-used FAQ template for category."""
        return self._get_least_used(self._faq.get(category, []))

    def get_greeting_response(self, category: str) -> Template | None:
        """Get least-used greeting template for category."""
        return self._get_least_used(self._greetings.get(category, []))

    def get_redirect_response(self) -> Template | None:
        """Get off-topic redirect response."""
        return self._get_least_used(self._greetings.get("off_topic", []))

    def _get_least_used(self, templates: list[Template]) -> Template | None:
        if not templates:
            return None
        # Pick the template with lowest usage count
        least_used = min(templates, key=lambda t: self._usage[t.id])
        self._usage[least_used.id] += 1
        return least_used

    @property
    def faq_categories(self) -> list[str]:
        """Return list of loaded FAQ category names."""
        return list(self._faq.keys())

    @property
    def greeting_categories(self) -> list[str]:
        """Return list of loaded greeting category names."""
        return list(self._greetings.keys())
