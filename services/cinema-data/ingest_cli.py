from __future__ import annotations

import argparse
import importlib
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .collection_runs import CollectionRun, CollectionRunStore
from .entity_resolution import resolve_artist_records
from .ingestion_report import IngestionReport
from .store import CinemaKnowledgeStore


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(module_name: str, store_path: str, run_store_path: str) -> IngestionReport:
    run_id = uuid.uuid4().hex[:12]
    started = utc_now_iso()
    report = IngestionReport(run_id=run_id, collector=module_name, started_at=started, errors=[])

    try:
        module = importlib.import_module(module_name)
        collect = getattr(module, "collect", None)
        if not callable(collect):
            raise TypeError(f"{module_name} must expose collect()")

        raw = list(collect())
        report.records_received = len(raw)

        resolved, review = resolve_artist_records(raw)
        report.records_resolved = len(resolved)
        report.review_required = len(review)
        report.sources_found = sum(len(item.get("sources", [])) for item in resolved)

        store = CinemaKnowledgeStore(store_path)
        store.upsert(resolved)
        report.records_persisted = len(resolved)
        report.status = "success"
    except Exception as exc:
        report.status = "failed"
        report.errors = [f"{type(exc).__name__}: {exc}"]
    finally:
        report.finished_at = utc_now_iso()

    run_store = CollectionRunStore(run_store_path)
    run_store.record(
        CollectionRun(
            run_id=report.run_id,
            collector=report.collector,
            started_at=report.started_at,
            finished_at=report.finished_at,
            records_received=report.records_received,
            records_persisted=report.records_persisted,
            status=report.status,
            errors=report.errors or [],
        )
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="CinemaOS controlled ingestion")
    parser.add_argument("module", help="Collector module path, e.g. services.cinema_data.collectors.tmdb")
    parser.add_argument("--store", default="services/cinema-data/data/cinema_knowledge.json")
    parser.add_argument("--runs", default="services/cinema-data/data/collection_runs.json")
    args = parser.parse_args()

    report = run(args.module, args.store, args.runs)
    print("CINEMAOS COLLECTION RUN")
    print("────────────────────────")
    print(f"Run ID: {report.run_id}")
    print(f"Collector: {report.collector}")
    print(f"Records received: {report.records_received}")
    print(f"Records resolved: {report.records_resolved}")
    print(f"Records persisted: {report.records_persisted}")
    print(f"Sources found: {report.sources_found}")
    print(f"Review required: {report.review_required}")
    print(f"Status: {report.status}")
    if report.errors:
        print(f"Errors: {report.errors}")


if __name__ == "__main__":
    main()
