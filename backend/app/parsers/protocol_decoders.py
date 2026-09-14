PFCP_MESSAGE_TYPES = {
    1: "Heartbeat Request", 2: "Heartbeat Response",
    3: "PFD Management Request", 4: "PFD Management Response",
    5: "Association Setup Request", 6: "Association Setup Response",
    7: "Association Update Request", 8: "Association Update Response",
    9: "Association Release Request", 10: "Association Release Response",
    12: "Node Report Request", 13: "Node Report Response",
    14: "Session Set Deletion Request", 15: "Session Set Deletion Response",
    50: "Session Establishment Request", 51: "Session Establishment Response",
    52: "Session Modification Request", 53: "Session Modification Response",
    54: "Session Deletion Request", 55: "Session Deletion Response",
    56: "Session Report Request", 57: "Session Report Response",
}


def decode_pfcp_info(payload: bytes) -> str | None:
    """
    PFCP's message type is always the second byte of the header,
    regardless of which optional fields follow (3GPP TS 29.244 §7.2.2).
    """
    if len(payload) < 2:
        return None
    msg_name = PFCP_MESSAGE_TYPES.get(payload[1])
    return f"PFCP {msg_name}" if msg_name else None


def decode_ngap_info(payload: bytes) -> str | None:
    """
    Decodes an NGAP PDU using pycrate's ASN.1 PER decoder, resolving the
    procedure code via pycrate's own NGAP constants rather than a
    hardcoded table. Returns None (falls back to scapy's summary) if
    decoding fails for any reason — experimental, may need adjustment
    depending on the installed pycrate version.
    """
    try:
        from pycrate_asn1dir import NGAP
        from pycrate_asn1dir.NGAP import NGAP_Constants

        pdu = NGAP.NGAP_PDU_Descriptions.NGAP_PDU
        pdu.from_aper(payload)
        pdu_choice, content = pdu.get_val()
        procedure_code = content.get("procedureCode")

        code_to_name = {
            getattr(NGAP_Constants, name): name.replace("id_", "").replace("_", "")
            for name in dir(NGAP_Constants)
            if name.startswith("id_") and isinstance(getattr(NGAP_Constants, name), int)
        }
        procedure_name = code_to_name.get(procedure_code)
        if not procedure_name:
            return None

        suffix = {
            "initiatingMessage": "",
            "successfulOutcome": "Response",
            "unsuccessfulOutcome": "Failure",
        }.get(pdu_choice, "")

        return f"{procedure_name}{suffix}"
    except Exception:
        return None