# CINE002.3 — Artist Entity Resolution

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Prevent duplicate artist records while avoiding unsafe automatic merges.

## Resolution rules

1. Normalize Unicode and case.
2. Normalize punctuation and whitespace.
3. Match canonical names exactly.
4. Match explicitly supplied aliases exactly.
5. Assign a stable canonical_artist_id.
6. Do not automatically fuzzy-merge ambiguous names.
7. Preserve unresolved/ambiguous records for later review.

Example:

    Rajinikanth
    Rajni
    Rajinikanth Superstar

may be represented as aliases of one canonical artist only when that relationship is explicitly supplied or otherwise verified by the data pipeline.

## Safety principle

False merges are more damaging than duplicate records in a historical knowledge system. CINE002.3 therefore uses conservative exact matching. Fuzzy similarity and human review will be added as a separate quality-controlled stage.

## Next

CINE002.4 — source-backed ingestion and persistent normalized storage.
