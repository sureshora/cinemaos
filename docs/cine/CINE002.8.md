# CINE002.8 — Controlled Ingestion CLI & Validation

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Make source ingestion repeatable, measurable and auditable.

## New components

- ingestion report model
- controlled ingestion CLI
- record validation
- collection-run persistence

## Report

Each run records:

- run ID
- collector
- start/end timestamps
- records received
- records resolved
- records persisted
- sources found
- review required
- status
- errors

## Validation

The validator checks the minimum source-backed artist contract:

- stable ID
- artist name
- sources collection
- source URL for each evidence record

Validation is deliberately conservative. A failed validation should stop production ingestion rather than silently creating low-quality historical records.

## Operational model

    collector
       |
       v
    validate
       |
       v
    resolve
       |
       v
    persist
       |
       v
    collection run report

## Next

CINE002.9 — API collection-run/status endpoints and an ingestion dashboard in Streamlit.
