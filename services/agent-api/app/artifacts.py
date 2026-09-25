from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
from typing import Any

ARTIFACT_TYPES = {
    "document", "image", "audio", "video", "map", "historical_record",
    "screenplay", "scene", "character", "music", "production_asset",
}
ARTIFACT_STATUSES = {
    "draft", "ingested", "processing", "ready", "review", "approved",
    "rejected", "archived",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ("artifactId", "artifactType", "title", "mediaType", "location", "schemaVersion")
    errors.extend(f"missing_{key}" for key in required if not artifact.get(key))
    if artifact.get("artifactType") not in ARTIFACT_TYPES:
        errors.append("invalid_artifact_type")
    if artifact.get("status") and artifact["status"] not in ARTIFACT_STATUSES:
        errors.append("invalid_status")
    if artifact.get("schemaVersion") != "1.0":
        errors.append("unsupported_schema_version")
    return errors


def content_hash(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonicalize(artifact: dict[str, Any]) -> dict[str, Any]:
    now = _now()
    result = {
        **artifact,
        "createdAt": artifact.get("createdAt", now),
        "updatedAt": now,
        "status": artifact.get("status", "ingested"),
        "metadata": artifact.get("metadata", {}),
        "sources": artifact.get("sources", []),
        "lineage": {
            "parentArtifactIds": [],
            **artifact.get("lineage", {}),
            "createdAt": artifact.get("lineage", {}).get("createdAt", now),
        },
        "schemaVersion": "1.0",
    }
    errors = validate_artifact(result)
    if errors:
        raise ValueError("; ".join(errors))
    return result


class ArtifactStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, items: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    def upsert(self, artifact: dict[str, Any]) -> dict[str, Any]:
        item = canonicalize(artifact)
        items = self.load()
        for index, current in enumerate(items):
            if current.get("artifactId") == item["artifactId"]:
                items[index] = item
                self.save(items)
                return item
        items.append(item)
        self.save(items)
        return item

    def get(self, artifact_id: str) -> dict[str, Any] | None:
        return next((item for item in self.load() if item.get("artifactId") == artifact_id), None)

    def search(self, **filters: Any) -> list[dict[str, Any]]:
        items = self.load()
        result = []
        for item in items:
            if filters.get("artifactTypes") and item.get("artifactType") not in filters["artifactTypes"]:
                continue
            if filters.get("status") and item.get("status") not in filters["status"]:
                continue
            entity_ids = filters.get("entityIds") or []
            if entity_ids and not set(entity_ids).intersection(item.get("metadata", {}).get("entityIds", [])):
                continue
            result.append(item)
        return result
