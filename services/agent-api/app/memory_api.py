from __future__ import annotations

from typing import Any

from .memory import MemoryStore

STORE = MemoryStore("services/cinema-data/data/production_memory.json")


def write_memory(payload: dict[str, Any]) -> dict[str, Any]:
    return STORE.upsert(payload)


def read_memory(memory_id: str) -> dict[str, Any] | None:
    return STORE.get(memory_id)


def query_memory(
    project_id: str,
    query: str | None = None,
    **filters: Any,
) -> list[dict[str, Any]]:
    return STORE.search(project_id, query, **filters)
