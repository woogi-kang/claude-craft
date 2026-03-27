"""Subscription monitoring: periodic re-scans with score change alerts."""

import logging
from datetime import datetime, timedelta, timezone

import httpx

from ..config import settings
from ..db.supabase import get_supabase_client
from .scanner import run_scan

logger = logging.getLogger("mediscope.monitoring")

FREQUENCY_HOURS = {
    "daily": 24,
    "weekly": 168,
    "biweekly": 336,
    "monthly": 720,
}


async def create_subscription(
    hospital_id: str,
    email: str,
    name: str,
    frequency: str = "weekly",
) -> dict | None:
    client = get_supabase_client()
    if client is None:
        return None

    now = datetime.now(timezone.utc).isoformat()
    hours = FREQUENCY_HOURS.get(frequency, 168)
    next_scan_at = (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()

    row = {
        "hospital_id": hospital_id,
        "email": email,
        "name": name,
        "frequency": frequency,
        "status": "active",
        "next_scan_at": next_scan_at,
        "created_at": now,
    }
    result = client.table("subscriptions").insert(row).execute()
    return result.data[0] if result.data else None


async def get_due_subscriptions() -> list[dict]:
    client = get_supabase_client()
    if client is None:
        return []

    now = datetime.now(timezone.utc).isoformat()
    result = (
        client.table("subscriptions")
        .select("*, hospitals(url)")
        .eq("status", "active")
        .lt("next_scan_at", now)
        .execute()
    )
    return result.data or []


async def record_score_history(
    hospital_id: str,
    audit_id: str | None,
    total_score: float,
    grade: str,
    category_scores: dict,
) -> dict | None:
    client = get_supabase_client()
    if client is None:
        return None

    row = {
        "hospital_id": hospital_id,
        "audit_id": audit_id,
        "total_score": int(round(total_score)) if total_score is not None else 0,
        "grade": grade,
        "category_scores": category_scores,
        "scanned_at": datetime.now(timezone.utc).isoformat(),
    }
    result = client.table("score_history").insert(row).execute()
    return result.data[0] if result.data else None


async def create_alert(
    subscription_id: str,
    hospital_id: str,
    alert_type: str,
    message: str,
    prev_score: float | None,
    new_score: float,
) -> dict | None:
    client = get_supabase_client()
    if client is None:
        return None

    row = {
        "subscription_id": subscription_id,
        "hospital_id": hospital_id,
        "type": alert_type,
        "message": message,
        "prev_score": int(round(prev_score)) if prev_score is not None else None,
        "new_score": int(round(new_score)),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = client.table("alerts").insert(row).execute()
    return result.data[0] if result.data else None


async def send_alert_email(
    email: str,
    hospital_name: str,
    prev_score: int,
    new_score: int,
) -> bool:
    """Send score change alert email via Resend API."""
    if not settings.resend_api_key:
        logger.debug("resend_api_key not configured, skipping email")
        return False

    diff = new_score - prev_score
    direction = "상승" if diff > 0 else "하락"
    color = "#22c55e" if diff > 0 else "#ef4444"

    html_body = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
      <h2 style="color: #1e293b;">CheckYourHospital 점수 변동 알림</h2>
      <p><strong>{hospital_name}</strong>의 SEO 점수가 변동되었습니다.</p>
      <div style="background: #f8fafc; border-radius: 8px; padding: 20px; margin: 16px 0;">
        <p style="font-size: 18px; margin: 0;">
          <span>{prev_score}점</span>
          <span style="color: {color}; font-weight: bold;"> → {new_score}점</span>
          <span style="color: {color};"> ({abs(diff)}점 {direction})</span>
        </p>
      </div>
      <p style="color: #64748b; font-size: 14px;">CheckYourHospital에서 발송된 자동 알림입니다.</p>
    </div>
    """

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {settings.resend_api_key}"},
                json={
                    "from": "CheckYourHospital <noreply@checkyourhospital.com>",
                    "to": email,
                    "subject": f"[CheckYourHospital] {hospital_name} 점수 변동 알림",
                    "html": html_body,
                },
            )
            if resp.status_code >= 400:
                logger.warning(f"Resend API error {resp.status_code}: {resp.text}")
                return False
            return True
    except httpx.HTTPError as exc:
        logger.warning(f"Failed to send alert email: {exc}")
        return False


async def process_subscription(subscription: dict) -> dict:
    hospital_id = subscription["hospital_id"]
    subscription_id = subscription["id"]
    hospital_url = subscription.get("hospitals", {}).get("url", "")

    if not hospital_url:
        logger.warning(f"No URL for hospital {hospital_id}, skipping")
        return {"status": "skipped", "reason": "no_url"}

    client = get_supabase_client()

    # Get previous score
    prev_record = (
        client.table("score_history")
        .select("total_score")
        .eq("hospital_id", hospital_id)
        .order("scanned_at", desc=True)
        .limit(1)
        .execute()
    )
    prev_score = prev_record.data[0]["total_score"] if prev_record.data else None

    # Run scan
    result = await run_scan(hospital_url)
    new_score = result.get("total_score", 0)
    grade = result.get("grade", "F")
    category_scores = result.get("category_scores", {})

    # Record history
    await record_score_history(hospital_id, None, new_score, grade, category_scores)

    # Create alert on score change
    if prev_score is not None and prev_score != new_score:
        diff = new_score - prev_score
        direction = "상승" if diff > 0 else "하락"
        alert_type = "score_improved" if diff > 0 else "score_dropped"
        message = f"SEO 점수가 {prev_score}점에서 {new_score}점으로 {abs(diff)}점 {direction}했습니다."
        await create_alert(
            subscription_id, hospital_id, alert_type, message, prev_score, new_score
        )

        # Send alert email
        hospital_name = subscription.get("name", "병원")
        await send_alert_email(
            email=subscription["email"],
            hospital_name=hospital_name,
            prev_score=int(round(prev_score)),
            new_score=int(round(new_score)),
        )

    # Update next_scan_at
    frequency = subscription.get("frequency", "weekly")
    hours = FREQUENCY_HOURS.get(frequency, 168)
    next_scan_at = (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()
    client.table("subscriptions").update(
        {"next_scan_at": next_scan_at}
    ).eq("id", subscription_id).execute()

    logger.info(
        f"Subscription {subscription_id} processed: "
        f"prev={prev_score} new={new_score}"
    )
    return {
        "status": "completed",
        "hospital_id": hospital_id,
        "prev_score": prev_score,
        "new_score": new_score,
        "grade": grade,
    }
