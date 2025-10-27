"""
Calendly MCP Server - Streamable HTTP Transport
Version 2.1.2

Uses Streamable HTTP (the new recommended transport) for Claude.ai custom connectors.
Replaces deprecated SSE transport.
"""

from mcp.server.fastmcp import FastMCP
import httpx
import os
from typing import Optional

# Initialize FastMCP server
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


# ============================================================================
# TOOLS
# ============================================================================

@mcp.tool()
async def get_current_user() -> dict:
    """Get information about the currently authenticated user"""
    return await calendly_request("GET", "users/me")


@mcp.tool()
async def get_user(uuid: str) -> dict:
    """Get information about a specific user by UUID"""
    return await calendly_request("GET", f"users/{uuid}")


@mcp.tool()
async def create_event_type(
    name: str,
    duration: int,
    owner: str,
    description: Optional[str] = None,
    location_kind: Optional[str] = None,
    color: Optional[str] = None
) -> dict:
    """Create a new one-on-one event type"""
    payload = {"name": name, "duration": duration, "owner": owner}
    if description:
        payload["description"] = description
    if color:
        payload["color"] = color
    if location_kind:
        payload["locations"] = [{"kind": location_kind}]
    return await calendly_request("POST", "event_types", json_data=payload)


@mcp.tool()
async def update_event_type(
    uuid: str,
    name: Optional[str] = None,
    duration: Optional[int] = None,
    description: Optional[str] = None,
    active: Optional[bool] = None
) -> dict:
    """Update an existing event type"""
    payload = {}
    if name:
        payload["name"] = name
    if duration:
        payload["duration"] = duration
    if description:
        payload["description"] = description
    if active is not None:
        payload["active"] = active
    return await calendly_request("PATCH", f"event_types/{uuid}", json_data=payload)


@mcp.tool()
async def list_event_types(
    user: Optional[str] = None,
    organization: Optional[str] = None,
    active: Optional[bool] = None
) -> dict:
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
async def get_event_type(uuid: str) -> dict:
    """Get details of a specific event type"""
    return await calendly_request("GET", f"event_types/{uuid}")


@mcp.tool()
async def list_events(
    user: Optional[str] = None,
    organization: Optional[str] = None,
    status: Optional[str] = None
) -> dict:
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
async def get_event(uuid: str) -> dict:
    """Get details of a scheduled event"""
    return await calendly_request("GET", f"scheduled_events/{uuid}")


@mcp.tool()
async def cancel_event(uuid: str, reason: Optional[str] = None) -> dict:
    """Cancel a scheduled event"""
    payload = {}
    if reason:
        payload["reason"] = reason
    return await calendly_request("POST", f"scheduled_events/{uuid}/cancellation", json_data=payload)


@mcp.tool()
async def get_organization(uuid: str) -> dict:
    """Get organization details"""
    return await calendly_request("GET", f"organizations/{uuid}")


@mcp.tool()
async def list_organization_memberships(organization: str) -> dict:
    """List organization members"""
    return await calendly_request("GET", "organization_memberships", params={"organization": organization})


# ============================================================================
# EXPORT STREAMABLE HTTP APP + STATIC .well-known
# ============================================================================

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

fastapi_app = FastAPI()

# Mount .well-known for plugin discovery
fastapi_app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")

@fastapi_app.get("/")
def healthcheck():
    return {"status": "ok"}

# Mount Claude MCP handler on /message
fastapi_app.mount("/", mcp.streamable_http_app())

# Entrypoint for local dev
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Calendly MCP Server (Streamable HTTP) starting on port {port}")
    print(f"📡 Endpoint: /message")
    print(f"🔓 Auth: None (using server-side API key)")
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)
