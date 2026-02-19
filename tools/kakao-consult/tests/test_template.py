"""Tests for the TemplateEngine."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.knowledge.templates import Template, TemplateEngine


@pytest.fixture
def templates_dir() -> Path:
    """Return the project templates directory."""
    return Path(__file__).resolve().parent.parent / "templates"


@pytest.fixture
def engine(templates_dir: Path) -> TemplateEngine:
    """Provide a loaded TemplateEngine instance."""
    eng = TemplateEngine(templates_dir)
    eng.load()
    return eng


# -- Loading ------------------------------------------------------------------


class TestLoadTemplates:
    """Verify template loading from YAML files."""

    def test_load_returns_correct_count(self, templates_dir: Path) -> None:
        eng = TemplateEngine(templates_dir)
        total = eng.load()
        # FAQ: pricing(2) + hours(1) + location(1) + reservation(2) + aftercare(1) = 7
        # Greetings: hello(2) + thanks(1) + goodbye(1) + off_topic(1) = 5
        assert total == 12

    def test_faq_categories_loaded(self, engine: TemplateEngine) -> None:
        cats = engine.faq_categories
        assert "pricing" in cats
        assert "hours" in cats
        assert "location" in cats
        assert "reservation" in cats
        assert "aftercare" in cats

    def test_greeting_categories_loaded(self, engine: TemplateEngine) -> None:
        cats = engine.greeting_categories
        assert "hello" in cats
        assert "thanks" in cats
        assert "goodbye" in cats
        assert "off_topic" in cats

    def test_load_empty_dir(self, tmp_path: Path) -> None:
        eng = TemplateEngine(tmp_path)
        total = eng.load()
        assert total == 0


# -- FAQ responses ------------------------------------------------------------


class TestGetFAQResponse:
    """Verify FAQ response retrieval."""

    def test_returns_template_for_valid_category(self, engine: TemplateEngine) -> None:
        result = engine.get_faq_response("pricing")
        assert result is not None
        assert isinstance(result, Template)
        assert result.category == "pricing"
        assert result.id.startswith("pricing_")
        assert len(result.text) > 0

    def test_returns_none_for_unknown_category(self, engine: TemplateEngine) -> None:
        result = engine.get_faq_response("nonexistent_category")
        assert result is None

    def test_hours_response(self, engine: TemplateEngine) -> None:
        result = engine.get_faq_response("hours")
        assert result is not None
        assert result.id == "hours_01"

    def test_location_response(self, engine: TemplateEngine) -> None:
        result = engine.get_faq_response("location")
        assert result is not None
        assert result.id == "location_01"


# -- Rotation -----------------------------------------------------------------


class TestRotation:
    """Verify that repeated calls rotate through available templates."""

    def test_rotation_returns_different_templates(self, engine: TemplateEngine) -> None:
        # pricing has 2 templates; calling twice should return both
        first = engine.get_faq_response("pricing")
        second = engine.get_faq_response("pricing")
        assert first is not None
        assert second is not None
        assert first.id != second.id

    def test_rotation_wraps_around(self, engine: TemplateEngine) -> None:
        # After exhausting all templates, rotation wraps to least-used
        first = engine.get_faq_response("pricing")
        second = engine.get_faq_response("pricing")
        third = engine.get_faq_response("pricing")
        assert first is not None
        assert third is not None
        # Third call returns the first template again (both at count 1 vs 2)
        assert third.id == first.id

    def test_single_template_always_returns_same(self, engine: TemplateEngine) -> None:
        # hours has only 1 template
        first = engine.get_faq_response("hours")
        second = engine.get_faq_response("hours")
        assert first is not None
        assert second is not None
        assert first.id == second.id


# -- Greeting responses -------------------------------------------------------


class TestGetGreetingResponse:
    """Verify greeting response retrieval."""

    def test_hello_response(self, engine: TemplateEngine) -> None:
        result = engine.get_greeting_response("hello")
        assert result is not None
        assert isinstance(result, Template)
        assert result.category == "hello"

    def test_thanks_response(self, engine: TemplateEngine) -> None:
        result = engine.get_greeting_response("thanks")
        assert result is not None
        assert result.id == "thanks_01"

    def test_goodbye_response(self, engine: TemplateEngine) -> None:
        result = engine.get_greeting_response("goodbye")
        assert result is not None
        assert result.id == "bye_01"

    def test_unknown_greeting_returns_none(self, engine: TemplateEngine) -> None:
        result = engine.get_greeting_response("unknown")
        assert result is None


# -- Redirect response --------------------------------------------------------


class TestGetRedirectResponse:
    """Verify off-topic redirect response."""

    def test_redirect_response(self, engine: TemplateEngine) -> None:
        result = engine.get_redirect_response()
        assert result is not None
        assert result.id == "redirect_01"
        assert "시술이나 예약" in result.text
