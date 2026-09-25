# CINE002.21 — Entity-Aware Retrieval & Source-Backed Research Orchestration

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Turn knowledge gaps discovered by CinemaOS into explicit, auditable research tasks.

## Flow

    Entity
      |
    Existing Knowledge
      |
    Requested Question
      |
    Missing Fields
      |
    Research Task
      |
    Approved Source Types
      |
    Future Collector Execution
      |
    Evidence
      |
    Validation / Review
      |
    Knowledge Update

## Research task

Each task records:

- task ID
- entity ID
- question
- missing/requested fields
- preferred source types
- status
- creation time
- evidence count
- notes

## API

POST /api/v1/cinema/research/plan

GET /api/v1/cinema/research/tasks

## UI

apps/cinema-intelligence/research.py provides a research planning console.

## Safety and provenance

CINE002.21 intentionally separates **research planning** from external collection. Creating a task does not silently browse or mutate knowledge. A later execution stage can run only approved collectors and feed results through the existing validation, provenance, contradiction, review and persistence pipeline.

## Next

CINE002.22 — controlled research execution: run approved collectors against a research task and attach returned evidence to the task.
