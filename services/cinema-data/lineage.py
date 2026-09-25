from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class LineageEvent:
    event_type: str
    stage: str
    occurred_at: str = field(default_factory=utc_now_iso)
    run_id: str = ""
    actor: str = "system"
    input_ref: str = ""
    output_ref: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeLineage:
    entity_id: str
    events: list[LineageEvent] = field(default_factory=list)

    def add(self, event: LineageEvent) -> None:
        self.events.append(event)

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "events": [asdict(event) for event in self.events],
        }


def build_lineage(
    record: dict[str, Any],
    *,
    run_id: str = "",
    collector: str = "",
) -> KnowledgeLineage:
    entity_id = str(
        record.get("canonical_artist_id")
        or record.get("id")
        or record.get("name")
        or "unknown"
    )
    lineage = KnowledgeLineage(entity_id=entity_id)

    lineage.add(
        LineageEvent(
            event_type="COLLECTED",
            stage="collector",
            run_id=run_id,
            actor=collector or "system",
            details={"name": record.get("name", "")},
        )
    )

    lineage.add(
        LineageEvent(
            event_type="NORMALIZED",
            stage="normalization",
            run_id=run_id,
            details={"schema": "artist-record-v1"},
        )
    )

    if record.get("canonical_artist_id"):
        lineage.add(
            LineageEvent(
                event_type="RESOLVED",
                stage="entity-resolution",
                run_id=run_id,
                output_ref=str(record["canonical_artist_id"]),
            )
        )

    for source in record.get("sources", []) or []:
        lineage.add(
            LineageEvent(
                event_type="EVIDENCE_ATTACHED",
                stage="provenance",
                run_id=run_id,
                input_ref=source.get("source_url", ""),
                details={
                    "source_name": source.get("source_name", ""),
                    "evidence_status": source.get("evidence_status", "unreviewed"),
                },
            )
        )

    lineage.add(
        LineageEvent(
            event_type="PERSISTED",
            stage="knowledge-store",
            run_id=run_id,
            output_ref=entity_id,
        )
    )
    return lineage


def calculate_quality_score(record: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "identity": bool(record.get("name")),
        "stable_id": bool(record.get("canonical_artist_id") or record.get("id")),
        "sources": bool(record.get("sources")),
        "source_urls": all(
            bool(source.get("source_url"))
            for source in record.get("sources", []) or []
        ),
        "collection_timestamp": bool(
            record.get("collected_at") or record.get("collection", {}).get("collected_at")
        ),
    }
    score = round(sum(checks.values()) / len(checks) * 100, 1)
    return {"score": score, "checks": checks}
