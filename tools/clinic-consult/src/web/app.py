"""FastAPI web application for reservation management.

Provides a dashboard for staff to create reservation requests,
monitor their status, and manage conversations with clinics.
"""

from __future__ import annotations

import json
import os
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED

from src.clinic.lookup import ClinicLookup
from src.reservation.exporter import ReservationExporter
from src.reservation.repository import VALID_TRANSITIONS, ReservationRepository

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
_HOSPITALS_DB = _PROJECT_ROOT.parent.parent / "data" / "clinic-results" / "hospitals.db"

app = FastAPI(title="Clinic Consult", docs_url="/api/docs")
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
_security = HTTPBasic()

# These are initialized in create_app()
_repo: ReservationRepository | None = None
_exporter: ReservationExporter | None = None
_clinic_lookup: ClinicLookup | None = None

# CSRF token store: session-scoped, keyed by username
_csrf_tokens: dict[str, str] = {}


def _get_auth_credentials() -> tuple[str, str]:
    """Read auth credentials from Settings (which loads .env automatically)."""
    from src.config import load_settings

    settings = load_settings()
    return settings.reserve_user, settings.reserve_pass


def verify_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(_security)],
) -> str:
    """Verify HTTP Basic Auth credentials. Returns the username."""
    expected_user, expected_pass = _get_auth_credentials()
    if not expected_pass:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="RESERVE_PASS environment variable not set",
            headers={"WWW-Authenticate": "Basic"},
        )
    user_ok = secrets.compare_digest(
        credentials.username.encode("utf-8"),
        expected_user.encode("utf-8"),
    )
    pass_ok = secrets.compare_digest(
        credentials.password.encode("utf-8"),
        expected_pass.encode("utf-8"),
    )
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def _generate_csrf_token(username: str) -> str:
    """Generate and store a CSRF token for the given user session."""
    token = secrets.token_hex(32)
    _csrf_tokens[username] = token
    return token


def _verify_csrf_token(username: str, token: str) -> None:
    """Verify the CSRF token matches. Raises 403 on mismatch."""
    expected = _csrf_tokens.get(username)
    if not expected or not secrets.compare_digest(token, expected):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")


def create_app(
    db_path: str | Path | None = None,
    export_dir: str | Path | None = None,
    hospitals_db: str | Path | None = None,
) -> FastAPI:
    """Initialize the app with database connections."""
    global _repo, _exporter, _clinic_lookup

    db = db_path or _PROJECT_ROOT / "data" / "consult.db"
    exports = export_dir or _PROJECT_ROOT / "data" / "exports"
    hdb = hospitals_db or _HOSPITALS_DB

    _repo = ReservationRepository(db)
    _repo.init_db()
    _exporter = ReservationExporter(exports)
    _clinic_lookup = ClinicLookup(hdb)

    return app


def _get_repo() -> ReservationRepository:
    if _repo is None:
        raise RuntimeError("App not initialized. Call create_app() first.")
    return _repo


def _get_exporter() -> ReservationExporter:
    if _exporter is None:
        raise RuntimeError("App not initialized. Call create_app() first.")
    return _exporter


def _get_lookup() -> ClinicLookup:
    if _clinic_lookup is None:
        raise RuntimeError("App not initialized. Call create_app() first.")
    return _clinic_lookup


# ------------------------------------------------------------------
# Status badge helpers
# ------------------------------------------------------------------

_STATUS_BADGES: dict[str, dict[str, str]] = {
    "created": {"label": "생성됨", "color": "#6b7280"},
    "contacting": {"label": "연락중", "color": "#3b82f6"},
    "greeting_sent": {"label": "발송됨", "color": "#8b5cf6"},
    "negotiating": {"label": "협의중", "color": "#f59e0b"},
    "paused_for_human": {"label": "일시정지", "color": "#ef4444"},
    "confirmed": {"label": "확정", "color": "#10b981"},
    "declined": {"label": "거절", "color": "#6b7280"},
    "completed": {"label": "완료", "color": "#059669"},
    "timed_out": {"label": "시간초과", "color": "#9ca3af"},
    "failed": {"label": "실패", "color": "#dc2626"},
}


def _badge(status: str) -> dict[str, str]:
    return _STATUS_BADGES.get(status, {"label": status, "color": "#6b7280"})


# ------------------------------------------------------------------
# Routes: Dashboard
# ------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    status: str | None = None,
    username: str = Depends(verify_credentials),
):
    """Main dashboard showing all reservations."""
    repo = _get_repo()
    reservations = repo.list_reservations(status=status)
    paused_count = len(repo.list_paused())
    csrf_token = _generate_csrf_token(username)

    # Dashboard stats
    all_res = repo.list_reservations(limit=10000)
    stats = {
        "total": len(all_res),
        "active": sum(1 for r in all_res if r["status"] in ("created", "contacting", "greeting_sent", "negotiating")),
        "confirmed": sum(1 for r in all_res if r["status"] in ("confirmed", "completed")),
        "declined": sum(1 for r in all_res if r["status"] == "declined"),
        "paused": paused_count,
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "reservations": reservations,
        "paused_count": paused_count,
        "current_status": status,
        "badge": _badge,
        "json_loads": json.loads,
        "csrf_token": csrf_token,
        "stats": stats,
    })


# ------------------------------------------------------------------
# Routes: Create reservation
# ------------------------------------------------------------------

@app.get("/create", response_class=HTMLResponse)
async def create_form(
    request: Request,
    username: str = Depends(verify_credentials),
):
    """Reservation creation form."""
    csrf_token = _generate_csrf_token(username)
    return templates.TemplateResponse("create.html", {
        "request": request,
        "csrf_token": csrf_token,
    })


@app.post("/create")
async def create_reservation(
    clinic_name: str = Form(...),
    procedure_name: str = Form(...),
    preferred_dates: str = Form(""),
    preferred_time: str = Form("any"),
    patient_name: str = Form(...),
    patient_nationality: str = Form("JP"),
    patient_age: str = Form(""),
    patient_gender: str = Form(""),
    patient_contact: str = Form(""),
    notes: str = Form(""),
    csrf_token: str = Form(...),
    username: str = Depends(verify_credentials),
):
    """Handle reservation form submission."""
    _verify_csrf_token(username, csrf_token)
    repo = _get_repo()
    lookup = _get_lookup()

    # Look up clinic
    clinics = lookup.find_by_name(clinic_name)
    clinic = clinics[0] if clinics else None
    clinic_id = clinic.hospital_no if clinic else None

    # Determine platform and contact URL
    # Respect MESSENGER_PLATFORM env var for default priority
    preferred = os.environ.get("MESSENGER_PLATFORM", "kakao").lower()
    contact_platform = preferred
    contact_url: str | None = None
    if clinic:
        # Check preferred platform first, then fallback
        if clinic.has_platform(preferred):
            contact_url = clinic.get_contact_url(preferred)
        elif clinic.has_kakao:
            contact_url = clinic.kakao_url
            contact_platform = "kakao"
        elif clinic.has_line:
            contact_url = clinic.line_url
            contact_platform = "line"

    # Parse dates
    dates = [d.strip() for d in preferred_dates.split(",") if d.strip()]

    # Generate request ID
    now = datetime.now(timezone.utc)
    request_id = f"REQ-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"

    age = int(patient_age) if patient_age.strip().isdigit() else None
    gender = patient_gender if patient_gender else None

    reservation_id = repo.create_reservation(
        request_id=request_id,
        clinic_name=clinic_name,
        patient_name=patient_name,
        procedure_name=procedure_name,
        clinic_id=clinic_id,
        clinic_contact_url=contact_url,
        contact_platform=contact_platform,
        patient_nationality=patient_nationality,
        patient_age=age,
        patient_gender=gender,
        patient_contact=patient_contact,
        preferred_dates=dates if dates else None,
        preferred_time=preferred_time,
        notes=notes or None,
    )

    return RedirectResponse(url=f"/reservations/{reservation_id}", status_code=303)


# ------------------------------------------------------------------
# Routes: Reservation detail
# ------------------------------------------------------------------

@app.get("/reservations/{reservation_id}", response_class=HTMLResponse)
async def reservation_detail(
    request: Request,
    reservation_id: int,
    username: str = Depends(verify_credentials),
):
    """Reservation detail page with conversation log."""
    repo = _get_repo()
    reservation = repo.get_reservation(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    messages = repo.get_messages(reservation_id)
    csrf_token = _generate_csrf_token(username)

    # Get valid next statuses for the current state
    next_statuses = sorted(VALID_TRANSITIONS.get(reservation["status"], frozenset()))

    return templates.TemplateResponse("detail.html", {
        "request": request,
        "reservation": reservation,
        "messages": messages,
        "badge": _badge,
        "json_loads": json.loads,
        "csrf_token": csrf_token,
        "valid_transitions": next_statuses,
    })


@app.post("/reservations/{reservation_id}/resume")
async def resume_reservation(
    reservation_id: int,
    message: str = Form(...),
    csrf_token: str = Form(...),
    username: str = Depends(verify_credentials),
):
    """Staff resumes a paused reservation with a manual message."""
    _verify_csrf_token(username, csrf_token)
    repo = _get_repo()
    reservation = repo.get_reservation(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    repo.add_message(
        reservation_id=reservation_id,
        direction="outgoing",
        content=message,
        llm_provider="staff",
        phase="negotiating",
    )
    repo.update_reservation(
        reservation_id,
        status="negotiating",
        paused_reason=None,
    )

    return RedirectResponse(url=f"/reservations/{reservation_id}", status_code=303)


@app.post("/reservations/{reservation_id}/status")
async def change_status(
    reservation_id: int,
    new_status: str = Form(...),
    csrf_token: str = Form(...),
    username: str = Depends(verify_credentials),
):
    """Change reservation status using VALID_TRANSITIONS."""
    _verify_csrf_token(username, csrf_token)
    repo = _get_repo()
    reservation = repo.get_reservation(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    allowed = VALID_TRANSITIONS.get(reservation["status"], frozenset())
    if new_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from '{reservation['status']}' to '{new_status}'",
        )

    update_kwargs: dict[str, Any] = {"status": new_status}
    if new_status in ("completed", "failed", "declined"):
        update_kwargs["completed_at"] = datetime.now(timezone.utc).isoformat()

    repo.update_reservation(reservation_id, **update_kwargs)
    return RedirectResponse(url=f"/reservations/{reservation_id}", status_code=303)


@app.post("/reservations/{reservation_id}/cancel")
async def cancel_reservation(
    reservation_id: int,
    csrf_token: str = Form(...),
    username: str = Depends(verify_credentials),
):
    """Cancel an active reservation."""
    _verify_csrf_token(username, csrf_token)
    repo = _get_repo()
    repo.update_reservation(
        reservation_id,
        status="failed",
        error_message="Cancelled by staff",
        completed_at=datetime.now(timezone.utc).isoformat(),
    )
    return RedirectResponse(url=f"/reservations/{reservation_id}", status_code=303)


@app.post("/reservations/{reservation_id}/complete")
async def complete_reservation(
    reservation_id: int,
    csrf_token: str = Form(...),
    username: str = Depends(verify_credentials),
):
    """Mark a confirmed reservation as completed."""
    _verify_csrf_token(username, csrf_token)
    repo = _get_repo()
    exporter = _get_exporter()

    repo.update_reservation(
        reservation_id,
        status="completed",
        completed_at=datetime.now(timezone.utc).isoformat(),
    )
    reservation = repo.get_reservation(reservation_id)
    if reservation:
        exporter.export_reservation(reservation)

    return RedirectResponse(url=f"/reservations/{reservation_id}", status_code=303)


# ------------------------------------------------------------------
# Routes: API endpoints
# ------------------------------------------------------------------

@app.get("/api/clinics/search")
async def search_clinics(
    q: str = Query("", min_length=1),
    username: str = Depends(verify_credentials),
):
    """Search clinics for autocomplete."""
    lookup = _get_lookup()
    results = lookup.search(q, limit=10)
    return [
        {
            "hospital_no": c.hospital_no,
            "name": c.name,
            "has_kakao": c.has_kakao,
            "has_line": c.has_line,
            "platforms": [p for p in ("kakao", "line") if c.has_platform(p)],
            "address": c.address,
            "phone": c.phone,
        }
        for c in results
    ]


@app.get("/api/reservations")
async def api_list_reservations(
    status: str | None = None,
    username: str = Depends(verify_credentials),
):
    """List reservations as JSON."""
    repo = _get_repo()
    return repo.list_reservations(status=status)


@app.get("/export/csv")
async def export_csv(username: str = Depends(verify_credentials)):
    """Export all reservations to CSV and download."""
    repo = _get_repo()
    exporter = _get_exporter()
    all_res = repo.list_reservations(limit=10000)
    path = exporter.export_all(all_res)
    return FileResponse(
        path=str(path),
        filename="reservations.csv",
        media_type="text/csv",
    )
