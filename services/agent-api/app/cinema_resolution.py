from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from evidence_resolution import resolve_evidence  # noqa: E402
from fact_store import FactStore  # noqa: E402

FACTS = FactStore(DATA_PACKAGE_ROOT / "data" / "knowledge_facts.json")


def resolve(
    *,
    entity_id: str,
    property_name: str,
    value: Any,
    source_score: float = 0.5,
) -> dict[str, Any]:
    evidence = {
        "entity_id": entity_id,
        "property_name": property_name,
        "value": value,
    }
    return resolve_evidence(evidence, FACTS.load(), source_score=source_score).to_dict()
