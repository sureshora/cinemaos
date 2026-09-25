from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Source Ranking", page_icon="📊", layout="wide")
st.title("📊 CinemaOS Source Reliability & Evidence Ranking")
st.caption("Compare evidence using source profile, freshness, corroboration and conflict signals")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
source_json = st.text_area(
    "Evidence JSON array",
    value='[{"source_name":"Wikidata","source_type":"knowledge_graph","collected_at":"2026-09-25T00:00:00+00:00","corroborated":true,"temporally_consistent":true}]',
)

if st.button("Rank Evidence"):
    try:
        import json
        items = json.loads(source_json)
        response = requests.post(
            f"{base}/api/v1/cinema/evidence/rank",
            json=items,
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()
    except (ValueError, requests.RequestException) as exc:
        st.error(f"Ranking failed: {exc}")
        st.stop()

    st.dataframe(result.get("items", []), use_container_width=True, hide_index=True)
    st.json(result)

st.divider()
st.subheader("Aggregate Confidence")

contradicted = st.checkbox("Evidence is contradicted")
reviewed = st.checkbox("Evidence has human review")

if st.button("Calculate Confidence"):
    try:
        import json
        items = json.loads(source_json)
        response = requests.post(
            f"{base}/api/v1/cinema/evidence/confidence",
            params={"contradicted": contradicted, "reviewed": reviewed},
            json=items,
            timeout=15,
        )
        response.raise_for_status()
        st.json(response.json())
    except (ValueError, requests.RequestException) as exc:
        st.error(f"Confidence calculation failed: {exc}")
