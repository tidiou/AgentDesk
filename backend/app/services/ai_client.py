import json
from anthropic import Anthropic
from anthropic import APIError as AnthropicAPIError
from openai import OpenAI
from openai import APIError as OpenAIAPIError

from app.config import ANTHROPIC_API_KEY, OPENAI_API_KEY, CLAUDE_MODEL, OPENAI_MODEL

_anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
_openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


# --- plain text calls (unchanged from before) ---

def _ask_anthropic(system_prompt: str, user_message: str, max_tokens: int) -> str:
    response = _anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return response.content[0].text


def _ask_openai(system_prompt: str, user_message: str, max_tokens: int) -> str:
    response = _openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


def ask_ai(system_prompt: str, user_message: str, max_tokens: int = 4096) -> str:
    if _anthropic_client:
        try:
            return _ask_anthropic(system_prompt, user_message, max_tokens)
        except AnthropicAPIError as e:
            print(f"[ai_client] Anthropic failed ({e}), falling back to OpenAI...")

    if _openai_client:
        try:
            return _ask_openai(system_prompt, user_message, max_tokens)
        except OpenAIAPIError as e:
            raise RuntimeError(f"Both Anthropic and OpenAI failed. Last error: {e}")

    raise RuntimeError("No AI provider is configured.")


# --- tool-based structured output (new) ---

def _call_tool_anthropic(
    system_prompt: str, user_message: str,
    tool_name: str, tool_description: str, input_schema: dict, max_tokens: int,
) -> dict:
    response = _anthropic_client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        tools=[{
            "name": tool_name,
            "description": tool_description,
            "input_schema": input_schema,
        }],
        tool_choice={"type": "tool", "name": tool_name},
        messages=[{"role": "user", "content": user_message}],
    )
    for block in response.content:
        if block.type == "tool_use":
            return block.input  # already a parsed dict
    raise RuntimeError("Anthropic response did not contain a tool_use block")


def _call_tool_openai(
    system_prompt: str, user_message: str,
    tool_name: str, tool_description: str, input_schema: dict, max_tokens: int,
) -> dict:
    response = _openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": input_schema,
            },
        }],
        tool_choice={"type": "function", "function": {"name": tool_name}},
    )
    tool_calls = response.choices[0].message.tool_calls
    if not tool_calls:
        raise RuntimeError("OpenAI response did not contain a tool call")
    return json.loads(tool_calls[0].function.arguments)  # string -> dict


def call_ai_tool(
    system_prompt: str,
    user_message: str,
    tool_name: str,
    tool_description: str,
    input_schema: dict,
    max_tokens: int = 4096,
) -> dict:
    """
    Provider-agnostic structured-output call. Forces the model to respond
    via a defined tool matching input_schema (JSON Schema), returning an
    already-parsed dict guaranteed to match that shape. Falls back from
    Anthropic to OpenAI on failure, same as ask_ai.
    """
    if _anthropic_client:
        try:
            return _call_tool_anthropic(
                system_prompt, user_message, tool_name, tool_description, input_schema, max_tokens
            )
        except AnthropicAPIError as e:
            print(f"[ai_client] Anthropic tool call failed ({e}), falling back to OpenAI...")

    if _openai_client:
        try:
            return _call_tool_openai(
                system_prompt, user_message, tool_name, tool_description, input_schema, max_tokens
            )
        except OpenAIAPIError as e:
            raise RuntimeError(f"Both providers failed for tool call. Last error: {e}")

    raise RuntimeError("No AI provider is configured.")