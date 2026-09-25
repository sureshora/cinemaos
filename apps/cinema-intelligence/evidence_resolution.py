from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Evidence Resolution", page_icon="🧩", layout="wide")
st.title("🧩 CinemaOS Evidence Resolution")
st.caption("Detect equivalent facts, conflicts and confidence changes before promotion")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
entity_id = st.text_input("Entity ID")
property_name = st.text_input("Property")
value = st.text_input("Candidate value")
source_score = st.slider("Source score", 0.0, 1.0, 0.75, 0.01)

if st.button("Resolve Evidence"):
    if not entity_id or not property_name:
        st.warning("Entity ID and property are required.")
        st.stop()

    try:
        response = requests.post(
            f"{base}/api/v1/cinema/research/evidence/resolve",
            params={
                "entity_id": entity_id,
                "property_name": property_name,
                "value": value,
                "source_score": source_score,
            },
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        st.error(f"Resolution API unavailable: {exc}")
        st.stop()

    status = result.get("status", "unknown")
    if status == "new":
        st.success("New fact candidate")
    elif status == "duplicate":
        st.info("Equivalent fact already exists")
    else:
        st.error("Conflicting fact detected")

    st.metric("Recalculated confidence", f"{float(result.get('confidence', 0)) * 100:.1f}%")
    st.json(result)
