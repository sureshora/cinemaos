from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Knowledge Governance", page_icon="🎬", layout="wide")
st.title("🎬 CinemaOS Knowledge Governance")
st.caption("Unified operational view of research, evidence, conflicts, confidence and provenance")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")

def get(path: str, params: dict | None = None) -> dict:
    response = requests.get(f"{base}{path}", params=params or {}, timeout=15)
    response.raise_for_status()
    return response.json()

try:
    tasks = get("/api/v1/cinema/research/tasks")
    evidence = get("/api/v1/cinema/research/evidence")
    conflicts = get("/api/v1/cinema/conflicts", {"status": "open"})
    ledger = get("/api/v1/cinema/provenance/verify")
except requests.RequestException as exc:
    st.error(f"Governance APIs unavailable: {exc}")
    st.stop()

task_items = tasks.get("tasks", [])
evidence_items = evidence.get("evidence", [])
conflict_items = conflicts.get("cases", [])

col1, col2, col3, col4 = st.columns(4)
col1.metric("Research Tasks", tasks.get("count", 0))
col2.metric("Evidence Records", evidence.get("count", 0))
col3.metric("Open Conflicts", conflicts.get("count", 0))
col4.metric("Ledger Events", ledger.get("event_count", 0))

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("🔬 Research Queue")
    if task_items:
        st.dataframe(task_items, use_container_width=True, hide_index=True)
    else:
        st.info("No research tasks.")

    st.subheader("🧾 Evidence")
    if evidence_items:
        st.dataframe(evidence_items, use_container_width=True, hide_index=True)
    else:
        st.info("No evidence records.")

with right:
    st.subheader("⚖️ Open Conflicts")
    if conflict_items:
        st.dataframe(conflict_items, use_container_width=True, hide_index=True)
    else:
        st.success("No open conflict cases.")

    st.subheader("🔐 Provenance Integrity")
    if ledger.get("valid"):
        st.success("Ledger integrity: PASS")
    else:
        st.error("Ledger integrity: FAILED")
        st.json(ledger)

st.divider()
st.subheader("Knowledge Governance Status")

status = {
    "research_tasks": len(task_items),
    "evidence_records": len(evidence_items),
    "open_conflicts": len(conflict_items),
    "provenance_valid": bool(ledger.get("valid")),
}
st.json(status)
