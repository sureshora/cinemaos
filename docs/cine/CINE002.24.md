# CINE002.24 — Evidence Validation & Controlled Knowledge Promotion

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Create a hard trust boundary between collected evidence and canonical Cinema Knowledge Facts.

## Workflow

    Evidence Candidate
         |
    Schema Validation
         |
    Duplicate/identity checks
         |
    Human Review
       / | \
 approved  needs_review  rejected
     |
 Controlled Promotion
     |
 Knowledge Fact
     |
 Confidence / Lineage

## Validation

Evidence is checked for required identifiers and a valid SHA-256 content hash.

## Review

Review decisions are explicitly recorded with:

- evidence ID
- reviewer
- decision
- timestamp
- reason

Allowed decisions:

- approved
- needs_review
- rejected

## Promotion

Only evidence with review_status=approved can be promoted.

The generated Knowledge Fact contains lineage back to:

- evidence
- source snapshot
- research task

## APIs

POST /api/v1/cinema/research/evidence/review

POST /api/v1/cinema/research/evidence/promote

## UI

apps/cinema-intelligence/evidence_review.py provides the human review and promotion console.

## Important limitation

The MVP uses explicit human review rather than automated truth determination. Duplicate detection and deeper source-consistency checks should be strengthened in later iterations.

## Next

CINE002.25 — evidence deduplication, contradiction-aware promotion and confidence recalculation.
