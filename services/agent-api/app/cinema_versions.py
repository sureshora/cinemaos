from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from versions import KnowledgeVersionStore  # noqa: E402

VERSIONS = KnowledgeVersionStore(DATA_PACKAGE_ROOT / "data" / "knowledge_versions.json")


def entity_versions(entity_id: str) -> list[dict[str, Any]]:
    return VERSIONS.for_entity(entity_id)
