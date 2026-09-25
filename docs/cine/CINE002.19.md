# CINE002.19 — Semantic Graph Queries & Cinema Brain Query Planning

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Translate a natural-language cinema question into an explicit, inspectable graph query plan.

## Pipeline

    Natural-language question
             |
        Query planner
             |
        Intent + constraints
             |
       Relationship plan
             |
        Graph traversal
             |
       Explainable paths
             |
        Evidence-ready result

## Query plan

The MVP identifies:

- intent
- relationship types
- maximum hops
- numeric relationship constraints
- year constraints
- expected answer shape

## API

POST /api/v1/cinema/query

Parameters:

- query
- start_id
- max_hops

## Explainability

The API returns the generated query plan together with graph paths. This allows the UI and future agents to inspect what the system attempted rather than treating the query as an opaque LLM operation.

## UI

apps/cinema-intelligence/query.py provides a natural-language Cinema Brain query explorer.

## Guardrails

The MVP:
- does not claim an LLM-generated answer
- uses deterministic relationship aliases
- bounds graph depth
- exposes the plan
- returns paths rather than unsupported conclusions

## Next

CINE002.20 — evidence-aware answer synthesis: combine graph paths, source evidence, temporal facts and confidence into a cited Cinema Brain response.
