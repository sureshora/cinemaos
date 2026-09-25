from __future__ import annotations

import requests
import streamlit as st

st.set_page_config(page_title="CinemaOS — Temporal Conflicts", page_icon="🕰️", layout="wide")
st.title("🕰️ CinemaOS Temporal Conflict Analysis")
st.caption("Compare event dates, validity intervals, publication dates and freshness")

base = st.sidebar.text_input("FastAPI URL", "http://localhost:8080").rstrip("/")


def source_editor(title: str, key_prefix: str) -> dict[str, str]:
    st.subheader(title)
    return {
        "event_date": st.text_input("Event date", key=f"{key_prefix}-event"),
        "valid_from": st.text_input("Valid from", key=f"{key_prefix}-from"),
        "valid_to": st.text_input("Valid to", key=f"{key_prefix}-to"),
        "published_at": st.text_input("Published at", key=f"{key_prefix}-pub"),
        "source_url": st.text_input("Source URL", key=f"{key_prefix}-url"),
        "source_name": st.text_input("Source name", key=f"{key_prefix}-name"),
    }

left, right = st.columns(2)
with left:
    source_a = source_editor("Evidence A", "left")
with right:
    source_b = source_editor("Evidence B", "right")

if st.button("Compare Temporal Evidence"):
    try:
        response = requests.post(
            f"{base}/api/v1/cinema/conflicts/temporal-analysis",
            json={"left": source_a, "right": source_b},
            timeout=15,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        st.error(f"Temporal analysis unavailable: {exc}")
        st.stop()

    st.subheader("Temporal Assessment")
    st.json(result)
    st.metric("Temporal relation", result.get("temporal_relation", "unknown"))
    st.metric("Publication order", result.get("publication_order", "unknown"))
    if result.get("overlap_days") is not None:
        st.metric("Validity overlap", f"{result['overlap_days']} days")

    for note in result.get("notes", []):
        st.info(note)
