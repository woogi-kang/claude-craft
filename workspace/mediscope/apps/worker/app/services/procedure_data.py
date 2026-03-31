"""Procedure data access layer — fetches dermatology procedure info from Supabase."""

from __future__ import annotations

from dataclasses import dataclass, field

from ..db.supabase import get_supabase_client


@dataclass
class ProcedureData:
    """Structured procedure data from DB."""

    name: str
    name_en: str = ""
    category: str = ""
    principle: str = ""
    mechanism_detail: str = ""
    method: str = ""
    duration: str = ""
    side_effects: str = ""
    pain_level: str = ""
    pain_description: str = ""
    downtime: str = ""
    post_care: str = ""
    average_price: str = ""
    target: str = ""
    effect: str = ""
    advantage: str = ""
    not_recommended: str = ""
    summary: str = ""
    price_by_country: dict[str, dict] = field(default_factory=dict)
    translations: dict[str, dict] = field(default_factory=dict)


async def get_procedure_data(procedure_name: str) -> ProcedureData | None:
    """Fetch procedure data from Supabase by name.

    Joins procedures → procedure_details → procedure_intl → intl_prices.
    """
    client = get_supabase_client()
    if client is None:
        return None

    # Find procedure by name (case-insensitive search)
    result = (
        client.table("procedures")
        .select("id, name, primary_category_id")
        .ilike("name", f"%{procedure_name}%")
        .limit(1)
        .execute()
    )

    if not result.data:
        # Try search_dict for alias matching
        alias_result = (
            client.table("search_dict")
            .select("procedure_id, canonical_term")
            .ilike("term", f"%{procedure_name}%")
            .limit(1)
            .execute()
        )
        if not alias_result.data:
            return None
        proc_id = alias_result.data[0].get("procedure_id")
        if not proc_id:
            return None
        result = (
            client.table("procedures")
            .select("id, name, primary_category_id")
            .eq("id", proc_id)
            .limit(1)
            .execute()
        )
        if not result.data:
            return None

    proc = result.data[0]
    proc_id = proc["id"]

    # Fetch category name
    category_name = ""
    if proc.get("primary_category_id"):
        cat_result = (
            client.table("procedure_categories")
            .select("name")
            .eq("id", proc["primary_category_id"])
            .limit(1)
            .execute()
        )
        if cat_result.data:
            category_name = cat_result.data[0].get("name", "")

    # Fetch procedure details
    detail_result = (
        client.table("procedure_details")
        .select("*")
        .eq("procedure_id", proc_id)
        .limit(1)
        .execute()
    )
    detail = detail_result.data[0] if detail_result.data else {}

    # Fetch translations
    intl_result = (
        client.table("procedure_intl")
        .select("*")
        .eq("procedure_id", proc_id)
        .execute()
    )
    translations: dict[str, dict] = {}
    for row in intl_result.data or []:
        lang = row.get("language_code", "")
        if lang:
            translations[lang] = row

    # Fetch international prices
    price_result = (
        client.table("intl_prices")
        .select("country_code, currency, price, price_unit")
        .eq("top_procedure_id", proc_id)
        .execute()
    )
    price_by_country: dict[str, dict] = {}
    for row in price_result.data or []:
        cc = row.get("country_code", "")
        if cc:
            price_by_country[cc] = {
                "currency": row.get("currency", ""),
                "price": row.get("price", 0),
                "price_unit": row.get("price_unit", ""),
            }

    return ProcedureData(
        name=proc.get("name", procedure_name),
        name_en=detail.get("procedure_name", ""),
        category=category_name,
        principle=detail.get("principle", ""),
        mechanism_detail=detail.get("mechanism_detail", ""),
        method=detail.get("method", ""),
        duration=detail.get("duration", "") or detail.get("duration_of_procedure", ""),
        side_effects=detail.get("side_effects", ""),
        pain_level=str(detail.get("pain_level", "")),
        pain_description=detail.get("pain_description", ""),
        downtime=detail.get("downtime", ""),
        post_care=detail.get("post_care", ""),
        average_price=detail.get("average_price", ""),
        target=detail.get("target", ""),
        effect=detail.get("effect", ""),
        advantage=detail.get("advantage", ""),
        not_recommended=detail.get("not_recommended", ""),
        summary=detail.get("summary", ""),
        price_by_country=price_by_country,
        translations=translations,
    )


async def list_procedures() -> list[dict]:
    """List all procedures grouped by category."""
    client = get_supabase_client()
    if client is None:
        return []

    # Fetch categories
    cat_result = (
        client.table("procedure_categories")
        .select("id, name, name_en, icon, display_order")
        .order("display_order")
        .execute()
    )
    categories = {c["id"]: c for c in (cat_result.data or [])}

    # Fetch procedures
    proc_result = (
        client.table("procedures")
        .select("id, name, primary_category_id, grade, thumbnail_url")
        .order("name")
        .execute()
    )

    grouped: dict[str, dict] = {}
    for proc in proc_result.data or []:
        cat_id = proc.get("primary_category_id")
        cat = categories.get(cat_id, {})
        cat_name = cat.get("name", "기타")

        if cat_name not in grouped:
            grouped[cat_name] = {
                "category": cat_name,
                "category_en": cat.get("name_en", ""),
                "icon": cat.get("icon", ""),
                "procedures": [],
            }
        grouped[cat_name]["procedures"].append({
            "id": proc["id"],
            "name": proc["name"],
            "grade": proc.get("grade"),
        })

    return list(grouped.values())
