from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


def build_adjacency(edges: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    adjacency: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        adjacency[str(edge["source_id"])].append(edge)
        adjacency[str(edge["target_id"])].append({
            **edge,
            "source_id": edge["target_id"],
            "target_id": edge["source_id"],
            "relationship_type": f"reverse:{edge['relationship_type']}",
        })
    return adjacency


def traverse(
    graph: dict[str, Any],
    start_id: str,
    *,
    target_id: str | None = None,
    max_hops: int = 3,
    relationship_types: set[str] | None = None,
) -> list[dict[str, Any]]:
    nodes = {str(node["id"]): node for node in graph.get("nodes", [])}
    adjacency = build_adjacency(graph.get("edges", []))
    queue = deque([(start_id, [start_id], [])])
    visited: set[tuple[str, int]] = {(start_id, 0)}
    paths: list[dict[str, Any]] = []

    while queue:
        current, node_path, edge_path = queue.popleft()
        if target_id and current == target_id and len(node_path) > 1:
            paths.append(_path_payload(nodes, node_path, edge_path))
            continue

        if len(edge_path) >= max_hops:
            continue

        for edge in adjacency.get(current, []):
            relation = str(edge.get("relationship_type", ""))
            if relationship_types and relation not in relationship_types:
                continue

            nxt = str(edge["target_id"])
            if nxt in node_path:
                continue

            state = (nxt, len(edge_path) + 1)
            if state in visited:
                continue
            visited.add(state)
            queue.append((nxt, node_path + [nxt], edge_path + [edge]))

    if not target_id:
        paths.extend(
            _path_payload(nodes, node_path, edge_path)
            for current, node_path, edge_path in queue
            if edge_path
        )

    return paths


def _path_payload(
    nodes: dict[str, dict[str, Any]],
    node_path: list[str],
    edge_path: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "hops": len(edge_path),
        "node_ids": node_path,
        "nodes": [nodes.get(node_id, {"id": node_id}) for node_id in node_path],
        "edges": edge_path,
    }
