from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Data Operations", page_icon="🎬", layout="wide")

st.title("🎬 CinemaOS Data Operations")
st.caption("World-class observability surface for the Cinema Knowledge ingestion pipeline")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")
if st.sidebar.button("Refresh"):
    st.cache_data.clear()

try:
    summary = requests.get(f"{base}/api/v1/cinema/ops/summary", timeout=10).json()
    runs = requests.get(f"{base}/api/v1/cinema/ops/runs", timeout=10).json().get("runs", [])
except requests.RequestException as exc:
    st.error(f"API unavailable: {exc}")
    st.stop()

m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("Artists", summary.get("artists", 0))
m2.metric("Film Credits", summary.get("films_credits", 0))
m3.metric("Career Events", summary.get("career_events", 0))
m4.metric("Awards", summary.get("awards", 0))
m5.metric("Evidence", summary.get("evidence_records", 0))

st.divider()
last = summary.get("last_run")
if last:
    status = last.get("status", "unknown")
    if status == "success":
        st.success(f"Last collection: {last.get('collector')} • {last.get('finished_at')}")
    elif status == "failed":
        st.error(f"Last collection failed: {last.get('collector')} • {last.get('finished_at')}")
    else:
        st.warning(f"Last collection: {status}")
else:
    st.info("No collection runs recorded yet.")

st.subheader("Collection Run History")
if runs:
    st.dataframe(runs, use_container_width=True, hide_index=True)
else:
    st.info("No collection history yet.")

st.subheader("Operational Principles")
st.markdown("""
- **Traceability:** every production fact should retain source evidence.
- **Historical safety:** ingestion is append-oriented; older evidence is not silently deleted.
- **Conservative resolution:** ambiguous identities require review.
- **Repeatability:** every collector execution produces a run record.
- **Separation of concerns:** UI consumes the API; collectors never write into the UI.
""")
