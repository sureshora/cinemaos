from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from graph_traversal import traverse  # noqa: E402
from relationship_graph import build_relationship_graph  # noqa: E402
from store import CinemaKnowledgeStore  # noqa: E402

STORE = CinemaKnowledgeStore()


def find_paths(
    start_id: str,
    *,
    target_id: str | None = None,
    max_hops: int = 3,
    relationship_types: set[str] | None = None,
) -> list[dict[str, Any]]:
    graph = build_relationship_graph(STORE.load())
    return traverse(
        graph,
        start_id,
        target_id=target_id,
        max_hops=max_hops,
        relationship_types=relationship_types,
    )
