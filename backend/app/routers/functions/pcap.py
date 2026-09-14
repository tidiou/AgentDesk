from fastapi import APIRouter, HTTPException

from app.functions.pcap_flow_generator import generate_pcap_flows, build_packet_records
from app.parsers.pcap_parser import parse_pcap_to_dataframe
from app.schemas.pcap import PcapAnalysisResponse
from app.services.job_store import get_job

router = APIRouter()


@router.post("/flows/{job_id}", response_model=PcapAnalysisResponse)
def generate_flows(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"No job found for id '{job_id}'")

    if job.category != "network":
        raise HTTPException(status_code=400, detail=f"Requires a pcap file, got '{job.category}'")

    try:
        packet_df = parse_pcap_to_dataframe(job.filepath)
        ai_result = generate_pcap_flows(job_id, job.parsed.filename, packet_df)
        packets, total_count = build_packet_records(job.filepath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flow analysis failed: {e}")

    return PcapAnalysisResponse(
        job_id=job_id,
        source_filename=job.parsed.filename,
        summary=ai_result["summary"],
        key_insights=ai_result["key_insights"],
        packets=packets,
        total_packet_count=total_count,
    )