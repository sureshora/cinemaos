from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import uuid
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class ProvenanceEvent:
    event_id: str
    event_type: str
    subject_id: str
    timestamp: str
    actor: str
    parent_event_ids: list[str]
    metadata: dict[str, Any]
    event_hash: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ProvenanceLedger:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def append(
        self,
        *,
        event_type: str,
        subject_id: str,
        actor: str,
        metadata: dict[str, Any] | None = None,
        parent_event_ids: list[str] | None = None,
    ) -> ProvenanceEvent:
        events = self.load()
        parents = parent_event_ids or ([events[-1]["event_id"]] if events else [])
        payload = {
            "event_type": event_type,
            "subject_id": subject_id,
            "timestamp": utc_now_iso(),
            "actor": actor,
            "parent_event_ids": parents,
            "metadata": metadata or {},
        }
        event_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        event = ProvenanceEvent(
            event_id=f"prov-{uuid.uuid4().hex[:16]}",
            event_hash=event_hash,
            **payload,
        )
        events.append(event.to_dict())
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(events, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return event

    def chain_for(self, subject_id: str) -> list[dict[str, Any]]:
        events = {event["event_id"]: event for event in self.load()}
        relevant = [
            event for event in events.values()
            if event.get("subject_id") == subject_id
        ]
        return sorted(relevant, key=lambda event: event.get("timestamp", ""))

    def verify(self) -> dict[str, Any]:
        events = self.load()
        failures: list[str] = []
        previous_ids = set()

        for event in events:
            payload = {
                "event_type": event["event_type"],
                "subject_id": event["subject_id"],
                "timestamp": event["timestamp"],
                "actor": event["actor"],
                "parent_event_ids": event["parent_event_ids"],
                "metadata": event["metadata"],
            }
            expected = hashlib.sha256(
                json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
            ).hexdigest()
            if expected != event.get("event_hash"):
                failures.append(event["event_id"])
            for parent in event.get("parent_event_ids", []):
                if parent not in previous_ids and parent != event["event_id"]:
                    failures.append(f"{event['event_id']}:missing_parent:{parent}")
            previous_ids.add(event["event_id"])

        return {
            "valid": not failures,
            "event_count": len(events),
            "failures": failures,
        }
