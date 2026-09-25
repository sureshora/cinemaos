from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Versions", page_icon="🗂️", layout="wide")
st.title("🗂️ CinemaOS Knowledge Versions")
st.caption("Reproducible views of what CinemaOS knew at a specific point in time")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
entity_id = st.text_input("Canonical Entity ID")

if entity_id:
    try:
        response = requests.get(
            f"{base}/api/v1/cinema/entities/{entity_id}/versions",
            timeout=10,
        )
        response.raise_for_status()
        versions = response.json().get("versions", [])
    except requests.RequestException as exc:
        st.error(f"Version API unavailable: {exc}")
        st.stop()

    st.metric("Knowledge versions", len(versions))
    for version in reversed(versions):
        st.subheader(version.get("version_id"))
        st.json(version)
        st.divider()
