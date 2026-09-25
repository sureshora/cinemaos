from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import Any, Iterable
from .normalize import normalize_artist

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def stable_id(value: str) -> str:
    return hashlib.sha256(value.strip().lower().encode("utf-8")).hexdigest()[:16]

def normalize_records(records: Iterable[dict[str, Any]], collector_name: str) -> list[dict[str, Any]]:
    output=[]
    for raw in records:
        record=normalize_artist(raw)
        record.setdefault("id", f"artist-{stable_id(record.get('name','unknown'))}")
        record.setdefault("collected_at", utc_now_iso())
        record.setdefault("collector", collector_name)
        for source in record.get("sources", []):
            source.setdefault("collector", collector_name)
        output.append(record)
    return output

def merge_artist_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]]={}
    for record in records:
        key=record.get("id") or f"artist-{stable_id(record.get('name','unknown'))}"
        if key not in merged:
            merged[key]=dict(record)
            continue
        current=merged[key]
        for field in ("languages","roles","aliases"):
            current[field]=list(dict.fromkeys(current.get(field,[])+record.get(field,[])))
        for field in ("career_events","filmography","awards","media","sources"):
            seen={repr(x) for x in current.get(field,[])}
            current[field]=current.get(field,[])+[x for x in record.get(field,[]) if repr(x) not in seen]
        current["social_links"]={**current.get("social_links",{}), **record.get("social_links",{})}
        for field in ("profile_image","summary"):
            if record.get(field):
                current[field]=record[field]
    return list(merged.values())
