from pathlib import Path
import struct
import pandas as pd
from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import ARP
from scapy.layers.dns import DNS

from app.schemas.parsed import ParsedPcap

SCTP_PROTOCOL_NUMBER = 132  # IP protocol number identifying SCTP

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


def _extract_sctp_ports(pkt):
    """
    Manually parses source/destination ports from an SCTP packet's common
    header (first 4 bytes), since scapy's SCTP contrib module isn't
    available in this environment.
    """
    payload = bytes(pkt[IP].payload)
    if len(payload) < 4:
        return None, None
    sport, dport = struct.unpack("!HH", payload[:4])
    return sport, dport


def _resolve_protocol(pkt, transport, sport, dport):
    if ARP in pkt:
        return "ARP"
    if ICMP in pkt:
        return "ICMP"
    if DNS in pkt:
        return "DNS"

    app_protocol = _detect_app_protocol(sport, dport)
    if app_protocol:
        return app_protocol

    if transport in ("TCP", "UDP", "SCTP"):
        return transport
    if IP in pkt:
        return "IP"
    return "OTHER"


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
        elif pkt[IP].proto == SCTP_PROTOCOL_NUMBER:
            transport = "SCTP"
            sport, dport = _extract_sctp_ports(pkt)

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


def extract_packet_records(filepath: Path) -> list[dict]:
    packets = rdpcap(str(filepath))
    if not packets:
        raise ValueError("Capture contains no packets")

    start_time = float(packets[0].time)
    records = []

    for pkt in packets:
        transport = "OTHER"
        sport = dport = None
        src = dst = "—"

        if IP in pkt:
            src, dst = pkt[IP].src, pkt[IP].dst
            if TCP in pkt:
                transport, sport, dport = "TCP", pkt[TCP].sport, pkt[TCP].dport
            elif UDP in pkt:
                transport, sport, dport = "UDP", pkt[UDP].sport, pkt[UDP].dport
            elif pkt[IP].proto == SCTP_PROTOCOL_NUMBER:
                transport = "SCTP"
                sport, dport = _extract_sctp_ports(pkt)
        elif ARP in pkt:
            src, dst = pkt[ARP].psrc, pkt[ARP].pdst

        protocol = _resolve_protocol(pkt, transport, sport, dport)

        records.append({
            "time": round(float(pkt.time) - start_time, 6),
            "source": src,
            "destination": dst,
            "protocol": protocol,
            "length": len(pkt),
            "info": pkt.summary(),
        })

    return records


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