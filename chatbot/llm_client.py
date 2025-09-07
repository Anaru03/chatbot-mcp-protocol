import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def query_llm(prompt: str) -> str:
    """
    Envía un prompt a Gemini 2.5 Flash y devuelve la respuesta.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)
            )
        )
        return response.text
    except Exception as e:
        return f"Error consultando Gemini: {e}"

if __name__ == "__main__":
    prompt = "Hola, ¿puedes saludarme?"
    respuesta = query_llm(prompt)
    print("Respuesta del LLM:")
    print(respuesta)
