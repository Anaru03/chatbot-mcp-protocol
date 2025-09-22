from .mcp_client import send_log
from tabulate import tabulate

def analyze_log_and_print(file_path, local: bool = False):
    """
    Llama al cliente para enviar el log y muestra los resultados en consola
    con diseño tabulado para IPs sospechosas y su reputación.
    """
    result = send_log(file_path)

    header_title = "=== Log Analysis Result ==="
    if local:
        header_title = "=== Log Analysis Result (MCP local) ==="
    print(f"\n{header_title}")
    
    print(f"Total connections: {result['total_connections']}")
    print(f"Failed attempts: {result['failed_attempts']}")
    print(f"Suspicious IPs: {', '.join(result['suspicious_ips']) if result['suspicious_ips'] else 'Ninguna'}")
    print(f"Possible brute force: {result['possible_bruteforce']}")
    
    # Reputación de IPs con tabla
    ip_rep = result.get('ip_reputation', {})
    if ip_rep:
        table = []
        for ip, info in ip_rep.items():
            try:
                # Verifica si info proviene de AbuseIPDB
                if 'data' in info:
                    data = info['data']
                    table.append([
                        ip,
                        data.get('abuseConfidenceScore', 0),
                        data.get('countryCode', ''),
                        data.get('usageType', ''),
                        data.get('isp', ''),
                        data.get('totalReports', 0),
                        data.get('lastReportedAt', '')
                    ])
                elif 'reputation' in info:
                    table.append([
                        ip,
                        info.get('reputation', '-'),
                        '-',
                        '-',
                        '-',
                        info.get('pulse_count', 0),
                        '-'
                    ])
                else:
                    table.append([ip, "Error", "-", "-", "-", "-", info.get('error', 'desconocido')])
            except Exception:
                table.append([ip, "Error", "-", "-", "-", "-", "desconocido"])
        headers = ["IP", "AbuseScore", "País", "Uso", "ISP", "TotalReportes", "Último Reporte"]
        print("\nIP Reputation:")
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
    else:
        print("\nIP Reputation: Ninguna o error al consultar")
