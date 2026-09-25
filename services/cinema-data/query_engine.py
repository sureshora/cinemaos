from __future__ import annotations

from typing import Any

from .graph_traversal import traverse
from .query_planner import QueryPlan


def execute_plan(graph: dict[str, Any], plan: QueryPlan, start_id: str) -> dict[str, Any]:
    paths = traverse(
        graph,
        start_id,
        max_hops=plan.max_hops,
        relationship_types=set(plan.relationship_types) if plan.relationship_types else None,
    )

    minimum_count = plan.constraints.get("minimum_relationship_count")
    if minimum_count:
        paths = [
            path for path in paths
            if len(path.get("edges", [])) >= minimum_count
        ]

    return {
        "query": plan.original_query,
        "intent": plan.intent,
        "constraints": plan.constraints,
        "answer_shape": plan.answer_shape,
        "paths": paths,
        "count": len(paths),
    }
