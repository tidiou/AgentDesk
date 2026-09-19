import json
from app.schemas.mcp_agent import MCPAgentResponse, AgentStep
from app.services.ai_client import run_mcp_turn

SYSTEM_PROMPT = """You are an autonomous agent with access to tools from a \
connected MCP server. Use those tools as needed to fully complete the given \
task — exploring, searching, or fetching multiple times if the task requires \
it.

Once you have everything needed to answer, respond with a clear, human-readable \
final answer written in plain prose. This is a strict requirement: never \
include raw JSON, field names like "snippet" or "threadId", or any verbatim \
copy of tool output in your final answer. Instead, read the data yourself and \
re-express it in your own words, the way you would explain it to a colleague \
over chat — short paragraphs or a simple bulleted list, translating any \
technical fields into natural language.

For example, if a tool returns raw data about an email, your final answer \
should say something like "An email from Immobilien Scout24 about new \
apartment listings in Bonn — looks like routine marketing, can wait" — never \
paste the raw snippet or JSON structure itself."""

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
            max_tokens=8192,
        )

        text_parts = []

        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "mcp_tool_use":
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

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            # The model has genuinely finished — this response's text is the real answer.
            return MCPAgentResponse(
                final_answer="\n".join(text_parts).strip(),
                steps=steps,
                iterations_used=iteration,
            )

    return MCPAgentResponse(
        final_answer="The agent reached its step limit without a conclusive answer. Partial progress is shown below.",
        steps=steps,
        iterations_used=MAX_ITERATIONS,
    )