from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import json
import uuid
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ReviewCase:
    case_id: str
    entity_id: str
    field: str
    reason: str
    status: str = "open"
    severity: str = "medium"
    created_at: str = field(default_factory=utc_now_iso)
    reviewed_at: str | None = None
    reviewer: str = ""
    decision: str = ""
    notes: str = ""
    evidence: list[dict[str, Any]] = field(default_factory=list)


class ReviewQueue:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, cases: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(cases, ensure_ascii=False, indent=2), encoding="utf-8")

    def create(
        self,
        entity_id: str,
        field: str,
        reason: str,
        *,
        severity: str = "medium",
        evidence: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        case = ReviewCase(
            case_id=uuid.uuid4().hex[:12],
            entity_id=entity_id,
            field=field,
            reason=reason,
            severity=severity,
            evidence=evidence or [],
        )
        cases = self.load()
        cases.append(asdict(case))
        self.save(cases)
        return asdict(case)

    def list(self, status: str = "open") -> list[dict[str, Any]]:
        return [case for case in self.load() if not status or case.get("status") == status]

    def decide(
        self,
        case_id: str,
        *,
        decision: str,
        reviewer: str,
        notes: str = "",
    ) -> dict[str, Any] | None:
        cases = self.load()
        for case in cases:
            if case.get("case_id") == case_id:
                case["status"] = "resolved"
                case["decision"] = decision
                case["reviewer"] = reviewer
                case["notes"] = notes
                case["reviewed_at"] = utc_now_iso()
                self.save(cases)
                return case
        return None
