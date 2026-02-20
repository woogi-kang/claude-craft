"""Tests for web app authentication and CSRF protection."""

from __future__ import annotations

import base64
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.web.app import app, create_app, _csrf_tokens, _repo, _clinic_lookup


def _auth_header(username: str, password: str) -> dict[str, str]:
    """Build HTTP Basic Auth header."""
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


@pytest.fixture
def web_client(tmp_path: Path):
    """Create a test client with initialized app."""
    # Set credentials via os.environ directly (safe for function-scoped fixtures)
    old_user = os.environ.get("RESERVE_USER")
    old_pass = os.environ.get("RESERVE_PASS")

    os.environ["RESERVE_USER"] = "testadmin"
    os.environ["RESERVE_PASS"] = "testpass123"

    # Create a minimal hospitals.db for ClinicLookup
    import sqlite3

    hospitals_db = tmp_path / "hospitals.db"
    conn = sqlite3.connect(str(hospitals_db))
    conn.execute(
        """CREATE TABLE IF NOT EXISTS hospitals (
            hospital_no INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT,
            address TEXT,
            url TEXT,
            final_url TEXT
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS social_channels (
            id INTEGER PRIMARY KEY,
            hospital_no INTEGER,
            platform TEXT,
            url TEXT,
            confidence REAL
        )"""
    )
    conn.execute(
        """CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            hospital_no INTEGER,
            name TEXT,
            name_english TEXT,
            role TEXT,
            education_json TEXT,
            career_json TEXT,
            credentials_json TEXT
        )"""
    )
    conn.commit()
    conn.close()

    create_app(
        db_path=tmp_path / "test_web.db",
        export_dir=tmp_path / "exports",
        hospitals_db=hospitals_db,
    )

    # Close SQLite connections opened in this thread so they get
    # lazily re-created inside the TestClient's event-loop thread.
    from src.web import app as app_module

    if app_module._repo is not None:
        app_module._repo.close()
        app_module._repo._conn = None
    if app_module._clinic_lookup is not None:
        app_module._clinic_lookup.close()
        app_module._clinic_lookup._conn = None

    client = TestClient(app)
    yield client

    # Clean up CSRF tokens
    _csrf_tokens.clear()

    # Restore env vars
    if old_user is None:
        os.environ.pop("RESERVE_USER", None)
    else:
        os.environ["RESERVE_USER"] = old_user
    if old_pass is None:
        os.environ.pop("RESERVE_PASS", None)
    else:
        os.environ["RESERVE_PASS"] = old_pass


class TestAuthentication:
    """Test HTTP Basic Auth enforcement."""

    def test_unauthenticated_gets_401(self, web_client: TestClient) -> None:
        response = web_client.get("/")
        assert response.status_code == 401

    def test_correct_credentials_grant_access(self, web_client: TestClient) -> None:
        response = web_client.get(
            "/",
            headers=_auth_header("testadmin", "testpass123"),
        )
        assert response.status_code == 200

    def test_wrong_password_gets_401(self, web_client: TestClient) -> None:
        response = web_client.get(
            "/",
            headers=_auth_header("testadmin", "wrongpass"),
        )
        assert response.status_code == 401

    def test_wrong_username_gets_401(self, web_client: TestClient) -> None:
        response = web_client.get(
            "/",
            headers=_auth_header("wronguser", "testpass123"),
        )
        assert response.status_code == 401

    def test_api_endpoint_requires_auth(self, web_client: TestClient) -> None:
        response = web_client.get("/api/reservations")
        assert response.status_code == 401


class TestCSRF:
    """Test CSRF token enforcement on POST endpoints."""

    def _get_csrf_token(self, client: TestClient) -> str:
        """Fetch the dashboard to generate a CSRF token."""
        client.get("/", headers=_auth_header("testadmin", "testpass123"))
        # Token is stored for the authenticated user
        return _csrf_tokens.get("testadmin", "")

    def test_post_without_csrf_gets_422_or_403(self, web_client: TestClient) -> None:
        """POST without csrf_token should fail (422 for missing field or 403 for invalid)."""
        response = web_client.post(
            "/create",
            data={
                "clinic_name": "Test",
                "procedure_name": "Botox",
                "patient_name": "Pat",
                # csrf_token intentionally omitted
            },
            headers=_auth_header("testadmin", "testpass123"),
        )
        # FastAPI returns 422 when required Form field is missing
        assert response.status_code == 422

    def test_invalid_csrf_token_gets_403(self, web_client: TestClient) -> None:
        """POST with wrong CSRF token should get 403."""
        # First generate a valid CSRF token
        self._get_csrf_token(web_client)

        response = web_client.post(
            "/create",
            data={
                "clinic_name": "Test Clinic",
                "procedure_name": "Botox",
                "patient_name": "Tanaka",
                "csrf_token": "definitely_invalid_token",
            },
            headers=_auth_header("testadmin", "testpass123"),
            follow_redirects=False,
        )
        assert response.status_code == 403

    def test_valid_csrf_token_succeeds(self, web_client: TestClient) -> None:
        """POST with correct CSRF token should succeed."""
        csrf = self._get_csrf_token(web_client)

        response = web_client.post(
            "/create",
            data={
                "clinic_name": "Test Clinic",
                "procedure_name": "Botox",
                "patient_name": "Tanaka",
                "patient_nationality": "JP",
                "preferred_dates": "",
                "preferred_time": "any",
                "patient_contact": "",
                "notes": "",
                "csrf_token": csrf,
            },
            headers=_auth_header("testadmin", "testpass123"),
            follow_redirects=False,
        )
        # Successful creation redirects (303) to the detail page
        assert response.status_code == 303
