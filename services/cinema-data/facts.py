from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import hashlib
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def fact_id(entity_id: str, property_name: str, value: Any) -> str:
    raw = json.dumps(
        {"entity": entity_id, "property": property_name, "value": value},
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]


@dataclass
class KnowledgeFact:
    entity_id: str
    property_name: str
    value: Any
    fact_id: str = ""
    confidence: float = 0.0
    confidence_label: str = "unknown"
    status: str = "unreviewed"
    valid_from: str | None = None
    valid_to: str | None = None
    source_refs: list[str] = field(default_factory=list)
    lineage_refs: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)
    updated_at: str = field(default_factory=utc_now_iso)
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.fact_id:
            self.fact_id = fact_id(self.entity_id, self.property_name, self.value)


def confidence_label(score: float) -> str:
    if score >= 0.90:
        return "very_high"
    if score >= 0.75:
        return "high"
    if score >= 0.50:
        return "medium"
    if score > 0:
        return "low"
    return "unknown"


def calculate_fact_confidence(
    *,
    source_count: int,
    verified_source_count: int = 0,
    reviewed: bool = False,
    contradicted: bool = False,
) -> float:
    """Transparent heuristic; production calibration comes later."""
    score = min(0.55, source_count * 0.15)
    score += min(0.25, verified_source_count * 0.10)
    if reviewed:
        score += 0.20
    if contradicted:
        score -= 0.35
    score = max(0.0, min(1.0, score))
    return round(score, 3)


def fact_from_record(
    record: dict[str, Any],
    property_name: str,
    value: Any,
    *,
    source_refs: list[str] | None = None,
    lineage_refs: list[str] | None = None,
    reviewed: bool = False,
    contradicted: bool = False,
) -> KnowledgeFact:
    entity_id = str(
        record.get("canonical_artist_id")
        or record.get("id")
        or record.get("name")
        or "unknown"
    )
    sources = source_refs or [
        str(source.get("source_url"))
        for source in record.get("sources", []) or []
        if source.get("source_url")
    ]
    score = calculate_fact_confidence(
        source_count=len(sources),
        verified_source_count=sum(
            1
            for source in record.get("sources", []) or []
            if source.get("evidence_status") == "reviewed"
        ),
        reviewed=reviewed,
        contradicted=contradicted,
    )
    return KnowledgeFact(
        entity_id=entity_id,
        property_name=property_name,
        value=value,
        confidence=score,
        confidence_label=confidence_label(score),
        status="reviewed" if reviewed else ("disputed" if contradicted else "unreviewed"),
        source_refs=sources,
        lineage_refs=lineage_refs or [],
    )


def fact_to_dict(fact: KnowledgeFact) -> dict[str, Any]:
    return asdict(fact)
