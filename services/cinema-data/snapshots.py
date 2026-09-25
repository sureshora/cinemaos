from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


@dataclass(frozen=True)
class SourceSnapshot:
    snapshot_id: str
    source_url: str
    captured_at: str
    content_sha256: str
    content_type: str = "text"
    collector: str = ""
    run_id: str = ""
    transformation_version: str = "v1"


class SnapshotStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)

    def create(
        self,
        *,
        source_url: str,
        content: str,
        collector: str = "",
        run_id: str = "",
        transformation_version: str = "v1",
        content_type: str = "text",
    ) -> SourceSnapshot:
        digest = content_hash(content)
        snapshot_id = digest[:20]
        directory = self.root / snapshot_id
        directory.mkdir(parents=True, exist_ok=True)

        (directory / "content.txt").write_text(content, encoding="utf-8")
        metadata = SourceSnapshot(
            snapshot_id=snapshot_id,
            source_url=source_url,
            captured_at=utc_now_iso(),
            content_sha256=digest,
            content_type=content_type,
            collector=collector,
            run_id=run_id,
            transformation_version=transformation_version,
        )
        (directory / "metadata.json").write_text(
            json.dumps(asdict(metadata), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return metadata

    def get(self, snapshot_id: str) -> tuple[dict[str, Any], str] | None:
        directory = self.root / snapshot_id
        metadata_file = directory / "metadata.json"
        content_file = directory / "content.txt"
        if not metadata_file.exists() or not content_file.exists():
            return None
        return (
            json.loads(metadata_file.read_text(encoding="utf-8")),
            content_file.read_text(encoding="utf-8"),
        )
