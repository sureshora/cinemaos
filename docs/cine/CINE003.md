# CINE003 — Multimodal Artifact Contract

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Define one canonical contract for every multimodal artifact moving through CinemaOS.

## Supported artifact types

- document
- image
- audio
- video
- map
- historical_record
- screenplay
- scene
- character
- music
- production_asset

## Common contract

Every artifact has:

- stable artifact ID
- artifact type
- lifecycle status
- title and description
- MIME/media type
- storage location
- metadata
- source references
- lineage
- checksum
- schema version

## Lifecycle

    draft -> ingested -> processing -> ready -> review -> approved -> archived

Rejected artifacts remain explicitly identifiable.

## Provenance

Sources and lineage are first-class contract fields. Derived artifacts can reference parent artifacts and the operation that produced them.

## API

POST /api/v1/cinema/artifacts
GET /api/v1/cinema/artifacts/{artifact_id}
POST /api/v1/cinema/artifacts/search
POST /api/v1/cinema/artifacts/hash

## TypeScript contract

packages/contracts/src/artifacts.ts
packages/contracts/src/artifactSchemas.ts

## Python contract

services/agent-api/app/artifacts.py
services/agent-api/app/artifact_api.py

## Architectural purpose

CINE003 is the multimodal boundary between Cinema Knowledge and future CinemaOS agents. Research evidence, screenplay documents, scene assets, images, audio, video, maps and production artifacts can share the same lifecycle, provenance and lineage model while retaining type-specific metadata.

## Next

CINE004 — Production Memory: durable project, session, artifact and decision memory with retrieval boundaries.
