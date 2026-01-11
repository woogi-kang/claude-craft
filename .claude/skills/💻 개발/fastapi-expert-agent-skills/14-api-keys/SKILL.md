# API Keys Skill

API Key 인증 및 웹훅 서명 검증을 구현합니다.

## Triggers

- "API 키", "api key", "webhook", "서명 검증"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `projectPath` | ✅ | 프로젝트 경로 |

---

## Output

### API Key Entity

```python
# app/domain/entities/api_key.py
from datetime import datetime, timezone
from pydantic import BaseModel


class ApiKeyEntity(BaseModel):
    """API Key domain entity."""

    id: int | None = None
    key: str
    name: str
    user_id: int
    scopes: list[str] = []
    is_active: bool = True
    expires_at: datetime | None = None
    last_used_at: datetime | None = None
    created_at: datetime | None = None

    model_config = {"from_attributes": True}

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        # Use timezone-aware datetime (SQLAlchemy 2.0 best practice)
        return datetime.now(timezone.utc) > self.expires_at
```

### API Key Generation

```python
# app/core/api_keys.py
import hashlib
import secrets
from datetime import datetime, timedelta

PREFIX = "sk_"  # Secret key prefix
PREFIX_LIVE = "sk_live_"
PREFIX_TEST = "sk_test_"


def generate_api_key(environment: str = "live") -> tuple[str, str]:
    """Generate a new API key and its hash.

    Returns:
        Tuple of (raw_key, hashed_key)

    Note: Using 64 bytes (86 chars) for security best practices
    matching industry standards (Stripe, GitHub, etc.)
    """
    prefix = PREFIX_LIVE if environment == "live" else PREFIX_TEST
    raw_key = prefix + secrets.token_urlsafe(64)  # 64 bytes = ~86 chars
    hashed_key = hash_api_key(raw_key)
    return raw_key, hashed_key


def hash_api_key(raw_key: str) -> str:
    """Hash an API key for storage."""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def verify_api_key(raw_key: str, hashed_key: str) -> bool:
    """Verify an API key against its hash."""
    return hash_api_key(raw_key) == hashed_key
```

### API Key Service

```python
# app/application/services/api_key.py
from datetime import datetime, timedelta, timezone

import structlog

from app.core.api_keys import generate_api_key, hash_api_key
from app.core.exceptions import AuthenticationError, NotFoundError
from app.domain.entities.api_key import ApiKeyEntity
from app.domain.repositories.api_key import ApiKeyRepository

logger = structlog.get_logger()


class ApiKeyService:
    """API Key management service."""

    def __init__(self, repository: ApiKeyRepository) -> None:
        self._repository = repository

    async def create(
        self,
        user_id: int,
        name: str,
        scopes: list[str] | None = None,
        expires_in_days: int | None = None,
    ) -> tuple[ApiKeyEntity, str]:
        """Create a new API key.

        Returns:
            Tuple of (ApiKeyEntity, raw_key) - raw_key shown only once
        """
        raw_key, hashed_key = generate_api_key()

        expires_at = None
        if expires_in_days:
            # Use timezone-aware datetime (SQLAlchemy 2.0 best practice)
            expires_at = datetime.now(timezone.utc) + timedelta(days=expires_in_days)

        entity = ApiKeyEntity(
            key=hashed_key,
            name=name,
            user_id=user_id,
            scopes=scopes or [],
            expires_at=expires_at,
        )

        created = await self._repository.create(entity)
        await logger.ainfo("API key created", user_id=user_id, name=name)

        return created, raw_key

    async def validate(self, raw_key: str) -> ApiKeyEntity:
        """Validate an API key and return its entity."""
        hashed_key = hash_api_key(raw_key)

        api_key = await self._repository.get_by_key(hashed_key)
        if not api_key:
            raise AuthenticationError("Invalid API key")

        if not api_key.is_active:
            raise AuthenticationError("API key is inactive")

        if api_key.is_expired:
            raise AuthenticationError("API key has expired")

        # Update last used timestamp
        await self._repository.update_last_used(api_key.id)

        return api_key

    async def revoke(self, api_key_id: int, user_id: int) -> None:
        """Revoke an API key."""
        api_key = await self._repository.get_by_id(api_key_id)
        if not api_key:
            raise NotFoundError(resource="ApiKey", identifier=api_key_id)

        if api_key.user_id != user_id:
            raise AuthenticationError("Not authorized to revoke this key")

        await self._repository.deactivate(api_key_id)
        await logger.ainfo("API key revoked", api_key_id=api_key_id)

    async def list_for_user(self, user_id: int) -> list[ApiKeyEntity]:
        """List all API keys for a user."""
        return await self._repository.list_by_user(user_id)
```

### API Key Authentication Dependency

```python
# app/api/v1/dependencies/api_key.py
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery

from app.api.v1.dependencies.services import get_api_key_service
from app.application.services.api_key import ApiKeyService
from app.core.exceptions import AuthenticationError
from app.domain.entities.api_key import ApiKeyEntity

# Accept API key from header or query parameter
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
api_key_query = APIKeyQuery(name="api_key", auto_error=False)


async def get_api_key(
    api_key_header: str | None = Security(api_key_header),
    api_key_query: str | None = Security(api_key_query),
    service: ApiKeyService = Depends(get_api_key_service),
) -> ApiKeyEntity:
    """Validate and return API key entity."""
    api_key = api_key_header or api_key_query

    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    try:
        return await service.validate(api_key)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.message),
            headers={"WWW-Authenticate": "ApiKey"},
        )


class ApiKeyScopeChecker:
    """Check if API key has required scopes."""

    def __init__(self, required_scopes: list[str]) -> None:
        self.required_scopes = required_scopes

    async def __call__(
        self,
        api_key: ApiKeyEntity = Depends(get_api_key),
    ) -> ApiKeyEntity:
        for scope in self.required_scopes:
            if scope not in api_key.scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"API key missing required scope: {scope}",
                )
        return api_key


def require_api_key_scopes(*scopes: str):
    """Dependency factory for API key scope checking."""
    return ApiKeyScopeChecker(list(scopes))


# Type alias
ValidApiKey = Annotated[ApiKeyEntity, Depends(get_api_key)]
```

### Webhook Signature Verification

```python
# app/core/webhooks.py
import hashlib
import hmac
import time
from typing import Any

from app.core.config import settings


def generate_webhook_signature(
    payload: bytes,
    secret: str,
    timestamp: int | None = None,
) -> str:
    """Generate webhook signature for payload.

    Format: t={timestamp},v1={signature}
    """
    if timestamp is None:
        timestamp = int(time.time())

    # Create signed payload
    signed_payload = f"{timestamp}.{payload.decode()}"

    # Generate HMAC signature
    signature = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    return f"t={timestamp},v1={signature}"


def verify_webhook_signature(
    payload: bytes,
    signature: str,
    secret: str,
    tolerance: int = 300,  # 5 minutes
) -> bool:
    """Verify webhook signature.

    Args:
        payload: Raw request body
        signature: Signature header value
        secret: Webhook secret
        tolerance: Max age of signature in seconds

    Returns:
        True if signature is valid
    """
    try:
        # Parse signature header
        parts = dict(item.split("=") for item in signature.split(","))
        timestamp = int(parts["t"])
        expected_sig = parts["v1"]

        # Check timestamp tolerance
        if abs(time.time() - timestamp) > tolerance:
            return False

        # Generate expected signature
        signed_payload = f"{timestamp}.{payload.decode()}"
        computed_sig = hmac.new(
            secret.encode(),
            signed_payload.encode(),
            hashlib.sha256,
        ).hexdigest()

        # Constant-time comparison
        return hmac.compare_digest(computed_sig, expected_sig)

    except (KeyError, ValueError):
        return False
```

### Webhook Endpoint

```python
# app/api/v1/routes/webhooks.py
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from app.core.config import settings
from app.core.webhooks import verify_webhook_signature

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


async def verify_stripe_signature(
    request: Request,
    stripe_signature: str = Header(alias="Stripe-Signature"),
) -> bytes:
    """Verify Stripe webhook signature."""
    body = await request.body()

    if not verify_webhook_signature(
        payload=body,
        signature=stripe_signature,
        secret=settings.STRIPE_WEBHOOK_SECRET,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature",
        )

    return body


@router.post("/stripe")
async def stripe_webhook(
    body: bytes = Depends(verify_stripe_signature),
):
    """Handle Stripe webhooks."""
    import json

    event = json.loads(body)
    event_type = event["type"]

    match event_type:
        case "payment_intent.succeeded":
            # Handle successful payment
            pass
        case "payment_intent.failed":
            # Handle failed payment
            pass
        case _:
            # Unknown event type
            pass

    return {"received": True}
```

### API Key Routes

```python
# app/api/v1/routes/api_keys.py
from fastapi import APIRouter, Depends

from app.api.v1.dependencies import ActiveUser
from app.api.v1.dependencies.services import get_api_key_service
from app.application.services.api_key import ApiKeyService
from app.schemas.api_key import ApiKeyCreate, ApiKeyResponse, ApiKeyCreatedResponse

router = APIRouter(prefix="/api-keys", tags=["api-keys"])


@router.post("", response_model=ApiKeyCreatedResponse)
async def create_api_key(
    request: ApiKeyCreate,
    current_user: ActiveUser,
    service: ApiKeyService = Depends(get_api_key_service),
):
    """Create a new API key. The raw key is shown only once."""
    api_key, raw_key = await service.create(
        user_id=current_user.id,
        name=request.name,
        scopes=request.scopes,
        expires_in_days=request.expires_in_days,
    )

    return ApiKeyCreatedResponse(
        id=api_key.id,
        name=api_key.name,
        key=raw_key,  # Only time raw key is shown
        scopes=api_key.scopes,
        expires_at=api_key.expires_at,
        created_at=api_key.created_at,
    )


@router.get("", response_model=list[ApiKeyResponse])
async def list_api_keys(
    current_user: ActiveUser,
    service: ApiKeyService = Depends(get_api_key_service),
):
    """List all API keys for current user."""
    return await service.list_for_user(current_user.id)


@router.delete("/{api_key_id}")
async def revoke_api_key(
    api_key_id: int,
    current_user: ActiveUser,
    service: ApiKeyService = Depends(get_api_key_service),
):
    """Revoke an API key."""
    await service.revoke(api_key_id, current_user.id)
    return {"message": "API key revoked"}
```

## References

- `_references/AUTH-PATTERN.md`
