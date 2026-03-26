"""Tests for FastAPI API endpoints using httpx AsyncClient."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.main import app


@pytest.mark.asyncio
class TestRootEndpoint:
    async def test_root_returns_service_info(self, test_client):
        resp = await test_client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["service"] == "checkyourhospital-worker"
        assert "version" in data


@pytest.mark.asyncio
class TestHealthEndpoint:
    async def test_health_ok(self, test_client):
        resp = await test_client.get("/worker/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"


@pytest.mark.asyncio
class TestScanEndpoint:
    async def test_scan_no_auth(self, test_client):
        resp = await test_client.post(
            "/worker/scan",
            json={"url": "https://example.com"},
        )
        assert resp.status_code == 401

    async def test_scan_accepted(self, test_client, auth_headers):
        with patch("app.security.ssrf.socket.getaddrinfo",
                   return_value=[(2, 1, 6, "", ("93.184.216.34", 443))]):
            resp = await test_client.post(
                "/worker/scan",
                json={"url": "https://example.com"},
                headers=auth_headers,
            )
        assert resp.status_code == 202
        data = resp.json()
        assert data["status"] == "queued"
        assert "task_id" in data

    async def test_scan_ssrf_blocked(self, test_client, auth_headers):
        with patch("app.security.ssrf.socket.getaddrinfo",
                   return_value=[(2, 1, 6, "", ("127.0.0.1", 443))]):
            resp = await test_client.post(
                "/worker/scan",
                json={"url": "https://localhost/test"},
                headers=auth_headers,
            )
        assert resp.status_code == 400
        assert "blocked" in resp.json()["detail"].lower()


@pytest.mark.asyncio
class TestBenchmarkEndpoint:
    async def test_benchmark_no_data(self, test_client):
        with patch("app.services.benchmark.get_supabase_client", return_value=None):
            resp = await test_client.get("/worker/benchmark")
        assert resp.status_code == 200
        data = resp.json()
        assert data["data"] is None


@pytest.mark.asyncio
class TestGeneratePdfEndpoint:
    async def test_generate_pdf_no_auth(self, test_client):
        resp = await test_client.post(
            "/worker/generate-pdf",
            json={"audit_id": "test-id"},
        )
        assert resp.status_code == 401

    async def test_generate_pdf_missing_audit_id(self, test_client, auth_headers):
        resp = await test_client.post(
            "/worker/generate-pdf",
            json={},
            headers=auth_headers,
        )
        assert resp.status_code == 422  # Pydantic validation error

    async def test_generate_pdf_success(self, test_client, auth_headers):
        mock_supabase = MagicMock()
        mock_supabase.table.return_value = mock_supabase
        mock_supabase.select.return_value = mock_supabase
        mock_supabase.eq.return_value = mock_supabase
        mock_supabase.single.return_value = mock_supabase
        mock_supabase.execute.return_value = MagicMock(
            data={
                "url": "https://example-hospital.com",
                "total_score": 72,
                "grade": "B",
                "scores": {"meta_tags": {"score": 100, "grade": "pass"}},
            }
        )

        with (
            patch("app.api.routes.get_supabase_client", return_value=mock_supabase),
            patch(
                "app.api.routes.generate_pdf",
                new_callable=AsyncMock,
                return_value="https://storage.example.com/reports/test-id.pdf",
            ),
        ):
            resp = await test_client.post(
                "/worker/generate-pdf",
                json={"audit_id": "test-id"},
                headers=auth_headers,
            )
        assert resp.status_code == 200
        data = resp.json()
        assert data["pdf_url"] == "https://storage.example.com/reports/test-id.pdf"

    async def test_generate_pdf_audit_not_found(self, test_client, auth_headers):
        mock_supabase = MagicMock()
        mock_supabase.table.return_value = mock_supabase
        mock_supabase.select.return_value = mock_supabase
        mock_supabase.eq.return_value = mock_supabase
        mock_supabase.single.return_value = mock_supabase
        mock_supabase.execute.return_value = MagicMock(data=None)

        with patch("app.api.routes.get_supabase_client", return_value=mock_supabase):
            resp = await test_client.post(
                "/worker/generate-pdf",
                json={"audit_id": "nonexistent-id"},
                headers=auth_headers,
            )
        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"].lower()
