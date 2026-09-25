# CINE002.22 — Controlled Research Execution

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Execute an approved research task against an explicitly approved collector while keeping collected evidence separate from trusted knowledge.

## Execution flow

    Research Task
         |
    Explicit Approval
         |
    Approved Collector
         |
    Source Retrieval
         |
    Evidence Candidates
         |
    Validation
         |
    Contradiction Detection
         |
    Human Review
         |
    Knowledge Persistence

## API

POST /api/v1/cinema/research/tasks/{task_id}/execute

Parameters:

- task_id
- collector_module
- approved=true

Execution is rejected unless explicit approval is supplied.

## Collector boundary

The MVP accepts only collector modules under the approved collectors namespace.

## Important trust boundary

Collected records are returned as **evidence candidates**. CINE002.22 does not automatically promote them to trusted knowledge.

## UI

apps/cinema-intelligence/research_execute.py provides a gated execution console.

## Next

CINE002.23 — automatic evidence snapshotting, validation and provenance attachment for research results.
