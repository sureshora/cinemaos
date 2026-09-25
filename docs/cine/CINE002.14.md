# CINE002.14 — Immutable Source Snapshots & Reproducible Knowledge Versions

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Preserve what a source actually contained at collection time and make knowledge states reproducible.

## Source snapshots

A snapshot stores:

- snapshot ID
- source URL
- capture timestamp
- SHA-256 content hash
- content type
- collector
- collection run ID
- transformation version

The content is stored separately from metadata.

## Knowledge versions

A knowledge version records:

- version ID
- entity ID
- generation timestamp
- schema version
- transformation version
- source snapshot IDs
- fact IDs
- record hash

This creates a reproducible chain:

    Source
      |
    Snapshot
      |
    Hash
      |
    Collection Run
      |
    Transformation
      |
    Knowledge Version
      |
    Facts

## API

GET /api/v1/cinema/entities/{entity_id}/versions

## UI

apps/cinema-intelligence/versions.py provides a version explorer.

## Integrity principle

A snapshot is content-addressed by SHA-256. If the captured content changes, its hash changes and it becomes a different snapshot.

## Production direction

The MVP uses local file storage. Production should move immutable snapshots to object storage with retention policy, signed manifests, encryption, access control and lifecycle management.

## Next

CINE002.15 — temporal knowledge: effective dates, historical state reconstruction and timeline-aware facts.
