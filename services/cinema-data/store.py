from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

DEFAULT_STORE = Path(__file__).resolve().parent / "data" / "cinema_knowledge.json"


class CinemaKnowledgeStore:
    """Small file-backed persistent store for the CINE002 MVP.

    The store is intentionally dependency-free. It provides a stable persistence
    boundary that can later be replaced by PostgreSQL without changing callers.
    """

    def __init__(self, path: str | Path = DEFAULT_STORE) -> None:
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, records: Iterable[dict[str, Any]]) -> Path:
        items = list(records)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(items, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return self.path

    def upsert(self, records: Iterable[dict[str, Any]]) -> Path:
        existing = self.load()
        by_id = {
            str(r.get("canonical_artist_id") or r.get("id") or r.get("name")): r
            for r in existing
        }

        for record in records:
            key = str(
                record.get("canonical_artist_id")
                or record.get("id")
                or record.get("name")
            )
            if key not in by_id:
                by_id[key] = dict(record)
                continue

            current = by_id[key]
            for field in ("languages", "roles", "aliases"):
                current[field] = list(
                    dict.fromkeys(
                        (current.get(field) or []) + (record.get(field) or [])
                    )
                )

            for field in ("career_events", "filmography", "awards", "media", "sources"):
                values = current.get(field) or []
                seen = {repr(value) for value in values}
                for value in record.get(field) or []:
                    if repr(value) not in seen:
                        seen.add(repr(value))
                        values.append(value)
                current[field] = values

            current["social_links"] = {
                **(current.get("social_links") or {}),
                **(record.get("social_links") or {}),
            }

            for field in ("name", "industry", "profile_image", "summary"):
                if record.get(field):
                    current[field] = record[field]

        return self.save(by_id.values())
