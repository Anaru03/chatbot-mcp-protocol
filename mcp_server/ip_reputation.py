# https://docs.abuseipdb.com/#introduction

import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ABUSEIPDB_API_KEY")

def check_ip_reputation(ip: str):
    """
    Consulta la reputación de una IP en AbuseIPDB.
    Retorna el JSON con información de abuso.
    """
    if not API_KEY:
        raise ValueError("API Key de AbuseIPDB no encontrada. Revisa tu .env")

    url = "https://api.abuseipdb.com/api/v2/check"
    querystring = {
        "ipAddress": ip,
        "maxAgeInDays": "90"   # últimos 90 días
    }
    headers = {
        "Accept": "application/json",
        "Key": API_KEY
    }

    response = requests.get(url, headers=headers, params=querystring)
    return response.json()
