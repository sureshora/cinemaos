from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

SERVICE_ROOT = Path(__file__).resolve().parents[2]
DATA_PACKAGE_ROOT = SERVICE_ROOT / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from fact_store import FactStore  # noqa: E402

FACTS = FactStore(DATA_PACKAGE_ROOT / "data" / "knowledge_facts.json")


def list_facts(entity_id: str) -> list[dict[str, Any]]:
    return FACTS.for_entity(entity_id)
