# CINE002.4 — Source-backed Ingestion & Persistent Normalized Storage

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Create a persistence boundary for normalized CinemaOS knowledge records.

## Flow

    source collector
          |
          v
    source adapter
          |
          v
    normalization
          |
          v
    entity resolution
          |
          v
    persistent knowledge store
          |
          +--> Streamlit
          +--> FastAPI
          +--> Next.js
          +--> Agents

## Current storage

The MVP uses a dependency-free JSON store under services/cinema-data/data. This is deliberately an abstraction boundary, not the final production database.

The store supports:
- load
- full save
- artist upsert
- historical list merging
- source/media preservation
- social-link merging

## Production migration path

The same store interface can later be backed by PostgreSQL with tables for:
- artists
- aliases
- films
- credits
- career_events
- awards
- media
- sources
- collection_runs
- entity_review_queue

## Data integrity

The ingestion layer preserves historical records and does not silently delete older evidence when a newer collection arrives.

## Next

CINE002.5 — expose the persistent knowledge store through FastAPI and connect the Streamlit UI to the API.
