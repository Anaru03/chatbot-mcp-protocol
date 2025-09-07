from mcp_server.analyzer import analyze_log_file
import os
from google import genai

EXAMPLE_LOGS = "mcp_server/example_logs"
client = genai.Client()

chat_history = []
mcp_history = []

def list_logs(folder):
    try:
        return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    except FileNotFoundError:
        return []

def choose_log():
    logs = list_logs(EXAMPLE_LOGS)
    if not logs:
        print("No hay logs de ejemplo disponibles.")
        return None
    
    print("\nLogs de ejemplo disponibles:")
    for i, log in enumerate(logs, 1):
        print(f"{i}. {log}")
    
    while True:
        idx = input("Selecciona el log a analizar (número): ").strip()
        if idx.isdigit() and 1 <= int(idx) <= len(logs):
            return os.path.join(EXAMPLE_LOGS, logs[int(idx)-1])
        print("Opción inválida, intenta nuevamente.")

def ask_gemini(prompt):
    chat_history.append(f"Usuario: {prompt}")
    context = "\n".join(chat_history)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=context
    )
    answer = response.text
    chat_history.append(f"Gemini: {answer}")
    return answer

def interactive_chat():
    nombre = input("¡Hola! ¿Cuál es tu nombre? ").strip()
    if not nombre:
        nombre = "Usuario"

    print(f"\n🤖 Hola {nombre}, bienvenida al MCP Log Analyzer Chatbot 🤖")
    print("Escoge una de las siguientes opciones para comenzar:\n")

    while True:
        print("1. Analizar log de ejemplo")
        print("2. Escribir/pegar un log manualmente")
        print("3. Preguntar al LLM")
        print("4. Ver historial de interacciones MCP")
        print("5. Salir")
        choice = input("Elige una opción (1-5): ").strip()

        if choice == "1":
            log_path = choose_log()
            if log_path is None:
                continue
            try:
                with open(log_path, "r", encoding="utf-8") as f:
                    contents = f.read()
                result = analyze_log_file(contents)
                mcp_history.append({"tipo": "análisis", "contenido": log_path, "resultado": result})
            except Exception as e:
                print(f"Error al leer o analizar el log: {e}")
                continue

        elif choice == "2":
            print("\nIngresa tu log. Escribe 'FIN' en una línea nueva para terminar:\n")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "FIN":
                    break
                lines.append(line)
            contents = "\n".join(lines)
            try:
                result = analyze_log_file(contents)
                mcp_history.append({"tipo": "análisis", "contenido": "manual", "resultado": result})
            except Exception as e:
                print(f"Error al analizar el log: {e}")
                continue

        elif choice == "3":
            pregunta = input("Escribe tu pregunta para el LLM: ").strip()
            respuesta = ask_gemini(pregunta)
            print(f"LLM dice: {respuesta}\n")
            mcp_history.append({"tipo": "llm", "pregunta": pregunta, "respuesta": respuesta})

        elif choice == "4":
            if not mcp_history:
                print("\n📭 No hay interacciones con MCP registradas aún.\n")
            else:
                print("\n=== Historial de interacciones MCP ===")
                for i, entry in enumerate(mcp_history, 1):
                    if entry["tipo"] == "análisis":
                        print(f"{i}. Análisis de log ({entry['contenido']}) -> {entry['resultado']}")
                    elif entry["tipo"] == "llm":
                        print(f"{i}. Pregunta: {entry['pregunta']} -> Respuesta: {entry['respuesta']}")
                print()

        elif choice == "5" or choice.lower() == "salir":
            print(f"¡Hasta luego, {nombre}! 👋")
            break

        else:
            print("Opción inválida, intenta nuevamente.\n")
            continue

        if choice in ["1", "2"]:
            print("\n=== Resultados del Log ===")
            print(f"Total de conexiones: {result['total_connections']}")
            print(f"Intentos fallidos: {result['failed_attempts']}")
            print(f"IPs sospechosas: {', '.join(result['suspicious_ips'])}")
            print(f"Posible ataque de fuerza bruta: {result['possible_bruteforce']}")
            print("\nReputación de las IPs:")
            for ip, info in result['ip_reputation'].items():
                if "reputación" in info or "reputation" in info:
                    rep = info.get("reputación", info.get("reputation", "desconocida"))
                    pulse = info.get("pulse_count", 0)
                    print(f" - {ip}: {rep} (conteo de alertas: {pulse})")
                else:
                    print(f" - {ip}: Error -> {info.get('error', 'desconocido')}")
            print("\n")
