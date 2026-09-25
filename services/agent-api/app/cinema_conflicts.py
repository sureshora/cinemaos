from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from conflict_cases import ConflictCaseStore, create_conflict_case  # noqa: E402
from fact_store import FactStore  # noqa: E402

CASES = ConflictCaseStore(DATA_PACKAGE_ROOT / "data" / "conflict_cases.json")
FACTS = FactStore(DATA_PACKAGE_ROOT / "data" / "knowledge_facts.json")


def create_case(
    *,
    entity_id: str,
    property_name: str,
    evidence_ids: list[str],
    fact_ids: list[str],
    notes: str = "",
) -> dict[str, Any]:
    case = create_conflict_case(
        entity_id=entity_id,
        property_name=property_name,
        evidence_ids=evidence_ids,
        fact_ids=fact_ids,
        notes=notes,
    )
    CASES.add(case)
    return case.to_dict()


def list_cases(status: str | None = None) -> list[dict[str, Any]]:
    cases = CASES.load()
    return [case for case in cases if not status or case.get("status") == status]


def resolve_case(
    case_id: str,
    *,
    reviewer: str,
    resolution: str,
    notes: str = "",
) -> dict[str, Any]:
    allowed = {"accept_existing", "accept_new", "retain_conflict", "reject_both"}
    if resolution not in allowed:
        raise ValueError(f"resolution must be one of {sorted(allowed)}")

    result = CASES.update(
        case_id,
        status="resolved",
        reviewer=reviewer,
        resolution=resolution,
        notes=notes,
    )
    if result is None:
        raise KeyError(f"Conflict case not found: {case_id}")
    return result
