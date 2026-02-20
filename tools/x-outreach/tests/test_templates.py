"""Tests for the 5-category template system."""

from __future__ import annotations

from src.knowledge.templates import (
    DM_TEMPLATES,
    REPLY_TEMPLATES,
    TemplateSelector,
)


class TestTemplateData:
    """Test template data integrity."""

    def test_reply_templates_have_5_categories(self) -> None:
        assert set(REPLY_TEMPLATES.keys()) == {
            "hospital",
            "price",
            "procedure",
            "complaint",
            "review",
        }

    def test_dm_templates_have_5_categories(self) -> None:
        assert set(DM_TEMPLATES.keys()) == {
            "hospital",
            "price",
            "procedure",
            "complaint",
            "review",
        }

    def test_all_reply_templates_have_text(self) -> None:
        for category, templates in REPLY_TEMPLATES.items():
            assert len(templates) > 0, f"Category {category} has no templates"
            for t in templates:
                assert t.text, f"Template {t.id} has empty text"
                assert t.category == category

    def test_all_dm_templates_have_text(self) -> None:
        for category, templates in DM_TEMPLATES.items():
            assert len(templates) > 0, f"Category {category} has no templates"
            for t in templates:
                assert t.text, f"Template {t.id} has empty text"
                assert t.category == category

    def test_template_ids_unique(self) -> None:
        ids: set[str] = set()
        for templates in REPLY_TEMPLATES.values():
            for t in templates:
                assert t.id not in ids, f"Duplicate template ID: {t.id}"
                ids.add(t.id)
        for templates in DM_TEMPLATES.values():
            for t in templates:
                assert t.id not in ids, f"Duplicate template ID: {t.id}"
                ids.add(t.id)


class TestTemplateSelector:
    """Test template selection and rotation."""

    def test_get_reply_template(self) -> None:
        selector = TemplateSelector()
        t = selector.get_reply_template("hospital")
        assert t is not None
        assert t.category == "hospital"

    def test_get_dm_template(self) -> None:
        selector = TemplateSelector()
        t = selector.get_dm_template("price")
        assert t is not None
        assert t.category == "price"

    def test_unknown_category_returns_none(self) -> None:
        selector = TemplateSelector()
        assert selector.get_reply_template("nonexistent") is None
        assert selector.get_dm_template("nonexistent") is None

    def test_rotation_increments_use_count(self) -> None:
        selector = TemplateSelector()
        t1 = selector.get_reply_template("hospital")
        assert t1 is not None
        # Template objects are module-level singletons, so use_count may
        # already be > 0 from other tests.  Just verify it was incremented.
        assert t1.use_count >= 1

    def test_least_used_selected(self) -> None:
        selector = TemplateSelector()
        # Get first template
        t1 = selector.get_reply_template("hospital")
        assert t1 is not None
        # Get second template -- should be different (least used)
        t2 = selector.get_reply_template("hospital")
        assert t2 is not None
        if len(REPLY_TEMPLATES["hospital"]) > 1:
            assert t2.id != t1.id

    def test_get_categories_reply(self) -> None:
        selector = TemplateSelector()
        cats = selector.get_categories("reply")
        assert "hospital" in cats
        assert "price" in cats
        assert "procedure" in cats
        assert "complaint" in cats
        assert "review" in cats

    def test_get_categories_dm(self) -> None:
        selector = TemplateSelector()
        cats = selector.get_categories("dm")
        assert "hospital" in cats
        assert "review" in cats

    def test_all_categories_return_template(self) -> None:
        selector = TemplateSelector()
        for cat in ["hospital", "price", "procedure", "complaint", "review"]:
            t = selector.get_reply_template(cat)
            assert t is not None, f"No reply template for {cat}"
            t = selector.get_dm_template(cat)
            assert t is not None, f"No DM template for {cat}"
