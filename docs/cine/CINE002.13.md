# CINE002.13 — Source Reliability, Freshness & Confidence Calibration

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Improve fact confidence by considering source reliability, evidence freshness, corroboration and review status.

## Source profile

Each source can have:

- source type
- base reliability
- expected freshness window
- verification status
- notes

Initial profiles are intentionally conservative and explicit for Wikidata and The Movie Database. Unknown sources receive a neutral baseline and must not be treated as authoritative automatically.

## Freshness

Evidence receives a freshness factor based on collection age and the source's expected freshness window.

This is an operational heuristic. It does not claim that an older source is false.

## Corroboration

Multiple independent source records can increase confidence with diminishing returns. Contradictions reduce confidence.

## API

GET /api/v1/cinema/entities/{entity_id}/confidence

## UI

apps/cinema-intelligence/confidence.py provides source-level confidence inspection.

## Important limitation

The current score is a transparent MVP heuristic, not a statistically calibrated probability. Production calibration should be learned from reviewed historical cases and measured source performance.

## Next

CINE002.14 — source snapshots, immutable evidence hashes and reproducible knowledge versions.
