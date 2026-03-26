"""Supabase client for Worker — uses service_role (secret) key."""

from supabase import create_client, Client

from ..config import settings

_client: Client | None = None


def get_supabase_client() -> Client | None:
    global _client
    if _client is not None:
        return _client

    if not settings.supabase_url or not settings.supabase_secret_key:
        return None

    _client = create_client(settings.supabase_url, settings.supabase_secret_key)
    return _client


async def save_scan_result(audit_id: str, result: dict) -> bool:
    """Save full scan result: update audits + insert audit_items."""
    client = get_supabase_client()
    if client is None:
        return False

    # Update audits table
    client.table("audits").update({
        "status": "completed",
        "total_score": result.get("total_score", 0),
        "grade": result.get("grade", "F"),
        "scores": result.get("category_scores", {}),
        "details": result.get("details", {}),
        "scan_duration_ms": result.get("scan_duration_ms"),
    }).eq("id", audit_id).execute()

    # Insert audit_items
    items = result.get("items", [])
    if items:
        rows = [
            {
                "audit_id": audit_id,
                "category": item["category"],
                "item_key": item["item_key"],
                "status": item["status"],
                "score": item.get("score"),
                "weight": item.get("weight"),
                "details": item.get("details"),
                "suggestion": item.get("suggestion"),
                "priority": item.get("priority"),
            }
            for item in items
        ]
        client.table("audit_items").insert(rows).execute()

    # Update hospital's latest score
    audit = client.table("audits").select("hospital_id").eq("id", audit_id).single().execute()
    if audit.data and audit.data.get("hospital_id"):
        client.table("hospitals").update({
            "latest_score": result.get("total_score", 0),
            "latest_audit_id": audit_id,
        }).eq("id", audit.data["hospital_id"]).execute()

    return True


async def update_audit_status(audit_id: str, status: str) -> bool:
    """Update audit status (pending/scanning/completed/failed)."""
    client = get_supabase_client()
    if client is None:
        return False

    client.table("audits").update({"status": status}).eq("id", audit_id).execute()
    return True
