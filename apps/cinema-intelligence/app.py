from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "sample_artists.json"

@st.cache_data
def load_artists() -> list[dict[str, Any]]:
    with DATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)

st.set_page_config(page_title="CinemaOS — Cinema Intelligence", page_icon="🎬", layout="wide")
st.title("🎬 CinemaOS — Cinema Intelligence")
st.write("Historical South Indian cinema knowledge MVP")
st.caption("Artist History • Filmography • Awards • Evidence • Social & Media")

with st.sidebar:
    st.header("Explore")
    query = st.text_input("Search artist", placeholder="Artist name")
    artists = load_artists()
    industries = sorted({a.get("industry","") for a in artists if a.get("industry")})
    industry = st.selectbox("Industry", ["All"] + industries)
    st.divider()
    st.subheader("Data Layer")
    st.success("Collector contract ready")
    st.info("Demo dataset loaded")

filtered = [a for a in artists if (industry == "All" or a.get("industry") == industry) and (not query or query.lower() in a.get("name","").lower())]
if not filtered:
    st.warning("No artist matches the current filters.")
    st.stop()

c1,c2,c3,c4=st.columns(4)
c1.metric("Artists",len(filtered))
c2.metric("Career events",sum(len(a.get("career_events",[])) for a in filtered))
c3.metric("Film credits",sum(len(a.get("filmography",[])) for a in filtered))
c4.metric("Sources",sum(len(a.get("sources",[])) for a in filtered))

artist=filtered[0]
st.header(artist["name"])
st.caption(f'Industry: {artist.get("industry","—")}  |  Languages: {" · ".join(artist.get("languages",[]))}  |  Roles: {" · ".join(artist.get("roles",[]))}')

t1,t2,t3,t4,t5=st.tabs(["Career Timeline","Filmography","Awards","Social & Media","Sources"])
with t1:
    events=pd.DataFrame(artist.get("career_events",[]))
    if events.empty: st.info("No historical events yet.")
    else: st.dataframe(events.sort_values("year"),use_container_width=True,hide_index=True)
with t2:
    films=pd.DataFrame(artist.get("filmography",[]))
    if films.empty: st.info("No filmography records yet.")
    else: st.dataframe(films.sort_values("year",ascending=False),use_container_width=True,hide_index=True)
with t3:
    awards=pd.DataFrame(artist.get("awards",[]))
    if awards.empty: st.info("No awards yet.")
    else: st.dataframe(awards.sort_values("year",ascending=False),use_container_width=True,hide_index=True)
with t4:
    st.json(artist.get("social_links",{}))
    media=pd.DataFrame(artist.get("media",[]))
    if not media.empty: st.dataframe(media,use_container_width=True,hide_index=True)
with t5:
    sources=pd.DataFrame(artist.get("sources",[]))
    if sources.empty: st.info("No sources yet.")
    else: st.dataframe(sources,use_container_width=True,hide_index=True)

st.caption("CINE002 MVP • demo records only • source-aware production collectors are next.")
