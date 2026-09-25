from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class EvidenceResolution:
    status: str
    duplicate_of: str | None
    contradictions: list[str]
    confidence: float
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _value_key(entity_id: str, property_name: str, value: Any) -> str:
    return f"{entity_id}|{property_name}|{str(value).strip().casefold()}"


def resolve_evidence(
    evidence: dict[str, Any],
    existing_facts: list[dict[str, Any]],
    *,
    source_score: float = 0.5,
) -> EvidenceResolution:
    entity_id = str(evidence.get("entity_id", ""))
    property_name = str(evidence.get("property_name", ""))
    value = evidence.get("value")
    key = _value_key(entity_id, property_name, value)

    duplicate_of = None
    contradictions: list[str] = []
    notes: list[str] = []

    for fact in existing_facts:
        fact_key = _value_key(
            str(fact.get("entity_id", "")),
            str(fact.get("property_name", "")),
            fact.get("value"),
        )
        if fact_key == key:
            duplicate_of = str(fact.get("fact_id"))
            notes.append("Equivalent fact already exists.")
        elif (
            str(fact.get("entity_id", "")) == entity_id
            and str(fact.get("property_name", "")) == property_name
            and fact.get("value") != value
        ):
            contradictions.append(str(fact.get("fact_id")))

    confidence = max(0.0, min(1.0, float(source_score)))
    if duplicate_of:
        confidence = min(1.0, confidence + 0.05)
    if contradictions:
        confidence = max(0.0, confidence - 0.25)
        notes.append("Conflicting fact requires review.")

    if contradictions:
        status = "conflict"
    elif duplicate_of:
        status = "duplicate"
    else:
        status = "new"

    return EvidenceResolution(
        status=status,
        duplicate_of=duplicate_of,
        contradictions=contradictions,
        confidence=round(confidence, 3),
        notes=notes,
    )
