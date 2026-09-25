from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from relationship_graph import build_relationship_graph  # noqa: E402
from store import CinemaKnowledgeStore  # noqa: E402

STORE = CinemaKnowledgeStore()


def cinema_relationship_graph(entity_id: str | None = None) -> dict[str, Any]:
    records = STORE.load()
    if entity_id:
        records = [
            record
            for record in records
            if str(record.get("canonical_artist_id") or record.get("id")) == entity_id
        ]
    return build_relationship_graph(records)
