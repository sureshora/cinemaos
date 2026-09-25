from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Production Memory", page_icon="🧠", layout="wide")
st.title("🧠 CinemaOS Production Memory")
st.caption("Durable project, session, decision, character, scene and production memory")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
project_id = st.sidebar.text_input("Project ID")

tab_write, tab_search = st.tabs(["Write Memory", "Retrieve Memory"])

with tab_write:
    memory_type = st.selectbox(
        "Memory type",
        ["project", "session", "artifact", "decision", "character", "scene", "continuity", "production", "agent"],
    )
    scope = st.selectbox("Scope", ["project", "season", "episode", "scene", "artifact", "session"])
    title = st.text_input("Title")
    content = st.text_area("Memory content")
    importance = st.slider("Importance", 0.0, 1.0, 0.7, 0.01)

    if st.button("Save Memory"):
        if not project_id or not title or not content:
            st.warning("Project ID, title and content are required.")
            st.stop()

        payload = {
            "memoryType": memory_type,
            "scope": scope,
            "projectId": project_id,
            "title": title,
            "content": content,
            "importance": importance,
        }
        try:
            response = requests.post(f"{base}/api/v1/cinema/memory", json=payload, timeout=15)
            response.raise_for_status()
            st.success("Memory saved.")
            st.json(response.json())
        except requests.RequestException as exc:
            st.error(f"Memory API unavailable: {exc}")

with tab_search:
    query = st.text_input("Search memory")
    types = st.multiselect(
        "Memory types",
        ["project", "session", "artifact", "decision", "character", "scene", "continuity", "production", "agent"],
    )

    if st.button("Retrieve Memory"):
        if not project_id:
            st.warning("Project ID is required.")
            st.stop()

        payload = {"projectId": project_id, "query": query or None}
        if types:
            payload["memoryTypes"] = types

        try:
            response = requests.post(f"{base}/api/v1/cinema/memory/search", json=payload, timeout=15)
            response.raise_for_status()
            result = response.json()
            st.metric("Memories found", result.get("count", 0))
            st.dataframe(result.get("memories", []), use_container_width=True, hide_index=True)
        except requests.RequestException as exc:
            st.error(f"Memory search failed: {exc}")
