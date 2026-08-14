from pydantic import BaseModel


class UATTestCase(BaseModel):
    id: str                    # e.g. "TC-001"
    requirement_ref: str       # which requirement this test case covers
    title: str                 # short description of what's being tested
    preconditions: str
    steps: list[str]
    expected_result: str
    priority: str              # "High" | "Medium" | "Low"


class UATGenerationResponse(BaseModel):
    job_id: str
    source_filename: str
    test_cases: list[UATTestCase]