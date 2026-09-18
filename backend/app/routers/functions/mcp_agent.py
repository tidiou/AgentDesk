from fastapi import APIRouter, HTTPException

from app.functions.mcp_agent import run_mcp_agent
from app.schemas.mcp_agent import MCPAgentRequest, MCPAgentResponse

router = APIRouter()


@router.post("/run", response_model=MCPAgentResponse)
def run_agent(request: MCPAgentRequest):
    try:
        return run_mcp_agent(
            mcp_server_url=request.mcp_server_url,
            auth_credential=request.auth_credential,
            task_description=request.task_description,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent run failed: {e}")