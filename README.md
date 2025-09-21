# MCP Server

Servidor MCP local desarrollado para el Proyecto 1 del curso CC3067 - Redes en la Universidad del Valle de Guatemala.
Su objetivo es analizar logs de red para detectar patrones sospechosos y entregar un reporte estructurado al chatbot anfitrión.

---

## 🖥️ Funcionalidades

* Analizar logs de red (.log o .txt) para detectar:

  * Intentos fallidos de conexión.
  * Accesos sospechosos desde IPs desconocidas.
  * Posibles ataques de fuerza bruta.
* Generar reportes estructurados en JSON.
* Integración con chatbot interactivo para mostrar resultados.
* Mantener historial de interacciones con el chatbot.
* Interacción con Git MCP server (crear repositorios, archivos y commits).
* Soporte de ejecución en dos modos de servidor:

  * `server.py` → Puerto **8000** (uso general y JSON-RPC).
  * `local_log_server.py` → Puerto **8001** (uso exclusivo para el análisis de logs vía chatbot).

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

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

## 🤖 Uso del Chatbot

Para iniciar el chatbot interactivo y conectar con el MCP Server local:

```bash
python chatbot_interactive_test.py
```

El chatbot permitirá:

    1. Analizar log de ejemplo [local directo (función interna)]
    2. Escribir/pegar un log manualmente
    3. Preguntar al LLM
    4. Usar Git MCP server
    5. Ver historial de interacciones MCP
    6. Ver logs completos del chatbot
    7. Analizar log usando MCP local [vía servidor (HTTP)]
    8. Salir

---

## 🔍 Funcionalidad del MCP Server

* Analiza archivos de logs de red (`.log` o `.txt`).
* Detecta intentos fallidos de conexión.
* Identifica accesos sospechosos desde IPs desconocidas.
* Detecta posibles ataques de fuerza bruta.
* Genera un reporte en formato JSON con los hallazgos.

### Endpoints del Servidor

| Endpoint            | Método | Descripción                  | Entrada                 | Salida                           |
| ------------------- | ------ | ---------------------------- | ----------------------- | -------------------------------- |
| /analyze\_logs      | POST   | Analiza un archivo de log    | Archivo `.log` o `.txt` | JSON con resumen de hallazgos    |
| /status             | GET    | Verifica estado del servidor | N/A                     | Estado del servidor (OK / Error) |
| /analyze\_log\_file | POST   | Analiza log vía MCP local    | Archivo `.log`          | JSON con resumen de hallazgos    |

---

## 📌 Notas

* Todos los análisis se realizan localmente.
* La interacción con Git MCP server permite simular control de versiones y commits dentro del proyecto.
* El MCP Server está preparado para integrarse con cualquier cliente que siga el estándar MCP (JSON-RPC).
* Para el análisis de logs desde el chatbot se recomienda usar **`local_log_server.py` en puerto 8001**.
