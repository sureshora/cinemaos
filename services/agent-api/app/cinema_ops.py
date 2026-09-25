from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

SERVICE_ROOT = Path(__file__).resolve().parents[2]
DATA_PACKAGE_ROOT = SERVICE_ROOT / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from collection_runs import CollectionRunStore  # noqa: E402
from store import CinemaKnowledgeStore  # noqa: E402


def get_store() -> CinemaKnowledgeStore:
    return CinemaKnowledgeStore()


def get_run_store() -> CollectionRunStore:
    return CollectionRunStore(DATA_PACKAGE_ROOT / "data" / "collection_runs.json")


def operations_summary() -> dict[str, Any]:
    records = get_store().load()
    runs = get_run_store().load()

    sources = sum(len(record.get("sources", [])) for record in records)
    events = sum(len(record.get("career_events", [])) for record in records)
    films = sum(len(record.get("filmography", [])) for record in records)
    awards = sum(len(record.get("awards", [])) for record in records)

    return {
        "artists": len(records),
        "films_credits": films,
        "career_events": events,
        "awards": awards,
        "evidence_records": sources,
        "collection_runs": len(runs),
        "last_run": runs[-1] if runs else None,
    }


def collection_runs(limit: int = 25) -> list[dict[str, Any]]:
    runs = get_run_store().load()
    return runs[-max(1, min(limit, 100)) :][::-1]
