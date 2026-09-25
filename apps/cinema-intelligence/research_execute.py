from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Research Execution", page_icon="🧪", layout="wide")
st.title("🧪 CinemaOS Controlled Research Execution")
st.caption("Explicitly approve a collector, execute it, then route results through validation and review")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
task_id = st.text_input("Research Task ID")
collector = st.text_input(
    "Approved collector module",
    "collectors.tmdb",
)

st.warning(
    "Execution is intentionally gated. Results are evidence candidates and must "
    "pass validation and review before becoming trusted knowledge."
)

approved = st.checkbox("I explicitly approve this research execution")

if st.button("Execute Approved Research"):
    if not task_id or not collector or not approved:
        st.error("Task ID, collector module and explicit approval are required.")
        st.stop()

    try:
        response = requests.post(
            f"{base}/api/v1/cinema/research/tasks/{task_id}/execute",
            params={
                "collector_module": collector,
                "approved": "true",
            },
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        st.error(f"Research execution failed: {exc}")
        st.stop()

    st.success("Evidence collection completed. Validation/review is still required.")
    task = payload.get("task", {})
    a, b, c = st.columns(3)
    a.metric("Records returned", task.get("records_returned", 0))
    b.metric("Evidence found", task.get("evidence_found", 0))
    c.metric("Status", task.get("status", "unknown"))

    st.subheader("Collected evidence candidates")
    st.json(payload.get("records", []))
