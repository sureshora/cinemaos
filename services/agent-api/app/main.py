from fastapi import FastAPI

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
