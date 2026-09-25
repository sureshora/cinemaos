from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Graph Intelligence", page_icon="🔎", layout="wide")
st.title("🔎 CinemaOS Graph Intelligence")
st.caption("Explore multi-hop relationships across the Cinema Knowledge Graph")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
start_id = st.sidebar.text_input("Start Entity ID")
target_id = st.sidebar.text_input("Target Entity ID (optional)")
max_hops = st.sidebar.slider("Maximum hops", 1, 8, 3)
relationships = st.sidebar.text_input(
    "Relationship filter (optional)",
    placeholder="acted_in,directed_by,produced_by",
)

if st.button("Find Paths"):
    if not start_id:
        st.warning("Enter a start entity ID.")
        st.stop()

    try:
        response = requests.get(
            f"{base}/api/v1/cinema/graph/traverse",
            params={
                "start_id": start_id,
                "target_id": target_id or None,
                "max_hops": max_hops,
                "relationships": relationships,
            },
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        st.error(f"Traversal API unavailable: {exc}")
        st.stop()

    st.metric("Paths found", payload.get("count", 0))

    for index, path in enumerate(payload.get("paths", []), start=1):
        with st.expander(f"Path {index} · {path.get('hops', 0)} hops"):
            nodes = path.get("nodes", [])
            edges = path.get("edges", [])
            for node_index, node in enumerate(nodes):
                st.markdown(f"**{node.get('label', node.get('id'))}** · {node.get('type', 'entity')}")
                if node_index < len(edges):
                    st.caption(f"↓ {edges[node_index].get('relationship_type')}")
