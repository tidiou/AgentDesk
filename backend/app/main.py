import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ingest
from app.routers.functions import uat, analytics, summary

app = FastAPI(
    title="AgentDesk API",
    description="Agentic document/data transformation toolkit",
    version="0.1.0",
)

ALLOWED_ORIGINS = ["http://localhost:5173"]
if os.getenv("FRONTEND_URL"):
    ALLOWED_ORIGINS.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix="/api/ingest", tags=["ingest"])
app.include_router(uat.router, prefix="/api/functions/uat", tags=["functions"])
app.include_router(analytics.router, prefix="/api/functions/analytics", tags=["functions"])
app.include_router(summary.router, prefix="/api/functions/summary", tags=["functions"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "AgentDesk"}