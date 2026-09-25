from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Knowledge API", page_icon="🎬", layout="wide")
st.title("🎬 CinemaOS — Knowledge API Client")
st.caption("Streamlit client connected to the shared FastAPI Cinema Knowledge API")

base_url = st.sidebar.text_input("API base URL", "http://localhost:8080").rstrip("/")
query = st.text_input("Artist search")
industry = st.text_input("Industry filter")

if st.button("Search"):
    response = requests.get(
        f"{base_url}/api/v1/cinema/artists",
        params={"q": query, "industry": industry},
        timeout=10,
    )
    response.raise_for_status()
    payload = response.json()
    st.metric("Artists returned", payload["count"])
    st.dataframe(payload["artists"], use_container_width=True, hide_index=True)
