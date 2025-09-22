import requests
from .config import API_URL

class MCPClient:
    """
    Cliente para interactuar con un servidor MCP.
    Permite enviar logs, llamar herramientas y recibir resultados.
    """

    def __init__(self, api_url=None):
        """
        Inicializa el cliente con la URL del servidor.
        Si no se provee, usa la URL por defecto de config.py
        """
        self.api_url = api_url or API_URL

    def send_log(self, file_path):
        """
        Envía un archivo de log al servidor FastAPI y devuelve el resultado en formato JSON.
        """
        try:
            with open(file_path, "rb") as f:
                response = requests.post(self.api_url, files={"file": f})
            response.raise_for_status()  # genera excepción si status != 200
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠ Error al enviar el log al servidor MCP: {e}")
            return {"error": str(e)}
        except FileNotFoundError:
            print(f"⚠ Archivo no encontrado: {file_path}")
            return {"error": "Archivo no encontrado"}
        except Exception as e:
            print(f"⚠ Error inesperado: {e}")
            return {"error": str(e)}

    def call_tool(self, tool_name: str, args: dict):
        """
        Llama a una herramienta del MCP server enviando el nombre de la herramienta y los argumentos.
        Retorna el resultado en JSON.
        """
        payload = {
            "tool_name": tool_name,
            "args": args
        }
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"⚠ Error al llamar la herramienta '{tool_name}': {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"⚠ Error inesperado al llamar la herramienta '{tool_name}': {e}")
            return {"error": str(e)}
