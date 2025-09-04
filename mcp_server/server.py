from fastapi import FastAPI, UploadFile, File
from mcp_server.analyzer import analyze_log_file

app = FastAPI(title="MCP Log Analyzer", version="1.0")

@app.get("/status")
def get_status():
    """Health check endpoint"""
    return {"status": "OK"}

@app.post("/analyze_logs")
async def analyze_logs(file: UploadFile = File(...)):
    """Receive a log file and analyze it"""
    contents = await file.read()
    results = analyze_log_file(contents.decode("utf-8"))
    return results