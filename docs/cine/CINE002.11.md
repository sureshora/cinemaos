# CINE002.11 — Contradiction Detection & Human Review

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Prevent conflicting historical evidence from silently becoming a single asserted fact.

## Contradiction engine

CINE002.11 detects conflicting scalar values across source-backed records for selected fields such as:

- birth_date
- death_date
- debut_year

The detector reports the competing values and their available evidence.

## Human review

Review cases are persisted with:

- case ID
- entity
- field
- reason
- severity
- evidence
- status
- reviewer
- decision
- notes
- review timestamp

## API

GET /api/v1/cinema/review/cases?status=open

POST /api/v1/cinema/review/cases/{case_id}/decision

## UI

apps/cinema-intelligence/review.py provides a human review console.

## Decision model

Reviewers can record:

- accept_source_a
- accept_source_b
- accept_both
- reject
- needs_more_evidence

The system records the human decision rather than silently rewriting historical source data.

## World-class direction

Future versions should support field-level fact objects, weighted source reliability, temporal validity, contradiction graphs, reviewer roles, approval policies, double-review for critical facts, and immutable audit events.

## Next

CINE002.12 — fact-level knowledge model and confidence engine.
