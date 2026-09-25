from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Cinema Brain", page_icon="🧠", layout="wide")
st.title("🧠 CinemaOS — Cinema Brain Query")
st.caption("Natural-language planning over the Cinema Knowledge Graph")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
start_id = st.sidebar.text_input("Start Entity ID")
max_hops = st.sidebar.slider("Maximum hops", 1, 8, 4)

query = st.text_area(
    "Ask a cinema knowledge question",
    placeholder="Which directors worked with this artist and what other films did they direct?",
)

if st.button("Run Cinema Brain Query"):
    if not start_id or not query.strip():
        st.warning("Enter both a start entity ID and a question.")
        st.stop()

    try:
        response = requests.post(
            f"{base}/api/v1/cinema/query",
            params={"query": query, "start_id": start_id, "max_hops": max_hops},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        st.error(f"Cinema Brain API unavailable: {exc}")
        st.stop()

    plan = payload.get("plan", {})
    st.subheader("Query Plan")
    st.json(plan)

    st.metric("Paths Found", payload.get("count", 0))

    st.subheader("Explainable Paths")
    for index, path in enumerate(payload.get("paths", []), start=1):
        with st.expander(f"Path {index} · {path.get('hops', 0)} hops"):
            for node_index, node in enumerate(path.get("nodes", [])):
                st.markdown(f"**{node.get('label', node.get('id'))}** · {node.get('type', 'entity')}")
                edges = path.get("edges", [])
                if node_index < len(edges):
                    st.caption(f"↓ {edges[node_index].get('relationship_type')}")

    with st.expander("Raw response"):
        st.json(payload)
