# CINE002.20 — Evidence-Aware Cinema Brain Answer Synthesis

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Combine graph paths, knowledge facts, source evidence and confidence into a transparent Cinema Brain response.

## Pipeline

    Natural-language query
             |
        Query planning
             |
        Graph traversal
             |
       Temporal/fact context
             |
       Evidence extraction
             |
       Confidence signal
             |
      Grounded response

## API

POST /api/v1/cinema/answer

Parameters:

- query
- start_id
- max_hops

## Response contract

The response contains:

- summary
- answer type
- path count
- relationship counts
- confidence score and label
- source evidence
- supporting facts
- explainable paths
- query plan
- limitations

## Evidence principle

The system does not manufacture citations. Evidence is returned only from source references already attached to graph relationships.

## Confidence principle

Confidence is inherited from currently available knowledge facts. It is not presented as a probability of truth.

## Human oversight

The response explicitly states that disputed historical facts require review. This keeps human judgment in the loop instead of silently converting graph traversal into an authoritative conclusion.

## UI

apps/cinema-intelligence/answer.py provides the grounded answer explorer.

## Next

CINE002.21 — entity-aware retrieval and source-backed research orchestration.
