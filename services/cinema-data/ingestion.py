from __future__ import annotations

from typing import Any, Iterable

from .entity_resolution import resolve_artist_records
from .store import CinemaKnowledgeStore


def ingest_records(
    records: Iterable[dict[str, Any]],
    store: CinemaKnowledgeStore,
) -> dict[str, Any]:
    """Normalize the resolved records and persist them without losing history."""
    resolved, review_queue = resolve_artist_records(records)
    path = store.upsert(resolved)

    return {
        "records_received": len(list(records)) if not isinstance(records, list) else len(records),
        "records_resolved": len(resolved),
        "review_queue": review_queue,
        "store_path": str(path),
    }
