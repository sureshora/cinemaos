from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Evidence:
    source_url: str
    source_name: str = ""
    source_type: str = "web"
    published_at: str | None = None
    collected_at: str = field(default_factory=utc_now_iso)
    collector: str = ""
    evidence_status: str = "unreviewed"
    notes: str = ""


def normalize_evidence(source: dict[str, Any], collector: str = "") -> dict[str, Any]:
    item = dict(source)
    item.setdefault("source_type", "web")
    item.setdefault("collected_at", utc_now_iso())
    item.setdefault("evidence_status", "unreviewed")
    if collector:
        item.setdefault("collector", collector)
    return item


def attach_provenance(
    record: dict[str, Any],
    *,
    collector: str,
    source_url: str = "",
    source_name: str = "",
    source_type: str = "web",
) -> dict[str, Any]:
    item = dict(record)
    sources = list(item.get("sources") or [])
    if source_url:
        sources.append(
            normalize_evidence(
                {
                    "source_url": source_url,
                    "source_name": source_name,
                    "source_type": source_type,
                },
                collector,
            )
        )
    item["sources"] = sources
    item.setdefault("collection", {})
    item["collection"].update(
        {
            "collector": collector,
            "collected_at": utc_now_iso(),
        }
    )
    return item
