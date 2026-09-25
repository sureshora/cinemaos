# CINE002.23 — Evidence Snapshotting, Validation & Provenance

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Attach every research result to a captured source snapshot, content hash and explicit lineage record.

## Pipeline

    Research Result
         |
    Source Validation
         |
    Immutable Snapshot
         |
    SHA-256
         |
    Evidence Record
         |
    Lineage
         |
    Review Queue

## Evidence record

Each evidence record contains:

- evidence ID
- research task ID
- entity ID
- source URL
- source name
- capture timestamp
- snapshot ID
- SHA-256 content hash
- status
- validation errors
- lineage references

## Validation

The MVP validates that a source has:

- source URL
- source name
- captured content

Invalid evidence is stored with status "invalid" and validation errors rather than being silently discarded.

## APIs

POST /api/v1/cinema/research/tasks/{task_id}/evidence

GET /api/v1/cinema/research/evidence

## UI

apps/cinema-intelligence/evidence.py provides an evidence capture and provenance console.

## Trust boundary

CINE002.23 stores evidence but does not promote evidence into canonical knowledge automatically. Promotion remains a later validation/review operation.

## Next

CINE002.24 — evidence validation and promotion workflow: schema checks, duplicate detection, source consistency, review queue and controlled promotion into Knowledge Facts.
