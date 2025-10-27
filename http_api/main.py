"""
Calendly HTTP API for Claude Custom Connector - COMPLETE
Version 2.1.0

Complete HTTP wrapper for all Calendly API v2 endpoints.
Matches the full functionality of the calendly-mcp-server.
"""

from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from typing import Optional, List, Dict, Any
import json

app = FastAPI(
    title="Calendly Connector API",
    description="Complete HTTP API for Calendly integration with Claude - All 45+ endpoints",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CALENDLY_BASE_URL = "https://api.calendly.com"


async def calendly_request(
    api_key: str,
    method: str, 
    endpoint: str, 
    json_data: dict = None, 
    params: dict = None
) -> Dict[str, Any]:
    """Make a request to Calendly API"""
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
# REQUEST/RESPONSE MODELS
# ============================================================================

class CreateEventTypeRequest(BaseModel):
    name: str
    duration: int
    owner: str
    description: Optional[str] = None
    location_kind: Optional[str] = None
    location_details: Optional[str] = None
    color: Optional[str] = None
    visibility: Optional[str] = None
    locale: Optional[str] = None

class UpdateEventTypeRequest(BaseModel):
    name: Optional[str] = None
    duration: Optional[int] = None
    description: Optional[str] = None
    location_kind: Optional[str] = None
    location_details: Optional[str] = None
    color: Optional[str] = None
    active: Optional[bool] = None
    visibility: Optional[str] = None

class UpdateAvailabilityScheduleRequest(BaseModel):
    availability_rules: str  # JSON string
    user: Optional[str] = None
    availability_setting: Optional[str] = None

class CreateEventInviteeRequest(BaseModel):
    event_type_uuid: str
    start_time: str
    email: str
    name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    timezone: Optional[str] = None
    guests: Optional[List[str]] = None
    questions_and_answers: Optional[str] = None  # JSON string

class CreateWebhookRequest(BaseModel):
    url: str
    organization: str
    events: List[str]
    scope: Optional[str] = "organization"
    signing_key: Optional[str] = None

class CreateOrganizationInvitationRequest(BaseModel):
    organization: str
    email: str

class CreateSchedulingLinkRequest(BaseModel):
    max_event_count: int
    owner: str
    owner_type: str

class DeleteInviteeDataRequest(BaseModel):
    emails: List[str]


# ============================================================================
# ROOT
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Calendly Connector API",
        "version": "2.1.0",
        "description": "Complete API with 45+ endpoints matching calendly-mcp-server",
        "documentation": "/docs",
        "openapi": "/openapi.json",
        "endpoints": {
            "users": 2,
            "event_types": 7,
            "scheduled_events": 5,
            "event_invitees": 2,
            "availability": 3,
            "organizations": 7,
            "webhooks": 4,
            "routing_forms": 4,
            "scheduling_links": 1,
            "no_shows": 3,
            "data_compliance": 1
        }
    }


# ============================================================================
# USER ENDPOINTS
# ============================================================================

@app.get("/users/me")
async def get_current_user(authorization: str = Header(...)):
    """Get information about the currently authenticated user"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", "users/me")


@app.get("/users/{user_uuid}")
async def get_user(user_uuid: str, authorization: str = Header(...)):
    """Get information about a specific user by UUID"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", f"users/{user_uuid}")


# ============================================================================
# EVENT TYPE MANAGEMENT (NEW!)
# ============================================================================

@app.post("/event-types")
async def create_event_type(
    request: CreateEventTypeRequest,
    authorization: str = Header(...)
):
    """🆕 Create a new one-on-one event type with custom settings"""
    api_key = authorization.replace("Bearer ", "")
    
    payload = {
        "name": request.name,
        "duration": request.duration,
        "owner": request.owner
    }
    
    if request.description:
        payload["description"] = request.description
    if request.color:
        payload["color"] = request.color
    if request.visibility:
        payload["visibility"] = request.visibility
    if request.locale:
        payload["locale"] = request.locale
    
    if request.location_kind:
        location = {"kind": request.location_kind}
        if request.location_details:
            if request.location_kind == "physical":
                location["location"] = request.location_details
            else:
                location["additional_info"] = request.location_details
        payload["locations"] = [location]
    
    return await calendly_request(api_key, "POST", "event_types", json_data=payload)


@app.patch("/event-types/{uuid}")
async def update_event_type(
    uuid: str,
    request: UpdateEventTypeRequest,
    authorization: str = Header(...)
):
    """🆕 Update an existing event type (duration, name, location, etc.)"""
    api_key = authorization.replace("Bearer ", "")
    
    payload = {}
    
    for key in ["name", "duration", "description", "color", "visibility", "active"]:
        value = getattr(request, key, None)
        if value is not None:
            payload[key] = value
    
    if request.location_kind:
        location = {"kind": request.location_kind}
        if request.location_details:
            if request.location_kind == "physical":
                location["location"] = request.location_details
            else:
                location["additional_info"] = request.location_details
        payload["locations"] = [location]
    
    return await calendly_request(api_key, "PATCH", f"event_types/{uuid}", json_data=payload)


@app.get("/event-types")
async def list_event_types(
    authorization: str = Header(...),
    user: Optional[str] = None,
    organization: Optional[str] = None,
    active: Optional[bool] = None,
    count: int = 20,
    sort: Optional[str] = None
):
    """List event types for a user or organization"""
    api_key = authorization.replace("Bearer ", "")
    
    params = {"count": count}
    if user:
        params["user"] = user
    if organization:
        params["organization"] = organization
    if active is not None:
        params["active"] = str(active).lower()
    if sort:
        params["sort"] = sort
    
    return await calendly_request(api_key, "GET", "event_types", params=params)


@app.get("/event-types/{uuid}")
async def get_event_type(uuid: str, authorization: str = Header(...)):
    """Get details of a specific event type"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", f"event_types/{uuid}")


@app.get("/event-types/{event_type}/available-times")
async def list_event_type_available_times(
    event_type: str,
    start_time: str,
    end_time: str,
    authorization: str = Header(...)
):
    """Get available time slots for an event type"""
    api_key = authorization.replace("Bearer ", "")
    
    params = {
        "event_type": event_type,
        "start_time": start_time,
        "end_time": end_time
    }
    
    return await calendly_request(api_key, "GET", "event_type_available_times", params=params)


# EVENT TYPE AVAILABILITY SCHEDULES (NEW!)

@app.get("/event-type-availability-schedules")
async def list_event_type_availability_schedules(
    event_type: str,
    authorization: str = Header(...)
):
    """🆕 List availability schedules for an event type"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key, 
        "GET", 
        "event_type_availability_schedules",
        params={"event_type": event_type}
    )


@app.patch("/event-type-availability-schedules/{event_type}")
async def update_event_type_availability_schedule(
    event_type: str,
    request: UpdateAvailabilityScheduleRequest,
    authorization: str = Header(...)
):
    """🆕 Update availability schedule for an event type"""
    api_key = authorization.replace("Bearer ", "")
    
    payload = {}
    if request.availability_rules:
        payload["availability_rule"] = json.loads(request.availability_rules)
    if request.user:
        payload["user"] = request.user
    if request.availability_setting:
        payload["availability_setting"] = request.availability_setting
    
    return await calendly_request(
        api_key,
        "PATCH",
        f"event_type_availability_schedules/{event_type}",
        json_data=payload
    )


# MEETING LOCATIONS (NEW!)

@app.get("/location")
async def list_user_meeting_locations(
    user: str,
    authorization: str = Header(...)
):
    """🆕 List available meeting locations for a user"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "GET",
        "location",
        params={"user": user}
    )


# ============================================================================
# SCHEDULED EVENTS
# ============================================================================

@app.get("/events")
async def list_events(
    authorization: str = Header(...),
    user: Optional[str] = None,
    organization: Optional[str] = None,
    invitee_email: Optional[str] = None,
    status: Optional[str] = None,
    min_start_time: Optional[str] = None,
    max_start_time: Optional[str] = None,
    count: int = 20
):
    """List scheduled events with various filters"""
    api_key = authorization.replace("Bearer ", "")
    
    params = {"count": count}
    for key in ["user", "organization", "invitee_email", "status", "min_start_time", "max_start_time"]:
        value = locals().get(key)
        if value:
            params[key] = value
    
    return await calendly_request(api_key, "GET", "scheduled_events", params=params)


@app.get("/events/{uuid}")
async def get_event(uuid: str, authorization: str = Header(...)):
    """Get details of a specific scheduled event"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", f"scheduled_events/{uuid}")


@app.post("/events/{uuid}/cancel")
async def cancel_event(
    uuid: str,
    authorization: str = Header(...),
    reason: Optional[str] = None
):
    """Cancel a scheduled event"""
    api_key = authorization.replace("Bearer ", "")
    
    payload = {}
    if reason:
        payload["reason"] = reason
    
    return await calendly_request(
        api_key,
        "POST",
        f"scheduled_events/{uuid}/cancellation",
        json_data=payload
    )


@app.post("/events")
async def create_event_invitee(
    request: CreateEventInviteeRequest,
    authorization: str = Header(...)
):
    """🆕 SCHEDULING API: Create a scheduled event (book a meeting) programmatically"""
    api_key = authorization.replace("Bearer ", "")
    
    payload = {
        "event_type_uuid": request.event_type_uuid,
        "start_time": request.start_time,
        "email": request.email,
        "name": request.name
    }
    
    optional = ["first_name", "last_name", "timezone", "guests"]
    for key in optional:
        value = getattr(request, key, None)
        if value:
            payload[key] = value
    
    if request.questions_and_answers:
        payload["questions_and_answers"] = json.loads(request.questions_and_answers)
    
    return await calendly_request(api_key, "POST", "scheduled_events", json_data=payload)


# ============================================================================
# EVENT INVITEES
# ============================================================================

@app.get("/events/{event_uuid}/invitees")
async def list_event_invitees(
    event_uuid: str,
    authorization: str = Header(...),
    email: Optional[str] = None,
    status: Optional[str] = None,
    count: int = 20
):
    """List invitees for a scheduled event"""
    api_key = authorization.replace("Bearer ", "")
    
    params = {"count": count}
    if email:
        params["email"] = email
    if status:
        params["status"] = status
    
    return await calendly_request(
        api_key,
        "GET",
        f"scheduled_events/{event_uuid}/invitees",
        params=params
    )


@app.get("/events/{event_uuid}/invitees/{invitee_uuid}")
async def get_event_invitee(
    event_uuid: str,
    invitee_uuid: str,
    authorization: str = Header(...)
):
    """Get details of a specific event invitee"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "GET",
        f"scheduled_events/{event_uuid}/invitees/{invitee_uuid}"
    )


# ============================================================================
# AVAILABILITY SCHEDULES
# ============================================================================

@app.get("/user-availability-schedules")
async def list_user_availability_schedules(
    user: str,
    authorization: str = Header(...)
):
    """List availability schedules for a user"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "GET",
        "user_availability_schedules",
        params={"user": user}
    )


@app.get("/user-availability-schedules/{uuid}")
async def get_user_availability_schedule(
    uuid: str,
    authorization: str = Header(...)
):
    """Get details of an availability schedule"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "GET",
        f"user_availability_schedules/{uuid}"
    )


@app.get("/user-busy-times")
async def list_user_busy_times(
    user: str,
    start_time: str,
    end_time: str,
    authorization: str = Header(...)
):
    """Get busy times for a user within a date range"""
    api_key = authorization.replace("Bearer ", "")
    
    params = {
        "user": user,
        "start_time": start_time,
        "end_time": end_time
    }
    
    return await calendly_request(api_key, "GET", "user_busy_times", params=params)


# ============================================================================
# ORGANIZATIONS
# ============================================================================

@app.get("/organizations/{uuid}")
async def get_organization(uuid: str, authorization: str = Header(...)):
    """Get organization details by UUID"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", f"organizations/{uuid}")


@app.get("/organization-memberships")
async def list_organization_memberships(
    organization: str,
    authorization: str = Header(...),
    email: Optional[str] = None,
    count: int = 20
):
    """List members of an organization"""
    api_key = authorization.replace("Bearer ", "")
    
    params = {"organization": organization, "count": count}
    if email:
        params["email"] = email
    
    return await calendly_request(api_key, "GET", "organization_memberships", params=params)


@app.get("/organization-memberships/{uuid}")
async def get_organization_membership(uuid: str, authorization: str = Header(...)):
    """Get details of an organization membership"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", f"organization_memberships/{uuid}")


@app.delete("/organization-memberships/{uuid}")
async def delete_organization_membership(uuid: str, authorization: str = Header(...)):
    """Remove a user from an organization"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "DELETE", f"organization_memberships/{uuid}")


@app.get("/organizations/{org_uuid}/invitations")
async def list_organization_invitations(
    org_uuid: str,
    authorization: str = Header(...),
    email: Optional[str] = None,
    status: Optional[str] = None,
    count: int = 20
):
    """List pending organization invitations"""
    api_key = authorization.replace("Bearer ", "")
    
    params = {"count": count}
    if email:
        params["email"] = email
    if status:
        params["status"] = status
    
    return await calendly_request(
        api_key,
        "GET",
        f"organizations/{org_uuid}/invitations",
        params=params
    )


@app.get("/organizations/{org_uuid}/invitations/{invitation_uuid}")
async def get_organization_invitation(
    org_uuid: str,
    invitation_uuid: str,
    authorization: str = Header(...)
):
    """Get details of an organization invitation"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "GET",
        f"organizations/{org_uuid}/invitations/{invitation_uuid}"
    )


@app.post("/organization-invitations")
async def create_organization_invitation(
    request: CreateOrganizationInvitationRequest,
    authorization: str = Header(...)
):
    """Invite a user to an organization"""
    api_key = authorization.replace("Bearer ", "")
    
    org_uuid = request.organization.split("/")[-1]
    
    return await calendly_request(
        api_key,
        "POST",
        f"organizations/{org_uuid}/invitations",
        json_data={"email": request.email}
    )


@app.delete("/organizations/{org_uuid}/invitations/{invitation_uuid}")
async def revoke_organization_invitation(
    org_uuid: str,
    invitation_uuid: str,
    authorization: str = Header(...)
):
    """Revoke a pending organization invitation"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "DELETE",
        f"organizations/{org_uuid}/invitations/{invitation_uuid}"
    )


# ============================================================================
# WEBHOOKS
# ============================================================================

@app.get("/webhook-subscriptions")
async def list_webhook_subscriptions(
    organization: str,
    authorization: str = Header(...),
    scope: str = "organization"
):
    """List webhook subscriptions for an organization"""
    api_key = authorization.replace("Bearer ", "")
    
    params = {"organization": organization, "scope": scope}
    
    return await calendly_request(api_key, "GET", "webhook_subscriptions", params=params)


@app.post("/webhook-subscriptions")
async def create_webhook_subscription(
    request: CreateWebhookRequest,
    authorization: str = Header(...)
):
    """Create a new webhook subscription"""
    api_key = authorization.replace("Bearer ", "")
    
    payload = {
        "url": request.url,
        "organization": request.organization,
        "events": request.events,
        "scope": request.scope
    }
    
    if request.signing_key:
        payload["signing_key"] = request.signing_key
    
    return await calendly_request(api_key, "POST", "webhook_subscriptions", json_data=payload)


@app.get("/webhook-subscriptions/{webhook_uuid}")
async def get_webhook_subscription(
    webhook_uuid: str,
    authorization: str = Header(...)
):
    """Get details of a webhook subscription"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(api_key, "GET", f"webhook_subscriptions/{webhook_uuid}")


@app.delete("/webhook-subscriptions/{webhook_uuid}")
async def delete_webhook_subscription(
    webhook_uuid: str,
    authorization: str = Header(...)
):
    """Delete a webhook subscription"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(api_key, "DELETE", f"webhook_subscriptions/{webhook_uuid}")


# ============================================================================
# ROUTING FORMS
# ============================================================================

@app.get("/routing-forms")
async def list_routing_forms(
    organization: str,
    authorization: str = Header(...),
    count: int = 20
):
    """List routing forms for an organization"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "GET",
        "routing_forms",
        params={"organization": organization, "count": count}
    )


@app.get("/routing-forms/{uuid}")
async def get_routing_form(uuid: str, authorization: str = Header(...)):
    """Get details of a routing form"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", f"routing_forms/{uuid}")


@app.get("/routing-forms/{form_uuid}/submissions")
async def list_routing_form_submissions(
    form_uuid: str,
    authorization: str = Header(...),
    count: int = 20
):
    """List submissions for a routing form"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "GET",
        f"routing_forms/{form_uuid}/submissions",
        params={"count": count}
    )


@app.get("/routing-form-submissions/{uuid}")
async def get_routing_form_submission(uuid: str, authorization: str = Header(...)):
    """Get details of a routing form submission"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", f"routing_form_submissions/{uuid}")


# ============================================================================
# SCHEDULING LINKS
# ============================================================================

@app.post("/scheduling-links")
async def create_scheduling_link(
    request: CreateSchedulingLinkRequest,
    authorization: str = Header(...)
):
    """Create a single-use scheduling link"""
    api_key = authorization.replace("Bearer ", "")
    
    payload = {
        "max_event_count": request.max_event_count,
        "owner": request.owner,
        "owner_type": request.owner_type
    }
    
    return await calendly_request(api_key, "POST", "scheduling_links", json_data=payload)


# ============================================================================
# INVITEE NO-SHOWS
# ============================================================================

@app.post("/invitee-no-shows")
async def create_invitee_no_show(
    invitee: str,
    authorization: str = Header(...)
):
    """Mark an invitee as a no-show"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "POST",
        "invitee_no_shows",
        json_data={"invitee": invitee}
    )


@app.get("/invitee-no-shows/{uuid}")
async def get_invitee_no_show(uuid: str, authorization: str = Header(...)):
    """Get no-show details"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "GET", f"invitee_no_shows/{uuid}")


@app.delete("/invitee-no-shows/{uuid}")
async def delete_invitee_no_show(uuid: str, authorization: str = Header(...)):
    """Unmark an invitee as a no-show"""
    api_key = authorization.replace("Bearer ", "")
    return await calendly_request(api_key, "DELETE", f"invitee_no_shows/{uuid}")


# ============================================================================
# DATA COMPLIANCE (GDPR)
# ============================================================================

@app.post("/data-compliance/deletion/invitees")
async def delete_invitee_data(
    request: DeleteInviteeDataRequest,
    authorization: str = Header(...)
):
    """Delete all data for invitee emails (GDPR compliance)"""
    api_key = authorization.replace("Bearer ", "")
    
    return await calendly_request(
        api_key,
        "POST",
        "data_compliance/deletion/invitees",
        json_data={"emails": request.emails}
    )


# ============================================================================
# SERVER STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Calendly Connector API (COMPLETE) starting on http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("📖 API Spec: http://localhost:8000/openapi.json")
    uvicorn.run(app, host="0.0.0.0", port=8000)
