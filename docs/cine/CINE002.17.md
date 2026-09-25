# CINE002.17 — Cinema Entity Relationship Graph

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Connect cinema entities into a reusable relationship graph.

## Entity types

- artist
- film
- director
- producer
- writer
- music
- technician
- award

## Relationship examples

- acted_in
- directed
- produced
- wrote
- composed
- credited_in
- directed_by
- produced_by
- written_by
- music_by
- received_award
- technician roles

## API

GET /api/v1/cinema/graph

Optional:

GET /api/v1/cinema/graph?entity_id={artist_id}

## UI

apps/cinema-intelligence/graph.py provides graph data inspection and relationship exploration.

## Architecture principle

The relationship graph is derived from the normalized Cinema Knowledge Store. It is a projection of canonical knowledge, not a parallel source of truth.

## Next

CINE002.18 — graph traversal and multi-hop cinema intelligence queries.
