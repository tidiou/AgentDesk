from pydantic import BaseModel


class PacketRecord(BaseModel):
    time: float
    source: str
    destination: str
    protocol: str
    length: int
    info: str


class PcapAnalysisResponse(BaseModel):
    job_id: str
    source_filename: str
    summary: str
    key_insights: list[str]
    packets: list[PacketRecord]
    total_packet_count: int