from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import ingest
from app.routers.functions import uat, analytics

app = FastAPI(
    title="AgentDesk API",
    description="Agentic document/data transformation toolkit",
    version="0.1.0",
)

# Allow the Vite dev server to talk to this API during local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers — each router owns one concern (ingestion, or one function)
app.include_router(ingest.router, prefix="/api/ingest", tags=["ingest"])
app.include_router(uat.router, prefix="/api/functions/uat", tags=["functions"])
app.include_router(analytics.router, prefix="/api/functions/analytics", tags=["functions"])


@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "AgentDesk"}