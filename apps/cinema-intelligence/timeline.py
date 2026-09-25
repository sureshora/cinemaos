from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Temporal Knowledge", page_icon="⏳", layout="wide")
st.title("⏳ CinemaOS Temporal Knowledge")
st.caption("Reconstruct what was known about an entity at a specific point in time")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
entity_id = st.text_input("Canonical Entity ID")
at = st.date_input("Historical date")

if entity_id:
    at_value = at.isoformat()
    try:
        response = requests.get(
            f"{base}/api/v1/cinema/entities/{entity_id}/state",
            params={"at": at_value},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        st.error(f"Temporal API unavailable: {exc}")
        st.stop()

    st.subheader(f"Knowledge state at {at_value}")
    state = payload.get("state", {})
    if not state:
        st.info("No temporal facts are available for this date.")
    for property_name, fact in state.items():
        st.markdown(f"### {property_name}")
        st.write(fact)
