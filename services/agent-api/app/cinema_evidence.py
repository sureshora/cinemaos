from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from evidence_pipeline import EvidenceStore, attach_evidence  # noqa: E402
from snapshots import SnapshotStore  # noqa: E402

SNAPSHOTS = SnapshotStore(DATA_PACKAGE_ROOT / "data" / "source_snapshots")
EVIDENCE = EvidenceStore(DATA_PACKAGE_ROOT / "data" / "evidence.json")


def capture_research_evidence(
    *,
    task_id: str,
    entity_id: str,
    sources: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    records = []
    for source in sources:
        records.append(
            attach_evidence(
                task_id=task_id,
                entity_id=entity_id,
                source=source,
                snapshot_store=SNAPSHOTS,
                evidence_store=EVIDENCE,
            ).to_dict()
        )
    return records


def list_evidence(task_id: str | None = None) -> list[dict[str, Any]]:
    records = EVIDENCE.load()
    if task_id:
        records = [record for record in records if record.get("task_id") == task_id]
    return records
