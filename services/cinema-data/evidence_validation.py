from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import hashlib
from typing import Any

from .fact_store import FactStore


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ReviewDecision:
    evidence_id: str
    reviewer: str
    decision: str
    decided_at: str
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EvidenceReviewStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, records: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, decision: ReviewDecision) -> None:
        records = self.load()
        records.append(decision.to_dict())
        self.save(records)


def validate_evidence(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("evidence_id", "task_id", "entity_id", "source_url", "snapshot_id", "content_sha256")
    errors.extend(f"missing_{field}" for field in required if not record.get(field))

    if record.get("content_sha256") and len(str(record["content_sha256"])) != 64:
        errors.append("invalid_sha256")

    return errors


def duplicate_key(record: dict[str, Any]) -> str:
    return hashlib.sha256(
        f"{record.get('entity_id')}|{record.get('source_url')}|{record.get('content_sha256')}".encode()
    ).hexdigest()


def review_evidence(
    record: dict[str, Any],
    *,
    reviewer: str,
    decision: str,
    reason: str = "",
) -> dict[str, Any]:
    if decision not in {"approved", "rejected", "needs_review"}:
        raise ValueError("decision must be approved, rejected or needs_review")

    errors = validate_evidence(record)
    if errors and decision == "approved":
        raise ValueError("Evidence cannot be approved while validation errors exist")

    result = dict(record)
    result["review_status"] = decision
    result["reviewer"] = reviewer
    result["reviewed_at"] = utc_now_iso()
    result["review_reason"] = reason
    result["validation_errors"] = errors
    return result


def promote_fact(
    evidence: dict[str, Any],
    *,
    property_name: str,
    value: Any,
    confidence: float,
    fact_store: FactStore,
) -> dict[str, Any]:
    if evidence.get("review_status") != "approved":
        raise PermissionError("Only approved evidence can be promoted")

    fact_id = hashlib.sha256(
        f"{evidence['entity_id']}|{property_name}|{value}|{evidence['evidence_id']}".encode()
    ).hexdigest()[:20]

    fact = {
        "fact_id": fact_id,
        "entity_id": evidence["entity_id"],
        "property_name": property_name,
        "value": value,
        "confidence": max(0.0, min(1.0, float(confidence))),
        "status": "reviewed",
        "source_refs": [evidence["source_url"]],
        "lineage_refs": [
            f"evidence:{evidence['evidence_id']}",
            f"snapshot:{evidence['snapshot_id']}",
            f"research_task:{evidence['task_id']}",
        ],
        "created_at": utc_now_iso(),
    }
    fact_store.upsert([_dict_to_fact(fact)])
    return fact


def _dict_to_fact(data: dict[str, Any]):
    from .facts import KnowledgeFact
    return KnowledgeFact(**data)
