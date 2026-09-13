import json
from app.functions.pcap_flows import compute_flows
from app.schemas.pcap import PcapFlowResponse, ConversationFlow
from app.services.ai_client import call_ai_tool

SYSTEM_PROMPT = """You are a network analyst reviewing reconstructed \
conversations (flows) from a packet capture. You will be given a summary \
of the top conversations by data volume — endpoints, protocol, packet \
count, total bytes, and duration.

Your job is to:
1. Write a brief plain-language summary of what this capture shows overall
2. Identify specific, genuinely interesting observations — a conversation \
that's unusually large, long-lived, short but bursty, or otherwise notable; \
any pattern suggesting a particular kind of traffic (e.g. a bulk transfer, \
many short-lived connections from one host, a long-lived idle connection)"""

FLOW_INSIGHTS_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "key_insights": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "key_insights"],
}

TOP_FLOWS_FOR_AI = 15


def generate_pcap_flows(job_id: str, source_filename: str, packet_df) -> PcapFlowResponse:
    flows_df = compute_flows(packet_df)

    top_flows = flows_df.head(TOP_FLOWS_FOR_AI).to_dict(orient="records")
    user_message = f"Top conversations by data volume:\n\n{json.dumps(top_flows, indent=2)}"

    result = call_ai_tool(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message,
        tool_name="analyze_network_flows",
        tool_description="Summarize and flag notable network conversations",
        input_schema=FLOW_INSIGHTS_SCHEMA,
        max_tokens=2048,
    )

    all_flows = [ConversationFlow(**f) for f in flows_df.to_dict(orient="records")]

    return PcapFlowResponse(
        job_id=job_id,
        source_filename=source_filename,
        summary=result["summary"],
        key_insights=result["key_insights"],
        flows=all_flows,
    )