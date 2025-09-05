import re
from mcp_server.otx_client import check_ip_reputation

def extract_ips(log_text: str):
    """Extract IPv4 addresses from logs"""
    return re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", log_text)

def analyze_log_file(log_text: str):
    """Analyze logs and check IP reputation"""
    lines = log_text.splitlines()
    failed_attempts = [line for line in lines if "failed" in line.lower()]

    ips = extract_ips(log_text)
    unique_ips = set(ips)

    suspicious_data = {}
    for ip in unique_ips:
        suspicious_data[ip] = check_ip_reputation(ip)

    return {
        "total_connections": len(lines),
        "failed_attempts": len(failed_attempts),
        "suspicious_ips": list(unique_ips),
        "possible_bruteforce": len(failed_attempts) > 20,
        "ip_reputation": suspicious_data
    }
