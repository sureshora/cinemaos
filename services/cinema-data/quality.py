from __future__ import annotations

from typing import Any

from .lineage import calculate_quality_score


def score_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    scored = []
    for record in records:
        item = dict(record)
        quality = calculate_quality_score(item)
        item["quality"] = quality
        scored.append(item)

    scores = [item["quality"]["score"] for item in scored]
    return {
        "records": scored,
        "count": len(scored),
        "average_score": round(sum(scores) / len(scores), 1) if scores else 0.0,
        "below_80": sum(score < 80 for score in scores),
        "below_60": sum(score < 60 for score in scores),
    }
