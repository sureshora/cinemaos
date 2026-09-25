from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import uuid
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ConflictCase:
    case_id: str
    entity_id: str
    property_name: str
    evidence_ids: list[str]
    fact_ids: list[str]
    status: str = "open"
    created_at: str = ""
    resolution: str | None = None
    reviewer: str | None = None
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ConflictCaseStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, cases: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, case: ConflictCase) -> None:
        cases = self.load()
        cases.append(case.to_dict())
        self.save(cases)

    def update(self, case_id: str, **changes: Any) -> dict[str, Any] | None:
        cases = self.load()
        for case in cases:
            if case.get("case_id") == case_id:
                case.update(changes)
                self.save(cases)
                return case
        return None


def create_conflict_case(
    *,
    entity_id: str,
    property_name: str,
    evidence_ids: list[str],
    fact_ids: list[str],
    notes: str = "",
) -> ConflictCase:
    return ConflictCase(
        case_id=f"conflict-{uuid.uuid4().hex[:12]}",
        entity_id=entity_id,
        property_name=property_name,
        evidence_ids=evidence_ids,
        fact_ids=fact_ids,
        created_at=utc_now_iso(),
        notes=notes,
    )
