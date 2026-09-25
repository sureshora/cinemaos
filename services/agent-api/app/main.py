from fastapi import FastAPI, HTTPException\n\nfrom .cinema_knowledge import artist_sources, get_artist, list_artists

app = FastAPI(
    title="CinemaOS Agent API",
    version="0.1.0",
    description="Agentic Cinema production orchestration API",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "cinemaos-agent-api",
        "milestone": "CINE001",
    }
\n\n@app.get("/api/v1/cinema/artists")\nasync def cinema_artists(q: str = "", industry: str = "") -> dict[str, object]:\n    records = list_artists(query=q, industry=industry)\n    return {"count": len(records), "artists": records}\n\n\n@app.get("/api/v1/cinema/artists/{canonical_artist_id}")\nasync def cinema_artist(canonical_artist_id: str) -> dict[str, object]:\n    record = get_artist(canonical_artist_id)\n    if record is None:\n        raise HTTPException(status_code=404, detail="Artist not found")\n    return record\n\n\n@app.get("/api/v1/cinema/artists/{canonical_artist_id}/sources")\nasync def cinema_artist_sources(canonical_artist_id: str) -> dict[str, object]:\n    record = get_artist(canonical_artist_id)\n    if record is None:\n        raise HTTPException(status_code=404, detail="Artist not found")\n    sources = artist_sources(canonical_artist_id)\n    return {"count": len(sources), "sources": sources}\n