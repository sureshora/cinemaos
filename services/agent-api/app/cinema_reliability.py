from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from source_reliability import aggregate_source_confidence, rank_evidence  # noqa: E402


def rank_sources(items: list[dict[str, Any]]) -> dict[str, Any]:
    ranked = rank_evidence(items)
    return {"count": len(ranked), "items": ranked}


def confidence(sources: list[dict[str, Any]], *, contradicted: bool = False, reviewed: bool = False) -> dict[str, Any]:
    return aggregate_source_confidence(sources, contradicted=contradicted, reviewed=reviewed)
