from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from provenance_ledger import ProvenanceLedger  # noqa: E402

LEDGER = ProvenanceLedger(DATA_PACKAGE_ROOT / "data" / "provenance_ledger.json")


def record_event(
    event_type: str,
    subject_id: str,
    actor: str,
    metadata: dict[str, Any] | None = None,
    parent_event_ids: list[str] | None = None,
) -> dict[str, Any]:
    return LEDGER.append(
        event_type=event_type,
        subject_id=subject_id,
        actor=actor,
        metadata=metadata,
        parent_event_ids=parent_event_ids,
    ).to_dict()


def lineage(subject_id: str) -> list[dict[str, Any]]:
    return LEDGER.chain_for(subject_id)


def verify_ledger() -> dict[str, Any]:
    return LEDGER.verify()
