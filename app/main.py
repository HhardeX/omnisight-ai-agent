import asyncio
from pathlib import Path

# Playwright requires Windows' Proactor event loop because it launches
# Chromium as a subprocess.
if sys_platform := __import__("sys").platform:
    if sys_platform == "win32":
        asyncio.set_event_loop_policy(
            asyncio.WindowsProactorEventLoopPolicy()
        )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.webhook import router as webhook_router
from app.api.results import router as results_router


app = FastAPI(
    title="OmniSight",
    description="Autonomous Multimodal UI Self-Healing & RPA Agent",
    version="0.1.0",
)


# Allow the Vite frontend to communicate with the FastAPI backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve captured OmniSight screenshots.
artifacts_dir = Path("artifacts")
artifacts_dir.mkdir(exist_ok=True)

app.mount(
    "/artifacts",
    StaticFiles(directory=str(artifacts_dir)),
    name="artifacts",
)


# Register API routers.
app.include_router(webhook_router)
app.include_router(results_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "omnisight-backend",
    }