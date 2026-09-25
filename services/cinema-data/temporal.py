from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class TemporalFact:
    fact_id: str
    entity_id: str
    property_name: str
    value: Any
    valid_from: str | None = None
    valid_to: str | None = None
    observed_at: str = ""
    source_refs: list[str] | None = None

    def __post_init__(self) -> None:
        if not self.observed_at:
            object.__setattr__(self, "observed_at", utc_now_iso())
        if self.source_refs is None:
            object.__setattr__(self, "source_refs", [])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def is_valid_at(fact: dict[str, Any], at: str) -> bool:
    point = parse_date(at)
    if point is None:
        raise ValueError(f"Invalid temporal query date: {at}")

    start = parse_date(fact.get("valid_from"))
    end = parse_date(fact.get("valid_to"))

    if start and point < start:
        return False
    if end and point > end:
        return False
    return True


def reconstruct_state(
    facts: list[dict[str, Any]],
    *,
    at: str,
) -> dict[str, Any]:
    """Return the latest valid value for each property at a point in time."""
    candidates: dict[str, list[dict[str, Any]]] = {}

    for fact in facts:
        if is_valid_at(fact, at):
            candidates.setdefault(str(fact["property_name"]), []).append(fact)

    state: dict[str, Any] = {}
    for property_name, values in candidates.items():
        values.sort(
            key=lambda item: (
                parse_date(item.get("valid_from"))
                or datetime.min.replace(tzinfo=timezone.utc),
                parse_date(item.get("observed_at"))
                or datetime.min.replace(tzinfo=timezone.utc),
            ),
            reverse=True,
        )
        state[property_name] = values[0]

    return state
