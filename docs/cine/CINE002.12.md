# CINE002.12 — Fact-Level Knowledge Model & Confidence Engine

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Move CinemaOS from record-level metadata toward atomic, auditable knowledge facts.

## Fact model

Each fact contains:

- entity_id
- property_name
- value
- fact_id
- confidence score
- confidence label
- review status
- validity period
- source references
- lineage references
- timestamps
- notes

Example:

    Entity: artist-123
    Property: debut_year
    Value: 1985
    Confidence: 0.85
    Sources: [source-A, source-B]
    Status: reviewed

## Confidence

The MVP uses an explicit, transparent heuristic based on:
- number of sources
- reviewed source evidence
- human review
- contradiction penalty

This is not a statistical truth probability. Production calibration should use measured source reliability and historical validation outcomes.

## API

GET /api/v1/cinema/entities/{entity_id}/facts

## UI

apps/cinema-intelligence/facts.py provides a fact explorer.

## Next

CINE002.13 — source reliability profiles, freshness scoring and confidence calibration.
