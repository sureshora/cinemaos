from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import uuid
from typing import Any

from .snapshots import SnapshotStore


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    task_id: str
    entity_id: str
    source_url: str
    source_name: str
    captured_at: str
    snapshot_id: str
    content_sha256: str
    status: str = "candidate"
    validation_errors: list[str] | None = None
    lineage: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EvidenceStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, records: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, record: EvidenceRecord) -> None:
        records = self.load()
        records.append(record.to_dict())
        self.save(records)


def validate_source(source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not source.get("source_url"):
        errors.append("missing_source_url")
    if not source.get("source_name"):
        errors.append("missing_source_name")
    if not source.get("content"):
        errors.append("missing_content")
    return errors


def attach_evidence(
    *,
    task_id: str,
    entity_id: str,
    source: dict[str, Any],
    snapshot_store: SnapshotStore,
    evidence_store: EvidenceStore,
) -> EvidenceRecord:
    errors = validate_source(source)
    content = str(source.get("content", ""))
    snapshot = snapshot_store.create(
        source_url=str(source.get("source_url", "")),
        content=content,
        collector=str(source.get("collector", "")),
        run_id=str(source.get("run_id", "")),
        transformation_version=str(source.get("transformation_version", "v1")),
        content_type=str(source.get("content_type", "text")),
    )

    evidence = EvidenceRecord(
        evidence_id=uuid.uuid4().hex[:16],
        task_id=task_id,
        entity_id=entity_id,
        source_url=str(source.get("source_url", "")),
        source_name=str(source.get("source_name", "")),
        captured_at=utc_now_iso(),
        snapshot_id=snapshot.snapshot_id,
        content_sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
        status="candidate" if not errors else "invalid",
        validation_errors=errors,
        lineage=[
            f"research_task:{task_id}",
            f"snapshot:{snapshot.snapshot_id}",
            f"collector:{source.get('collector', '')}",
        ],
    )
    evidence_store.add(evidence)
    return evidence
