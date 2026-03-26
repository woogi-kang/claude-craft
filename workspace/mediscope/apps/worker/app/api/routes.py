"""API routes: health check and scan endpoint."""

import uuid
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException
from pydantic import BaseModel, HttpUrl

from ..config import settings
from ..db.supabase import get_supabase_client, save_scan_result, update_audit_status
from ..security.rate_limit import RateLimiter
from ..security.ssrf import SSRFError, validate_url
from ..services.pdf_generator import generate_pdf
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
    import logging
    logger = logging.getLogger("mediscope.scan")

    max_pages = options.get("max_pages", 50)
    max_depth = options.get("depth", 3)

    try:
        if audit_id:
            await update_audit_status(audit_id, "scanning")

        logger.info(f"Scan started: {url} (audit_id={audit_id})")
        result = await run_scan(url, max_pages=max_pages, max_depth=max_depth)
        result["task_id"] = task_id
        logger.info(f"Scan completed: {url} score={result.get('total_score')}")

        if audit_id:
            await save_scan_result(audit_id, result)

            # Generate PDF report in background
            try:
                audit_data = {
                    "url": url,
                    "total_score": result.get("total_score", 0),
                    "grade": result.get("grade", "F"),
                    "category_scores": result.get("category_scores", {}),
                }
                pdf_url = await generate_pdf(audit_id, audit_data)
                logger.info(f"PDF generated for audit_id={audit_id}: {pdf_url}")
            except Exception as pdf_err:
                logger.warning(f"PDF generation failed for audit_id={audit_id}: {pdf_err}")
    except Exception as e:
        logger.exception(f"Scan failed: {url} error={e}")
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


# --- Generate PDF ---

class GeneratePdfRequest(BaseModel):
    audit_id: str


class GeneratePdfResponse(BaseModel):
    pdf_url: str
    size_bytes: int


@router.post("/generate-pdf", response_model=GeneratePdfResponse)
async def generate_pdf_endpoint(
    body: GeneratePdfRequest,
    _token: str = Depends(verify_bearer),
):
    """Generate a PDF report for a completed audit."""
    import logging

    logger = logging.getLogger("mediscope.pdf")

    client = get_supabase_client()
    if client is None:
        raise HTTPException(status_code=500, detail="Supabase not configured")

    # Fetch audit data
    result = (
        client.table("audits")
        .select("url, total_score, grade, scores")
        .eq("id", body.audit_id)
        .single()
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Audit not found")

    audit = result.data
    audit_data = {
        "url": audit["url"],
        "total_score": audit.get("total_score", 0),
        "grade": audit.get("grade", "F"),
        "category_scores": audit.get("scores", {}),
    }

    try:
        pdf_url = await generate_pdf(body.audit_id, audit_data)
    except Exception as e:
        logger.exception(f"PDF generation failed: {e}")
        raise HTTPException(status_code=500, detail="PDF generation failed")

    # Estimate size (re-fetch from storage is overkill; use a rough estimate)
    # For a proper size, we'd need to check storage metadata
    return GeneratePdfResponse(pdf_url=pdf_url, size_bytes=0)
