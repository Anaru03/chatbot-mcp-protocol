from mcp_server.analyzer import analyze_log_file
from .git_mcp_client import create_repo, create_file, commit, list_repos
import os
import json
import re
from google import genai
from datetime import datetime
from tabulate import tabulate
from .logger import log_interaction
from .show_logs import show_logs
from .llm_client import query_llm
import requests
from chatbot.mcp_client import MCPClient
from chatbot.mcp_integration import search_song, create_playlist, add_to_history, get_history

# ------------------------------ Configuración ------------------------------
EXAMPLE_LOGS = "mcp_server/example_logs"
CONTEXT_FILE = "chatbot/logs/context.json"
MCP_LOCAL_URL = "http://127.0.0.1:8001/analyze_log_file"

client = genai.Client()
spotify_history = []

# ------------------------------- Manejo de contexto -------------------------------
def load_context():
    if os.path.exists(CONTEXT_FILE):
        try:
            with open(CONTEXT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("chat_history", []), data.get("mcp_history", [])
        except Exception:
            return [], []
    return [], []

def save_context(chat_history, mcp_history):
    os.makedirs(os.path.dirname(CONTEXT_FILE), exist_ok=True)
    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "chat_history": chat_history,
            "mcp_history": mcp_history
        }, f, indent=2)

# ------------------------------- Funciones auxiliares -------------------------------
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

def chunk_text(text, size=120):
    """Divide un texto en fragmentos de longitud size para impresión ordenada"""
    return [text[i:i+size] for i in range(0, len(text), size)]

# ------------------------------- Chat interactivo principal -------------------------------
def interactive_chat():
    chat_history, mcp_history = load_context()
    nombre = input("¡Hola! ¿Cuál es tu nombre? ").strip()
    if not nombre:
        nombre = "Usuario"
    print(f"\n🤖 Hola {nombre}, bienvenida al MCP Log Analyzer Chatbot 🤖")

    while True:
        print("\nEscoge una de las siguientes opciones para comenzar:")
        print("1. Analizar log de ejemplo (local)")
        print("2. Escribir/pegar un log manualmente")
        print("3. Preguntar al LLM")
        print("4. Usar Git MCP server")
        print("5. Ver historial de interacciones MCP")
        print("6. Ver logs completos del chatbot")
        print("7. Analizar log usando MCP local")
        print("8. Spotify MCP")
        print("9. Salir")
        choice = input("Elige una opción (1-9): ").strip()

        # ------------------ OPCIONES 1 y 2 ------------------
        if choice in ["1", "2"]:
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
                    if not re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]", line):
                        print("⚠ Línea no válida, debe empezar con [YYYY-MM-DD HH:MM:SS]")
                        continue
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

                log_interaction(
                    user_message="Analizar log",
                    bot_response=str(result),
                    source="mcp",
                    mcp_server="analyzer"
                )

                print("\n=== Resultados del Log ===")
                print(f"Total de conexiones: {result['total_connections']}")
                print(f"Intentos fallidos: {result['failed_attempts']}")
                print(f"IPs sospechosas: {', '.join(result['suspicious_ips'])}")
                print(f"Posible ataque de fuerza bruta: {result['possible_bruteforce']}\n")

                if result['ip_reputation']:
                    table = []
                    for ip, info in result['ip_reputation'].items():
                        data = info.get('data', {})
                        if data:
                            table.append([
                                ip,
                                data.get('abuseConfidenceScore', 0),
                                data.get('countryCode', ''),
                                data.get('usageType', ''),
                                data.get('isp', ''),
                                data.get('totalReports', 0),
                                data.get('lastReportedAt', '')
                            ])
                        else:
                            table.append([ip, "Error", "-", "-", "-", "-", info.get('error', 'desconocido')])
                    headers = ["IP", "AbuseScore", "País", "Uso", "ISP", "TotalReportes", "Último Reporte"]
                    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No hay IPs sospechosas con reputación disponible.\n")

            except Exception as e:
                print(f"Error al analizar el log: {e}")
                continue

        # ------------------ OPCIÓN 3 ------------------
        elif choice == "3":
            pregunta = input("Escribe tu pregunta para el LLM: ").strip()
            try:
                respuesta = query_llm(pregunta)
            except Exception as e:
                respuesta = f"Error al consultar LLM: {e}"

            print("\n=== Pregunta ===")
            print(pregunta)
            print("\n=== Respuesta ===")
            for bloque in chunk_text(respuesta, 120):
                print(bloque)
            print("\n")

            mcp_history.append({
                "tipo": "llm",
                "pregunta": pregunta,
                "respuesta": respuesta,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            log_interaction(
                user_message=pregunta,
                bot_response=respuesta,
                source="chatbot"
            )

        # ------------------ OPCIÓN 4 ------------------
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
                    print(tabulate([["Acción", f"Crear repo {repo_name}"], ["Resultado", msg]], tablefmt="fancy_grid"))
                    mcp_history.append({"tipo": "git", "acción": "crear_repo", "repositorio": repo_name, "resultado": msg, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    log_interaction(f"Crear repo {repo_name}", msg, source="mcp", mcp_server="git")

                elif git_choice == "2":
                    repo_name = input("Repositorio donde crear el archivo: ").strip()
                    file_name = input("Nombre del archivo: ").strip()
                    content = input("Contenido del archivo: ").strip()
                    msg = create_file(repo_name, file_name, content)
                    print(tabulate([["Acción", f"Crear archivo {file_name} en {repo_name}"], ["Resultado", msg]], tablefmt="fancy_grid"))
                    mcp_history.append({"tipo": "git", "acción": "crear_file", "repositorio": repo_name, "archivo": file_name, "resultado": msg, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    log_interaction(f"Crear archivo {file_name} en {repo_name}", msg, source="mcp", mcp_server="git")

                elif git_choice == "3":
                    repo_name = input("Repositorio donde hacer commit: ").strip()
                    message = input("Mensaje del commit: ").strip()
                    msg = commit(repo_name, message)
                    print(tabulate([["Acción", f"Commit en {repo_name}"], ["Mensaje", message], ["Resultado", msg]], tablefmt="fancy_grid"))
                    mcp_history.append({"tipo": "git", "acción": "commit", "repositorio": repo_name, "mensaje": msg, "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    log_interaction(f"Commit en {repo_name}", msg, source="mcp", mcp_server="git")

                elif git_choice == "4":
                    repos = list_repos()
                    if repos:
                        table = [[i+1, r] for i, r in enumerate(repos)]
                        print(tabulate(table, headers=["#", "Repositorio"], tablefmt="fancy_grid"))
                    else:
                        print("No hay repositorios creados aún.")
                elif git_choice == "5":
                    break
                else:
                    print("Opción inválida, intenta nuevamente.")

        # ------------------ OPCIÓN 5 ------------------
        elif choice == "5":
            if not mcp_history:
                print("\n📭 No hay interacciones con MCP registradas aún.\n")
            else:
                print("\n=== Historial de interacciones MCP ===\n")
                for i, entry in enumerate(mcp_history, 1):
                    fecha = entry.get("fecha", "")
                    tipo = entry.get("tipo", "")
                    print(f"{i}. [{fecha}] ({tipo})")
                    if tipo == "análisis":
                        contenido = entry.get("contenido", "")
                        total = entry["resultado"].get("total_connections", "")
                        fallidos = entry["resultado"].get("failed_attempts", "")
                        print(f"   - Conexiones: {total}, Fallidos: {fallidos}, Log: {contenido}")
                    elif tipo == "llm":
                        pregunta = entry.get("pregunta", "")
                        respuesta = entry.get("respuesta", "")
                        print(f"   - Pregunta: {pregunta}")
                        for bloque in chunk_text(respuesta, 100):
                            print(f"     {bloque}")
                    elif tipo == "git":
                        accion = entry.get("acción", "")
                        repo = entry.get("repositorio", "")
                        archivo = entry.get("archivo", "")
                        mensaje = entry.get("mensaje", "")
                        resultado = entry.get("resultado", "")
                        print(f"   - Acción: {accion}, Repo: {repo}")
                        if archivo:
                            print(f"     Archivo: {archivo}")
                        if mensaje:
                            print(f"     Mensaje: {mensaje}")
                        if resultado:
                            print(f"     Resultado: {resultado}")
                    elif tipo == "spotify_search":
                        query = entry.get("query", "")
                        print(f"   - Spotify búsqueda: {query}")
                        for t in entry.get("results", []):
                            print(f"     {t['name']} - {', '.join(t['artists'])}")
                    elif tipo == "spotify_playlist":
                        name = entry.get("name", "")
                        url = entry.get("url", "")
                        print(f"   - Playlist creada: {name} -> {url}")
                    else:
                        print(f"   - {entry}")
                    print("-"*60)

        # ------------------ OPCIÓN 6 ------------------
        elif choice == "6":
            print("\n=== Mostrando logs completos del chatbot ===\n")
            show_logs()

        # ------------------ OPCIÓN 7 (MCP local) ------------------
        elif choice == "7":
            log_path = choose_log()
            if not log_path:
                continue
            try:
                with open(log_path, "rb") as f:
                    response = requests.post(
                        MCP_LOCAL_URL,
                        files={"file": f}
                    )
                    result = response.json()

                mcp_history.append({
                    "tipo": "mcp_local",
                    "contenido": log_path,
                    "resultado": result,
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                log_interaction(
                    user_message="Analizar log en MCP local",
                    bot_response=str(result),
                    source="mcp",
                    mcp_server="local_log_server"
                )

                print("\n=== Resultados del Log (MCP local) ===")
                print(f"Total de conexiones: {result.get('total_connections', 0)}")
                print(f"Intentos fallidos: {result.get('failed_attempts', 0)}")
                print(f"IPs sospechosas: {', '.join(result.get('suspicious_ips', []))}")
                print(f"Posible ataque de fuerza bruta: {result.get('possible_bruteforce', False)}\n")

                if result.get('ip_reputation'):
                    table = []
                    for ip, info in result['ip_reputation'].items():
                        data = info.get('data', {})
                        if data:
                            table.append([
                                ip,
                                data.get('abuseConfidenceScore', 0),
                                data.get('countryCode', ''),
                                data.get('usageType', ''),
                                data.get('isp', ''),
                                data.get('totalReports', 0),
                                data.get('lastReportedAt', '')
                            ])
                        else:
                            table.append([ip, "Error", "-", "-", "-", "-", info.get('error', 'desconocido')])
                    headers = ["IP", "AbuseScore", "País", "Uso", "ISP", "TotalReportes", "Último Reporte"]
                    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
                else:
                    print("No hay IPs sospechosas con reputación disponible.\n")

            except Exception as e:
                print(f"Error al consultar MCP local: {e}")

        # ------------------ OPCIÓN 8 (Spotify MCP) ------------------
        elif choice == "8":
            while True:
                print("\n--- Spotify MCP ---")
                print("1. Buscar canción")
                print("2. Crear playlist con últimas canciones buscadas")
                print("3. Volver al menú principal")
                spotify_choice = input("Elige una opción (1-3): ").strip()

                if spotify_choice == "1":
                    query = input("Ingresa el nombre de la canción o artista: ").strip()
                    results = search_song(query)
                    if results:
                        print("Resultados encontrados:")
                        for i, track in enumerate(results, 1):
                            print(f"{i}. {track['name']} - {', '.join(track['artists'])}")
                        spotify_history = results
                        add_to_history(results)
                        mcp_history.append({
                            "tipo": "spotify_search",
                            "query": query,
                            "results": results,
                            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                    else:
                        print("No se encontraron resultados.")

                elif spotify_choice == "2":
                    history = get_history()
                    if not history:
                        print("Primero busca canciones antes de crear una playlist.")
                        continue
                    playlist_name = input("Nombre de la playlist: ").strip()
                    track_ids = [track["id"] for track in history]
                    url = create_playlist(playlist_name, track_ids, public=True)
                    if url:
                        print(f"✅ Playlist creada: {url}")
                        mcp_history.append({
                            "tipo": "spotify_playlist",
                            "name": playlist_name,
                            "track_ids": track_ids,
                            "url": url,
                            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                elif spotify_choice == "3":
                    break
                else:
                    print("Opción inválida, intenta nuevamente.")

                    
        # ------------------ OPCIÓN 9 (Salir) ------------------
        elif choice == "9":
            save_context(chat_history, mcp_history)
            print(f"¡Hasta luego, {nombre}! 👋")
            break
                    
