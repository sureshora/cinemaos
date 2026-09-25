from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# The monorepo currently uses a hyphenated service directory. Add its parent
# to sys.path so the API can consume the dependency-free cinema-data package.
SERVICE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SERVICE_ROOT))

from cinema_data.store import CinemaKnowledgeStore  # noqa: E402


def get_store() -> CinemaKnowledgeStore:
    return CinemaKnowledgeStore()


def list_artists(query: str = "", industry: str = "") -> list[dict[str, Any]]:
    records = get_store().load()
    q = query.casefold().strip()
    return [
        record
        for record in records
        if (not q or q in str(record.get("name", "")).casefold())
        and (not industry or record.get("industry") == industry)
    ]


def get_artist(canonical_artist_id: str) -> dict[str, Any] | None:
    for record in get_store().load():
        if str(record.get("canonical_artist_id") or record.get("id")) == canonical_artist_id:
            return record
    return None
