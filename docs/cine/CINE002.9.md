# CINE002.9 — Cinema Intelligence Data Operations Console

Status: IMPLEMENTED ON FEATURE BRANCH

## Design target

World-class operational visibility for the CinemaOS knowledge ingestion platform.

## API

GET /api/v1/cinema/ops/summary

GET /api/v1/cinema/ops/runs?limit=25

## Dashboard

The Streamlit operations console exposes:

- artist count
- film-credit count
- career-event count
- award count
- evidence count
- latest collection status
- collection history
- operational data-quality principles

## Production architecture

    External Sources
          |
       Collectors
          |
       Validation
          |
    Entity Resolution
          |
       Provenance
          |
      Persistent Store
          |
        FastAPI
          |
    ┌─────┴─────┐
 Streamlit    Next.js
 Operations   Product UI
    Console
          |
       Agents

## World-class requirements for the next phase

The current console is the MVP control surface. The production target should add:

- PostgreSQL
- job scheduling and queues
- retries with exponential backoff
- rate-limit handling
- structured logs
- metrics and tracing
- data-quality scoring
- lineage graph
- human review queues
- source freshness monitoring
- schema/version migration
- role-based access control
- audit trail
- alerting
- connector health checks
- reproducible collection snapshots

CINE002.9 establishes the observable control-plane boundary without prematurely coupling the MVP to a specific infrastructure vendor.
