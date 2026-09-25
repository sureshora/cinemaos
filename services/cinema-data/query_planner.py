from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Any


@dataclass(frozen=True)
class QueryPlan:
    original_query: str
    intent: str
    entity_terms: list[str]
    relationship_types: list[str]
    max_hops: int
    constraints: dict[str, Any]
    answer_shape: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


RELATIONSHIP_ALIASES = {
    "acted": "acted_in",
    "acted in": "acted_in",
    "act": "acted_in",
    "directed": "directed",
    "directors": "directed_by",
    "directed by": "directed_by",
    "produced": "produced",
    "produced by": "produced_by",
    "written": "wrote",
    "wrote": "wrote",
    "music": "music_by",
    "music director": "music_by",
    "composer": "music_by",
    "award": "received_award",
}


def _relationship_types(query: str) -> list[str]:
    lowered = query.casefold()
    matches = []
    for alias, relation in RELATIONSHIP_ALIASES.items():
        if alias in lowered and relation not in matches:
            matches.append(relation)
    return matches


def plan_query(query: str, *, max_hops: int = 4) -> QueryPlan:
    text = query.strip()
    lowered = text.casefold()

    intent = "graph_exploration"
    if any(word in lowered for word in ("who", "which", "find", "show")):
        intent = "relationship_lookup"
    if any(word in lowered for word in ("timeline", "history", "historical", "in 19", "in 20")):
        intent = "temporal_analysis"
    if any(word in lowered for word in ("why", "evidence", "source", "verify")):
        intent = "evidence_analysis"

    constraints: dict[str, Any] = {}
    count_match = re.search(r"(?:more than|at least)\s+(\d+)\s+times", lowered)
    if count_match:
        constraints["minimum_relationship_count"] = int(count_match.group(1))

    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", lowered)
    if year_match:
        constraints["year"] = int(year_match.group(1))

    return QueryPlan(
        original_query=text,
        intent=intent,
        entity_terms=[],
        relationship_types=_relationship_types(text),
        max_hops=max(1, min(max_hops, 8)),
        constraints=constraints,
        answer_shape="paths_with_evidence",
    )
