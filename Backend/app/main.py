from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import analytics, auth, crowd_reports, predictions, stations
from .config import settings
from .database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="Crowd Prediction API",
    version="1.0.0",
    description="Backend services for real-time transit crowd analytics with MongoDB"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize database connection on startup"""
    await connect_to_mongo()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Close database connection on shutdown"""
    await close_mongo_connection()


@app.get("/health", tags=["system"])
async def health_check() -> dict:
    return {"status": "ok", "database": "mongodb"}


app.include_router(auth.router)
app.include_router(stations.router)
app.include_router(crowd_reports.router)
app.include_router(predictions.router)
app.include_router(analytics.router)
