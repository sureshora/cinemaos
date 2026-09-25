from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class KnowledgeVersion:
    version_id: str
    entity_id: str
    generated_at: str
    schema_version: str
    transformation_version: str
    source_snapshot_ids: list[str]
    fact_ids: list[str]
    record_hash: str


class KnowledgeVersionStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, versions: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(versions, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def add(self, version: KnowledgeVersion) -> None:
        versions = self.load()
        versions.append(asdict(version))
        self.save(versions)

    def for_entity(self, entity_id: str) -> list[dict[str, Any]]:
        return [v for v in self.load() if v.get("entity_id") == entity_id]
