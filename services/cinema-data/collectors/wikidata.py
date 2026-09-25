from __future__ import annotations

import os
from typing import Any

import requests

name = "wikidata"

SPARQL_URL = "https://query.wikidata.org/sparql"

QUERY = """
SELECT ?person ?personLabel ?birthDate ?occupationLabel WHERE {
  VALUES ?person { wd:Q1395425 }
  OPTIONAL { ?person wdt:P569 ?birthDate. }
  OPTIONAL { ?person wdt:P106 ?occupation. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 50
"""


def collect() -> list[dict[str, Any]]:
    """Collect one verified seed artist from Wikidata.

    Seed IDs are intentionally explicit for the first production batch. This
    avoids broad uncontrolled harvesting and makes every imported identity
    auditable.
    """
    query = os.getenv("CINEMA_WIKIDATA_QUERY", QUERY)
    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "CinemaOS/0.1 (AdmnWizard cinema intelligence)",
    }
    response = requests.get(
        SPARQL_URL,
        params={"query": query, "format": "json"},
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    bindings = response.json()["results"]["bindings"]

    if not bindings:
        return []

    first = bindings[0]
    person_url = first["person"]["value"]
    person_id = person_url.rsplit("/", 1)[-1]
    name_value = first["personLabel"]["value"]

    occupations = sorted(
        {
            item["occupationLabel"]["value"]
            for item in bindings
            if item.get("occupationLabel")
        }
    )

    return [{
        "id": f"wikidata-{person_id}",
        "name": name_value,
        "roles": occupations,
        "sources": [{
            "source_url": f"https://www.wikidata.org/wiki/{person_id}",
            "source_name": "Wikidata",
            "source_type": "knowledge_graph",
            "evidence_status": "source-backed",
        }],
    }]
