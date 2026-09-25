from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Grounded Answers", page_icon="💡", layout="wide")
st.title("💡 CinemaOS Evidence-Grounded Answers")
st.caption("Graph paths + facts + evidence + confidence, presented with limitations")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
start_id = st.sidebar.text_input("Start Entity ID")
max_hops = st.sidebar.slider("Maximum hops", 1, 8, 4)

query = st.text_area(
    "Cinema question",
    placeholder="Which directors worked with this artist and what other films did they direct?",
)

if st.button("Generate Grounded Answer"):
    if not start_id or not query.strip():
        st.warning("Enter a start entity ID and question.")
        st.stop()

    try:
        response = requests.post(
            f"{base}/api/v1/cinema/answer",
            params={"query": query, "start_id": start_id, "max_hops": max_hops},
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        st.error(f"Grounded Answer API unavailable: {exc}")
        st.stop()

    st.subheader("Answer")
    st.write(payload.get("summary", ""))

    confidence = payload.get("confidence", {})
    st.metric(
        "Knowledge Confidence",
        f"{float(confidence.get('score', 0)) * 100:.1f}%",
        confidence.get("label", "unknown"),
    )

    st.subheader("Evidence")
    for item in payload.get("evidence", []):
        st.markdown(
            f"- **{item.get('relationship')}** · "
            f"{item.get('source_url')}"
        )

    st.subheader("Explainable Paths")
    for index, path in enumerate(payload.get("paths", []), start=1):
        with st.expander(f"Path {index} · {path.get('hops', 0)} hops"):
            for node_index, node in enumerate(path.get("nodes", [])):
                st.markdown(
                    f"**{node.get('label', node.get('id'))}** "
                    f"· {node.get('type', 'entity')}"
                )
                edges = path.get("edges", [])
                if node_index < len(edges):
                    st.caption(f"↓ {edges[node_index].get('relationship_type')}")

    st.subheader("Limitations")
    for limitation in payload.get("limitations", []):
        st.info(limitation)

    with st.expander("Query Plan"):
        st.json(payload.get("query_plan", {}))
