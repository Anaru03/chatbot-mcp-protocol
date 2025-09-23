# Dockerfile para Cloud Run
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run usa esta variable de entorno
ENV PORT=8080

EXPOSE 8080

CMD ["uvicorn", "mcp_server.server:app", "--host", "0.0.0.0", "--port", "8080"]