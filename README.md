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

---

## 🎮 Uso del Chatbot Interactivo

Ejecutar el chatbot interactivo que consume el MCP Server:

```bash
python chatbot_interactive_test.py
```

### Menú principal del chatbot:

1. Analizar log de ejemplo.
2. Escribir/pegar un log manualmente.
3. Preguntar al LLM (manteniendo contexto en la sesión).
4. Usar Git MCP server (crear repositorios, archivos y commits).
5. Ver historial de interacciones MCP (en tabla ordenada).
6. Salir.

---

## 📂 Ejemplo de Análisis de Log

1. Seleccionar un log de ejemplo (`sample.log`) o ingresar manualmente un log.
2. El chatbot mostrará:

   * Total de conexiones.
   * Intentos fallidos.
   * IPs sospechosas.
   * Posible ataque de fuerza bruta.
   * Reputación de las IPs.

---

## 📖 Historial de Interacciones

El chatbot mantiene un historial completo de interacciones con:

* Logs analizados.
* Preguntas al LLM.
* Acciones en Git MCP server.

El historial se puede ver en cualquier momento desde la opción 5 del menú.

---

## ⚙️ Requisitos

* Python 3.11+
* Librerías listadas en `requirements.txt`:

  * `fastapi`
  * `uvicorn`
  * `pandas`
  * `google-genai`
  * etc.

---

## 📌 Notas

* Todos los análisis se realizan localmente.
* La interacción con Git MCP server permite simular control de versiones y commits dentro del proyecto.
* El MCP Server está preparado para integrarse con cualquier cliente que siga el estándar MCP (JSON-RPC).
