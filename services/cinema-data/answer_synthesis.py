from __future__ import annotations

from collections import Counter
from typing import Any


def _evidence_for_path(path: dict[str, Any]) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []
    for edge in path.get("edges", []):
        for ref in edge.get("source_refs", []) or []:
            evidence.append({
                "source_url": ref,
                "relationship": edge.get("relationship_type"),
                "source_id": edge.get("source_id"),
                "target_id": edge.get("target_id"),
            })
    return evidence


def synthesize_answer(
    *,
    query: str,
    plan: dict[str, Any],
    paths: list[dict[str, Any]],
    facts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    facts = facts or []
    evidence = []
    for path in paths:
        evidence.extend(_evidence_for_path(path))

    unique_evidence = []
    seen = set()
    for item in evidence:
        key = (item["source_url"], item["relationship"])
        if key not in seen:
            seen.add(key)
            unique_evidence.append(item)

    relation_counts = Counter(
        edge.get("relationship_type")
        for path in paths
        for edge in path.get("edges", [])
    )

    confidence_values = [
        float(fact.get("confidence", 0))
        for fact in facts
        if fact.get("confidence") is not None
    ]
    confidence = round(sum(confidence_values) / len(confidence_values), 3) if confidence_values else 0.0

    if confidence >= 0.90:
        label = "very_high"
    elif confidence >= 0.75:
        label = "high"
    elif confidence >= 0.50:
        label = "medium"
    elif confidence > 0:
        label = "low"
    else:
        label = "unknown"

    return {
        "query": query,
        "summary": (
            f"CinemaOS found {len(paths)} explainable relationship path(s) "
            f"for the requested query."
        ),
        "answer_type": "evidence_grounded_graph_result",
        "path_count": len(paths),
        "relationship_counts": dict(relation_counts),
        "confidence": {"score": confidence, "label": label},
        "evidence": unique_evidence,
        "facts": facts,
        "paths": paths,
        "query_plan": plan,
        "limitations": [
            "The answer is limited to the currently ingested knowledge graph.",
            "Source evidence should be reviewed before treating disputed historical facts as final.",
        ],
    }
