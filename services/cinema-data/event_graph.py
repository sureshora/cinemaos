from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class TemporalEvent:
    event_id: str
    entity_id: str
    event_type: str
    title: str
    event_date: str | None = None
    end_date: str | None = None
    related_entity_ids: list[str] | None = None
    source_refs: list[str] | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_artist_event_graph(record: dict[str, Any]) -> dict[str, Any]:
    entity_id = str(
        record.get("canonical_artist_id")
        or record.get("id")
        or record.get("name")
        or "unknown"
    )
    nodes = [{
        "id": entity_id,
        "type": "artist",
        "label": record.get("name", entity_id),
    }]
    edges: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []

    for index, event in enumerate(record.get("career_events", []) or []):
        event_id = str(event.get("event_id") or f"{entity_id}:career:{index}")
        item = TemporalEvent(
            event_id=event_id,
            entity_id=entity_id,
            event_type=str(event.get("type", "career_event")),
            title=str(event.get("title") or event.get("description") or "Career event"),
            event_date=event.get("date") or event.get("year"),
            end_date=event.get("end_date"),
            related_entity_ids=event.get("related_entity_ids", []),
            source_refs=[
                str(source.get("source_url"))
                for source in event.get("sources", [])
                if source.get("source_url")
            ],
            metadata={k: v for k, v in event.items() if k not in {"event_id", "type", "title", "description", "date", "year", "end_date", "related_entity_ids", "sources"}},
        )
        events.append(item.to_dict())
        nodes.append({"id": event_id, "type": "event", "label": item.title})
        edges.append({"source": entity_id, "target": event_id, "type": item.event_type})

    for index, film in enumerate(record.get("filmography", []) or []):
        title = str(film.get("title") or film.get("name") or "Untitled film")
        film_id = str(film.get("film_id") or f"{entity_id}:film:{index}")
        nodes.append({"id": film_id, "type": "film", "label": title})
        edges.append({"source": entity_id, "target": film_id, "type": "film_credit"})
        events.append({
            "event_id": film_id,
            "entity_id": entity_id,
            "event_type": "film_credit",
            "title": title,
            "event_date": film.get("release_date") or film.get("year"),
            "related_entity_ids": film.get("related_entity_ids", []),
            "source_refs": [film.get("source_url")] if film.get("source_url") else [],
            "metadata": film,
        })

    for index, award in enumerate(record.get("awards", []) or []):
        title = str(award.get("name") or award.get("title") or "Award")
        award_id = str(award.get("award_id") or f"{entity_id}:award:{index}")
        nodes.append({"id": award_id, "type": "award", "label": title})
        edges.append({"source": entity_id, "target": award_id, "type": "award"})
        events.append({
            "event_id": award_id,
            "entity_id": entity_id,
            "event_type": "award",
            "title": title,
            "event_date": award.get("date") or award.get("year"),
            "related_entity_ids": award.get("related_entity_ids", []),
            "source_refs": [award.get("source_url")] if award.get("source_url") else [],
            "metadata": award,
        })

    return {"entity_id": entity_id, "nodes": nodes, "edges": edges, "events": sorted(events, key=lambda x: str(x.get("event_date") or ""))}
