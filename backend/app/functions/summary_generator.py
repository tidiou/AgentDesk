from app.schemas.summary import DocumentSummaryResponse
from app.services.ai_client import call_ai_tool

SYSTEM_PROMPT = """You are an expert analyst who distills documents into their \
essential substance for a busy reader who has not read the source material.

Given the full text of a document, your job is to:
1. Extract the salient points — the key facts, arguments, or ideas, stated \
concisely and in your own words, not copied verbatim from the source
2. Identify the "red thread" — the single underlying theme, argument, or \
narrative thru-line that connects the document's ideas, if one genuinely \
exists. Not every document has one (e.g. a reference list or unrelated \
requirements catalog may not) — if there isn't a clear connecting thread, \
say so explicitly rather than inventing one
3. Suggest concrete takeaways — what the reader should conclude, act on, or \
remember after reading this document

Be concise and substantive. Avoid vague generalities — every point should be \
specific enough that someone could act on or reference it without re-reading \
the source."""

SUMMARY_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "salient_points": {
            "type": "array",
            "items": {"type": "string"},
            "description": "The key facts, ideas, or arguments from the document, concisely stated",
        },
        "red_thread": {
            "type": ["string", "null"],
            "description": "The single connecting theme or narrative thru-line, or null if none genuinely exists",
        },
        "takeaways": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Concrete, actionable conclusions the reader should draw",
        },
    },
    "required": ["salient_points", "red_thread", "takeaways"],
}


def generate_summary(job_id: str, source_filename: str, document_text: str) -> DocumentSummaryResponse:
    user_message = f"Here is the document to summarize:\n\n{document_text}"

    result = call_ai_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
        tool_name="summarize_document",
        tool_description="Extract salient points, a connecting theme, and takeaways from a document",
        input_schema=SUMMARY_TOOL_SCHEMA,
        max_tokens=4096,
    )

    return DocumentSummaryResponse(
        job_id=job_id,
        source_filename=source_filename,
        salient_points=result["salient_points"],
        red_thread=result["red_thread"],
        takeaways=result["takeaways"],
    )