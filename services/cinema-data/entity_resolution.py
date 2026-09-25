from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Iterable


def canonical_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def canonical_key(value: str) -> str:
    return canonical_text(value).replace(" ", "")


@dataclass
class EntityCandidate:
    canonical_id: str
    name: str
    aliases: set[str] = field(default_factory=set)


class ArtistEntityResolver:
    """Conservative artist resolver.

    Exact canonical-name or alias matches are auto-resolved. Fuzzy matching is
    intentionally not automatic yet; ambiguous names should be reviewed rather
    than silently merged.
    """

    def __init__(self) -> None:
        self.entities: dict[str, EntityCandidate] = {}
        self.lookup: dict[str, str] = {}

    def register(
        self,
        canonical_id: str,
        name: str,
        aliases: Iterable[str] = (),
    ) -> EntityCandidate:
        candidate = self.entities.setdefault(
            canonical_id,
            EntityCandidate(canonical_id=canonical_id, name=name),
        )
        candidate.aliases.update(a for a in aliases if a)
        for value in [name, *candidate.aliases]:
            key = canonical_key(value)
            if key:
                self.lookup[key] = canonical_id
        return candidate

    def resolve(self, name: str, aliases: Iterable[str] = ()) -> str | None:
        for value in [name, *aliases]:
            found = self.lookup.get(canonical_key(value))
            if found:
                return found
        return None


def resolve_artist_records(records: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Assign canonical IDs where exact evidence supports a merge.

    Returns (resolved_records, review_queue).
    """
    resolver = ArtistEntityResolver()
    resolved: list[dict[str, Any]] = []
    review: list[dict[str, Any]] = []

    for record in records:
        name = str(record.get("name", "")).strip()
        aliases = record.get("aliases", []) or []
        existing = resolver.resolve(name, aliases)

        if existing:
            item = dict(record)
            item["canonical_artist_id"] = existing
            resolved.append(item)
            continue

        canonical_id = record.get("id") or f"artist-{canonical_key(name) or 'unknown'}"
        resolver.register(canonical_id, name, aliases)
        item = dict(record)
        item["canonical_artist_id"] = canonical_id
        resolved.append(item)

    return resolved, review
