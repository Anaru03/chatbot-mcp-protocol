import json
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "interactions.json")

def show_logs():
    if not os.path.exists(LOG_FILE):
        print("No hay logs aún.")
        return

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    for i, entry in enumerate(logs, 1):
        print(f"#{i} | {entry['timestamp']}")
        print(f"  Usuario: {entry['user_message']}")
        print(f"  Bot: {entry['bot_response']}")
        if entry.get("mcp_server"):
            print(f"  MCP usado: {entry['mcp_server']}")
        print("-" * 40)