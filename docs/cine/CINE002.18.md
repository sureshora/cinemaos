# CINE002.18 — Graph Traversal & Multi-Hop Cinema Intelligence

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Allow CinemaOS to traverse connected cinema entities and return explainable relationship paths.

## Query model

A traversal can specify:

- start entity
- optional target entity
- maximum hops
- optional relationship-type filter

Maximum hops are bounded at 8 in the API to prevent uncontrolled graph expansion in the MVP.

## API

GET /api/v1/cinema/graph/traverse

Parameters:

- start_id
- target_id
- max_hops
- relationships (comma-separated)

## Explainability

Each returned path includes:

- ordered node IDs
- node metadata
- relationship edges
- hop count

Example conceptual path:

    Artist
      -> acted_in
    Film A
      -> directed_by
    Director X
      -> directed
    Film B
      -> music_by
    Composer Y

## UI

apps/cinema-intelligence/traverse.py provides an interactive multi-hop path explorer.

## Safety

The engine avoids cycles within an individual path and bounds traversal depth. Production graph infrastructure can later add cost budgets, pagination, ranking and cached traversals.

## Next

CINE002.19 — semantic graph queries and natural-language Cinema Brain query planning.
