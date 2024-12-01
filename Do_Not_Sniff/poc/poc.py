from scapy.all import rdpcap, DNS, DNSQR

pcap_file = "capture5.pcapng"
attacker_domain = "attacker.example.com"
extracted_data = []

packets = rdpcap(pcap_file)
for packet in packets:
    if packet.haslayer(DNS) and packet[DNS].qr == 0 and packet.haslayer(DNSQR):
        query_name = packet[DNSQR].qname.decode('utf-8').rstrip('.')
        if attacker_domain in query_name:
            data_labels = query_name[: -len(f".{attacker_domain}")].split(".")
            numeric_labels = [int(label) for label in data_labels if label.isdigit()]
            filtered_labels = [label for label in data_labels if not label.isdigit()]
            extracted_chunk = "".join(filtered_labels)
            if numeric_labels:
                extracted_data.append((numeric_labels[0], extracted_chunk))

# 정렬 후 데이터 조합
extracted_data.sort(key=lambda x: x[0])
sorted_chunks = [chunk for _, chunk in extracted_data]

with open("extracted_data5.txt", "w") as f:
    f.write("".join(sorted_chunks))

print("데이터 추출 완료: extracted_data.txt")


import base64

with open("extracted_data5.txt", "r") as f:
    base64_data = f.read()

try:
    decoded_data = base64.b64decode(base64_data, validate=True)
except base64.binascii.Error as e:
    print(f"[ERROR] Invalid Base64 data: {e}")


with open("restored_file5.png", "wb") as f:
    f.write(decoded_data)

print("복원이 완료되었습니다: restored_file.png")