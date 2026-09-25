from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Confidence", page_icon="🎯", layout="wide")
st.title("🎯 CinemaOS Confidence & Source Reliability")
st.caption("Source reliability × freshness × corroboration × review status")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
entity_id = st.text_input("Canonical Entity ID")

if entity_id:
    try:
        response = requests.get(
            f"{base}/api/v1/cinema/entities/{entity_id}/confidence",
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        st.error(f"Confidence API unavailable: {exc}")
        st.stop()

    score = payload.get("score", 0)
    st.metric("Calibrated MVP Confidence", f"{score * 100:.1f}%")
    st.write("Label:", payload.get("label", "unknown"))

    sources = payload.get("sources", [])
    if sources:
        st.subheader("Source profiles")
        st.dataframe(sources, use_container_width=True, hide_index=True)
    else:
        st.info("No source evidence is available.")
