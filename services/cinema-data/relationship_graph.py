from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class Relationship:
    source_id: str
    target_id: str
    relationship_type: str
    valid_from: str | None = None
    valid_to: str | None = None
    source_refs: list[str] | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def entity_id(record: dict[str, Any]) -> str:
    return str(record.get("canonical_artist_id") or record.get("id") or record.get("name") or "unknown")


def build_relationship_graph(records: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []

    def add_node(node_id: str, node_type: str, label: str) -> None:
        nodes.setdefault(node_id, {"id": node_id, "type": node_type, "label": label})

    def add_edge(
        source: str,
        target: str,
        relationship_type: str,
        *,
        source_refs: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        edges.append(
            Relationship(
                source_id=source,
                target_id=target,
                relationship_type=relationship_type,
                source_refs=source_refs or [],
                metadata=metadata or {},
            ).to_dict()
        )

    for record in records:
        artist = entity_id(record)
        add_node(artist, "artist", str(record.get("name", artist)))

        for credit in record.get("filmography", []) or []:
            film_id = str(credit.get("film_id") or credit.get("tmdb_id") or credit.get("title") or "unknown-film")
            film_label = str(credit.get("title") or credit.get("name") or film_id)
            add_node(film_id, "film", film_label)
            refs = [str(credit["source_url"])] if credit.get("source_url") else []
            role = str(credit.get("role") or "Actor").casefold()
            relation = {
                "actor": "acted_in",
                "actress": "acted_in",
                "director": "directed",
                "producer": "produced",
                "writer": "wrote",
                "music": "composed",
                "composer": "composed",
            }.get(role, "credited_in")
            add_edge(artist, film_id, relation, source_refs=refs)

            for person_key, relationship_type, node_type in (
                ("director_id", "directed_by", "director"),
                ("producer_id", "produced_by", "producer"),
                ("writer_id", "written_by", "writer"),
                ("music_id", "music_by", "music"),
            ):
                person_id = credit.get(person_key)
                if person_id:
                    label_key = person_key.replace("_id", "")
                    add_node(str(person_id), node_type, str(credit.get(label_key) or person_id))
                    add_edge(film_id, str(person_id), relationship_type, source_refs=refs)

            for tech in credit.get("technicians", []) or []:
                tech_id = str(tech.get("id") or tech.get("name") or "unknown-technician")
                add_node(tech_id, "technician", str(tech.get("name") or tech_id))
                add_edge(
                    film_id,
                    tech_id,
                    str(tech.get("role") or "technician").casefold().replace(" ", "_"),
                    source_refs=refs,
                )

        for award in record.get("awards", []) or []:
            award_id = str(award.get("award_id") or award.get("id") or award.get("name") or "unknown-award")
            add_node(award_id, "award", str(award.get("name") or award_id))
            add_edge(artist, award_id, "received_award", source_refs=[award["source_url"]] if award.get("source_url") else [])

    return {
        "nodes": list(nodes.values()),
        "edges": edges,
        "node_count": len(nodes),
        "edge_count": len(edges),
    }
