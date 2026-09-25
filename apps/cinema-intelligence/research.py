from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Research Planner", page_icon="🔬", layout="wide")
st.title("🔬 CinemaOS Research Planner")
st.caption("Identify knowledge gaps and prepare source-backed research tasks")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
entity_id = st.text_input("Canonical Entity ID")
question = st.text_area("Research question")

fields = st.multiselect(
    "Fields to investigate",
    [
        "birth_date",
        "debut_year",
        "filmography",
        "directors",
        "producers",
        "writers",
        "music",
        "technicians",
        "awards",
        "career_events",
    ],
)

sources = st.multiselect(
    "Preferred source types",
    ["knowledge_graph", "film_database", "official_source", "archive"],
)

if st.button("Plan Research"):
    if not entity_id or not question.strip() or not fields:
        st.warning("Enter an entity, question and at least one field.")
        st.stop()

    try:
        response = requests.post(
            f"{base}/api/v1/cinema/research/plan",
            params={
                "entity_id": entity_id,
                "question": question,
                "requested_fields": ",".join(fields),
                "source_types": ",".join(sources),
            },
            timeout=15,
        )
        response.raise_for_status()
        task = response.json()
    except requests.RequestException as exc:
        st.error(f"Research API unavailable: {exc}")
        st.stop()

    st.success(f"Research task {task.get('task_id')} created")
    st.metric("Missing fields", len(task.get("missing_fields", [])))
    st.json(task)

st.divider()
st.subheader("Existing Research Tasks")

try:
    response = requests.get(f"{base}/api/v1/cinema/research/tasks", timeout=10)
    response.raise_for_status()
    tasks = response.json().get("tasks", [])
    st.dataframe(tasks, use_container_width=True, hide_index=True)
except requests.RequestException:
    st.info("Research task list unavailable.")
