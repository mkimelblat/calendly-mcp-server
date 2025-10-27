from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from typing import AsyncGenerator
import asyncio

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from MCP Server!"}

@app.post("/tools/echo")
async def echo_tool(request: Request):
    body = await request.json()
    input_text = body.get("input", "")

    async def stream_response() -> AsyncGenerator[str, None]:
        yield f"{input_text}\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")
