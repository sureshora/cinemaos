from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Evidence", page_icon="🧾", layout="wide")
st.title("🧾 CinemaOS Evidence & Provenance")
st.caption("Capture source evidence with immutable snapshots and lineage")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
task_id = st.text_input("Research Task ID")
entity_id = st.text_input("Entity ID")

st.subheader("Evidence source")
source_name = st.text_input("Source name")
source_url = st.text_input("Source URL")
content = st.text_area("Captured source content")
collector = st.text_input("Collector", "manual")

if st.button("Capture Evidence"):
    if not task_id or not entity_id or not source_name or not source_url or not content:
        st.error("Task, entity, source name, URL and content are required.")
        st.stop()

    payload = [{
        "source_name": source_name,
        "source_url": source_url,
        "content": content,
        "collector": collector,
        "content_type": "text",
        "transformation_version": "v1",
    }]

    try:
        response = requests.post(
            f"{base}/api/v1/cinema/research/tasks/{task_id}/evidence",
            params={"entity_id": entity_id},
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        st.error(f"Evidence API unavailable: {exc}")
        st.stop()

    st.success(f"Captured {result.get('count', 0)} evidence record(s)")
    st.json(result)

st.divider()
st.subheader("Existing Evidence")

try:
    params = {"task_id": task_id} if task_id else {}
    response = requests.get(
        f"{base}/api/v1/cinema/research/evidence",
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    st.dataframe(
        response.json().get("evidence", []),
        use_container_width=True,
        hide_index=True,
    )
except requests.RequestException:
    st.info("Evidence list unavailable.")
