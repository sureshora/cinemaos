from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .facts import KnowledgeFact, fact_to_dict


class FactStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, facts: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(facts, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def upsert(self, facts: list[KnowledgeFact]) -> None:
        existing = {item["fact_id"]: item for item in self.load()}
        for fact in facts:
            existing[fact.fact_id] = fact_to_dict(fact)
        self.save(list(existing.values()))

    def for_entity(self, entity_id: str) -> list[dict[str, Any]]:
        return [
            item
            for item in self.load()
            if item.get("entity_id") == entity_id
        ]
