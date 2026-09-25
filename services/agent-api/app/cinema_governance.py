from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from conflict_cases import ConflictCaseStore  # noqa: E402
from fact_store import FactStore  # noqa: E402
from provenance_ledger import ProvenanceLedger  # noqa: E402
from research_store import ResearchTaskStore  # noqa: E402

TASKS = ResearchTaskStore(DATA_PACKAGE_ROOT / "data" / "research_tasks.json")
CONFLICTS = ConflictCaseStore(DATA_PACKAGE_ROOT / "data" / "conflict_cases.json")
FACTS = FactStore(DATA_PACKAGE_ROOT / "data" / "knowledge_facts.json")
LEDGER = ProvenanceLedger(DATA_PACKAGE_ROOT / "data" / "provenance_ledger.json")


def governance_summary() -> dict[str, Any]:
    tasks = TASKS.load()
    conflicts = CONFLICTS.load()
    facts = FACTS.load()
    ledger = LEDGER.verify()

    return {
        "research": {
            "total": len(tasks),
            "ready": sum(item.get("status") == "ready" for item in tasks),
            "running": sum(item.get("status") == "running" for item in tasks),
            "evidence_collected": sum(item.get("status") == "evidence_collected" for item in tasks),
        },
        "conflicts": {
            "total": len(conflicts),
            "open": sum(item.get("status") == "open" for item in conflicts),
            "resolved": sum(item.get("status") == "resolved" for item in conflicts),
        },
        "knowledge": {
            "facts": len(facts),
        },
        "provenance": ledger,
        "overall_status": "healthy" if ledger.get("valid") else "attention_required",
    }
