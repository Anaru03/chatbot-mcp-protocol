from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from mcp_server.analyzer import analyze_log_file

app = FastAPI(title="MCP Log Analyzer Remote", version="1.0")

@app.get("/status")
def get_status():
    return {"status": "OK"}

@app.post("/analyze_logs")
async def analyze_logs(file: UploadFile = File(...)):
    contents = await file.read()
    result = analyze_log_file(contents.decode("utf-8"))
    return result

@app.post("/jsonrpc")
async def jsonrpc(request: Request):
    try:
        data = await request.json()
        jsonrpc_id = data.get("id")
        method = data.get("method")
        params = data.get("params", {})

        if method != "analyze_logs":
            return JSONResponse(
                content={"jsonrpc": "2.0",
                         "error": {"code": -32601, "message": "Method not found"},
                         "id": jsonrpc_id}
            )

        log_content = params.get("log_content")
        if not log_content:
            return JSONResponse(
                content={"jsonrpc": "2.0",
                         "error": {"code": -32602, "message": "Missing log_content parameter"},
                         "id": jsonrpc_id}
            )

        result = analyze_log_file(log_content)
        return JSONResponse(content={"jsonrpc": "2.0", "result": result, "id": jsonrpc_id})

    except Exception as e:
        return JSONResponse(content={"jsonrpc": "2.0",
                                     "error": {"code": -32000, "message": str(e)},
                                     "id": None})