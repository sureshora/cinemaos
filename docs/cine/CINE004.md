# CINE004 — Production Memory

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Establish durable, project-scoped memory for CinemaOS agents and production workflows.

## Memory types

- project
- session
- artifact
- decision
- character
- scene
- continuity
- production
- agent

## Memory scopes

- project
- season
- episode
- scene
- artifact
- session

## Contract

packages/contracts/src/memory.ts defines:

- MemoryRecord
- MemoryQuery
- MemoryWriteEvent
- memory type and scope enumerations

## Persistence

services/agent-api/app/memory.py provides a durable JSON-backed store for the MVP with:

- validation
- canonicalization
- upsert
- direct retrieval
- project-scoped search
- type filtering
- scope filtering
- entity filtering
- artifact filtering
- importance-aware ordering

## APIs

POST /api/v1/cinema/memory

GET /api/v1/cinema/memory/{memory_id}

POST /api/v1/cinema/memory/search

## UI

apps/cinema-intelligence/memory.py provides write and retrieval workflows.

## Architectural principle

Memory is project-scoped and separate from the canonical Cinema Knowledge graph. Knowledge answers what CinemaOS knows about the world; Production Memory records what a particular project, session or agent knows, decides or needs to remember.

## Next

CINE004.1 — Memory event ledger and append-only write history for auditable production memory.
