from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from artifacts import ArtifactStore, content_hash  # noqa: E402

STORE = ArtifactStore(DATA_PACKAGE_ROOT / "data" / "artifacts.json")


def create_artifact(payload: dict[str, Any]) -> dict[str, Any]:
    return STORE.upsert(payload)


def get_artifact(artifact_id: str) -> dict[str, Any] | None:
    return STORE.get(artifact_id)


def search_artifacts(**filters: Any) -> list[dict[str, Any]]:
    return STORE.search(**filters)


def hash_content(content: str) -> str:
    return content_hash(content.encode("utf-8"))
