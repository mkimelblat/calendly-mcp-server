"""
Calendly MCP Server - Authless SSE Transport
Version 2.1.0

Properly configured authless MCP server for Claude.ai custom connectors.
"""

from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import httpx
import os
from typing import Optional
import uvicorn

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
    """
    Create a new one-on-one event type with custom settings.
    
    Args:
        name: Event type name (e.g., '45 Minute Meeting')
        duration: Duration in minutes
        owner: Owner user URI
        description: Event description (optional)
        location_kind: zoom_conference, google_conference, microsoft_teams_conference, etc. (optional)
        color: Color hex code like #8247f5 (optional)
    """
    payload = {
        "name": name,
        "duration": duration,
        "owner": owner
    }
    
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
    """
    Update an existing event type.
    
    Args:
        uuid: Event type UUID
        name: New name (optional)
        duration: New duration in minutes (optional)
        description: New description (optional)
        active: Active status (optional)
    """
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
    """
    List event types for a user or organization.
    
    Args:
        user: User URI (optional)
        organization: Organization URI (optional)
        active: Filter by active status (optional)
    """
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
    """Get details of a specific event type by UUID"""
    return await calendly_request("GET", f"event_types/{uuid}")


@mcp.tool()
async def list_user_meeting_locations(user: str) -> dict:
    """List available meeting locations for a user"""
    return await calendly_request("GET", "location", params={"user": user})


@mcp.tool()
async def list_events(
    user: Optional[str] = None,
    organization: Optional[str] = None,
    status: Optional[str] = None
) -> dict:
    """
    List scheduled events.
    
    Args:
        user: User URI (optional)
        organization: Organization URI (optional)
        status: Filter by status - active or canceled (optional)
    """
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
    """Get details of a specific scheduled event"""
    return await calendly_request("GET", f"scheduled_events/{uuid}")


@mcp.tool()
async def cancel_event(uuid: str, reason: Optional[str] = None) -> dict:
    """
    Cancel a scheduled event.
    
    Args:
        uuid: Event UUID
        reason: Cancellation reason (optional, sent to invitees)
    """
    payload = {}
    if reason:
        payload["reason"] = reason
    
    return await calendly_request("POST", f"scheduled_events/{uuid}/cancellation", json_data=payload)


@mcp.tool()
async def get_organization(uuid: str) -> dict:
    """Get organization details by UUID"""
    return await calendly_request("GET", f"organizations/{uuid}")


@mcp.tool()
async def list_organization_memberships(organization: str) -> dict:
    """List members of an organization"""
    return await calendly_request("GET", "organization_memberships", params={"organization": organization})


# ============================================================================
# CUSTOM ROUTES FOR AUTHLESS MCP
# ============================================================================

async def root_handler(request):
    """Root endpoint - indicates this is an authless MCP server"""
    return JSONResponse({
        "name": "Calendly Complete API",
        "version": "2.1.0",
        "protocol": "mcp",
        "transport": "sse",
        "auth": "none",
        "description": "Authless MCP server for Calendly API",
        "endpoints": {
            "sse": "/sse",
            "messages": "/messages/"
        }
    })


async def well_known_handler(request):
    """Return 404 for OAuth discovery - this is an authless server"""
    return JSONResponse(
        {"error": "This is an authless MCP server - no OAuth required"},
        status_code=404
    )


# ============================================================================
# CREATE APPLICATION WITH CORS
# ============================================================================

# Get the MCP SSE app
mcp_app = mcp.sse_app()

# Create custom routes
routes = [
    Route("/", root_handler),
    Route("/.well-known/oauth-protected-resource", well_known_handler),
    Route("/.well-known/oauth-authorization-server", well_known_handler),
    Mount("/", app=mcp_app),  # Mount MCP app for /sse and /messages
]

# Create Starlette app with CORS middleware
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
]

app = Starlette(routes=routes, middleware=middleware)


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Calendly MCP Server (Authless SSE) starting on port {port}")
    print(f"📡 SSE endpoint: /sse")
    print(f"🔓 Auth: None (using server-side API key)")
    uvicorn.run(app, host="0.0.0.0", port=port)
