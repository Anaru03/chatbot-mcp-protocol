import json
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs", "interactions.json")

def log_interaction(user_message, bot_response, source="chatbot", mcp_server=None):
    """Guarda interacción en un archivo JSON."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "mcp_server": mcp_server,
        "user_message": user_message,
        "bot_response": bot_response
    }

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(log_entry)
        f.seek(0)
        json.dump(data, f, indent=2)