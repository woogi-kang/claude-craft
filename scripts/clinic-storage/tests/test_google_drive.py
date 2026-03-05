"""Tests for optional Google Drive uploader configuration."""

import pytest

from clinic_crawler.google_drive import (
    _build_drive_name,
    _auth_mode,
    _doctor_root_folder_name,
    _organize_by_place_id,
    _truthy,
    is_drive_enabled,
    keep_local_copy_after_upload,
    upload_screenshot,
)


def test_truthy_parser():
    assert _truthy("1")
    assert _truthy("TRUE")
    assert _truthy("yes")
    assert not _truthy("0")
    assert not _truthy("false")
    assert not _truthy(None)


def test_drive_toggle_env(monkeypatch):
    monkeypatch.setenv("CLINIC_SCREENSHOT_BACKEND", "gdrive")
    assert is_drive_enabled()
    monkeypatch.setenv("CLINIC_SCREENSHOT_BACKEND", "local")
    assert not is_drive_enabled()


def test_drive_name_uses_prefix_and_place_id(monkeypatch):
    monkeypatch.setenv("CLINIC_GDRIVE_FILE_PREFIX", "crawl")
    out = _build_drive_name("20951918", "/tmp/abc.jpg")
    assert out == "crawl_20951918_doctors.jpg"


def test_auth_mode_default(monkeypatch):
    monkeypatch.delenv("CLINIC_GDRIVE_AUTH_MODE", raising=False)
    assert _auth_mode() == "service_account"


def test_organize_by_place_default(monkeypatch):
    monkeypatch.delenv("CLINIC_GDRIVE_ORGANIZE_BY_PLACE_ID", raising=False)
    assert _organize_by_place_id()


def test_organize_by_place_toggle(monkeypatch):
    monkeypatch.setenv("CLINIC_GDRIVE_ORGANIZE_BY_PLACE_ID", "0")
    assert not _organize_by_place_id()


def test_doctor_root_folder_default(monkeypatch):
    monkeypatch.delenv("CLINIC_GDRIVE_DOCTOR_ROOT_FOLDER", raising=False)
    assert _doctor_root_folder_name() == "doctor_profiles"


def test_doctor_root_folder_from_env(monkeypatch):
    monkeypatch.setenv("CLINIC_GDRIVE_DOCTOR_ROOT_FOLDER", "doctor_info")
    assert _doctor_root_folder_name() == "doctor_info"


def test_keep_local_copy_default(monkeypatch):
    monkeypatch.delenv("CLINIC_GDRIVE_KEEP_LOCAL_COPY", raising=False)
    assert not keep_local_copy_after_upload()


def test_keep_local_copy_toggle(monkeypatch):
    monkeypatch.setenv("CLINIC_GDRIVE_KEEP_LOCAL_COPY", "1")
    assert keep_local_copy_after_upload()


def test_upload_rejects_unknown_auth_mode(monkeypatch, tmp_path):
    image = tmp_path / "shot.jpg"
    image.write_bytes(b"test")
    monkeypatch.setenv("CLINIC_GDRIVE_AUTH_MODE", "unknown")
    monkeypatch.setenv("CLINIC_GDRIVE_FOLDER_ID", "folder123")

    with pytest.raises(ValueError, match="Unsupported CLINIC_GDRIVE_AUTH_MODE"):
        upload_screenshot(str(image), "20951918")


def test_upload_requires_credentials(monkeypatch, tmp_path):
    image = tmp_path / "shot.jpg"
    image.write_bytes(b"test")
    monkeypatch.setenv("CLINIC_GDRIVE_AUTH_MODE", "service_account")
    monkeypatch.delenv("CLINIC_GDRIVE_CREDENTIALS_JSON", raising=False)
    monkeypatch.setenv("CLINIC_GDRIVE_FOLDER_ID", "folder123")

    with pytest.raises(ValueError, match="CLINIC_GDRIVE_CREDENTIALS_JSON"):
        upload_screenshot(str(image), "20951918")


def test_upload_requires_folder(monkeypatch, tmp_path):
    image = tmp_path / "shot.jpg"
    image.write_bytes(b"test")
    creds = tmp_path / "svc.json"
    creds.write_text("{}", encoding="utf-8")
    monkeypatch.setenv("CLINIC_GDRIVE_AUTH_MODE", "service_account")
    monkeypatch.setenv("CLINIC_GDRIVE_CREDENTIALS_JSON", str(creds))
    monkeypatch.delenv("CLINIC_GDRIVE_FOLDER_ID", raising=False)

    with pytest.raises(ValueError, match="CLINIC_GDRIVE_FOLDER_ID"):
        upload_screenshot(str(image), "20951918")


def test_upload_requires_local_file(monkeypatch, tmp_path):
    creds = tmp_path / "svc.json"
    creds.write_text("{}", encoding="utf-8")
    missing = tmp_path / "missing.jpg"
    monkeypatch.setenv("CLINIC_GDRIVE_AUTH_MODE", "service_account")
    monkeypatch.setenv("CLINIC_GDRIVE_CREDENTIALS_JSON", str(creds))
    monkeypatch.setenv("CLINIC_GDRIVE_FOLDER_ID", "folder123")

    with pytest.raises(FileNotFoundError):
        upload_screenshot(str(missing), "20951918")
