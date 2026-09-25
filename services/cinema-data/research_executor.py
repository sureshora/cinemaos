from __future__ import annotations

import importlib
from datetime import datetime, timezone
from typing import Any

from .research_store import ResearchTaskStore


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ResearchExecutor:
    """Execute only explicitly approved collector modules."""

    def __init__(self, task_store: ResearchTaskStore):
        self.task_store = task_store

    def execute(
        self,
        task_id: str,
        collector_module: str,
        *,
        approved: bool = False,
    ) -> dict[str, Any]:
        task = next(
            (item for item in self.task_store.load() if item.get("task_id") == task_id),
            None,
        )
        if task is None:
            raise KeyError(f"Research task not found: {task_id}")

        if not approved:
            raise PermissionError("Research execution requires explicit approval")

        allowed_prefix = "collectors."
        if not collector_module.startswith(allowed_prefix):
            raise PermissionError("Only approved cinema collector modules may execute")

        module = importlib.import_module(collector_module)
        collect = getattr(module, "collect", None)
        if not callable(collect):
            raise TypeError(f"{collector_module} does not expose collect()")

        task["status"] = "running"
        task["started_at"] = utc_now_iso()
        self.task_store.save(self.task_store.load())

        records = list(collect())

        task["status"] = "evidence_collected"
        task["finished_at"] = utc_now_iso()
        task["evidence_found"] = sum(len(record.get("sources", [])) for record in records)
        task["collector_module"] = collector_module
        task["records_returned"] = len(records)
        self.task_store.update(task_id, **task)

        return {
            "task": task,
            "records": records,
            "requires_validation": True,
            "requires_review": True,
        }
