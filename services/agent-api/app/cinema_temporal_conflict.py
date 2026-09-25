from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from temporal_conflicts import assess_temporal_conflict  # noqa: E402


def compare_temporal_evidence(
    left: dict[str, Any],
    right: dict[str, Any],
) -> dict[str, Any]:
    return assess_temporal_conflict(left, right).to_dict()
