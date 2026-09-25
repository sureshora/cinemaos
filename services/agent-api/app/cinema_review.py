from __future__ import annotations

import sys
from pathlib import Path

SERVICE_ROOT = Path(__file__).resolve().parents[2]
DATA_PACKAGE_ROOT = SERVICE_ROOT / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from review import ReviewQueue  # noqa: E402

QUEUE = ReviewQueue(DATA_PACKAGE_ROOT / "data" / "review_queue.json")


def list_cases(status: str = "open"):
    return QUEUE.list(status)


def decide_case(case_id: str, decision: str, reviewer: str, notes: str = ""):
    return QUEUE.decide(
        case_id,
        decision=decision,
        reviewer=reviewer,
        notes=notes,
    )
