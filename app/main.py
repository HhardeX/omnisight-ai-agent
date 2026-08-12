from fastapi import FastAPI

from app.api.webhook import router as webhook_router


app = FastAPI(
    title="OmniSight",
    description="Autonomous Multimodal UI Self-Healing & RPA Agent",
    version="0.1.0",
)


app.include_router(webhook_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "omnisight-backend",
    }