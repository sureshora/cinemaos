from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import uuid
from typing import Any

MEMORY_TYPES = {
    "project", "session", "artifact", "decision", "character",
    "scene", "continuity", "production", "agent",
}
MEMORY_SCOPES = {"project", "season", "episode", "scene", "artifact", "session"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_memory(memory: dict[str, Any]) -> list[str]:
    required = ("memoryId", "memoryType", "scope", "projectId", "title", "content", "schemaVersion")
    errors = [f"missing_{key}" for key in required if not memory.get(key)]
    if memory.get("memoryType") not in MEMORY_TYPES:
        errors.append("invalid_memory_type")
    if memory.get("scope") not in MEMORY_SCOPES:
        errors.append("invalid_memory_scope")
    if memory.get("schemaVersion") != "1.0":
        errors.append("unsupported_schema_version")
    return errors


def canonicalize(memory: dict[str, Any]) -> dict[str, Any]:
    timestamp = now()
    result = {
        **memory,
        "memoryId": memory.get("memoryId") or f"mem-{uuid.uuid4().hex[:16]}",
        "entityIds": memory.get("entityIds", []),
        "artifactIds": memory.get("artifactIds", []),
        "parentMemoryIds": memory.get("parentMemoryIds", []),
        "sourceIds": memory.get("sourceIds", []),
        "importance": max(0.0, min(1.0, float(memory.get("importance", 0.5)))),
        "createdAt": memory.get("createdAt", timestamp),
        "updatedAt": timestamp,
        "schemaVersion": "1.0",
    }
    errors = validate_memory(result)
    if errors:
        raise ValueError("; ".join(errors))
    return result


class MemoryStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, records: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    def upsert(self, memory: dict[str, Any]) -> dict[str, Any]:
        item = canonicalize(memory)
        records = self.load()
        for index, current in enumerate(records):
            if current.get("memoryId") == item["memoryId"]:
                records[index] = item
                self.save(records)
                return item
        records.append(item)
        self.save(records)
        return item

    def get(self, memory_id: str) -> dict[str, Any] | None:
        return next((item for item in self.load() if item.get("memoryId") == memory_id), None)

    def search(self, project_id: str, query: str | None = None, **filters: Any) -> list[dict[str, Any]]:
        records = [item for item in self.load() if item.get("projectId") == project_id]
        if filters.get("memoryTypes"):
            records = [item for item in records if item.get("memoryType") in filters["memoryTypes"]]
        if filters.get("scopes"):
            records = [item for item in records if item.get("scope") in filters["scopes"]]
        if filters.get("entityIds"):
            wanted = set(filters["entityIds"])
            records = [item for item in records if wanted.intersection(item.get("entityIds", []))]
        if filters.get("artifactIds"):
            wanted = set(filters["artifactIds"])
            records = [item for item in records if wanted.intersection(item.get("artifactIds", []))]
        if query:
            terms = query.casefold().split()
            records = [
                item for item in records
                if all(term in (item.get("title", "") + " " + item.get("content", "")).casefold() for term in terms)
            ]
        records.sort(key=lambda item: (item.get("importance", 0), item.get("updatedAt", "")), reverse=True)
        return records[: int(filters.get("limit", 50))]
