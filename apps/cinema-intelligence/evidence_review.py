from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Evidence Review", page_icon="✅", layout="wide")
st.title("✅ CinemaOS Evidence Review & Promotion")
st.caption("Validate evidence, record a human decision, then explicitly promote approved evidence into a Knowledge Fact")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
reviewer = st.sidebar.text_input("Reviewer", "human-reviewer")

evidence_json = st.text_area(
    "Evidence JSON",
    placeholder='{"evidence_id":"...","task_id":"...","entity_id":"...","source_url":"...","snapshot_id":"...","content_sha256":"..."}',
)

decision = st.selectbox("Decision", ["approved", "needs_review", "rejected"])
reason = st.text_area("Review reason")

if st.button("Review Evidence"):
    try:
        import json
        evidence = json.loads(evidence_json)
        response = requests.post(
            f"{base}/api/v1/cinema/research/evidence/review",
            params={"reviewer": reviewer, "decision": decision, "reason": reason},
            json=evidence,
            timeout=15,
        )
        response.raise_for_status()
        st.success("Review decision recorded.")
        st.json(response.json())
    except (ValueError, requests.RequestException) as exc:
        st.error(f"Review failed: {exc}")

st.divider()
st.subheader("Promote Approved Evidence")

property_name = st.text_input("Knowledge property")
value_text = st.text_input("Knowledge value")
confidence = st.slider("Confidence", 0.0, 1.0, 0.75, 0.01)

if st.button("Promote to Knowledge Fact"):
    try:
        import json
        evidence = json.loads(evidence_json)
        value = value_text
        response = requests.post(
            f"{base}/api/v1/cinema/research/evidence/promote",
            params={
                "property_name": property_name,
                "confidence": confidence,
            },
            json={**evidence, "review_status": "approved"},
            timeout=15,
        )
        response.raise_for_status()
        st.success("Evidence promoted to a Knowledge Fact.")
        st.json(response.json())
    except (ValueError, requests.RequestException) as exc:
        st.error(f"Promotion failed: {exc}")
