from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Review Queue", page_icon="🧑‍⚖️", layout="wide")
st.title("🧑‍⚖️ CinemaOS Human Review Queue")
st.caption("Resolve ambiguous or contradictory historical cinema evidence")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
reviewer = st.sidebar.text_input("Reviewer", "cinema-researcher")

try:
    response = requests.get(
        f"{base}/api/v1/cinema/review/cases",
        params={"status": "open"},
        timeout=10,
    )
    response.raise_for_status()
    cases = response.json().get("cases", [])
except requests.RequestException as exc:
    st.error(f"Review API unavailable: {exc}")
    st.stop()

st.metric("Open review cases", len(cases))

for case in cases:
    with st.expander(
        f"{case.get('severity','medium').upper()} · "
        f"{case.get('entity_id')} · {case.get('field')}"
    ):
        st.write(case.get("reason", ""))
        if case.get("evidence"):
            st.json(case["evidence"])

        decision = st.selectbox(
            "Decision",
            ["accept_source_a", "accept_source_b", "accept_both", "reject", "needs_more_evidence"],
            key=f"decision-{case['case_id']}",
        )
        notes = st.text_area("Review notes", key=f"notes-{case['case_id']}")

        if st.button("Record decision", key=f"save-{case['case_id']}"):
            result = requests.post(
                f"{base}/api/v1/cinema/review/cases/{case['case_id']}/decision",
                params={"decision": decision, "reviewer": reviewer, "notes": notes},
                timeout=10,
            )
            result.raise_for_status()
            st.success("Decision recorded. Refresh to update the queue.")
