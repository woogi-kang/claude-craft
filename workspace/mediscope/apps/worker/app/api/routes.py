"""API routes: health check and scan endpoint."""

import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException
from pydantic import BaseModel, HttpUrl

from ..config import settings
from ..db.supabase import save_scan_result, update_audit_status
from ..security.rate_limit import RateLimiter
from ..security.ssrf import SSRFError, validate_url
from ..services.scanner import run_scan

router = APIRouter()
rate_limiter = RateLimiter(max_requests=settings.rate_limit_rpm, window_seconds=60)


# --- Auth ---

async def verify_bearer(authorization: Annotated[str | None, Header()] = None) -> str:
    if not settings.worker_api_key:
        return "anonymous"  # No auth configured
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Bearer token")
    token = authorization.removeprefix("Bearer ")
    if token != settings.worker_api_key:
        raise HTTPException(status_code=401, detail="Invalid Bearer token")
    return token


# --- Health ---

@router.get("/health")
async def health():
    return {"status": "ok", "service": "mediscope-worker"}


# --- Scan ---

class ScanRequest(BaseModel):
    audit_id: str | None = None
    url: HttpUrl
    options: dict | None = None


class ScanResponse(BaseModel):
    task_id: str
    status: str


async def _run_scan_task(task_id: str, url: str, audit_id: str | None, options: dict):
    """Background task: run scan and save results."""
    max_pages = options.get("max_pages", 50)
    max_depth = options.get("depth", 3)

    try:
        if audit_id:
            await update_audit_status(audit_id, "scanning")

        result = await run_scan(url, max_pages=max_pages, max_depth=max_depth)
        result["task_id"] = task_id

        if audit_id:
            await save_scan_result(audit_id, result)
            await update_audit_status(audit_id, "completed")
    except Exception:
        if audit_id:
            await update_audit_status(audit_id, "failed")


@router.post("/scan", response_model=ScanResponse, status_code=202)
async def scan(
    body: ScanRequest,
    background_tasks: BackgroundTasks,
    _token: str = Depends(verify_bearer),
):
    url_str = str(body.url)

    # Rate limit by URL domain
    from urllib.parse import urlparse

    domain = urlparse(url_str).netloc
    if not rate_limiter.is_allowed(domain):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # SSRF validation
    try:
        validate_url(url_str)
    except SSRFError as e:
        raise HTTPException(status_code=400, detail=f"URL blocked: {e}")

    task_id = str(uuid.uuid4())
    options = body.options or {}

    background_tasks.add_task(_run_scan_task, task_id, url_str, body.audit_id, options)

    return ScanResponse(task_id=task_id, status="queued")
