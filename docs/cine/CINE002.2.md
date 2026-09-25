# CINE002.2 — Source Adapter Framework

## Status

IMPLEMENTED ON FEATURE BRANCH

## Objective

Make external or legacy Python collectors plug-and-play without coupling them to CinemaOS UI code.

## Adapter contract

Each adapter exposes:

    name = "source-name"

    def collect() -> list[dict]:
        ...

Adapters may wrap an existing collector, transform its output, and preserve source evidence.

## Included

- generic collector protocol
- normalization pipeline
- stable artist IDs
- historical merge
- source metadata preservation
- reference adapter
- command-line collector runner

## Integration pattern

    Existing collector
          |
          v
    Source adapter
          |
          v
    normalize_records()
          |
          v
    merge_artist_records()
          |
          v
    normalized cinema dataset

## Data quality rules

1. Never invent missing facts.
2. Preserve the original source URL whenever available.
3. Preserve collection timestamp.
4. Keep historical events instead of replacing them.
5. Treat aliases as entity-resolution inputs.
6. Keep uncertain/unverified records identifiable.
7. Keep demo data separate from collected production data.

## Next milestone

CINE002.3 will add entity resolution and deduplication across artist names, aliases, film credits and source records.
