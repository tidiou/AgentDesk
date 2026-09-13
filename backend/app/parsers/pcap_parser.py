from pathlib import Path
import pandas as pd
from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP
from app.schemas.parsed import ParsedPcap


def parse_pcap_to_dataframe(filepath: Path) -> pd.DataFrame:
    """
    Reads a pcap/pcapng file and extracts one row per packet with the
    fields needed for conversation/flow analysis. Non-IP packets
    (ARP, etc.) are skipped, since flows are defined by IP endpoints.
    """
    packets = rdpcap(str(filepath))
    records = []

    for pkt in packets:
        if IP not in pkt:
            continue

        proto = "OTHER"
        sport = dport = None
        if TCP in pkt:
            proto, sport, dport = "TCP", pkt[TCP].sport, pkt[TCP].dport
        elif UDP in pkt:
            proto, sport, dport = "UDP", pkt[UDP].sport, pkt[UDP].dport

        records.append({
            "timestamp": float(pkt.time),
            "src_ip": pkt[IP].src,
            "dst_ip": pkt[IP].dst,
            "src_port": sport,
            "dst_port": dport,
            "protocol": proto,
            "length": len(pkt),
        })

    if not records:
        raise ValueError("No IP packets found in this capture")

    return pd.DataFrame(records)

def parse_pcap(filepath: Path) -> ParsedPcap:
    df = parse_pcap_to_dataframe(filepath)
    all_ips = pd.concat([df["src_ip"], df["dst_ip"]]).unique()

    return ParsedPcap(
        filename=filepath.name,
        file_type=filepath.suffix.lstrip(".").lower(),
        packet_count=len(df),
        unique_ips=len(all_ips),
        duration_seconds=round(float(df["timestamp"].max() - df["timestamp"].min()), 2),
    )