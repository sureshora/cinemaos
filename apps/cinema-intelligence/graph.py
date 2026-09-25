from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Knowledge Graph", page_icon="🕸️", layout="wide")
st.title("🕸️ CinemaOS Knowledge Graph")
st.caption("Artists • Films • Directors • Producers • Writers • Music • Technicians • Awards")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
entity_id = st.sidebar.text_input("Artist Entity ID (optional)")

if st.button("Build Graph"):
    try:
        response = requests.get(
            f"{base}/api/v1/cinema/graph",
            params={"entity_id": entity_id} if entity_id else {},
            timeout=15,
        )
        response.raise_for_status()
        graph = response.json()
    except requests.RequestException as exc:
        st.error(f"Graph API unavailable: {exc}")
        st.stop()

    a, b = st.columns(2)
    a.metric("Nodes", graph.get("node_count", 0))
    b.metric("Relationships", graph.get("edge_count", 0))

    st.subheader("Entities")
    st.dataframe(graph.get("nodes", []), use_container_width=True, hide_index=True)

    st.subheader("Relationships")
    st.dataframe(graph.get("edges", []), use_container_width=True, hide_index=True)

    with st.expander("Graph JSON"):
        st.json(graph)
