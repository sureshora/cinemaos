from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from source_reliability import aggregate_source_confidence  # noqa: E402
from store import CinemaKnowledgeStore  # noqa: E402


def entity_confidence(entity_id: str) -> dict[str, Any] | None:
    for record in CinemaKnowledgeStore().load():
        current = str(record.get("canonical_artist_id") or record.get("id"))
        if current == entity_id:
            return aggregate_source_confidence(
                record.get("sources", []) or [],
                contradicted=bool(record.get("contradicted")),
                reviewed=record.get("status") == "reviewed",
            )
    return None
