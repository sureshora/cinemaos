from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Event Graph", page_icon="🕸️", layout="wide")
st.title("🕸️ CinemaOS Temporal Event Graph")
st.caption("Career events, films and awards connected to an artist timeline")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
entity_id = st.text_input("Canonical Entity ID")

if entity_id:
    try:
        response = requests.get(
            f"{base}/api/v1/cinema/entities/{entity_id}/event-graph",
            timeout=10,
        )
        response.raise_for_status()
        graph = response.json()
    except requests.RequestException as exc:
        st.error(f"Event Graph API unavailable: {exc}")
        st.stop()

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    events = graph.get("events", [])

    a, b, c = st.columns(3)
    a.metric("Nodes", len(nodes))
    b.metric("Relationships", len(edges))
    c.metric("Timeline Events", len(events))

    st.subheader("Historical Timeline")
    for event in events:
        date = event.get("event_date") or "Unknown date"
        st.markdown(f"**{date} — {event.get('title')}**")
        st.caption(event.get("event_type", "event"))
        if event.get("source_refs"):
            st.write("Evidence:", event["source_refs"])
        st.divider()

    with st.expander("Graph JSON"):
        st.json({"nodes": nodes, "edges": edges})
