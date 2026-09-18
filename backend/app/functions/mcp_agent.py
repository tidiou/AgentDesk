import json
from app.schemas.mcp_agent import MCPAgentResponse, AgentStep
from app.services.ai_client import run_mcp_turn

SYSTEM_PROMPT = """You are an autonomous agent with access to tools from a \
connected MCP server. Use those tools as needed to fully complete the given \
task — exploring, searching, or fetching multiple times if the task requires \
it. Once you have everything needed to answer, respond with a clear, \
complete final answer and do not call any further tools."""

MAX_ITERATIONS = 8


def _extract_tool_result_text(block) -> str:
    """
    An mcp_tool_result's content can itself be a list of content items
    (commonly text). This defensively extracts something readable
    regardless of the exact shape, rather than assuming one structure.
    """
    content = getattr(block, "content", None)
    if isinstance(content, list):
        parts = [getattr(c, "text", None) or str(c) for c in content]
        return " ".join(parts)
    return str(content)


def run_mcp_agent(mcp_server_url: str, auth_credential: str, task_description: str) -> MCPAgentResponse:
    messages = [{"role": "user", "content": task_description}]
    steps: list[AgentStep] = []

    for iteration in range(1, MAX_ITERATIONS + 1):
        response = run_mcp_turn(
            messages=messages,
            system_prompt=SYSTEM_PROMPT,
            mcp_server_url=mcp_server_url,
            auth_credential=auth_credential,
        )

        text_parts = []
        made_tool_call = False

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "mcp_tool_use":
                made_tool_call = True
                steps.append(AgentStep(
                    step_number=iteration,
                    action=f"Called tool: {block.name}",
                    detail=json.dumps(block.input),
                ))
            elif block.type == "mcp_tool_result":
                steps.append(AgentStep(
                    step_number=iteration,
                    action="Tool result received",
                    detail=_extract_tool_result_text(block)[:300],
                ))

        # Carry the model's full response forward, so the next turn (if any)
        # has complete context of what was called and what came back.
        messages.append({"role": "assistant", "content": response.content})

        if not made_tool_call:
            # No new tool call this turn — the model is done, this is its final answer.
            return MCPAgentResponse(
                final_answer="\n".join(text_parts),
                steps=steps,
                iterations_used=iteration,
            )

    # Safety net: hit the iteration cap without a clean final answer.
    return MCPAgentResponse(
        final_answer="The agent reached its step limit without a conclusive answer. Partial progress is shown below.",
        steps=steps,
        iterations_used=MAX_ITERATIONS,
    )