from fastapi import FastAPI

app = FastAPI(
    title="OmniSight",
    description="Autonomous Multimodal UI Self-Healing & RPA Agent",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "omnisight-backend",
    }