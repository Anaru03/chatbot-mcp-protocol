from .mcp_client import send_log

def analyze_log_and_print(file_path):
    """
    Llama al cliente para enviar el log y muestra los resultados en consola.
    """
    result = send_log(file_path)

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