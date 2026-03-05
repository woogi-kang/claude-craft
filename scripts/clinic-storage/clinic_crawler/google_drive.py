"""Google Drive screenshot uploader for clinic crawler.

This module is optional. Local screenshot persistence remains the default.
Enable Drive uploads by setting:

    CLINIC_SCREENSHOT_BACKEND=gdrive
    CLINIC_GDRIVE_AUTH_MODE=service_account
    CLINIC_GDRIVE_CREDENTIALS_JSON=/abs/path/service-account.json
    CLINIC_GDRIVE_FOLDER_ID=<drive-folder-id>

Optional:
    CLINIC_GDRIVE_AUTH_MODE=adc
    CLINIC_GDRIVE_SHARE_PUBLIC=1
    CLINIC_GDRIVE_FILE_PREFIX=clinic
    CLINIC_GDRIVE_ORGANIZE_BY_PLACE_ID=1
    CLINIC_GDRIVE_DOCTOR_ROOT_FOLDER=doctor_profiles
    CLINIC_GDRIVE_KEEP_LOCAL_COPY=0
"""

from __future__ import annotations

import hashlib
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

try:  # pragma: no cover - platform dependent
    import fcntl
except ImportError:  # pragma: no cover - non-POSIX
    fcntl = None

DRIVE_SCOPE = "https://www.googleapis.com/auth/drive.file"
FOLDER_MIME = "application/vnd.google-apps.folder"
_FOLDER_CACHE: dict[tuple[str, str], str] = {}
_LOCK_DIR = Path(tempfile.gettempdir()) / "clinic_gdrive_locks"


@dataclass
class DriveUploadResult:
    """Result metadata from Google Drive upload."""

    file_id: str
    url: str


def _truthy(raw: str | None) -> bool:
    return (raw or "").strip().lower() in {"1", "true", "yes", "on"}


def is_drive_enabled() -> bool:
    """Return True when screenshot backend is configured as gdrive."""
    backend = os.environ.get("CLINIC_SCREENSHOT_BACKEND", "local")
    return backend.strip().lower() == "gdrive"


def _build_drive_name(place_id: str, local_path: str) -> str:
    prefix = os.environ.get("CLINIC_GDRIVE_FILE_PREFIX", "clinic").strip() or "clinic"
    suffix = Path(local_path).suffix or ".jpg"
    return f"{prefix}_{place_id}_doctors{suffix}"


def _auth_mode() -> str:
    return os.environ.get("CLINIC_GDRIVE_AUTH_MODE", "service_account").strip().lower()


def _organize_by_place_id() -> bool:
    raw = os.environ.get("CLINIC_GDRIVE_ORGANIZE_BY_PLACE_ID", "1")
    return _truthy(raw)


def _doctor_root_folder_name() -> str:
    raw = os.environ.get("CLINIC_GDRIVE_DOCTOR_ROOT_FOLDER", "doctor_profiles").strip()
    return raw or "doctor_profiles"


def keep_local_copy_after_upload() -> bool:
    raw = os.environ.get("CLINIC_GDRIVE_KEEP_LOCAL_COPY", "0")
    return _truthy(raw)


def _cache_key(parent_id: str, name: str) -> tuple[str, str]:
    return (parent_id, name)


class _FolderCreationLock:
    """Cross-process lock for folder creation on this host."""

    def __init__(self, parent_id: str, name: str):
        self.parent_id = parent_id
        self.name = name
        self._fh: TextIO | None = None

    def __enter__(self) -> _FolderCreationLock:
        if fcntl is None:
            return self
        _LOCK_DIR.mkdir(parents=True, exist_ok=True)
        key = hashlib.sha1(f"{self.parent_id}:{self.name}".encode("utf-8")).hexdigest()
        lock_path = _LOCK_DIR / f"{key}.lock"
        self._fh = lock_path.open("a+", encoding="utf-8")
        fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX)
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        if self._fh is None or fcntl is None:
            return False
        try:
            fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
        finally:
            self._fh.close()
        return False


def _find_child_folder(service, parent_id: str, name: str) -> str | None:
    safe_name = name.replace("'", "\\'")
    query = (
        f"name = '{safe_name}' and "
        f"mimeType = '{FOLDER_MIME}' and "
        f"trashed = false and "
        f"'{parent_id}' in parents"
    )
    resp = service.files().list(
        q=query,
        pageSize=10,
        fields="files(id,name,createdTime)",
        orderBy="createdTime asc",
        includeItemsFromAllDrives=True,
        supportsAllDrives=True,
    ).execute()
    items = resp.get("files") or []
    if not items:
        return None
    return items[0]["id"]


def _create_child_folder(service, parent_id: str, name: str) -> str:
    created = service.files().create(
        body={
            "name": name,
            "mimeType": FOLDER_MIME,
            "parents": [parent_id],
        },
        fields="id",
        supportsAllDrives=True,
    ).execute()
    return created["id"]


def _ensure_child_folder(service, parent_id: str, name: str) -> str:
    key = _cache_key(parent_id, name)
    cached = _FOLDER_CACHE.get(key)
    if cached:
        return cached

    # Lock find/create sequence to avoid duplicate folder creation in
    # multi-process batch crawls running on the same host.
    with _FolderCreationLock(parent_id, name):
        cached = _FOLDER_CACHE.get(key)
        if cached:
            return cached

        existing = _find_child_folder(service, parent_id, name)
        folder_id = existing or _create_child_folder(service, parent_id, name)
        _FOLDER_CACHE[key] = folder_id
        return folder_id


def _resolve_upload_parent(service, folder_id: str, place_id: str) -> str:
    if not _organize_by_place_id():
        return folder_id

    doctor_root = _ensure_child_folder(service, folder_id, _doctor_root_folder_name())
    place_folder = _ensure_child_folder(service, doctor_root, str(place_id))
    return place_folder


def _build_credentials():
    mode = _auth_mode()
    if mode == "adc":
        try:
            from google.oauth2.credentials import Credentials
        except ImportError as exc:  # pragma: no cover - depends on optional deps
            raise RuntimeError(
                "Google auth dependency missing. "
                "Install with: pip install google-auth"
            ) from exc

        # Prefer gcloud user Application Default Credentials so this path
        # remains stable even when GOOGLE_APPLICATION_CREDENTIALS points to
        # a service account JSON.
        adc_path = Path.home() / ".config" / "gcloud" / "application_default_credentials.json"
        if adc_path.exists():
            return Credentials.from_authorized_user_file(str(adc_path), scopes=[DRIVE_SCOPE])

        import google.auth

        creds, _ = google.auth.default(scopes=[DRIVE_SCOPE])
        return creds

    if mode != "service_account":
        raise ValueError(
            f"Unsupported CLINIC_GDRIVE_AUTH_MODE '{mode}'. "
            "Use 'service_account' or 'adc'."
        )

    credentials_path = os.environ.get("CLINIC_GDRIVE_CREDENTIALS_JSON", "").strip()
    if not credentials_path:
        raise ValueError("Missing CLINIC_GDRIVE_CREDENTIALS_JSON")

    try:
        from google.oauth2 import service_account
    except ImportError as exc:  # pragma: no cover - depends on optional deps
        raise RuntimeError(
            "Google auth dependency missing. "
            "Install with: pip install google-auth"
        ) from exc
    return service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=[DRIVE_SCOPE],
    )


def upload_screenshot(local_path: str, place_id: str) -> DriveUploadResult:
    """Upload screenshot file to Google Drive and return file metadata."""
    folder_id = os.environ.get("CLINIC_GDRIVE_FOLDER_ID", "").strip()
    share_public = _truthy(os.environ.get("CLINIC_GDRIVE_SHARE_PUBLIC"))

    if not folder_id:
        raise ValueError("Missing CLINIC_GDRIVE_FOLDER_ID")
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Screenshot file not found: {local_path}")

    creds = _build_credentials()

    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError as exc:  # pragma: no cover - depends on optional deps
        raise RuntimeError(
            "Google Drive upload dependencies missing. "
            "Install with: pip install google-api-python-client google-auth"
        ) from exc

    service = build("drive", "v3", credentials=creds, cache_discovery=False)
    target_parent = _resolve_upload_parent(service, folder_id, place_id)

    drive_name = _build_drive_name(place_id, local_path)
    created = service.files().create(
        body={"name": drive_name, "parents": [target_parent]},
        media_body=MediaFileUpload(local_path, mimetype="image/jpeg", resumable=False),
        fields="id, webViewLink",
        supportsAllDrives=True,
    ).execute()

    file_id = created["id"]
    if share_public:
        service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"},
            supportsAllDrives=True,
        ).execute()

    url = created.get("webViewLink") or f"https://drive.google.com/file/d/{file_id}/view"
    return DriveUploadResult(file_id=file_id, url=url)
