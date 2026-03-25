"""Supabase client stub — requires Database worker to provide schema."""

from ..config import settings


def get_supabase_client():
    """Get Supabase client. Requires MEDISCOPE_SUPABASE_URL and MEDISCOPE_SUPABASE_SERVICE_KEY."""
    if not settings.supabase_url or not settings.supabase_service_key:
        return None

    from supabase import create_client

    return create_client(settings.supabase_url, settings.supabase_service_key)


async def save_scan_result(audit_id: str, result: dict) -> bool:
    """Save scan result to Supabase. Returns True on success."""
    client = get_supabase_client()
    if client is None:
        return False

    client.table("scan_results").upsert(
        {"audit_id": audit_id, "result": result}
    ).execute()
    return True


async def update_audit_status(audit_id: str, status: str) -> bool:
    """Update audit status in Supabase."""
    client = get_supabase_client()
    if client is None:
        return False

    client.table("audits").update({"status": status}).eq("id", audit_id).execute()
    return True
