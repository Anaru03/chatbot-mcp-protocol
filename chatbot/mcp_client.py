import requests
from .config import API_URL

def send_log(file_path):
    """
    Envía un archivo de log al servidor FastAPI y devuelve el resultado.
    """
    with open(file_path, "rb") as f:
        response = requests.post(API_URL, files={"file": f})
    return response.json()
