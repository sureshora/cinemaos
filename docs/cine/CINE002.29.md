# CINE002.29 — End-to-End Research Provenance Ledger

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Create one auditable chain connecting research operations, evidence, review and knowledge changes.

## Provenance event model

Each event records:

- event ID
- event type
- subject ID
- timestamp
- actor
- parent event IDs
- metadata
- SHA-256 event hash

## Chain

    Research Task
       |
    Collector Run
       |
    Source Snapshot
       |
    Evidence
       |
    Validation
       |
    Conflict / Resolution
       |
    Review
       |
    Promotion
       |
    Knowledge Version

The individual application modules can attach their IDs and metadata to provenance events.

## APIs

POST /api/v1/cinema/provenance/events

GET /api/v1/cinema/provenance/{subject_id}

GET /api/v1/cinema/provenance/verify

## Integrity

The ledger verifies event hashes and parent references to detect tampering or broken lineage.

## UI

apps/cinema-intelligence/provenance.py provides lineage tracing and ledger verification.

## Principle

The provenance ledger is an audit trail, not a replacement for the domain stores. Domain records retain their own structured data while the ledger records how those records were produced or changed.

## Next

CINE002.30 — unified Cinema Knowledge Governance dashboard: research tasks, evidence, conflicts, reliability, provenance and review queues in one operational console.
