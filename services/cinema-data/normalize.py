from __future__ import annotations
from typing import Any

def normalize_artist(raw: dict[str, Any]) -> dict[str, Any]:
    record = dict(raw)
    for key in ("languages", "roles", "aliases", "career_events", "filmography", "awards", "media", "sources"):
        record.setdefault(key, [])
    record.setdefault("social_links", {})
    return record
