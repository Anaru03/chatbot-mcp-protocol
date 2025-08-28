# chatbot-mcp-protocol

netshield-mcp/
├── venv/                        # Entorno virtual (ya creado)
├── chatbot/                     # Chatbot anfitrión
│   ├── __init__.py
│   ├── chatbot.py               # Chatbot principal
│   ├── mcp_client.py           # Cliente JSON-RPC para conectar con MCP local y remoto
│   ├── config.py               # Configuración de rutas, puertos y URLs
│   └── logs/                   # Carpeta para registros de interacciones
│
├── mcp_server/                 # Nuestro MCP Server (NetShield MCP)
│   ├── __init__.py
│   ├── server.py               # Servidor principal con FastAPI
│   ├── analyzer.py             # Lógica de análisis de logs
│   ├── schemas.py              # Modelos de datos con Pydantic
│   ├── tests/                  # Pruebas unitarias del MCP Server
│   │   ├── test_server.py
│   │   └── test_analyzer.py
│   └── example_logs/
│       └── sample.log          # Logs de ejemplo para pruebas
│
├── examples/                   # Ejemplos para estudiantes y catedrático
│   ├── request_example.json    # Solicitud JSON-RPC de ejemplo
│   ├── response_example.json   # Respuesta JSON-RPC de ejemplo
│   └── chatbot_usage.md        # Guía de uso paso a paso
│
├── docs/                       # Documentación del proyecto
│   ├── Definicion_MCP_Server.docx
│   ├── Definicion_MCP_Server.pdf
│   └── API_Documentation.md
│
├── requirements.txt            # Librerías necesarias
├── README.md                   # Documentación principal
└── .gitignore
