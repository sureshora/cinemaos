from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Provenance", page_icon="🔗", layout="wide")
st.title("🔗 CinemaOS Research Provenance Ledger")
st.caption("Trace a cinema knowledge subject from research through evidence, review and promotion")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
subject_id = st.text_input("Subject ID")

if st.button("Trace Lineage"):
    if not subject_id:
        st.warning("Enter a subject ID.")
        st.stop()
    try:
        response = requests.get(
            f"{base}/api/v1/cinema/provenance/{subject_id}",
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        st.error(f"Provenance API unavailable: {exc}")
        st.stop()

    st.metric("Provenance events", result.get("count", 0))
    for event in result.get("events", []):
        st.markdown(
            f"**{event.get('event_type')}** · "
            f"{event.get('timestamp')} · actor={event.get('actor')}"
        )
        st.caption(f"Event: {event.get('event_id')} · Hash: {event.get('event_hash')}")
        st.json(event.get("metadata", {}))
        st.divider()

st.subheader("Ledger Integrity")
if st.button("Verify Ledger"):
    try:
        response = requests.get(f"{base}/api/v1/cinema/provenance/verify", timeout=15)
        response.raise_for_status()
        result = response.json()
        if result.get("valid"):
            st.success(f"Ledger verified: {result.get('event_count', 0)} events")
        else:
            st.error("Ledger verification failed")
        st.json(result)
    except requests.RequestException as exc:
        st.error(f"Verification failed: {exc}")
