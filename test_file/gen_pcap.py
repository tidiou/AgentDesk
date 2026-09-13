from scapy.all import IP, TCP, Ether, wrpcap

# 1. Define source and destination details
src_ip = "192.168.1.10"
dst_ip = "10.0.0.1"
src_port = 12345
dst_port = 80

# 2. Build packet sequence (TCP 3-way handshake + HTTP Request)
syn = Ether() / IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="S", seq=1000)
syn_ack = Ether() / IP(src=dst_ip, dst=src_ip) / TCP(sport=dst_port, dport=src_port, flags="SA", seq=5000, ack=1001)
ack = Ether() / IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port, flags="A", seq=1001, ack=5001)
http_req = (
    Ether() / IP(src=src_ip, dst=dst_ip) /
    TCP(sport=src_port, dport=dst_port, flags="PA", seq=1001, ack=5001) /
    "GET /api/test HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
)

# 3. Save to a PCAP file
packets = [syn, syn_ack, ack, http_req]
wrpcap("application_test.pcap", packets)

print("PCAP file 'application_test.pcap' generated successfully!")