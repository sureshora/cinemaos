from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Facts", page_icon="🧠", layout="wide")
st.title("🧠 CinemaOS Fact Explorer")
st.caption("Fact-level knowledge with confidence, evidence and lineage references")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
entity_id = st.text_input("Canonical Entity ID")

if entity_id:
    try:
        response = requests.get(
            f"{base}/api/v1/cinema/entities/{entity_id}/facts",
            timeout=10,
        )
        response.raise_for_status()
        facts = response.json().get("facts", [])
    except requests.RequestException as exc:
        st.error(f"Fact API unavailable: {exc}")
        st.stop()

    st.metric("Facts", len(facts))
    for fact in facts:
        st.subheader(f"{fact.get('property_name')} = {fact.get('value')}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Confidence", f"{fact.get('confidence', 0) * 100:.1f}%")
        c2.metric("Label", fact.get("confidence_label", "unknown"))
        c3.metric("Status", fact.get("status", "unreviewed"))
        st.write("Sources:", fact.get("source_refs", []))
        st.write("Lineage:", fact.get("lineage_refs", []))
        if fact.get("notes"):
            st.caption(fact["notes"])
        st.divider()
