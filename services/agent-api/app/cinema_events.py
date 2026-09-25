from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from event_graph import build_artist_event_graph  # noqa: E402
from store import CinemaKnowledgeStore  # noqa: E402

STORE = CinemaKnowledgeStore()


def artist_event_graph(entity_id: str) -> dict[str, Any] | None:
    for record in STORE.load():
        current = str(record.get("canonical_artist_id") or record.get("id"))
        if current == entity_id:
            return build_artist_event_graph(record)
    return None
