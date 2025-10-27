#!/usr/bin/env python3
"""
Calendly MCP Server

A complete Model Context Protocol server for the Calendly API.
Provides full CRUD operations for all Calendly resources.
"""

import os
import logging
from typing import Any, Dict, Optional
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("calendly-mcp")

# Calendly API configuration
CALENDLY_API_KEY = os.getenv("CALENDLY_API_KEY")
CALENDLY_BASE_URL = "https://api.calendly.com"

if not CALENDLY_API_KEY:
    raise ValueError("CALENDLY_API_KEY environment variable is required")


class CalendlyClient:
    """HTTP client for Calendly API requests"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = CALENDLY_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Calendly API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=json,
                    timeout=30.0
                )
                response.raise_for_status()
                
                # Some endpoints return empty responses (204 No Content)
                if response.status_code == 204:
                    return {"success": True, "message": "Operation completed successfully"}
                
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": e.response.text
                }
            except Exception as e:
                logger.error(f"Request failed: {str(e)}")
                return {"error": True, "message": str(e)}


# Initialize the MCP server
app = Server("calendly-mcp")
calendly = CalendlyClient(CALENDLY_API_KEY)


# ============================================================================
# EVENT TYPES
# ============================================================================

@app.tool()
async def get_event_type(uuid: str) -> str:
    """
    Get details of a specific event type.
    
    Args:
        uuid: The UUID of the event type
    """
    result = await calendly.request("GET", f"/event_types/{uuid}")
    return str(result)


@app.tool()
async def list_event_types(
    user: Optional[str] = None,
    organization: Optional[str] = None,
    active: Optional[bool] = None,
    count: int = 20
) -> str:
    """
    List event types for a user or organization.
    
    Args:
        user: URI of the user (e.g., https://api.calendly.com/users/XXX)
        organization: URI of the organization
        active: Filter by active status
        count: Number of results to return (max 100)
    """
    params = {"count": count}
    if user:
        params["user"] = user
    if organization:
        params["organization"] = organization
    if active is not None:
        params["active"] = str(active).lower()
    
    result = await calendly.request("GET", "/event_types", params=params)
    return str(result)


@app.tool()
async def update_event_type(
    uuid: str,
    name: Optional[str] = None,
    duration: Optional[int] = None,
    description_plain: Optional[str] = None,
    description_html: Optional[str] = None,
    location_kind: Optional[str] = None,
    location_details: Optional[str] = None,
    color: Optional[str] = None,
    active: Optional[bool] = None
) -> str:
    """
    Update an existing event type.
    
    Args:
        uuid: The UUID of the event type to update
        name: New name for the event type
        duration: New duration in minutes
        description_plain: Plain text description
        description_html: HTML description
        location_kind: Type of location (zoom_conference, google_conference, physical, etc.)
        location_details: Additional location info
        color: Hex color code (e.g., #8247f5)
        active: Whether the event type is active
    """
    payload = {}
    
    if name is not None:
        payload["name"] = name
    if duration is not None:
        payload["duration"] = duration
    if description_plain is not None:
        payload["description_plain"] = description_plain
    if description_html is not None:
        payload["description_html"] = description_html
    if color is not None:
        payload["color"] = color
    if active is not None:
        payload["active"] = active
    
    # Handle location
    if location_kind:
        location = {"kind": location_kind}
        if location_details:
            if location_kind == "physical":
                location["location"] = location_details
            elif location_kind in ["inbound_call", "outbound_call"]:
                location["phone_number"] = location_details
            else:
                location["additional_info"] = location_details
        payload["location"] = location
    
    result = await calendly.request("PATCH", f"/event_types/{uuid}", json=payload)
    return str(result)


@app.tool()
async def delete_event_type(uuid: str) -> str:
    """
    Delete an event type.
    
    Args:
        uuid: The UUID of the event type to delete
    """
    result = await calendly.request("DELETE", f"/event_types/{uuid}")
    return str(result)


# ============================================================================
# AVAILABILITY SCHEDULES
# ============================================================================

@app.tool()
async def get_user_availability_schedule(uuid: str) -> str:
    """
    Get details of a user availability schedule.
    
    Args:
        uuid: The UUID of the availability schedule
    """
    result = await calendly.request("GET", f"/user_availability_schedules/{uuid}")
    return str(result)


@app.tool()
async def list_user_availability_schedules(user: str) -> str:
    """
    List all availability schedules for a user.
    
    Args:
        user: URI of the user (e.g., https://api.calendly.com/users/XXX)
    """
    params = {"user": user}
    result = await calendly.request("GET", "/user_availability_schedules", params=params)
    return str(result)


@app.tool()
async def create_user_availability_schedule(
    user: str,
    name: str,
    timezone: str,
    rules: str
) -> str:
    """
    Create a new availability schedule.
    
    Args:
        user: URI of the user
        name: Name for the schedule
        timezone: IANA timezone (e.g., America/New_York)
        rules: JSON string of availability rules
    """
    import json
    payload = {
        "user": user,
        "name": name,
        "timezone": timezone,
        "rules": json.loads(rules)
    }
    result = await calendly.request("POST", "/user_availability_schedules", json=payload)
    return str(result)


@app.tool()
async def update_user_availability_schedule(
    uuid: str,
    name: Optional[str] = None,
    timezone: Optional[str] = None,
    rules: Optional[str] = None
) -> str:
    """
    Update an existing availability schedule.
    
    Args:
        uuid: The UUID of the schedule to update
        name: New name for the schedule
        timezone: New IANA timezone
        rules: JSON string of new availability rules
    """
    import json
    payload = {}
    
    if name is not None:
        payload["name"] = name
    if timezone is not None:
        payload["timezone"] = timezone
    if rules is not None:
        payload["rules"] = json.loads(rules)
    
    result = await calendly.request("PATCH", f"/user_availability_schedules/{uuid}", json=payload)
    return str(result)


@app.tool()
async def delete_user_availability_schedule(uuid: str) -> str:
    """
    Delete an availability schedule.
    
    Args:
        uuid: The UUID of the schedule to delete
    """
    result = await calendly.request("DELETE", f"/user_availability_schedules/{uuid}")
    return str(result)


# ============================================================================
# SCHEDULED EVENTS
# ============================================================================

@app.tool()
async def get_event(uuid: str) -> str:
    """
    Get details of a scheduled event.
    
    Args:
        uuid: The UUID of the scheduled event
    """
    result = await calendly.request("GET", f"/scheduled_events/{uuid}")
    return str(result)


@app.tool()
async def list_events(
    user: Optional[str] = None,
    organization: Optional[str] = None,
    invitee_email: Optional[str] = None,
    status: Optional[str] = None,
    min_start_time: Optional[str] = None,
    max_start_time: Optional[str] = None,
    count: int = 20
) -> str:
    """
    List scheduled events.
    
    Args:
        user: URI of the user
        organization: URI of the organization
        invitee_email: Filter by invitee email
        status: Filter by status (active, canceled)
        min_start_time: Minimum start time (ISO 8601)
        max_start_time: Maximum start time (ISO 8601)
        count: Number of results (max 100)
    """
    params = {"count": count}
    if user:
        params["user"] = user
    if organization:
        params["organization"] = organization
    if invitee_email:
        params["invitee_email"] = invitee_email
    if status:
        params["status"] = status
    if min_start_time:
        params["min_start_time"] = min_start_time
    if max_start_time:
        params["max_start_time"] = max_start_time
    
    result = await calendly.request("GET", "/scheduled_events", params=params)
    return str(result)


@app.tool()
async def cancel_event(uuid: str, reason: Optional[str] = None) -> str:
    """
    Cancel a scheduled event.
    
    Args:
        uuid: The UUID of the event to cancel
        reason: Reason for cancellation (sent to invitees)
    """
    payload = {}
    if reason:
        payload["reason"] = reason
    
    result = await calendly.request("POST", f"/scheduled_events/{uuid}/cancellation", json=payload)
    return str(result)


@app.tool()
async def list_event_invitees(
    event_uuid: str,
    email: Optional[str] = None,
    status: Optional[str] = None,
    count: int = 20
) -> str:
    """
    List invitees for a scheduled event.
    
    Args:
        event_uuid: UUID of the scheduled event
        email: Filter by invitee email
        status: Filter by status (active, canceled)
        count: Number of results (max 100)
    """
    params = {"count": count}
    if email:
        params["email"] = email
    if status:
        params["status"] = status
    
    result = await calendly.request("GET", f"/scheduled_events/{event_uuid}/invitees", params=params)
    return str(result)


# ============================================================================
# USERS
# ============================================================================

@app.tool()
async def get_current_user() -> str:
    """Get information about the currently authenticated user."""
    result = await calendly.request("GET", "/users/me")
    return str(result)


@app.tool()
async def get_user(uuid: str) -> str:
    """
    Get information about a specific user.
    
    Args:
        uuid: The UUID of the user (or "me" for current user)
    """
    result = await calendly.request("GET", f"/users/{uuid}")
    return str(result)


# ============================================================================
# WEBHOOKS
# ============================================================================

@app.tool()
async def list_webhook_subscriptions(
    organization: str,
    scope: str = "organization"
) -> str:
    """
    List webhook subscriptions.
    
    Args:
        organization: URI of the organization
        scope: Scope of webhooks (organization or user)
    """
    params = {
        "organization": organization,
        "scope": scope
    }
    result = await calendly.request("GET", "/webhook_subscriptions", params=params)
    return str(result)


@app.tool()
async def create_webhook_subscription(
    url: str,
    organization: str,
    events: str,
    scope: str = "organization",
    signing_key: Optional[str] = None
) -> str:
    """
    Create a webhook subscription.
    
    Args:
        url: The URL to send webhook events to
        organization: URI of the organization
        events: JSON array of event types to subscribe to
        scope: Scope (organization or user)
        signing_key: Optional signing key for webhook verification
    """
    import json
    payload = {
        "url": url,
        "organization": organization,
        "events": json.loads(events),
        "scope": scope
    }
    if signing_key:
        payload["signing_key"] = signing_key
    
    result = await calendly.request("POST", "/webhook_subscriptions", json=payload)
    return str(result)


@app.tool()
async def delete_webhook_subscription(webhook_uuid: str) -> str:
    """
    Delete a webhook subscription.
    
    Args:
        webhook_uuid: UUID of the webhook subscription to delete
    """
    result = await calendly.request("DELETE", f"/webhook_subscriptions/{webhook_uuid}")
    return str(result)


# ============================================================================
# ORGANIZATION
# ============================================================================

@app.tool()
async def list_organization_memberships(
    organization: str,
    email: Optional[str] = None,
    count: int = 20
) -> str:
    """
    List members of an organization.
    
    Args:
        organization: URI of the organization
        email: Filter by member email
        count: Number of results (max 100)
    """
    params = {
        "organization": organization,
        "count": count
    }
    if email:
        params["email"] = email
    
    result = await calendly.request("GET", "/organization_memberships", params=params)
    return str(result)


@app.tool()
async def create_organization_invitation(
    organization: str,
    email: str
) -> str:
    """
    Invite a user to an organization.
    
    Args:
        organization: URI of the organization
        email: Email address to invite
    """
    payload = {
        "organization": organization,
        "email": email
    }
    result = await calendly.request("POST", "/organization_invitations", json=payload)
    return str(result)


# ============================================================================
# HELPER TOOLS
# ============================================================================

@app.tool()
async def list_available_times(
    event_type: str,
    start_time: str,
    end_time: str
) -> str:
    """
    Get available time slots for an event type.
    
    Args:
        event_type: URI of the event type
        start_time: Start of range (ISO 8601)
        end_time: End of range (ISO 8601)
    """
    params = {
        "event_type": event_type,
        "start_time": start_time,
        "end_time": end_time
    }
    result = await calendly.request("GET", "/event_type_available_times", params=params)
    return str(result)


@app.tool()
async def list_user_busy_times(
    user: str,
    start_time: str,
    end_time: str
) -> str:
    """
    Get busy times for a user.
    
    Args:
        user: URI of the user
        start_time: Start of range (ISO 8601)
        end_time: End of range (ISO 8601)
    """
    params = {
        "user": user,
        "start_time": start_time,
        "end_time": end_time
    }
    result = await calendly.request("GET", "/user_busy_times", params=params)
    return str(result)


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

async def main():
    """Run the MCP server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("Calendly MCP Server starting...")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
