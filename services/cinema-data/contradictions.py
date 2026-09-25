from __future__ import annotations

from collections import defaultdict
from typing import Any


def _value_key(value: Any) -> str:
    return str(value).strip().casefold()


def detect_contradictions(
    records: list[dict[str, Any]],
    fields: tuple[str, ...] = ("birth_date", "death_date", "debut_year"),
) -> list[dict[str, Any]]:
    """Find explicit conflicting scalar values across source-backed records."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for record in records:
        entity_id = str(record.get("canonical_artist_id") or record.get("id") or record.get("name"))
        grouped[entity_id].append(record)

    findings: list[dict[str, Any]] = []
    for entity_id, group in grouped.items():
        for field in fields:
            values: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for record in group:
                value = record.get(field)
                if value not in (None, ""):
                    values[_value_key(value)].append(record)

            if len(values) > 1:
                findings.append({
                    "entity_id": entity_id,
                    "field": field,
                    "values": [
                        {
                            "value": original.get(field),
                            "sources": original.get("sources", []),
                        }
                        for original in [items[0] for items in values.values()]
                    ],
                    "reason": f"Conflicting values detected for {field}",
                })

    return findings
