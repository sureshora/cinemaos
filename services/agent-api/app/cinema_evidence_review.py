from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

DATA_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "cinema-data"
sys.path.insert(0, str(DATA_PACKAGE_ROOT))

from evidence_validation import EvidenceReviewStore, promote_fact, review_evidence  # noqa: E402
from fact_store import FactStore  # noqa: E402

REVIEWS = EvidenceReviewStore(DATA_PACKAGE_ROOT / "data" / "evidence_reviews.json")
FACTS = FactStore(DATA_PACKAGE_ROOT / "data" / "knowledge_facts.json")


def review(record: dict[str, Any], reviewer: str, decision: str, reason: str = "") -> dict[str, Any]:
    result = review_evidence(record, reviewer=reviewer, decision=decision, reason=reason)
    from evidence_validation import ReviewDecision
    REVIEWS.add(
        ReviewDecision(
            evidence_id=str(record["evidence_id"]),
            reviewer=reviewer,
            decision=decision,
            decided_at=str(result["reviewed_at"]),
            reason=reason,
        )
    )
    return result


def promote(evidence: dict[str, Any], property_name: str, value: Any, confidence: float) -> dict[str, Any]:
    return promote_fact(
        evidence,
        property_name=property_name,
        value=value,
        confidence=confidence,
        fact_store=FACTS,
    )
