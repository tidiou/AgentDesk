import pandas as pd


def _canonical_key(row):
    endpoint_a = (row["src_ip"], row["src_port"])
    endpoint_b = (row["dst_ip"], row["dst_port"])
    if endpoint_a <= endpoint_b:
        return (endpoint_a, endpoint_b, row["protocol"], row["app_protocol"])
    return (endpoint_b, endpoint_a, row["protocol"], row["app_protocol"])


def compute_flows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["flow_key"] = df.apply(_canonical_key, axis=1)

    flows = []
    for key, group in df.groupby("flow_key"):
        (ip_a, port_a), (ip_b, port_b), proto, app_proto = key
        flows.append({
            "endpoint_a": f"{ip_a}:{port_a}" if port_a else ip_a,
            "endpoint_b": f"{ip_b}:{port_b}" if port_b else ip_b,
            "protocol": proto,
            "app_protocol": app_proto,
            "packet_count": len(group),
            "total_bytes": int(group["length"].sum()),
            "duration_seconds": round(float(group["timestamp"].max() - group["timestamp"].min()), 3),
            "start_time": float(group["timestamp"].min()),
        })

    flows_df = pd.DataFrame(flows).sort_values("total_bytes", ascending=False).reset_index(drop=True)
    return flows_df