from pydantic import BaseModel


class ConversationFlow(BaseModel):
    endpoint_a: str
    endpoint_b: str
    protocol: str
    app_protocol: str | None
    packet_count: int
    total_bytes: int
    duration_seconds: float
    start_time: float


class PcapFlowResponse(BaseModel):
    job_id: str
    source_filename: str
    summary: str
    key_insights: list[str]
    flows: list[ConversationFlow]