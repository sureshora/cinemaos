from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class SourceProfile:
    source_name: str
    source_type: str = "web"
    base_reliability: float = 0.50
    freshness_days: int = 365
    verified: bool = False
    notes: str = ""


DEFAULT_PROFILES = {
    "Wikidata": SourceProfile("Wikidata", "knowledge_graph", 0.80, 180, True),
    "The Movie Database": SourceProfile("The Movie Database", "film_database", 0.75, 90, True),
}


def freshness_factor(collected_at: str | None, freshness_days: int) -> float:
    if not collected_at:
        return 0.50
    try:
        collected = datetime.fromisoformat(collected_at.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        age_days = max(0, (now - collected).days)
    except ValueError:
        return 0.50

    if age_days <= freshness_days:
        return 1.0
    if age_days >= freshness_days * 3:
        return 0.40
    return round(1.0 - 0.6 * ((age_days - freshness_days) / (freshness_days * 2)), 3)


def score_source(source: dict[str, Any]) -> dict[str, Any]:
    name = str(source.get("source_name", "Unknown"))
    profile = DEFAULT_PROFILES.get(name, SourceProfile(name))

    reliability = profile.base_reliability
    if source.get("evidence_status") == "reviewed":
        reliability = min(1.0, reliability + 0.10)

    freshness = freshness_factor(
        source.get("collected_at"),
        profile.freshness_days,
    )

    score = round(reliability * freshness, 3)
    return {
        "source_name": name,
        "source_type": profile.source_type,
        "reliability": reliability,
        "freshness_factor": freshness,
        "score": score,
        "profile": asdict(profile),
    }


def aggregate_source_confidence(
    sources: list[dict[str, Any]],
    *,
    contradicted: bool = False,
    reviewed: bool = False,
) -> dict[str, Any]:
    scored = [score_source(source) for source in sources]
    if not scored:
        return {"score": 0.0, "label": "unknown", "sources": []}

    # Independent corroboration increases confidence, with diminishing returns.
    weighted = sorted((item["score"] for item in scored), reverse=True)
    confidence = weighted[0]
    for index, value in enumerate(weighted[1:], start=1):
        confidence += value * (0.35 / (index + 1))

    if reviewed:
        confidence += 0.10
    if contradicted:
        confidence -= 0.30

    confidence = round(max(0.0, min(1.0, confidence)), 3)

    if confidence >= 0.90:
        label = "very_high"
    elif confidence >= 0.75:
        label = "high"
    elif confidence >= 0.50:
        label = "medium"
    elif confidence > 0:
        label = "low"
    else:
        label = "unknown"

    return {"score": confidence, "label": label, "sources": scored}


def rank_evidence(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ranked = []
    for item in items:
        score = score_source(item)
        if item.get("corroborated"): score["score"] = min(1.0, round(score["score"] + 0.05, 3))
        if item.get("temporally_consistent"): score["score"] = min(1.0, round(score["score"] + 0.03, 3))
        if item.get("conflicting"): score["score"] = max(0.0, round(score["score"] - 0.20, 3))
        ranked.append({**item, "reliability": score})
    return sorted(ranked, key=lambda item: item["reliability"]["score"], reverse=True)
