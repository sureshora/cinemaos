from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from research import create_research_task, identify_missing_fields  # noqa: E402
from research_store import ResearchTaskStore  # noqa: E402
from store import CinemaKnowledgeStore  # noqa: E402

TASKS = ResearchTaskStore(DATA_PACKAGE_ROOT / "data" / "research_tasks.json")
STORE = CinemaKnowledgeStore()


def get_record(entity_id: str) -> dict[str, Any] | None:
    for record in STORE.load():
        current = str(record.get("canonical_artist_id") or record.get("id"))
        if current == entity_id:
            return record
    return None


def plan_research(
    entity_id: str,
    question: str,
    requested_fields: list[str],
    source_types: list[str] | None = None,
) -> dict[str, Any]:
    record = get_record(entity_id)
    missing = identify_missing_fields(record, requested_fields)
    task = create_research_task(
        entity_id,
        question,
        requested_fields=missing,
        source_types=source_types,
    )
    task.status = "ready" if missing else "no_missing_fields"
    task.notes.append(
        "Research planning only: no external source is fetched automatically."
    )
    TASKS.add(task)
    result = task.to_dict()
    result["existing_record"] = bool(record)
    result["missing_fields"] = missing
    return result


def list_research_tasks(status: str | None = None) -> list[dict[str, Any]]:
    return TASKS.list(status)
