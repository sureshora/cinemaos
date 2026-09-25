# CINE002.6 — Evidence, Provenance & Collection Runs

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Make every collected cinema fact traceable to its source and collection run.

## Evidence fields

- source_url
- source_name
- source_type
- published_at
- collected_at
- collector
- evidence_status
- notes

## Collection runs

Every future collector execution can be recorded with:
- run ID
- collector
- start/end time
- received records
- persisted records
- status
- errors

## API

GET /api/v1/cinema/artists/{canonical_artist_id}/sources

## Data quality principle

CinemaOS should distinguish:
- collected
- source-backed
- unreviewed
- reviewed
- disputed
- rejected

The system must not silently turn an unverified source into a verified fact.

## Next

CINE002.7 — connect real source collectors and build the first production-quality artist ingestion batch.
