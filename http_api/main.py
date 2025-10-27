"""
Calendly MCP Server - Streamable HTTP Transport
Version 2.1.3 (Fixed for Railway/Replit)
"""

from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import httpx
import os
from typing import Optional

# ----------------------------------------------------------------------------
# Initialize MCP Server
# ----------------------------------------------------------------------------

mcp = FastMCP("Calendly Complete API")
CALENDLY_BASE_URL = "https://api.calendly.com"


def get_api_key() -> str:
    """Get Calendly API key from environment"""
    api_key = os.getenv("CALENDLY_API_KEY")
    if not api_key:
        raise ValueError("CALENDLY_API_KEY environment variable is required")
    return api_key


async def calendly_request(method: str, endpoint: str, json_data: dict = None, params: dict = None):
    """Make a request to Calendly API"""
    api_key = get_api_key()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=f"{CALENDLY_BASE_URL}/{endpoint.lstrip('/')}",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json=json_data,
                params=params,
                timeout=30.0
            )
            if response.status_code >= 400:
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": response.text
                }
            if response.status_code == 204:
                return {"success": True, "message": "Operation completed"}
            return response.json()
        except Exception as e:
            return {"error": True, "message": str(e)}

# ----------------------------------------------------------------------------
# TOOLS
# ----------------------------------------------------------------------------

@mcp.tool()
async def get_current_user() -> dict:
    """Get information about the currently authenticated user"""
    return await calendly_request("GET", "users/me")


@mcp.tool()
async def list_event_types(user: Optional[str] = None, organization: Optional[str] = None, active: Optional[bool] = None) -> dict:
    """List event types for a user or organization"""
    params = {}
    if user:
        params["user"] = user
    if organization:
        params["organization"] = organization
    if active is not None:
        params["active"] = str(active).lower()
    return await calendly_request("GET", "event_types", params=params)


@mcp.tool()
async def create_event_type(name: str, duration: int, owner: str, description: Optional[str] = None) -> dict:
    """Create a new event type"""
    payload = {"name": name, "duration": duration, "owner": owner}
    if description:
        payload["description"] = description
    return await calendly_request("POST", "event_types", json_data=payload)


@mcp.tool()
async def list_events(user: Optional[str] = None, organization: Optional[str] = None, status: Optional[str] = None) -> dict:
    """List scheduled events"""
    params = {}
    if user:
        params["user"] = user
    if organization:
        params["organization"] = organization
    if status:
        params["status"] = status
    return await calendly_request("GET", "scheduled_events", params=params)


@mcp.tool()
async def cancel_event(uuid: str, reason: Optional[str] = None) -> dict:
    """Cancel a scheduled event"""
    payload = {}
    if reason:
        payload["reason"] = reason
    return await calendly_request("POST", f"scheduled_events/{uuid}/cancellation", json_data=payload)


# ----------------------------------------------------------------------------
# FastAPI Integration (for Claude + Static)
# ----------------------------------------------------------------------------

fastapi_app = FastAPI()

# Serve /.well-known for Claude or OpenAI plugin discovery
fastapi_app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")

@fastapi_app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Calendly MCP Server running"}

# Mount the MCP handler at root
fastapi_app.mount("/", mcp.streamable_http_app())

# Expose the FastAPI app as the uvicorn entrypoint
app = fastapi_app

# ----------------------------------------------------------------------------
# Local dev entrypoint
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Calendly MCP Server starting on port {port}")
    print(f"📡 MCP endpoint: /message")
    uvicorn.run(app, host="0.0.0.0", port=port)
