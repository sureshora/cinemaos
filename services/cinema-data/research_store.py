from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .research import ResearchTask


class ResearchTaskStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, tasks: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, task: ResearchTask) -> None:
        tasks = self.load()
        tasks.append(task.to_dict())
        self.save(tasks)

    def update(self, task_id: str, **changes: Any) -> dict[str, Any] | None:
        tasks = self.load()
        for task in tasks:
            if task.get("task_id") == task_id:
                task.update(changes)
                self.save(tasks)
                return task
        return None

    def list(self, status: str | None = None) -> list[dict[str, Any]]:
        tasks = self.load()
        if status:
            tasks = [task for task in tasks if task.get("status") == status]
        return tasks
