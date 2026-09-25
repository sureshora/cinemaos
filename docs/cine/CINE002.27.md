# CINE002.27 — Temporal Conflict Analysis

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Add temporal reasoning to conflict review so CinemaOS can distinguish differences in event dates, validity intervals and source publication chronology.

## Analysis

The MVP compares:

- event date
- valid-from date
- valid-to date
- publication date
- source freshness
- interval overlap

## Output

The temporal assessment reports:

- temporal relation
- validity overlap in days where intervals are available
- publication order
- freshness
- explanatory notes

## API

POST /api/v1/cinema/conflicts/temporal-analysis

The request contains two evidence objects: left and right.

## UI

apps/cinema-intelligence/temporal_conflict.py provides side-by-side temporal comparison.

## Principle

Temporal analysis provides context for a reviewer; it does not automatically determine which historical source is correct.

## Next

CINE002.28 — source reliability scoring and conflict-aware evidence ranking.
