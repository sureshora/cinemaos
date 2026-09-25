from __future__ import annotations

import os
from typing import Any

import requests

name = "tmdb"

API_BASE = "https://api.themoviedb.org/3"


def collect() -> list[dict[str, Any]]:
    """Collect a person selected explicitly through TMDB_PERSON_ID.

    No broad crawl is performed. The API key and person ID must be supplied
    through environment variables.
    """
    api_key = os.getenv("TMDB_API_KEY")
    person_id = os.getenv("TMDB_PERSON_ID")

    if not api_key or not person_id:
        return []

    response = requests.get(
        f"{API_BASE}/person/{person_id}",
        params={"api_key": api_key, "append_to_response": "combined_credits"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    credits = []
    for item in payload.get("combined_credits", {}).get("cast", []):
        credits.append({
            "year": (item.get("release_date") or item.get("first_air_date") or "")[:4],
            "title": item.get("title") or item.get("name") or "",
            "language": item.get("original_language") or "",
            "role": "Actor",
            "character": item.get("character") or "",
            "source_url": f"https://www.themoviedb.org/person/{person_id}",
        })

    return [{
        "id": f"tmdb-{person_id}",
        "name": payload.get("name") or "",
        "roles": ["Actor"] if payload.get("known_for_department") == "Acting" else [],
        "profile_image": payload.get("profile_path") or "",
        "filmography": credits,
        "sources": [{
            "source_url": f"https://www.themoviedb.org/person/{person_id}",
            "source_name": "The Movie Database",
            "source_type": "film_database",
            "evidence_status": "source-backed",
        }],
    }]
