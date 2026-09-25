# CINE002.16 — Temporal Event Graph & Career Timeline

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Connect historical career events, film credits and awards into a timeline-aware graph.

## Graph

    Artist
      |
      +---- Career Event
      |
      +---- Film Credit
      |
      +---- Award

Every graph event can carry:
- event date
- end date
- related entity IDs
- source references
- structured metadata

## API

GET /api/v1/cinema/entities/{entity_id}/event-graph

## UI

apps/cinema-intelligence/event_graph.py provides a timeline and graph-data explorer.

## Design principle

The graph is derived from the normalized knowledge record. It does not become a second uncontrolled source of truth.

## Next

CINE002.17 — entity relationship graph: artists, films, directors, producers, technicians, music and awards as connected cinema entities.
