# MCP Server

Servidor MCP desarrollado para el Proyecto 1 del curso CC3067 - Redes en la Universidad del Valle de Guatemala.
Su objetivo es **analizar logs de red**, detectar patrones sospechosos y entregar un reporte estructurado al chatbot anfitrión o vía API HTTP.

---

## 🖥️ Funcionalidades

* Analizar logs de red (`.log` o `.txt`) para detectar:

  * Intentos fallidos de conexión.
  * Accesos sospechosos desde IPs desconocidas.
  * Posibles ataques de fuerza bruta.
* Generar reportes estructurados en **JSON**.
* Integración con chatbot interactivo para mostrar resultados.
* Mantener historial de interacciones con el chatbot.
* Interacción con Git MCP server (crear repositorios, archivos y commits).
* Soporte de ejecución en **dos modos de servidor**:

  * `server.py` → Puerto **8000** (uso general y JSON-RPC).
  * `local_log_server.py` → Puerto **8001** (uso exclusivo para análisis de logs vía chatbot).
* Despliegue en **Google Cloud Run** para disponibilidad pública y escalable.
* Soporte de análisis de logs vía **JSON-RPC** o **HTTP POST**.

---

## 🚀 Instalación y Configuración Local

### 1. Clonar el repositorio

> Se clonó un repositorio de un compañero como base para este proyecto.

```bash
git clone https://github.com/Anaru03/chatbot-mcp-protocol
cd chatbot-mcp-protocol
```

### 2. Crear y activar entorno virtual

```bash
# Linux / Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el servidor MCP local

#### Opción 1: Servidor principal (`server.py`) – Puerto 8000

```bash
uvicorn mcp_server.server:app --reload --port 8000
```

#### Opción 2: Servidor local de logs (`local_log_server.py`) – Puerto 8001

```bash
uvicorn mcp_server.local_log_server:app --reload --port 8001
```

---

## 🐳 Uso con Docker y Google Cloud Run

### 1. Build de la imagen Docker

```bash
docker build -t gcr.io/<PROJECT_ID>/mcp-log-analyzer .
```

### 2. Subir imagen a Google Container Registry

```bash
gcloud builds submit --tag gcr.io/<PROJECT_ID>/mcp-log-analyzer
```

### 3. Desplegar en Cloud Run

```bash
gcloud run deploy mcp-log-analyzer \
  --image gcr.io/<PROJECT_ID>/mcp-log-analyzer \
  --platform managed \
  --region us-central1
```

* Después del deploy, recibirás la **URL pública** del servicio.
* Todos los endpoints disponibles se pueden consumir vía HTTP POST o GET.

---

## 🤖 Uso del Chatbot

Para iniciar el chatbot interactivo y conectar con el MCP Server local:

```bash
python chatbot_interactive_test.py
```

El chatbot permite:

1. Analizar log de ejemplo (uso directo local).
2. Escribir/pegar un log manualmente.
3. Preguntar al LLM.
4. Usar Git MCP server.
5. Ver historial de interacciones MCP.
6. Ver logs completos del chatbot.
7. Analizar log usando MCP local (vía servidor HTTP).
8. Spotify MCP
9. Salir

---

## 🔍 Endpoints del MCP Server

| Endpoint       | Método | Descripción                  | Entrada                 | Salida                           |
| -------------- | ------ | ---------------------------- | ----------------------- | -------------------------------- |
| /analyze\_logs | POST   | Analiza un archivo de log    | Archivo `.log` o `.txt` | JSON con resumen de hallazgos    |
| /status        | GET    | Verifica estado del servidor | N/A                     | Estado del servidor (OK / Error) |
| /jsonrpc       | POST   | Analiza log vía JSON-RPC     | JSON con `"file_path"`  | JSON con resumen de hallazgos    |

### Ejemplos de prueba

#### Analizar log vía HTTP POST

```bash
curl -X POST \
-F "file=@C:/REDES/chatbot-mcp-protocol/mcp_server/example_logs/sample.log" \
https://mcp-log-analyzer-266080399609.us-central1.run.app/analyze_logs
```

#### Analizar log vía JSON-RPC

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{
      "jsonrpc": "2.0",
      "method": "analyze_logs",
      "params": { "file_path": "mcp_server/example_logs/sample.log" },
      "id": 1
    }' \
https://mcp-log-analyzer-266080399609.us-central1.run.app/jsonrpc
```

---

## 📌 Notas

* Todos los análisis se realizan **localmente** dentro del servidor MCP.
* La interacción con Git MCP server permite **simular control de versiones** dentro del proyecto.
* El MCP Server puede integrarse con cualquier cliente que siga el estándar MCP (JSON-RPC).
* Para el análisis de logs desde el chatbot se recomienda usar **`local_log_server.py` en puerto 8001**.
* Con Cloud Run, tu MCP Server es **público, escalable y accesible vía URL** para pruebas externas.
* Repositorio del MCP MoodSTdel compañero [Rodrimansidub14](https://github.com/Rodrimansidub14) : https://github.com/Rodrimansidub14/MoodST 

---