# CINE002.26 — Conflict Case Management & Evidence Comparison

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Turn conflicting cinema evidence into explicit review cases instead of silently overwriting facts.

## Conflict case

A case records:

- case ID
- entity ID
- property name
- evidence IDs
- fact IDs
- status
- reviewer
- resolution
- notes
- creation time

## Resolution options

- accept_existing
- accept_new
- retain_conflict
- reject_both

These options are deliberately explicit. The system does not infer the correct historical answer automatically.

## APIs

POST /api/v1/cinema/conflicts

GET /api/v1/cinema/conflicts

POST /api/v1/cinema/conflicts/{case_id}/resolve

## UI

apps/cinema-intelligence/conflicts.py provides a conflict-review console.

## Architecture

Conflicts remain separate from canonical facts until a human resolution is recorded. This preserves competing evidence and makes historical disagreements auditable.

## Next

CINE002.27 — temporal conflict analysis: compare validity periods, publication dates, observation dates and source freshness before presenting a conflict to the reviewer.
