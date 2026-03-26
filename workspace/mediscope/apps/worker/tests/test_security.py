"""Tests for SSRF prevention."""

from unittest.mock import patch

import pytest

from app.security.ssrf import SSRFError, validate_url


class TestSSRF:
    def _mock_resolve(self, ip: str):
        """Helper: mock DNS resolution to return a specific IP."""
        return patch(
            "app.security.ssrf.socket.getaddrinfo",
            return_value=[(2, 1, 6, "", (ip, 443))],
        )

    def test_block_localhost(self):
        with self._mock_resolve("127.0.0.1"):
            with pytest.raises(SSRFError):
                validate_url("https://localhost/test")

    def test_block_127_range(self):
        with self._mock_resolve("127.0.0.1"):
            with pytest.raises(SSRFError):
                validate_url("https://127.0.0.1/test")

    def test_block_10_network(self):
        with self._mock_resolve("10.0.0.1"):
            with pytest.raises(SSRFError):
                validate_url("https://internal.example.com/")

    def test_block_172_16_network(self):
        with self._mock_resolve("172.16.0.1"):
            with pytest.raises(SSRFError):
                validate_url("https://private.example.com/")

    def test_block_192_168_network(self):
        with self._mock_resolve("192.168.1.1"):
            with pytest.raises(SSRFError):
                validate_url("https://home.example.com/")

    def test_block_169_254_metadata(self):
        with self._mock_resolve("169.254.169.254"):
            with pytest.raises(SSRFError):
                validate_url("https://metadata.example.com/")

    def test_allow_public_ip(self):
        with self._mock_resolve("93.184.216.34"):
            result = validate_url("https://example.com/")
        assert result == "https://example.com/"

    def test_block_non_http_scheme(self):
        with pytest.raises(SSRFError):
            validate_url("ftp://example.com/file")

    def test_block_no_hostname(self):
        with pytest.raises(SSRFError):
            validate_url("https:///path")

    def test_block_metadata_hostname(self):
        with pytest.raises(SSRFError):
            validate_url("https://metadata.google.internal/")

    def test_block_dns_failure(self):
        import socket

        with patch(
            "app.security.ssrf.socket.getaddrinfo",
            side_effect=socket.gaierror("DNS failed"),
        ):
            with pytest.raises(SSRFError):
                validate_url("https://nonexistent.example.com/")
