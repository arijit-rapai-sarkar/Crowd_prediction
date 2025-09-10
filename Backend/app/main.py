# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api import auth, stations, crowd_reports, predictions, analytics

# Create database tables (for dev; in production use Alembic migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Crowding Predictor API", version="1.0.0")

# Configure CORS (allow frontend React app to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(stations.router)
app.include_router(crowd_reports.router)
app.include_router(predictions.router)
app.include_router(analytics.router)

# Health check routes
@app.get("/")
def read_root():
    return {"message": "Crowding Predictor API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
