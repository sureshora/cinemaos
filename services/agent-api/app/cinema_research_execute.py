from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from research_executor import ResearchExecutor  # noqa: E402
from research_store import ResearchTaskStore  # noqa: E402

TASKS = ResearchTaskStore(DATA_PACKAGE_ROOT / "data" / "research_tasks.json")
EXECUTOR = ResearchExecutor(TASKS)


def execute_research(
    task_id: str,
    collector_module: str,
    *,
    approved: bool = False,
) -> dict[str, Any]:
    return EXECUTOR.execute(
        task_id,
        collector_module,
        approved=approved,
    )
