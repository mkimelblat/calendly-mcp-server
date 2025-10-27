# API Reference

Complete documentation for all available tools in the Calendly MCP Server.

## Table of Contents

- [Event Types](#event-types)
- [Availability Schedules](#availability-schedules)
- [Scheduled Events](#scheduled-events)
- [Users](#users)
- [Webhooks](#webhooks)
- [Organization](#organization)
- [Helper Tools](#helper-tools)

---

## Event Types

### `get_event_type`

Get details of a specific event type.

**Parameters:**
- `uuid` (string, required): The UUID of the event type

**Example:**
```
Get details for event type with UUID abc123
```

---

### `list_event_types`

List event types for a user or organization.

**Parameters:**
- `user` (string, optional): URI of the user
- `organization` (string, optional): URI of the organization
- `active` (boolean, optional): Filter by active status
- `count` (integer, optional): Number of results (default: 20, max: 100)

**Example:**
```
List all active event types for user https://api.calendly.com/users/XXX
```

---

### `update_event_type` ⭐

Update an existing event type.

**Parameters:**
- `uuid` (string, required): The UUID of the event type
- `name` (string, optional): New name
- `duration` (integer, optional): New duration in minutes
- `description_plain` (string, optional): Plain text description
- `description_html` (string, optional): HTML description
- `location_kind` (string, optional): Type of location
  - `zoom_conference`, `google_conference`, `microsoft_teams_conference`
  - `physical`, `inbound_call`, `outbound_call`, `custom`, `ask_invitee`
- `location_details` (string, optional): Additional location information
- `color` (string, optional): Hex color code (e.g., #8247f5)
- `active` (boolean, optional): Whether the event type is active

**Examples:**
```
Update event type abc123 to 20 minutes duration
```
```
Change event type abc123 location to zoom_conference
```
```
Rename event type abc123 to "Quick Chat" and make it 15 minutes
```

---

### `delete_event_type` ⭐

Delete an event type.

**Parameters:**
- `uuid` (string, required): The UUID of the event type

**Example:**
```
Delete event type with UUID abc123
```

---

## Availability Schedules

### `get_user_availability_schedule`

Get details of a user availability schedule.

**Parameters:**
- `uuid` (string, required): The UUID of the availability schedule

**Example:**
```
Get schedule details for UUID abc123
```

---

### `list_user_availability_schedules`

List all availability schedules for a user.

**Parameters:**
- `user` (string, required): URI of the user

**Example:**
```
List all schedules for user https://api.calendly.com/users/XXX
```

---

### `create_user_availability_schedule` ⭐

Create a new availability schedule.

**Parameters:**
- `user` (string, required): URI of the user
- `name` (string, required): Name for the schedule
- `timezone` (string, required): IANA timezone (e.g., America/New_York)
- `rules` (string, required): JSON string of availability rules

**Rules Format:**
```json
[
  {
    "type": "wday",
    "wday": "monday",
    "intervals": [
      {"from": "09:00", "to": "17:00"}
    ]
  },
  {
    "type": "wday",
    "wday": "friday",
    "intervals": [
      {"from": "09:00", "to": "14:00"}
    ]
  }
]
```

**Example:**
```
Create a new schedule "Afternoon Only" for user XXX in America/Los_Angeles
with Monday-Friday 1pm-5pm availability
```

---

### `update_user_availability_schedule` ⭐

Update an existing availability schedule.

**Parameters:**
- `uuid` (string, required): The UUID of the schedule
- `name` (string, optional): New name
- `timezone` (string, optional): New IANA timezone
- `rules` (string, optional): JSON string of new availability rules

**Example:**
```
Update schedule abc123 to block Friday afternoons after 2pm
```

---

### `delete_user_availability_schedule` ⭐

Delete an availability schedule.

**Parameters:**
- `uuid` (string, required): The UUID of the schedule

**Example:**
```
Delete schedule with UUID abc123
```

---

## Scheduled Events

### `get_event`

Get details of a scheduled event.

**Parameters:**
- `uuid` (string, required): The UUID of the scheduled event

**Example:**
```
Get event details for UUID abc123
```

---

### `list_events`

List scheduled events.

**Parameters:**
- `user` (string, optional): URI of the user
- `organization` (string, optional): URI of the organization
- `invitee_email` (string, optional): Filter by invitee email
- `status` (string, optional): Filter by status (active, canceled)
- `min_start_time` (string, optional): Minimum start time (ISO 8601)
- `max_start_time` (string, optional): Maximum start time (ISO 8601)
- `count` (integer, optional): Number of results (default: 20, max: 100)

**Example:**
```
List all active events for user XXX next week
```

---

### `cancel_event`

Cancel a scheduled event.

**Parameters:**
- `uuid` (string, required): The UUID of the event
- `reason` (string, optional): Reason for cancellation (sent to invitees)

**Example:**
```
Cancel event abc123 with reason "Schedule conflict"
```

---

### `list_event_invitees`

List invitees for a scheduled event.

**Parameters:**
- `event_uuid` (string, required): UUID of the scheduled event
- `email` (string, optional): Filter by invitee email
- `status` (string, optional): Filter by status (active, canceled)
- `count` (integer, optional): Number of results (default: 20, max: 100)

**Example:**
```
List all invitees for event abc123
```

---

## Users

### `get_current_user`

Get information about the currently authenticated user.

**Parameters:** None

**Example:**
```
Get my user information
```

---

### `get_user`

Get information about a specific user.

**Parameters:**
- `uuid` (string, required): The UUID of the user (or "me" for current user)

**Example:**
```
Get user information for UUID abc123
```

---

## Webhooks

### `list_webhook_subscriptions`

List webhook subscriptions.

**Parameters:**
- `organization` (string, required): URI of the organization
- `scope` (string, optional): Scope (organization or user, default: organization)

**Example:**
```
List all webhooks for organization XXX
```

---

### `create_webhook_subscription` ⭐

Create a webhook subscription.

**Parameters:**
- `url` (string, required): The URL to send webhook events to
- `organization` (string, required): URI of the organization
- `events` (string, required): JSON array of event types
- `scope` (string, optional): Scope (organization or user)
- `signing_key` (string, optional): Signing key for verification

**Event Types:**
- `invitee.created`
- `invitee.canceled`
- `invitee_no_show.created`
- `invitee_no_show.deleted`
- `routing_form_submission.created`

**Example:**
```
Create webhook at https://example.com/webhooks for invitee.created events
```

---

### `delete_webhook_subscription` ⭐

Delete a webhook subscription.

**Parameters:**
- `webhook_uuid` (string, required): UUID of the webhook subscription

**Example:**
```
Delete webhook abc123
```

---

## Organization

### `list_organization_memberships`

List members of an organization.

**Parameters:**
- `organization` (string, required): URI of the organization
- `email` (string, optional): Filter by member email
- `count` (integer, optional): Number of results (default: 20, max: 100)

**Example:**
```
List all members of organization XXX
```

---

### `create_organization_invitation` ⭐

Invite a user to an organization.

**Parameters:**
- `organization` (string, required): URI of the organization
- `email` (string, required): Email address to invite

**Example:**
```
Invite user@example.com to organization XXX
```

---

## Helper Tools

### `list_available_times`

Get available time slots for an event type.

**Parameters:**
- `event_type` (string, required): URI of the event type
- `start_time` (string, required): Start of range (ISO 8601)
- `end_time` (string, required): End of range (ISO 8601)

**Example:**
```
Show available times for event type XXX next week
```

---

### `list_user_busy_times`

Get busy times for a user.

**Parameters:**
- `user` (string, required): URI of the user
- `start_time` (string, required): Start of range (ISO 8601)
- `end_time` (string, required): End of range (ISO 8601)

**Example:**
```
Show when user XXX is busy tomorrow
```

---

## Common Patterns

### URIs

Calendly uses URIs to reference resources:
- Users: `https://api.calendly.com/users/{uuid}`
- Organizations: `https://api.calendly.com/organizations/{uuid}`
- Event Types: `https://api.calendly.com/event_types/{uuid}`

### ISO 8601 Timestamps

Use format: `YYYY-MM-DDTHH:MM:SSZ` (UTC)
- Example: `2025-10-27T14:30:00Z`

### Timezones

Use IANA timezone names:
- `America/New_York`
- `America/Los_Angeles`
- `Europe/London`
- `Asia/Tokyo`

---

⭐ = New capability not available in standard Calendly integrations
