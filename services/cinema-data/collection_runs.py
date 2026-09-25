from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CollectionRun:
    run_id: str
    collector: str
    started_at: str = field(default_factory=utc_now_iso)
    finished_at: str | None = None
    records_received: int = 0
    records_persisted: int = 0
    status: str = "started"
    errors: list[str] = field(default_factory=list)


class CollectionRunStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, runs: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(runs, ensure_ascii=False, indent=2), encoding="utf-8")

    def record(self, run: CollectionRun) -> None:
        runs = self.load()
        runs.append(asdict(run))
        self.save(runs)
