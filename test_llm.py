from chatbot.llm_client import query_llm

if __name__ == "__main__":
    prompt = "Hola, ¿puedes explicarme qué es Python?"
    respuesta = query_llm(prompt)
    print("Respuesta del LLM:")
    print(respuesta)
