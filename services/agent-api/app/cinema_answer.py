from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from answer_synthesis import synthesize_answer  # noqa: E402
from fact_store import FactStore  # noqa: E402
from query_engine import execute_plan  # noqa: E402
from query_planner import plan_query  # noqa: E402
from relationship_graph import build_relationship_graph  # noqa: E402
from store import CinemaKnowledgeStore  # noqa: E402

STORE = CinemaKnowledgeStore()
FACTS = FactStore(DATA_PACKAGE_ROOT / "data" / "knowledge_facts.json")


def grounded_query(query: str, *, start_id: str, max_hops: int = 4) -> dict[str, Any]:
    plan = plan_query(query, max_hops=max_hops)
    graph = build_relationship_graph(STORE.load())
    result = execute_plan(graph, plan, start_id=start_id)

    entity_facts = FACTS.for_entity(start_id)
    answer = synthesize_answer(
        query=query,
        plan=plan.to_dict(),
        paths=result["paths"],
        facts=entity_facts,
    )
    return answer
