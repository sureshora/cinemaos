# CINE002.1 — Collector Integration & Historical Normalization

## Status

IMPLEMENTED ON FEATURE BRANCH

## Purpose

Create the integration boundary for existing Python collectors without coupling collector code to Streamlit.

## Contract

Every collector module exposes:

    name = "source-name"

    def collect() -> list[dict]:
        ...

The returned records are normalized, assigned stable IDs when needed, stamped with collection metadata, and merged without discarding historical events.

## Run

From repository root:

    python -m services.cinema-data.run_collectors services.cinema-data.collectors.example_adapter

The reference adapter intentionally returns zero records. Replace it with the user's existing collector module or add a thin adapter around it.

## Important rule

CINE002.1 does not invent production facts. Demo records remain separate from collected records. Production data must retain source URLs and collection timestamps.

## Next

1. Bring the user's existing collector .py files into adapters.
2. Add entity resolution for names/aliases.
3. Add source-specific collectors.
4. Persist normalized records.
5. Expose the same records through FastAPI and the Next.js UI.
