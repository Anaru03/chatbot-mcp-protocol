from mcp_server.analyzer import analyze_log_file
from .git_mcp_client import create_repo, create_file, commit, list_repos
import os
from google import genai
from datetime import datetime
from tabulate import tabulate

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
    
    while True:
        print("\nEscoge una de las siguientes opciones para comenzar:")
        print("1. Analizar log de ejemplo")
        print("2. Escribir/pegar un log manualmente")
        print("3. Preguntar al LLM")
        print("4. Usar Git MCP server")
        print("5. Ver historial de interacciones MCP")
        print("6. Salir")
        choice = input("Elige una opción (1-6): ").strip()

        if choice == "1" or choice == "2":
            if choice == "1":
                log_path = choose_log()
                if not log_path:
                    continue
                try:
                    with open(log_path, "r", encoding="utf-8") as f:
                        contents = f.read()
                except Exception as e:
                    print(f"Error al leer el log: {e}")
                    continue
            else:
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
                mcp_history.append({
                    "tipo": "análisis",
                    "contenido": log_path if choice == "1" else "manual",
                    "resultado": result,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
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
            except Exception as e:
                print(f"Error al analizar el log: {e}")
                continue

        elif choice == "3":
            pregunta = input("Escribe tu pregunta para el LLM: ").strip()
            respuesta = ask_gemini(pregunta)
            print(f"LLM dice: {respuesta}\n")
            mcp_history.append({
                "tipo": "llm",
                "pregunta": pregunta,
                "respuesta": respuesta,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        elif choice == "4":
            while True:
                print("\n--- Git MCP server ---")
                print("1. Crear repositorio")
                print("2. Crear archivo en repositorio")
                print("3. Hacer commit")
                print("4. Listar repositorios")
                print("5. Volver al menú principal")
                git_choice = input("Elige una opción (1-5): ").strip()

                if git_choice == "1":
                    repo_name = input("Nombre del repositorio: ").strip()
                    msg = create_repo(repo_name)
                    print(msg)
                    mcp_history.append({"tipo": "git", "acción": "crear_repo", "repositorio": repo_name, "resultado": msg, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                elif git_choice == "2":
                    repo_name = input("Repositorio donde crear el archivo: ").strip()
                    file_name = input("Nombre del archivo: ").strip()
                    content = input("Contenido del archivo: ").strip()
                    msg = create_file(repo_name, file_name, content)
                    print(msg)
                    mcp_history.append({"tipo": "git", "acción": "crear_file", "repositorio": repo_name, "archivo": file_name, "resultado": msg, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                elif git_choice == "3":
                    repo_name = input("Repositorio donde hacer commit: ").strip()
                    message = input("Mensaje del commit: ").strip()
                    msg = commit(repo_name, message)
                    print(msg)
                    mcp_history.append({"tipo": "git", "acción": "commit", "repositorio": repo_name, "mensaje": msg, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                elif git_choice == "4":
                    repos = list_repos()
                    if repos:
                        print("\nRepositorios existentes:")
                        for r in repos:
                            print(f" - {r}")
                    else:
                        print("\nNo hay repositorios creados aún.")
                elif git_choice == "5":
                    break
                else:
                    print("Opción inválida, intenta nuevamente.")

        elif choice == "5":
            if not mcp_history:
                print("\n📭 No hay interacciones con MCP registradas aún.\n")
            else:
                print("\n=== Historial de interacciones MCP ===\n")
                table = []
                for i, entry in enumerate(mcp_history, 1):
                    fecha = entry.get("fecha", "")
                    tipo = entry.get("tipo", "")
                    if tipo == "análisis":
                        contenido = entry.get("contenido", "")
                        total = entry["resultado"].get("total_connections", "")
                        fallidos = entry["resultado"].get("failed_attempts", "")
                        resumen = f"Conexiones: {total}, Fallidos: {fallidos}, Log: {contenido}"
                    elif tipo == "llm":
                        pregunta = entry.get("pregunta", "")
                        respuesta = entry.get("respuesta", "")
                        resumen = f"P: {pregunta} | R: {respuesta[:50]}..."
                    elif tipo == "git":
                        accion = entry.get("acción", "")
                        repo = entry.get("repositorio", "")
                        archivo = entry.get("archivo", "")
                        mensaje = entry.get("mensaje", "")
                        resultado = entry.get("resultado", "")
                        resumen = f"Acción: {accion}, Repo: {repo}"
                        if archivo:
                            resumen += f", Archivo: {archivo}"
                        if mensaje:
                            resumen += f", Mensaje: {mensaje}"
                        if resultado:
                            resumen += f", Resultado: {resultado}"
                    else:
                        resumen = str(entry)
                    table.append([i, fecha, tipo, resumen])
                
                print(tabulate(table, headers=["#", "Fecha", "Tipo", "Resumen"], tablefmt="grid"))

        elif choice == "6":
            print(f"¡Hasta luego, {nombre}! 👋")
            break
