from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

SERVICE_ROOT = Path(__file__).resolve().parents[2]
DATA_PACKAGE_ROOT = SERVICE_ROOT / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from lineage import build_lineage, calculate_quality_score  # noqa: E402
from store import CinemaKnowledgeStore  # noqa: E402


def get_record(canonical_artist_id: str) -> dict[str, Any] | None:
    for record in CinemaKnowledgeStore().load():
        if str(record.get("canonical_artist_id") or record.get("id")) == canonical_artist_id:
            return record
    return None


def get_lineage(canonical_artist_id: str) -> dict[str, Any] | None:
    record = get_record(canonical_artist_id)
    if not record:
        return None
    lineage = build_lineage(
        record,
        run_id=str(record.get("collection", {}).get("run_id", "")),
        collector=str(record.get("collection", {}).get("collector", "")),
    )
    return lineage.to_dict()


def get_quality(canonical_artist_id: str) -> dict[str, Any] | None:
    record = get_record(canonical_artist_id)
    if not record:
        return None
    return calculate_quality_score(record)
