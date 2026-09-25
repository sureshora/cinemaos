from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Knowledge Quality", page_icon="🧭", layout="wide")
st.title("🧭 CinemaOS Knowledge Quality & Lineage")
st.caption("Trace every artist record from collection to persisted knowledge")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
artist_id = st.text_input("Canonical Artist ID")

if artist_id:
    try:
        quality = requests.get(f"{base}/api/v1/cinema/artists/{artist_id}/quality", timeout=10)
        lineage = requests.get(f"{base}/api/v1/cinema/artists/{artist_id}/lineage", timeout=10)
        quality.raise_for_status()
        lineage.raise_for_status()
    except requests.RequestException as exc:
        st.error(f"Unable to retrieve lineage: {exc}")
        st.stop()

    payload = quality.json()
    score = payload.get("score", 0)
    st.metric("Knowledge Quality Score", f"{score}%")

    st.subheader("Quality checks")
    st.json(payload.get("checks", {}))

    st.subheader("Knowledge lineage")
    events = lineage.json().get("events", [])
    for event in events:
        st.markdown(
            f"**{event.get('event_type')}** · {event.get('stage')} · "
            f"{event.get('occurred_at')}"
        )
        if event.get("input_ref"):
            st.caption(f"Input: {event['input_ref']}")
        if event.get("output_ref"):
            st.caption(f"Output: {event['output_ref']}")
        if event.get("details"):
            st.json(event["details"])
        st.divider()
