# Project Setup Skill

FastAPI 프로젝트 초기 설정 및 의존성 구성을 수행합니다.

## Triggers

- "프로젝트 생성", "프로젝트 설정", "fastapi init", "fastapi create"

---

## Input

| 항목 | 필수 | 설명 |
|------|------|------|
| `projectName` | ✅ | 프로젝트 이름 (snake_case) |
| `pythonVersion` | ❌ | Python 버전 (기본: 3.11) |
| `database` | ❌ | 데이터베이스 종류 (postgresql/mysql/sqlite) |

---

## Output

### pyproject.toml

```toml
[project]
name = "{project_name}"
version = "0.1.0"
description = "A FastAPI application with Clean Architecture"
readme = "README.md"
requires-python = ">=3.11"

dependencies = [
    # FastAPI Core
    "fastapi>=0.115.4,<0.116",
    "uvicorn[standard]>=0.32.0,<0.33",
    "gunicorn>=23.0.0,<24.0",

    # Database
    "sqlalchemy[asyncio]>=2.0.36,<3.0",
    "asyncpg>=0.30.0,<0.31",
    "alembic>=1.14.0,<2.0",
    "sqlalchemy-utils>=0.42.0",  # Type utilities

    # Validation & Settings
    "pydantic>=2.10.0,<3.0",
    "pydantic-settings>=2.7.0,<3.0",

    # Authentication
    "PyJWT>=2.10.0,<3.0",       # JWT tokens (not python-jose - has CVEs)
    "passlib[bcrypt,argon2]>=1.7.4,<2.0",  # Password hashing with argon2 preferred

    # HTTP Client
    "httpx>=0.28.0,<0.29",
    "tenacity>=8.4.0,<9.0",  # Retry logic for HTTP clients

    # Rate Limiting
    "slowapi>=0.1.9,<0.2",  # Rate limiting middleware

    # Caching
    "redis>=5.2.0,<6.0",
    "fastapi-cache2>=0.2.0,<0.3",

    # Background Tasks
    "celery[redis]>=5.4.0,<6.0",
    "arq>=0.26.0,<0.27",

    # Logging & Observability
    "structlog>=24.4.0,<25.0",
    "opentelemetry-instrumentation-fastapi>=0.49b0",
    "prometheus-fastapi-instrumentator>=7.0.0,<8.0",

    # Utilities
    "python-multipart>=0.0.18,<0.1",
    "python-dotenv>=1.0.0,<2.0",

    # Security
    "python-magic>=0.4.27",  # MIME type detection for file uploads
]

[project.optional-dependencies]
dev = [
    # Testing
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "pytest-mock>=3.14.0",
    "httpx>=0.28.0",
    "factory-boy>=3.3.0",
    "faker>=33.0.0",

    # Code Quality
    "ruff>=0.8.0",
    "mypy>=1.13.0",
    "pre-commit>=4.0.0",

    # Development
    "ipython>=8.29.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
target-version = "py311"
line-length = 88
extend-select = ["D", "RUF"]  # docstring + ruff rules
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "D",   # pydocstyle
    "RUF", # ruff-specific rules
]
ignore = [
    "E501",  # line too long (handled by formatter)
    "B008",  # do not perform function calls in argument defaults
    "D100",  # Missing docstring in public module
    "D104",  # Missing docstring in public package
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --cov=app --cov-report=term-missing"
filterwarnings = [
    "ignore::DeprecationWarning",
]

[tool.coverage.run]
source = ["app"]
omit = ["*/migrations/*", "*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
```

### 디렉토리 구조

```
{project_name}/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── routes/
│   │       │   └── __init__.py
│   │       └── dependencies/
│   │           └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   └── __init__.py
│   │   └── repositories/
│   │       └── __init__.py
│   ├── application/
│   │   ├── __init__.py
│   │   └── services/
│   │       └── __init__.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── session.py
│   │   │   └── models/
│   │   │       └── __init__.py
│   │   ├── repositories/
│   │   │   └── __init__.py
│   │   └── cache/
│   │       └── __init__.py
│   └── schemas/
│       ├── __init__.py
│       └── base.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   └── __init__.py
│   ├── integration/
│   │   └── __init__.py
│   └── e2e/
│       └── __init__.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

### main.py

```python
# app/main.py
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan events."""
    # Startup
    setup_logging()
    yield
    # Shutdown


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return app


app = create_app()
```

### .env.example

```bash
# Application
PROJECT_NAME="{project_name}"
VERSION="0.1.0"
DEBUG=true
API_V1_PREFIX="/api/v1"

# Database
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/{project_name}"

# Redis
REDIS_URL="redis://localhost:6379/0"

# Security
SECRET_KEY="your-secret-key-change-in-production"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000"]
```

### .gitignore

```gitignore
# Byte-compiled
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
.venv/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Build
dist/
build/
*.egg-info/

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# OS
.DS_Store
Thumbs.db
```

---

## 실행 명령어

```bash
# 프로젝트 디렉토리 생성
mkdir {project_name}
cd {project_name}

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# 의존성 설치
pip install -e ".[dev]"

# 환경 변수 설정
cp .env.example .env

# 개발 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## References

- `_references/ARCHITECTURE-PATTERN.md`
