from pydantic import BaseModel


class MCPAgentRequest(BaseModel):
    mcp_server_url: str
    auth_credential: str
    task_description: str


class AgentStep(BaseModel):
    step_number: int
    action: str          # e.g. "Called tool: search_tickets"
    detail: str          # a short, human-readable description of what happened


class MCPAgentResponse(BaseModel):
    final_answer: str
    steps: list[AgentStep]
    iterations_used: int