from pathlib import Path
import pandas as pd
from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP

from app.schemas.parsed import ParsedPcap

APP_PROTOCOL_PORTS = {
    3868: "DIAMETER",
    2123: "GTP",
    2152: "GTP",
    38412: "NGAP",
}


def _detect_app_protocol(sport, dport):
    for port in (sport, dport):
        if port in APP_PROTOCOL_PORTS:
            return APP_PROTOCOL_PORTS[port]
    return None


def parse_pcap_to_dataframe(filepath: Path) -> pd.DataFrame:
    packets = rdpcap(str(filepath))
    records = []

    for pkt in packets:
        if IP not in pkt:
            continue

        transport = "OTHER"
        sport = dport = None
        if TCP in pkt:
            transport, sport, dport = "TCP", pkt[TCP].sport, pkt[TCP].dport
        elif UDP in pkt:
            transport, sport, dport = "UDP", pkt[UDP].sport, pkt[UDP].dport

        app_protocol = _detect_app_protocol(sport, dport)

        records.append({
            "timestamp": float(pkt.time),
            "src_ip": pkt[IP].src,
            "dst_ip": pkt[IP].dst,
            "src_port": sport,
            "dst_port": dport,
            "protocol": transport,
            "app_protocol": app_protocol,
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