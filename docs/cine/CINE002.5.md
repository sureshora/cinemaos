# CINE002.5 — FastAPI Knowledge API & Streamlit API Client

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Expose the persistent Cinema Knowledge Store through FastAPI so Streamlit, Next.js and future CinemaOS agents can use the same data source.

## API

GET /api/v1/cinema/artists?q=&industry=

GET /api/v1/cinema/artists/{canonical_artist_id}

## Architecture

    Cinema collectors
          |
    normalized persistent store
          |
       FastAPI
       /     \
 Streamlit  Next.js
          |
       Agents

## Important boundary

The Streamlit application remains a client. It does not own the production data model.

## Current MVP

The API reads the dependency-free persistent store. Authentication, pagination, PostgreSQL, source-specific permissions and advanced filtering are deliberately deferred.

## Next

CINE002.6 — source/evidence model, collection-run tracking and API metadata so every fact can be traced to where and when it was collected.
