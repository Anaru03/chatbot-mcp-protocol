from mcp_server.ip_reputation import check_ip_reputation
from tabulate import tabulate

ips = [
    "8.8.8.8",
    "1.1.1.1",
    "192.168.1.100"
]

table = []
for ip in ips:
    try:
        result = check_ip_reputation(ip)['data']
        table.append([
            ip,
            result.get('abuseConfidenceScore', 0),
            result.get('countryCode', ''),
            result.get('usageType', ''),
            result.get('isp', ''),
            result.get('totalReports', 0),
            result.get('lastReportedAt', '')
        ])
    except Exception as e:
        table.append([ip, "Error", "-", "-", "-", "-", str(e)])

headers = ["IP", "AbuseScore", "País", "Uso", "ISP", "TotalReportes", "Último Reporte"]
print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
