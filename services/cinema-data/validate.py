from __future__ import annotations

from typing import Any


REQUIRED_ARTIST_FIELDS = ("id", "name", "sources")


def validate_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_ARTIST_FIELDS:
        if field not in record:
            errors.append(f"missing field: {field}")

    if not str(record.get("name", "")).strip():
        errors.append("empty artist name")

    sources = record.get("sources", [])
    if not isinstance(sources, list):
        errors.append("sources must be a list")
    else:
        for index, source in enumerate(sources):
            if not source.get("source_url"):
                errors.append(f"source[{index}] missing source_url")

    return errors


def validate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    failures = []
    for index, record in enumerate(records):
        errors = validate_record(record)
        if errors:
            failures.append({"index": index, "errors": errors})

    return {
        "valid": not failures,
        "records": len(records),
        "failures": failures,
    }
