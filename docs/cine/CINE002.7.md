# CINE002.7 — Controlled Source Collectors & First Production Ingestion Boundary

Status: IMPLEMENTED ON FEATURE BRANCH

## Sources

### Wikidata

A controlled SPARQL collector is included. It uses an explicit seed query and preserves the Wikidata entity URL as evidence.

### TMDB

A controlled person collector is included. It requires:
- TMDB_API_KEY
- TMDB_PERSON_ID

It fetches one explicitly selected person and their combined credits. No broad crawl is performed.

## Why controlled ingestion

The first production batch should be auditable. CinemaOS should not ingest thousands of uncertain records before validating identity resolution, provenance and historical merge behavior.

## Pipeline

source API -> collector -> source evidence -> normalization -> entity resolution -> persistent store -> FastAPI -> UI

## Environment

Copy services/cinema-data/.env.example into the local environment and provide credentials only where required.

## Next

CINE002.8 — ingestion CLI integration, validation report, and first repeatable collection run with persisted run metadata.
