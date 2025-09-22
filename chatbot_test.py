# chatbot_test.py
from chatbot.chatbot import analyze_log_and_print

if __name__ == "__main__":
    log_file = "mcp_server/example_logs/sample.log"
    analyze_log_and_print(log_file, local=False)  # local=True si quieres simular opción 7
