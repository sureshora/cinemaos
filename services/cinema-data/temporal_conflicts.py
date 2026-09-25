from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class TemporalAssessment:
    temporal_relation: str
    overlap_days: int | None
    publication_order: str
    freshness_days: int | None
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        try:
            return datetime.fromisoformat(f"{value}T00:00:00+00:00")
        except ValueError:
            return None


def _interval(item: dict[str, Any]) -> tuple[datetime | None, datetime | None]:
    start = _parse_date(item.get("valid_from") or item.get("event_date"))
    end = _parse_date(item.get("valid_to") or item.get("event_end_date") or item.get("event_date"))
    return start, end


def assess_temporal_conflict(
    left: dict[str, Any],
    right: dict[str, Any],
    *,
    as_of: datetime | None = None,
) -> TemporalAssessment:
    left_start, left_end = _interval(left)
    right_start, right_end = _interval(right)
    notes: list[str] = []

    if left_start and right_start:
        if left_start == right_start:
            relation = "same_start"
        elif left_start < right_start:
            relation = "left_earlier"
        else:
            relation = "right_earlier"
    else:
        relation = "unknown"

    overlap_days = None
    if left_start and left_end and right_start and right_end:
        overlap_start = max(left_start, right_start)
        overlap_end = min(left_end, right_end)
        if overlap_start <= overlap_end:
            overlap_days = (overlap_end - overlap_start).days
            notes.append("Validity intervals overlap.")

    left_pub = _parse_date(left.get("published_at") or left.get("publication_date"))
    right_pub = _parse_date(right.get("published_at") or right.get("publication_date"))
    if left_pub and right_pub:
        publication_order = "left_earlier" if left_pub < right_pub else "right_earlier" if right_pub < left_pub else "same_day"
    else:
        publication_order = "unknown"

    freshness_days = None
    reference = as_of or datetime.now(timezone.utc)
    newest_pub = max([d for d in (left_pub, right_pub) if d], default=None)
    if newest_pub:
        freshness_days = max(0, (reference - newest_pub).days)

    if left_pub and left_start and left_pub < left_start:
        notes.append("Left source predates the event it reports.")
    if right_pub and right_start and right_pub < right_start:
        notes.append("Right source predates the event it reports.")

    return TemporalAssessment(
        temporal_relation=relation,
        overlap_days=overlap_days,
        publication_order=publication_order,
        freshness_days=freshness_days,
        notes=notes,
    )
