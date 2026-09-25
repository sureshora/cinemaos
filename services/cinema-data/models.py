from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class SourceRef:
    url: str
    source_name: str = ""
    source_type: str = "web"
    collected_at: str = field(default_factory=utc_now_iso)

@dataclass
class CareerEvent:
    year: int | None
    event_type: str
    title: str
    description: str = ""
    source_url: str = ""

@dataclass
class ArtistRecord:
    id: str
    name: str
    industry: str = ""
    languages: list[str] = field(default_factory=list)
    roles: list[str] = field(default_factory=list)
    aliases: list[str] = field(default_factory=list)
    profile_image: str = ""
    career_events: list[CareerEvent] = field(default_factory=list)
    filmography: list[dict[str, Any]] = field(default_factory=list)
    awards: list[dict[str, Any]] = field(default_factory=list)
    social_links: dict[str, str] = field(default_factory=dict)
    media: list[dict[str, Any]] = field(default_factory=list)
    sources: list[SourceRef] = field(default_factory=list)
    collected_at: str = field(default_factory=utc_now_iso)
