from app.schemas.uat import UATTestCase, UATGenerationResponse
from app.services.ai_client import call_ai_tool

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


def generate_uat_spec(job_id: str, source_filename: str, document_text: str) -> UATGenerationResponse:
    """
    Takes the extracted text of an SRS document and generates a structured
    UAT test specification via the AI tool-calling layer.
    """
    user_message = f"Here is the SRS document to analyze:\n\n{document_text}"

    result = call_ai_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
        tool_name="generate_uat_test_cases",
        tool_description="Generate a structured set of UAT test cases from an SRS document",
        input_schema=UAT_TOOL_SCHEMA,
        max_tokens=8192,  # UAT specs can be long; give room for many test cases
    )

    test_cases = [UATTestCase(**tc) for tc in result["test_cases"]]

    return UATGenerationResponse(
        job_id=job_id,
        source_filename=source_filename,
        test_cases=test_cases,
    )