from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Conflicts", page_icon="⚖️", layout="wide")
st.title("⚖️ CinemaOS Conflict Review")
st.caption("Compare conflicting evidence and record an explicit historical resolution")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
reviewer = st.sidebar.text_input("Reviewer", "human-reviewer")
status = st.sidebar.selectbox("Status", ["open", "resolved"])

try:
    response = requests.get(
        f"{base}/api/v1/cinema/conflicts",
        params={"status": status},
        timeout=10,
    )
    response.raise_for_status()
    cases = response.json().get("cases", [])
except requests.RequestException as exc:
    st.error(f"Conflict API unavailable: {exc}")
    st.stop()

st.metric("Conflict cases", len(cases))

for case in cases:
    with st.expander(
        f"{case.get('case_id')} · {case.get('entity_id')} · {case.get('property_name')}"
    ):
        st.write("Evidence IDs:", case.get("evidence_ids", []))
        st.write("Fact IDs:", case.get("fact_ids", []))
        st.write("Notes:", case.get("notes", ""))

        if case.get("status") == "open":
            resolution = st.selectbox(
                "Resolution",
                [
                    "accept_existing",
                    "accept_new",
                    "retain_conflict",
                    "reject_both",
                ],
                key=f"resolution-{case.get('case_id')}",
            )
            notes = st.text_area(
                "Resolution notes",
                key=f"notes-{case.get('case_id')}",
            )

            if st.button("Resolve Case", key=f"resolve-{case.get('case_id')}"):
                try:
                    result = requests.post(
                        f"{base}/api/v1/cinema/conflicts/{case.get('case_id')}/resolve",
                        params={
                            "reviewer": reviewer,
                            "resolution": resolution,
                            "notes": notes,
                        },
                        timeout=15,
                    )
                    result.raise_for_status()
                    st.success("Conflict case resolved.")
                    st.json(result.json())
                except requests.RequestException as exc:
                    st.error(f"Resolution failed: {exc}")
