# CINE002.28 — Source Reliability Scoring & Conflict-Aware Evidence Ranking

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Provide transparent source reliability and evidence ranking signals for research and conflict review.

## Reliability factors

The MVP considers:

- source profile
- base reliability
- collection freshness
- human review
- corroboration
- temporal consistency
- contradiction penalty

## Source profiles

Profiles can represent sources such as:

- official sources
- official archives
- major publications
- knowledge graphs
- film databases

Unknown sources receive a conservative default profile.

## APIs

POST /api/v1/cinema/evidence/rank

POST /api/v1/cinema/evidence/confidence

## UI

apps/cinema-intelligence/source_ranking.py provides source ranking and aggregate confidence inspection.

## Important interpretation rule

Reliability and confidence are decision-support signals, not claims that a source is objectively true. They should help a reviewer prioritize evidence, not replace source inspection.

## Next

CINE002.29 — research provenance ledger and end-to-end lineage: connect source, snapshot, collector run, evidence, conflict, review and knowledge version into one auditable chain.
