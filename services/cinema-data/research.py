from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import uuid
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ResearchTask:
    task_id: str
    entity_id: str
    question: str
    requested_fields: list[str] = field(default_factory=list)
    source_types: list[str] = field(default_factory=list)
    status: str = "planned"
    created_at: str = field(default_factory=utc_now_iso)
    evidence_found: int = 0
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def create_research_task(
    entity_id: str,
    question: str,
    *,
    requested_fields: list[str] | None = None,
    source_types: list[str] | None = None,
) -> ResearchTask:
    return ResearchTask(
        task_id=uuid.uuid4().hex[:12],
        entity_id=entity_id,
        question=question,
        requested_fields=requested_fields or [],
        source_types=source_types or ["knowledge_graph", "film_database"],
    )


def identify_missing_fields(
    record: dict[str, Any] | None,
    requested_fields: list[str],
) -> list[str]:
    record = record or {}
    return [
        field
        for field in requested_fields
        if record.get(field) in (None, "", [], {})
    ]
