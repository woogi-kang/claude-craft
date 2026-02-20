"""Database schema definitions -- delegated to outreach_shared.

The canonical DDL lives in outreach_shared.db.models. This module
re-exports the shared schema for backwards compatibility.
"""

from __future__ import annotations

from outreach_shared.db.models import ALL_DDL

# Legacy names used by repository.init_db
ALL_TABLES = ALL_DDL
INDEXES: list[str] = []  # Indexes are included in ALL_DDL
MIGRATIONS: list[str] = []
