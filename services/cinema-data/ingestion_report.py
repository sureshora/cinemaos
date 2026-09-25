from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class IngestionReport:
    run_id: str
    collector: str
    started_at: str
    finished_at: str | None = None
    records_received: int = 0
    records_resolved: int = 0
    records_persisted: int = 0
    sources_found: int = 0
    review_required: int = 0
    status: str = "started"
    errors: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
