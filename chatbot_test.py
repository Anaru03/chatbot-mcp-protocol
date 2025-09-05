import requests

def analyze_log(file_path):
    url = "http://127.0.0.1:8000/analyze_logs"
    with open(file_path, "rb") as f:
        response = requests.post(url, files={"file": f})
    return response.json()

if __name__ == "__main__":
    log_file = "mcp_server/example_logs/sample.log"
    result = analyze_log(log_file)
    
    print("\n=== Log Analysis Result ===")
    print(f"Total connections: {result['total_connections']}")
    print(f"Failed attempts: {result['failed_attempts']}")
    print(f"Suspicious IPs: {', '.join(result['suspicious_ips'])}")
    print(f"Possible brute force: {result['possible_bruteforce']}")
    print("\nIP Reputation:")
    for ip, info in result['ip_reputation'].items():
        if "reputation" in info:
            print(f" - {ip}: {info['reputation']} (pulse_count: {info.get('pulse_count', 0)})")
        else:
            print(f" - {ip}: Error -> {info['error']}")
