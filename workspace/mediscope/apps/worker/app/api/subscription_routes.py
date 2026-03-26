"""Subscription monitoring API routes."""

import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from ..services.monitoring import (
    create_subscription,
    get_due_subscriptions,
    process_subscription,
)
from .routes import verify_bearer

router = APIRouter(tags=["subscriptions"])
logger = logging.getLogger("mediscope.subscriptions")


class CreateSubscriptionRequest(BaseModel):
    hospital_id: str
    email: str
    name: str
    frequency: str = "weekly"


class SubscriptionResponse(BaseModel):
    id: str
    hospital_id: str
    email: str
    name: str
    frequency: str
    status: str
    next_scan_at: str


class ProcessDueResponse(BaseModel):
    processed: int
    results: list[dict]


@router.post("/subscriptions", response_model=SubscriptionResponse, status_code=201)
async def create_sub(
    body: CreateSubscriptionRequest,
    _token: str = Depends(verify_bearer),
):
    if body.frequency not in ("daily", "weekly", "biweekly", "monthly"):
        raise HTTPException(
            status_code=400,
            detail="frequency must be daily, weekly, biweekly, or monthly",
        )

    result = await create_subscription(
        hospital_id=body.hospital_id,
        email=body.email,
        name=body.name,
        frequency=body.frequency,
    )
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to create subscription")
    return result


@router.get("/subscriptions", response_model=list[SubscriptionResponse])
async def list_subscriptions(
    email: str = Query(..., description="Filter by subscriber email"),
    _token: str = Depends(verify_bearer),
):
    from ..db.supabase import get_supabase_client

    client = get_supabase_client()
    if client is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    result = client.table("subscriptions").select("*").eq("email", email).execute()
    return result.data or []


@router.delete("/subscriptions/{subscription_id}", status_code=204)
async def delete_subscription(
    subscription_id: str,
    _token: str = Depends(verify_bearer),
):
    from ..db.supabase import get_supabase_client

    client = get_supabase_client()
    if client is None:
        raise HTTPException(status_code=500, detail="Database not configured")

    client.table("subscriptions").update(
        {"status": "cancelled"}
    ).eq("id", subscription_id).execute()


@router.post("/subscriptions/process-due", response_model=ProcessDueResponse)
async def process_due_subscriptions(
    _token: str = Depends(verify_bearer),
):
    due = await get_due_subscriptions()
    if not due:
        return ProcessDueResponse(processed=0, results=[])

    results = []
    for sub in due:
        try:
            result = await process_subscription(sub)
            results.append(result)
        except Exception as e:
            logger.exception(f"Failed to process subscription {sub.get('id')}: {e}")
            results.append({"status": "failed", "error": str(e)[:200]})

    return ProcessDueResponse(processed=len(results), results=results)
