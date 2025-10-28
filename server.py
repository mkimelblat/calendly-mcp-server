#!/usr/bin/env python3
"""
Calendly MCP Server - COMPLETE API Coverage (v2.3)

The most comprehensive Model Context Protocol server for Calendly API v2.
Includes ALL endpoints including Event Type Management APIs.

NEW in v2.3: Automatic location detection to prevent location_kind errors
"""

import os
import logging
from typing import Any, Dict, Optional, Sequence
import httpx
import asyncio
import json
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("calendly-mcp")

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
        json_data: Optional[Dict] = None
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
                    json=json_data,
                    timeout=30.0
                )
                response.raise_for_status()
                
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
    
    async def get_event_type_location(self, event_type_uuid: str) -> Optional[Dict[str, Any]]:
        """
        Helper function to get location info from an event type.
        Returns the location configuration or None if not found.
        """
        try:
            result = await self.request("GET", f"/event_types/{event_type_uuid}")
            if result.get("error"):
                logger.warning(f"Could not fetch event type details: {result.get('message')}")
                return None
            
            locations = result.get("resource", {}).get("locations", [])
            if not locations:
                logger.info(f"Event type {event_type_uuid} has no locations configured")
                return None
            
            if len(locations) == 1:
                # Single location - return it for auto-population
                logger.info(f"Auto-detected location: {locations[0]['kind']}")
                return locations[0]
            else:
                # Multiple locations - return all for error messaging
                logger.info(f"Event type has {len(locations)} locations configured")
                return {"multiple": True, "locations": locations}
                
        except Exception as e:
            logger.error(f"Error fetching event type location: {str(e)}")
            return None


server = Server("calendly-mcp")
calendly = CalendlyClient(CALENDLY_API_KEY)


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List all available tools - COMPLETE Calendly API v2 coverage including Event Type Management"""
    return [
        # USER ENDPOINTS
        Tool(
            name="get_current_user",
            description="Get information about the currently authenticated user",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="get_user",
            description="Get information about a specific user by UUID",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "User UUID"}},
                "required": ["uuid"]
            }
        ),
        
        # EVENT TYPE MANAGEMENT ENDPOINTS (NEW!)
        Tool(
            name="create_event_type",
            description="🆕 Create a new one-on-one event type with custom settings",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Event type name (e.g., '45 Minute Meeting')"},
                    "owner": {"type": "string", "description": "Owner user URI"},
                    "duration": {"type": "integer", "description": "Duration in minutes"},
                    "description": {"type": "string", "description": "Event description"},
                    "color": {"type": "string", "description": "Color hex code (e.g., #8247f5)"},
                    "location_kind": {"type": "string", "description": "zoom_conference, google_conference, microsoft_teams_conference, physical, etc."},
                    "location_details": {"type": "string", "description": "Additional location info"},
                    "visibility": {"type": "string", "description": "public or private"},
                    "locale": {"type": "string", "description": "Locale (e.g., en, es, fr)"}
                },
                "required": ["name", "owner", "duration"]
            }
        ),
        Tool(
            name="update_event_type",
            description="🆕 Update an existing event type (duration, name, location, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "Event type UUID"},
                    "name": {"type": "string", "description": "New name"},
                    "duration": {"type": "integer", "description": "New duration in minutes"},
                    "description": {"type": "string", "description": "New description"},
                    "color": {"type": "string", "description": "New color hex code"},
                    "location_kind": {"type": "string", "description": "New location type"},
                    "location_details": {"type": "string", "description": "Location details"},
                    "visibility": {"type": "string", "description": "public or private"},
                    "active": {"type": "boolean", "description": "Active status"}
                },
                "required": ["uuid"]
            }
        ),
        Tool(
            name="list_event_types",
            description="List event types for a user or organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "user": {"type": "string", "description": "User URI"},
                    "organization": {"type": "string", "description": "Organization URI"},
                    "active": {"type": "boolean", "description": "Filter by active status"},
                    "count": {"type": "integer", "description": "Number of results (max 100)"},
                    "sort": {"type": "string", "description": "Sort order (name:asc, name:desc)"}
                }
            }
        ),
        Tool(
            name="get_event_type",
            description="Get details of a specific event type",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "Event type UUID"}},
                "required": ["uuid"]
            }
        ),
        Tool(
            name="list_event_type_available_times",
            description="Get available time slots for an event type",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_type": {"type": "string", "description": "Event type URI"},
                    "start_time": {"type": "string", "description": "Start of range (ISO 8601)"},
                    "end_time": {"type": "string", "description": "End of range (ISO 8601)"}
                },
                "required": ["event_type", "start_time", "end_time"]
            }
        ),
        Tool(
            name="list_event_type_availability_schedules",
            description="🆕 List availability schedules for an event type",
            inputSchema={
                "type": "object",
                "properties": {"event_type": {"type": "string", "description": "Event type UUID"}},
                "required": ["event_type"]
            }
        ),
        Tool(
            name="update_event_type_availability_schedule",
            description="""🆕 Update availability schedule for an event type
            
            IMPORTANT: 
            - event_type must be FULL URI (https://api.calendly.com/event_types/UUID)
            - availability_rule must include 'rules' array AND 'timezone'
            - To block a day, set intervals to [] (empty array)
            
            Example availability_rule JSON string:
            {
              "rules": [
                {"type": "wday", "wday": "monday", "intervals": [{"from": "09:00", "to": "17:00"}]},
                {"type": "wday", "wday": "friday", "intervals": []}
              ],
              "timezone": "America/Los_Angeles"
            }
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "event_type": {"type": "string", "description": "Full event type URI (e.g., https://api.calendly.com/event_types/UUID)"},
                    "user": {"type": "string", "description": "User URI"},
                    "availability_setting": {"type": "string", "description": "host or custom"},
                    "availability_rule": {"type": "string", "description": "JSON string containing rules array and timezone"}
                },
                "required": ["event_type", "availability_setting", "availability_rule"]
            }
        ),
        Tool(
            name="list_user_meeting_locations",
            description="🆕 List available meeting locations for a user",
            inputSchema={
                "type": "object",
                "properties": {"user": {"type": "string", "description": "User URI"}},
                "required": ["user"]
            }
        ),
        
        # SCHEDULED EVENT ENDPOINTS
        Tool(
            name="list_events",
            description="List scheduled events with various filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "user": {"type": "string", "description": "User URI"},
                    "organization": {"type": "string", "description": "Organization URI"},
                    "invitee_email": {"type": "string", "description": "Filter by invitee email"},
                    "status": {"type": "string", "description": "Status: active or canceled"},
                    "min_start_time": {"type": "string", "description": "Min start time (ISO 8601)"},
                    "max_start_time": {"type": "string", "description": "Max start time (ISO 8601)"},
                    "count": {"type": "integer", "description": "Number of results (max 100)"}
                }
            }
        ),
        Tool(
            name="get_event",
            description="Get details of a specific scheduled event",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "Event UUID"}},
                "required": ["uuid"]
            }
        ),
        Tool(
            name="cancel_event",
            description="Cancel a scheduled event",
            inputSchema={
                "type": "object",
                "properties": {
                    "uuid": {"type": "string", "description": "Event UUID"},
                    "reason": {"type": "string", "description": "Cancellation reason"}
                },
                "required": ["uuid"]
            }
        ),
        Tool(
            name="create_event_invitee",
            description="""🆕 SCHEDULING API: Create a scheduled event (book a meeting) programmatically
            
            NEW in v2.3: Automatically detects and uses the event type's location if not specified.
            This prevents "Invalid location kind" errors when booking meetings.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "event_type_uuid": {"type": "string", "description": "Event type UUID"},
                    "start_time": {"type": "string", "description": "Start time (ISO 8601)"},
                    "email": {"type": "string", "description": "Invitee email"},
                    "name": {"type": "string", "description": "Invitee full name"},
                    "first_name": {"type": "string", "description": "Invitee first name"},
                    "last_name": {"type": "string", "description": "Invitee last name"},
                    "timezone": {"type": "string", "description": "Timezone (e.g., America/New_York)"},
                    "location_kind": {"type": "string", "description": "Location type: physical, inbound_call, outbound_call, ask_invitee, zoom_conference, google_conference, gotomeeting_conference, microsoft_teams_conference, webex_conference, custom"},
                    "location_location": {"type": "string", "description": "Additional location details (required for ask_invitee, outbound_call, custom, or physical if multiple options exist)"},
                    "text_reminder_number": {"type": "string", "description": "Phone number for SMS reminders (E.164 format, e.g., +14155551234)"},
                    "guests": {"type": "array", "description": "Array of guest email addresses (max 10)"},
                    "questions_and_answers": {"type": "string", "description": "JSON string of Q&A pairs"},
                    "tracking": {"type": "string", "description": "JSON string with UTM parameters and salesforce_uuid"}
                },
                "required": ["event_type_uuid", "start_time", "email", "name"]
            }
        ),
        Tool(
            name="list_event_invitees",
            description="List invitees for a scheduled event",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_uuid": {"type": "string", "description": "Event UUID"},
                    "email": {"type": "string", "description": "Filter by invitee email"},
                    "status": {"type": "string", "description": "Status: active or canceled"},
                    "count": {"type": "integer", "description": "Number of results"}
                },
                "required": ["event_uuid"]
            }
        ),
        Tool(
            name="get_event_invitee",
            description="Get details of a specific event invitee",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_uuid": {"type": "string", "description": "Event UUID"},
                    "invitee_uuid": {"type": "string", "description": "Invitee UUID"}
                },
                "required": ["event_uuid", "invitee_uuid"]
            }
        ),
        
        # AVAILABILITY ENDPOINTS
        Tool(
            name="list_user_availability_schedules",
            description="List availability schedules for a user",
            inputSchema={
                "type": "object",
                "properties": {"user": {"type": "string", "description": "User URI"}},
                "required": ["user"]
            }
        ),
        Tool(
            name="get_user_availability_schedule",
            description="Get details of an availability schedule",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "Schedule UUID"}},
                "required": ["uuid"]
            }
        ),
        Tool(
            name="list_user_busy_times",
            description="Get busy times for a user within a date range",
            inputSchema={
                "type": "object",
                "properties": {
                    "user": {"type": "string", "description": "User URI"},
                    "start_time": {"type": "string", "description": "Start time (ISO 8601)"},
                    "end_time": {"type": "string", "description": "End time (ISO 8601)"}
                },
                "required": ["user", "start_time", "end_time"]
            }
        ),
        
        # ORGANIZATION ENDPOINTS
        Tool(
            name="get_organization",
            description="Get organization details by UUID",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "Organization UUID"}},
                "required": ["uuid"]
            }
        ),
        Tool(
            name="list_organization_memberships",
            description="List members of an organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "organization": {"type": "string", "description": "Organization URI"},
                    "email": {"type": "string", "description": "Filter by email"},
                    "count": {"type": "integer", "description": "Number of results"}
                },
                "required": ["organization"]
            }
        ),
        Tool(
            name="get_organization_membership",
            description="Get details of an organization membership",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "Membership UUID"}},
                "required": ["uuid"]
            }
        ),
        Tool(
            name="delete_organization_membership",
            description="Remove a user from an organization",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "Membership UUID"}},
                "required": ["uuid"]
            }
        ),
        Tool(
            name="list_organization_invitations",
            description="List pending organization invitations",
            inputSchema={
                "type": "object",
                "properties": {
                    "organization": {"type": "string", "description": "Organization URI"},
                    "email": {"type": "string", "description": "Filter by email"},
                    "status": {"type": "string", "description": "Status: pending or declined"},
                    "count": {"type": "integer", "description": "Number of results"}
                },
                "required": ["organization"]
            }
        ),
        Tool(
            name="get_organization_invitation",
            description="Get details of an organization invitation",
            inputSchema={
                "type": "object",
                "properties": {
                    "org_uuid": {"type": "string"},
                    "invitation_uuid": {"type": "string"}
                },
                "required": ["org_uuid", "invitation_uuid"]
            }
        ),
        Tool(
            name="create_organization_invitation",
            description="Invite a user to an organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "organization": {"type": "string", "description": "Organization URI"},
                    "email": {"type": "string", "description": "Email address to invite"}
                },
                "required": ["organization", "email"]
            }
        ),
        Tool(
            name="revoke_organization_invitation",
            description="Revoke a pending organization invitation",
            inputSchema={
                "type": "object",
                "properties": {
                    "org_uuid": {"type": "string"},
                    "invitation_uuid": {"type": "string"}
                },
                "required": ["org_uuid", "invitation_uuid"]
            }
        ),
        
        # WEBHOOK ENDPOINTS
        Tool(
            name="list_webhook_subscriptions",
            description="List webhook subscriptions for an organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "organization": {"type": "string", "description": "Organization URI"},
                    "scope": {"type": "string", "description": "Scope: organization or user"}
                },
                "required": ["organization"]
            }
        ),
        Tool(
            name="create_webhook_subscription",
            description="Create a new webhook subscription",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Webhook URL"},
                    "events": {"type": "array", "description": "Array of event types"},
                    "organization": {"type": "string", "description": "Organization URI"},
                    "scope": {"type": "string", "description": "Scope: organization or user"},
                    "signing_key": {"type": "string", "description": "Optional signing key"}
                },
                "required": ["url", "events", "organization"]
            }
        ),
        Tool(
            name="get_webhook_subscription",
            description="Get details of a webhook subscription",
            inputSchema={
                "type": "object",
                "properties": {"webhook_uuid": {"type": "string", "description": "Webhook UUID"}},
                "required": ["webhook_uuid"]
            }
        ),
        Tool(
            name="delete_webhook_subscription",
            description="Delete a webhook subscription",
            inputSchema={
                "type": "object",
                "properties": {"webhook_uuid": {"type": "string", "description": "Webhook UUID"}},
                "required": ["webhook_uuid"]
            }
        ),
        
        # ROUTING FORMS
        Tool(
            name="list_routing_forms",
            description="List routing forms for an organization",
            inputSchema={
                "type": "object",
                "properties": {
                    "organization": {"type": "string", "description": "Organization URI"},
                    "count": {"type": "integer", "description": "Number of results"}
                },
                "required": ["organization"]
            }
        ),
        Tool(
            name="get_routing_form",
            description="Get details of a routing form",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "Routing form UUID"}},
                "required": ["uuid"]
            }
        ),
        Tool(
            name="list_routing_form_submissions",
            description="List submissions for a routing form",
            inputSchema={
                "type": "object",
                "properties": {
                    "form_uuid": {"type": "string", "description": "Routing form UUID"},
                    "count": {"type": "integer", "description": "Number of results"}
                },
                "required": ["form_uuid"]
            }
        ),
        Tool(
            name="get_routing_form_submission",
            description="Get details of a routing form submission",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "Submission UUID"}},
                "required": ["uuid"]
            }
        ),
        
        # SCHEDULING LINKS
        Tool(
            name="create_scheduling_link",
            description="Create a single-use scheduling link",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_event_count": {"type": "integer", "description": "Max bookings (default: 1)"},
                    "owner": {"type": "string", "description": "Event type owner URI"},
                    "owner_type": {"type": "string", "description": "EventType or User"}
                },
                "required": ["max_event_count", "owner", "owner_type"]
            }
        ),
        
        # NO-SHOW MANAGEMENT
        Tool(
            name="create_invitee_no_show",
            description="Mark an invitee as a no-show",
            inputSchema={
                "type": "object",
                "properties": {"invitee": {"type": "string", "description": "Invitee URI"}},
                "required": ["invitee"]
            }
        ),
        Tool(
            name="get_invitee_no_show",
            description="Get no-show details",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "No-show UUID"}},
                "required": ["uuid"]
            }
        ),
        Tool(
            name="delete_invitee_no_show",
            description="Unmark an invitee as a no-show",
            inputSchema={
                "type": "object",
                "properties": {"uuid": {"type": "string", "description": "No-show UUID"}},
                "required": ["uuid"]
            }
        ),
        
        # DATA COMPLIANCE
        Tool(
            name="delete_invitee_data",
            description="Delete all data for invitee emails (GDPR compliance)",
            inputSchema={
                "type": "object",
                "properties": {"emails": {"type": "array", "description": "Array of email addresses"}},
                "required": ["emails"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    """Handle tool execution requests"""
    try:
        result = {}
        
        # USER ENDPOINTS
        if name == "get_current_user":
            result = await calendly.request("GET", "/users/me")
        elif name == "get_user":
            result = await calendly.request("GET", f"/users/{arguments['uuid']}")
            
        # EVENT TYPE MANAGEMENT
        elif name == "create_event_type":
            # Build location object if specified
            payload = {
                "name": arguments["name"],
                "host": arguments["owner"],
                "duration": arguments["duration"]
            }
            
            # Add optional fields
            for field in ["description", "color", "visibility", "locale"]:
                if field in arguments:
                    payload[field] = arguments[field]
            
            # Handle location
            if "location_kind" in arguments:
                location = {"kind": arguments["location_kind"]}
                if "location_details" in arguments:
                    location["location"] = arguments["location_details"]
                payload["location"] = location
            
            result = await calendly.request("POST", "/event_types", json_data=payload)
            
        elif name == "update_event_type":
            uuid = arguments.pop("uuid")
            payload = {}
            
            # Add any provided fields to payload
            for field in ["name", "duration", "description", "color", "visibility", "active"]:
                if field in arguments:
                    payload[field] = arguments[field]
            
            # Handle location update
            if "location_kind" in arguments:
                location = {"kind": arguments["location_kind"]}
                if "location_details" in arguments:
                    location["location"] = arguments["location_details"]
                payload["location"] = location
            
            result = await calendly.request("PATCH", f"/event_types/{uuid}", json_data=payload)
            
        elif name == "list_event_types":
            result = await calendly.request("GET", "/event_types", params=arguments)
        elif name == "get_event_type":
            result = await calendly.request("GET", f"/event_types/{arguments['uuid']}")
        elif name == "list_event_type_available_times":
            result = await calendly.request("GET", "/event_type_available_times", params=arguments)
        elif name == "list_event_type_availability_schedules":
            result = await calendly.request("GET", f"/event_types/{arguments['event_type']}/availability_schedules")
        elif name == "update_event_type_availability_schedule":
            # Parse the availability_rule JSON string
            availability_rule = json.loads(arguments["availability_rule"])
            
            payload = {
                "availability_setting": arguments["availability_setting"],
                "availability_rule": availability_rule
            }
            
            if "user" in arguments:
                payload["user"] = arguments["user"]
            
            # Extract UUID from event_type URI
            event_type_uri = arguments["event_type"]
            event_type_uuid = event_type_uri.split("/")[-1]
            
            result = await calendly.request(
                "PUT",
                f"/event_types/{event_type_uuid}/availability_schedule",
                json_data=payload
            )
        elif name == "list_user_meeting_locations":
            result = await calendly.request("GET", "/user_meeting_locations", params={"user": arguments["user"]})
            
        # SCHEDULED EVENTS
        elif name == "list_events":
            result = await calendly.request("GET", "/scheduled_events", params=arguments)
        elif name == "get_event":
            result = await calendly.request("GET", f"/scheduled_events/{arguments['uuid']}")
        elif name == "cancel_event":
            uuid = arguments.pop("uuid")
            result = await calendly.request("POST", f"/scheduled_events/{uuid}/cancellation", json_data=arguments)
            
        elif name == "create_event_invitee":
            # 🆕 NEW: Auto-detect location if not provided
            event_type_uuid = arguments['event_type_uuid']
            
            # Check if location_kind was provided
            if "location_kind" not in arguments:
                logger.info(f"No location_kind provided, attempting to auto-detect from event type {event_type_uuid}")
                
                # Fetch event type location info
                location_info = await calendly.get_event_type_location(event_type_uuid)
                
                if location_info:
                    if location_info.get("multiple"):
                        # Multiple locations - provide helpful error
                        locations = location_info.get("locations", [])
                        location_kinds = [loc.get("kind") for loc in locations]
                        return [TextContent(
                            type="text",
                            text=f"Error: This event type has multiple locations configured. Please specify one of: {', '.join(location_kinds)}"
                        )]
                    else:
                        # Single location - auto-populate
                        arguments["location_kind"] = location_info["kind"]
                        logger.info(f"✅ Auto-populated location_kind: {location_info['kind']}")
                        
                        # Also add location details if present and needed
                        if "location" in location_info:
                            arguments["location_location"] = location_info["location"]
            
            # Continue with existing logic
            # 1. Convert event_type_uuid to full URI
            event_type_uri = f"https://api.calendly.com/event_types/{event_type_uuid}"
            
            # 2. Build the invitee object (nested structure)
            invitee = {
                "email": arguments["email"]
            }
            
            # Handle name vs first_name/last_name (conditionally required)
            if "name" in arguments:
                invitee["name"] = arguments["name"]
            if "first_name" in arguments:
                invitee["first_name"] = arguments["first_name"]
            if "last_name" in arguments:
                invitee["last_name"] = arguments["last_name"]
            
            # Add optional invitee fields
            if "timezone" in arguments:
                invitee["timezone"] = arguments["timezone"]
            if "text_reminder_number" in arguments:
                invitee["text_reminder_number"] = arguments["text_reminder_number"]
            
            # 3. Build the main payload with correct structure
            payload = {
                "event_type": event_type_uri,  # Full URI, not UUID
                "start_time": arguments["start_time"],
                "invitee": invitee  # Nested object
            }
            
            # 4. Handle LOCATION object (conditional, with nuances)
            if "location_kind" in arguments:
                location = {
                    "kind": arguments["location_kind"]
                }
                if "location_location" in arguments:
                    location["location"] = arguments["location_location"]
                
                payload["location"] = location
            
            # 5. Add optional top-level fields
            if "guests" in arguments:
                payload["event_guests"] = arguments["guests"]
            
            if "text_reminder_number" in arguments:
                payload["text_reminder_number"] = arguments["text_reminder_number"]
            
            if "questions_and_answers" in arguments:
                payload["questions_and_answers"] = json.loads(arguments["questions_and_answers"])
            
            if "tracking" in arguments:
                payload["tracking"] = json.loads(arguments["tracking"])
            
            # 6. Make the API request
            result = await calendly.request("POST", "/invitees", json_data=payload)
            
        # EVENT INVITEES
        elif name == "list_event_invitees":
            event_uuid = arguments.pop("event_uuid")
            result = await calendly.request("GET", f"/scheduled_events/{event_uuid}/invitees", params=arguments)
        elif name == "get_event_invitee":
            result = await calendly.request("GET", f"/scheduled_events/{arguments['event_uuid']}/invitees/{arguments['invitee_uuid']}")
            
        # AVAILABILITY
        elif name == "list_user_availability_schedules":
            result = await calendly.request("GET", "/user_availability_schedules", params={"user": arguments["user"]})
        elif name == "get_user_availability_schedule":
            result = await calendly.request("GET", f"/user_availability_schedules/{arguments['uuid']}")
        elif name == "list_user_busy_times":
            params = {
                "user": arguments["user"],
                "start_time": arguments["start_time"],
                "end_time": arguments["end_time"]
            }
            result = await calendly.request("GET", "/user_busy_times", params=params)
            
        # ORGANIZATION
        elif name == "get_organization":
            result = await calendly.request("GET", f"/organizations/{arguments['uuid']}")
        elif name == "list_organization_memberships":
            org = arguments.pop("organization")
            result = await calendly.request("GET", "/organization_memberships", params={"organization": org, **arguments})
        elif name == "get_organization_membership":
            result = await calendly.request("GET", f"/organization_memberships/{arguments['uuid']}")
        elif name == "delete_organization_membership":
            result = await calendly.request("DELETE", f"/organization_memberships/{arguments['uuid']}")
        elif name == "list_organization_invitations":
            org = arguments.pop("organization")
            result = await calendly.request("GET", f"/organizations/{org}/invitations", params=arguments)
        elif name == "get_organization_invitation":
            result = await calendly.request("GET", f"/organizations/{arguments['org_uuid']}/invitations/{arguments['invitation_uuid']}")
        elif name == "create_organization_invitation":
            org_uri = arguments.pop("organization")
            org_uuid = org_uri.split("/")[-1]
            result = await calendly.request("POST", f"/organizations/{org_uuid}/invitations", json_data=arguments)
        elif name == "revoke_organization_invitation":
            result = await calendly.request("DELETE", f"/organizations/{arguments['org_uuid']}/invitations/{arguments['invitation_uuid']}")
            
        # WEBHOOKS
        elif name == "list_webhook_subscriptions":
            result = await calendly.request("GET", "/webhook_subscriptions", params=arguments)
        elif name == "create_webhook_subscription":
            result = await calendly.request("POST", "/webhook_subscriptions", json_data=arguments)
        elif name == "get_webhook_subscription":
            result = await calendly.request("GET", f"/webhook_subscriptions/{arguments['webhook_uuid']}")
        elif name == "delete_webhook_subscription":
            result = await calendly.request("DELETE", f"/webhook_subscriptions/{arguments['webhook_uuid']}")
            
        # ROUTING FORMS
        elif name == "list_routing_forms":
            result = await calendly.request("GET", "/routing_forms", params=arguments)
        elif name == "get_routing_form":
            result = await calendly.request("GET", f"/routing_forms/{arguments['uuid']}")
        elif name == "list_routing_form_submissions":
            form_uuid = arguments.pop("form_uuid")
            result = await calendly.request("GET", f"/routing_forms/{form_uuid}/submissions", params=arguments)
        elif name == "get_routing_form_submission":
            result = await calendly.request("GET", f"/routing_form_submissions/{arguments['uuid']}")
            
        # SCHEDULING LINKS
        elif name == "create_scheduling_link":
            result = await calendly.request("POST", "/scheduling_links", json_data=arguments)
            
        # NO-SHOWS
        elif name == "create_invitee_no_show":
            result = await calendly.request("POST", "/invitee_no_shows", json_data=arguments)
        elif name == "get_invitee_no_show":
            result = await calendly.request("GET", f"/invitee_no_shows/{arguments['uuid']}")
        elif name == "delete_invitee_no_show":
            result = await calendly.request("DELETE", f"/invitee_no_shows/{arguments['uuid']}")
            
        # DATA COMPLIANCE
        elif name == "delete_invitee_data":
            result = await calendly.request("POST", "/data_compliance/deletion/invitees", json_data=arguments)
        
        else:
            result = {"error": True, "message": f"Unknown tool: {name}"}
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        logger.error(f"Tool execution error: {str(e)}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        logger.info("🚀 Calendly MCP Server (v2.3 - Auto Location Detection) starting...")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="calendly-mcp",
                server_version="2.3.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
