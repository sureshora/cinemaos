# CINE002.25 — Evidence Deduplication, Contradiction Resolution & Confidence Recalculation

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Prevent duplicate knowledge and detect conflicting values before evidence is promoted into canonical facts.

## Resolution states

- new — no equivalent fact or conflict found
- duplicate — equivalent fact already exists
- conflict — same entity/property has a different value

## Confidence

The MVP recalculates a confidence signal from source score, with small corroboration benefit for duplicates and a contradiction penalty.

This remains a transparent heuristic, not a probability of truth.

## API

POST /api/v1/cinema/research/evidence/resolve

Parameters:

- entity_id
- property_name
- value
- source_score

## UI

apps/cinema-intelligence/evidence_resolution.py provides a resolution console.

## Promotion principle

Conflict results should remain in review rather than being silently overwritten. Duplicate results should reference the existing fact instead of creating uncontrolled copies.

## Next

CINE002.26 — conflict case management and evidence comparison: side-by-side sources, temporal overlap analysis and human resolution decisions.
