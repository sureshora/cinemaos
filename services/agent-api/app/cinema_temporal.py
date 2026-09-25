from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from fact_store import FactStore  # noqa: E402
from temporal import reconstruct_state  # noqa: E402

FACTS = FactStore(DATA_PACKAGE_ROOT / "data" / "knowledge_facts.json")


def entity_state_at(entity_id: str, at: str) -> dict[str, Any]:
    facts = FACTS.for_entity(entity_id)
    return reconstruct_state(facts, at=at)
