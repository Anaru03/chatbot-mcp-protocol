import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Inicializa el cliente de Gemini
client = genai.Client()

# Archivo para guardar el historial de interacción
HISTORY_FILE = "chatbot/logs/llm_history.json"

# ------------------------------- Manejo de historial -------------------------------
def load_history():
    """Carga el historial de interacciones guardadas."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    """Guarda el historial de interacciones."""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

# ------------------------------- Función principal -------------------------------
def query_llm(prompt: str) -> str:
    """
    Envía un prompt a Gemini 2.5 Flash considerando el historial de conversación.
    Mantiene el contexto para que el LLM recuerde el hilo de la conversación.
    """
    history = load_history()
    
    # Construir prompt incluyendo el historial
    full_prompt = "Eres un asistente conversacional que recuerda el contexto de la conversación.\n"
    if history:
        for entry in history:
            if entry.get("tipo") == "llm":
                full_prompt += f"Usuario: {entry['pregunta']}\n"
                full_prompt += f"Bot: {entry['respuesta']}\n"
    full_prompt += f"Usuario: {prompt}\nBot:"

    try:
        # Generar respuesta usando Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        answer = response.text

        # Guardar la interacción en el historial
        history.append({
            "tipo": "llm",
            "pregunta": prompt,
            "respuesta": answer
        })
        save_history(history)

        return answer
    except Exception as e:
        return f"Error consultando Gemini: {e}"