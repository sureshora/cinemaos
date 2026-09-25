# CINE002.10 — Knowledge Quality & Lineage Engine

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Create auditable lineage from source collection through the final CinemaOS knowledge record.

## Lineage

    Source
      |
    Collector
      |
    Collected
      |
    Normalized
      |
    Entity Resolved
      |
    Evidence Attached
      |
    Persisted

Each stage can carry run ID, timestamps, actor/collector, input references, output references and structured details.

## Quality scoring

The MVP calculates a transparent score from explicit checks:

- identity present
- stable ID present
- source evidence present
- source URLs present
- collection timestamp present

This is a data-quality indicator, not a claim that a fact is objectively true.

## API

GET /api/v1/cinema/artists/{canonical_artist_id}/lineage

GET /api/v1/cinema/artists/{canonical_artist_id}/quality

## UI

apps/cinema-intelligence/quality.py provides a trace view for an individual artist.

## World-class direction

Future versions should add:
- fact-level lineage, not only record-level lineage
- immutable event IDs
- source snapshots
- transformation versions
- confidence calibration
- human review decisions
- contradiction detection
- freshness/decay scoring
- provenance graph storage
- cryptographic content hashes
- full audit trail

## Next

CINE002.11 — contradiction detection and human review workflow.
