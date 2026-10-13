from concurrent.futures import ThreadPoolExecutor

from app.config import UAT_CHUNK_CHARS, UAT_MAX_PARALLEL, UAT_MAX_TOKENS_PER_CALL
from app.functions.doc_chunker import chunk_document, split_in_half
from app.schemas.uat import UATTestCase, UATGenerationResponse
from app.services.ai_client import call_ai_tool, OutputTruncatedError

# How many times a chunk may be halved and retried if its output is still
# cut off. 2 means a chunk can become at most 4 smaller calls.
MAX_SPLIT_DEPTH = 2
# Below this size, halving won't help: the output problem isn't the input size.
MIN_SPLITTABLE_CHARS = 2_000

SYSTEM_PROMPT = """You are an expert QA engineer specializing in User Acceptance \
Testing (UAT). Given a Software Requirements Specification (SRS) document, your job \
is to extract testable requirements and generate a thorough set of UAT test cases.

For each distinct requirement or user-facing behavior described in the document, \
generate one or more test cases that would let a business user verify the system \
meets that requirement. Cover both the "happy path" and relevant edge cases where \
they're implied by the requirement. Be specific and concrete in test steps — avoid \
vague instructions like "test the feature works."

Assign each test case a sequential ID (TC-001, TC-002, ...), reference which part \
of the requirements it covers, and set a priority (High, Medium, or Low) based on \
how central the requirement seems to the system's core purpose."""

# JSON Schema describing the tool's expected input — this is what forces
# the model's response into the exact shape we need.
UAT_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "test_cases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "e.g. TC-001"},
                    "requirement_ref": {
                        "type": "string",
                        "description": "Which requirement or section this test case covers",
                    },
                    "title": {"type": "string", "description": "Short description of what's being tested"},
                    "preconditions": {"type": "string"},
                    "steps": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Ordered list of steps the tester performs",
                    },
                    "expected_result": {"type": "string"},
                    "priority": {"type": "string", "enum": ["High", "Medium", "Low"]},
                },
                "required": [
                    "id", "requirement_ref", "title",
                    "preconditions", "steps", "expected_result", "priority",
                ],
            },
        },
    },
    "required": ["test_cases"],
}


def _build_outline(headings: list[str], limit: int = 3_000) -> str:
    """A compact table of contents, so each chunk knows where it sits in the whole."""
    outline = "\n".join(f"- {h}" for h in headings)
    return outline[:limit] + ("\n- ..." if len(outline) > limit else "")


def _chunk_message(chunk: str, part: int, total: int, filename: str, outline: str) -> str:
    if total == 1:
        return f"Here is the SRS document to analyze:\n\n{chunk}"
    context = f"Document outline (for context only):\n{outline}\n\n" if outline else ""
    return (
        f"The SRS document '{filename}' is too long to process at once, so it has been "
        f"split into {total} parts. This is part {part} of {total}.\n\n"
        f"{context}"
        "Generate test cases ONLY for requirements that appear in the text of this part. "
        "Do not invent test cases for sections that are only listed in the outline. "
        "Number test cases from TC-001; they will be renumbered when the parts are merged.\n\n"
        f"--- PART {part} OF {total} ---\n\n{chunk}"
    )


def _generate_for_chunk(chunk: str, part: int, total: int, filename: str,
                        outline: str, depth: int = 0) -> list[dict]:
    """
    Generates test cases for one chunk. If the model's answer is cut off
    (too many test cases for one response), split this chunk in half and
    retry each half: smaller input means a smaller answer.
    """
    try:
        result = call_ai_tool(
            system_prompt=SYSTEM_PROMPT,
            user_message=_chunk_message(chunk, part, total, filename, outline),
            tool_name="generate_uat_test_cases",
            tool_description="Generate a structured set of UAT test cases from an SRS document",
            input_schema=UAT_TOOL_SCHEMA,
            max_tokens=UAT_MAX_TOKENS_PER_CALL,
        )
        return result["test_cases"]
    except OutputTruncatedError:
        if depth >= MAX_SPLIT_DEPTH or len(chunk) < MIN_SPLITTABLE_CHARS:
            raise
        print(f"[uat] part {part}/{total} output truncated, splitting in half and retrying")
        first, second = split_in_half(chunk)
        # Both halves still say "part N of total": they're the same part, just smaller.
        return (_generate_for_chunk(first, part, total, filename, outline, depth + 1)
                + _generate_for_chunk(second, part, total, filename, outline, depth + 1))


def generate_uat_spec(job_id: str, source_filename: str, document_text: str,
                      headings: list[str] | None = None) -> UATGenerationResponse:
    """
    Takes the extracted text of an SRS document and generates a structured
    UAT test specification via the AI tool-calling layer.

    Short documents go out in a single call, same as before. Long ones are
    split by section (see doc_chunker), processed in parallel, then merged
    in document order and renumbered TC-001, TC-002, ...
    """
    headings = headings or []
    chunks = chunk_document(document_text, headings, UAT_CHUNK_CHARS)
    total = len(chunks)
    outline = _build_outline(headings) if total > 1 else ""
    print(f"[uat] {source_filename}: {len(document_text):,} chars -> {total} part(s)")

    # Each AI call spends most of its time waiting on the network, so running
    # several at once (threads) cuts total time roughly by UAT_MAX_PARALLEL.
    pool = ThreadPoolExecutor(max_workers=min(UAT_MAX_PARALLEL, total))
    try:
        futures = [
            pool.submit(_generate_for_chunk, chunk, i + 1, total, source_filename, outline)
            for i, chunk in enumerate(chunks)
        ]
        # Collected in submission order, so the merged spec follows the document.
        per_chunk = [f.result() for f in futures]
    except Exception:
        # One part failed for good: cancel parts still queued so we don't
        # pay for AI calls whose results would be thrown away.
        pool.shutdown(wait=False, cancel_futures=True)
        raise
    pool.shutdown()

    merged = [tc for chunk_cases in per_chunk for tc in chunk_cases]
    width = max(3, len(str(len(merged))))  # TC-001, or TC-1000 once past 999
    test_cases = [
        UATTestCase(**{**tc, "id": f"TC-{i:0{width}d}"})
        for i, tc in enumerate(merged, start=1)
    ]

    return UATGenerationResponse(
        job_id=job_id,
        source_filename=source_filename,
        test_cases=test_cases,
        parts_processed=total,
    )
