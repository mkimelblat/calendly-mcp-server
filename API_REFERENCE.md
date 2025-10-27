# API Reference

Complete documentation for all available tools in the Calendly MCP Server.

## Table of Contents

- [Event Type Management](#event-type-management) ⭐ NEW
- [Event Types](#event-types)
- [Scheduled Events](#scheduled-events)
- [Event Invitees](#event-invitees)
- [Availability Schedules](#availability-schedules)
- [Users](#users)
- [Organizations](#organizations)
- [Webhooks](#webhooks)
- [Routing Forms](#routing-forms)
- [Scheduling Links](#scheduling-links)
- [No-Shows](#no-shows)
- [Data Compliance](#data-compliance)

---

## Event Type Management ⭐ NEW

### `create_event_type`

🆕 Create a new one-on-one event type with custom settings.

**Parameters:**
- `name` (string, required): Event type name (e.g., '45 Minute Meeting')
- `owner` (string, required): Owner user URI
- `duration` (integer, required): Duration in minutes
- `description` (string, optional): Event description
- `color` (string, optional): Color hex code (e.g., #8247f5)
- `location_kind` (string, optional): Type of location
  - `zoom_conference`, `google_conference`, `microsoft_teams_conference`
  - `physical`, `inbound_call`, `outbound_call`, `custom`, `ask_invitee`
- `location_details` (string, optional): Additional location information
- `visibility` (string, optional): `public` or `private`
- `locale` (string, optional): Locale (e.g., en, es, fr)

**Example:**
```
Create a new 45-minute event type called "Strategy Session" with Zoom
```

**Note:** Only supports one-on-one event types with basic configuration.

---

### `update_event_type`

🆕 Update an existing event type.

**Parameters:**
- `uuid` (string, required): The UUID of the event type
- `name` (string, optional): New name
- `duration` (integer, optional): New duration in minutes
- `description` (string, optional): New description
- `color` (string, optional): New color hex code
- `location_kind` (string, optional): New location type
- `location_details` (string, optional): Location details
- `visibility` (string, optional): `public` or `private`
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

### `list_event_type_availability_schedules`

🆕 List availability schedules for an event type.

**Parameters:**
- `event_type` (string, required): Event type UUID

**Example:**
```
List availability schedules for event type abc123
```

---

### `update_event_type_availability_schedule`

🆕 Update availability schedule for an event type.

**Parameters:**
- `event_type` (string, required): Event type UUID
- `availability_rules` (string, optional): JSON string of availability rules
- `user` (string, optional): User URI
- `availability_setting` (string, optional): `host` or `custom`

**Rules Format:**
```json
{
  "timezone": "America/New_York",
  "rules": [
    {
      "type": "wday",
      "wday": "monday",
      "intervals": [{"from": "09:00", "to": "17:00"}]
    },
    {
      "type": "date",
      "date": "2025-12-25",
      "intervals": []
    }
  ]
}
```

**Example:**
```
Update availability for event type abc123 to only Monday-Friday 9am-5pm
```

**Important:** This endpoint replaces ALL existing rules. Get current rules first, modify them, then send all rules back.

---

### `list_user_meeting_locations`

🆕 List available meeting locations for a user.

**Parameters:**
- `user` (string, required): User URI

**Example:**
```
List all meeting locations for user https://api.calendly.com/users/XXX
```

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
- `sort` (string, optional): Sort order (name:asc, name:desc)

**Example:**
```
List all active event types for user https://api.calendly.com/users/XXX
```

---

### `list_event_type_available_times`

Get available time slots for an event type.

**Parameters:**
- `event_type` (string, required): URI of the event type
- `start_time` (string, required): Start of range (ISO 8601)
- `end_time` (string, required): End of range (ISO 8601)

**Example:**
```
Show available times for event type XXX next week
```

**Note:** Maximum range is 7 days.

---

## Scheduled Events

### `create_event_invitee`

🆕 SCHEDULING API: Create a scheduled event (book a meeting) programmatically.

**Parameters:**
- `event_type_uuid` (string, required): Event type UUID
- `start_time` (string, required): Start time (ISO 8601)
- `email` (string, required): Invitee email
- `name` (string, required): Invitee full name
- `first_name` (string, optional): Invitee first name
- `last_name` (string, optional): Invitee last name
- `timezone` (string, optional): Timezone (e.g., America/New_York)
- `guests` (array, optional): Array of guest email addresses
- `questions_and_answers` (string, optional): JSON string of Q&A pairs

**Example:**
```
Schedule a meeting for john@example.com tomorrow at 2pm using my "30 min chat" event type
```

**Note:** Requires a paid Calendly plan.

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

### `get_event`

Get details of a scheduled event.

**Parameters:**
- `uuid` (string, required): The UUID of the scheduled event

**Example:**
```
Get event details for UUID abc123
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

## Event Invitees

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

### `get_event_invitee`

Get details of a specific event invitee.

**Parameters:**
- `event_uuid` (string, required): UUID of the event
- `invitee_uuid` (string, required): UUID of the invitee

**Example:**
```
Get invitee details for event abc123, invitee xyz789
```

---

## Availability Schedules

### `list_user_availability_schedules`

List all availability schedules for a user.

**Parameters:**
- `user` (string, required): URI of the user

**Example:**
```
List all schedules for user https://api.calendly.com/users/XXX
```

---

### `get_user_availability_schedule`

Get details of a user availability schedule.

**Parameters:**
- `uuid` (string, required): The UUID of the availability schedule

**Example:**
```
Get schedule details for UUID abc123
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
- `uuid` (string, required): The UUID of the user

**Example:**
```
Get user information for UUID abc123
```

---

## Organizations

### `get_organization`

Get organization details by UUID.

**Parameters:**
- `uuid` (string, required): Organization UUID

**Example:**
```
Get organization details for UUID abc123
```

---

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

### `get_organization_membership`

Get details of an organization membership.

**Parameters:**
- `uuid` (string, required): Membership UUID

**Example:**
```
Get membership details for UUID abc123
```

---

### `delete_organization_membership`

Remove a user from an organization.

**Parameters:**
- `uuid` (string, required): Membership UUID

**Example:**
```
Remove membership abc123 from organization
```

---

### `list_organization_invitations`

List pending organization invitations.

**Parameters:**
- `organization` (string, required): URI of the organization
- `email` (string, optional): Filter by email
- `status` (string, optional): Status: pending or declined
- `count` (integer, optional): Number of results

**Example:**
```
List pending invitations for organization XXX
```

---

### `get_organization_invitation`

Get details of an organization invitation.

**Parameters:**
- `org_uuid` (string, required): Organization UUID
- `invitation_uuid` (string, required): Invitation UUID

**Example:**
```
Get invitation details for org abc123, invitation xyz789
```

---

### `create_organization_invitation`

Invite a user to an organization.

**Parameters:**
- `organization` (string, required): URI of the organization
- `email` (string, required): Email address to invite

**Example:**
```
Invite user@example.com to organization XXX
```

---

### `revoke_organization_invitation`

Revoke a pending organization invitation.

**Parameters:**
- `org_uuid` (string, required): Organization UUID
- `invitation_uuid` (string, required): Invitation UUID

**Example:**
```
Revoke invitation xyz789 from organization abc123
```

---

## Webhooks

### `list_webhook_subscriptions`

List webhook subscriptions for an organization.

**Parameters:**
- `organization` (string, required): URI of the organization
- `scope` (string, optional): Scope (organization or user, default: organization)

**Example:**
```
List all webhooks for organization XXX
```

---

### `create_webhook_subscription`

Create a webhook subscription.

**Parameters:**
- `url` (string, required): The URL to send webhook events to
- `organization` (string, required): URI of the organization
- `events` (array, required): Array of event types
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

### `get_webhook_subscription`

Get details of a webhook subscription.

**Parameters:**
- `webhook_uuid` (string, required): UUID of the webhook subscription

**Example:**
```
Get webhook details for UUID abc123
```

---

### `delete_webhook_subscription`

Delete a webhook subscription.

**Parameters:**
- `webhook_uuid` (string, required): UUID of the webhook subscription

**Example:**
```
Delete webhook abc123
```

---

## Routing Forms

### `list_routing_forms`

List routing forms for an organization.

**Parameters:**
- `organization` (string, required): URI of the organization
- `count` (integer, optional): Number of results

**Example:**
```
List all routing forms for organization XXX
```

---

### `get_routing_form`

Get details of a routing form.

**Parameters:**
- `uuid` (string, required): Routing form UUID

**Example:**
```
Get routing form details for UUID abc123
```

---

### `list_routing_form_submissions`

List submissions for a routing form.

**Parameters:**
- `form_uuid` (string, required): Routing form UUID
- `count` (integer, optional): Number of results

**Example:**
```
List submissions for routing form abc123
```

---

### `get_routing_form_submission`

Get details of a routing form submission.

**Parameters:**
- `uuid` (string, required): Submission UUID

**Example:**
```
Get submission details for UUID abc123
```

---

## Scheduling Links

### `create_scheduling_link`

Create a single-use scheduling link.

**Parameters:**
- `max_event_count` (integer, required): Max bookings (default: 1)
- `owner` (string, required): Event type owner URI
- `owner_type` (string, required): EventType or User

**Example:**
```
Create a single-use link for my "30 min chat" event type
```

**Note:** Links expire after 90 days if unused.

---

## No-Shows

### `create_invitee_no_show`

Mark an invitee as a no-show.

**Parameters:**
- `invitee` (string, required): Invitee URI

**Example:**
```
Mark invitee abc123 as no-show
```

---

### `get_invitee_no_show`

Get no-show details.

**Parameters:**
- `uuid` (string, required): No-show UUID

**Example:**
```
Get no-show details for UUID abc123
```

---

### `delete_invitee_no_show`

Unmark an invitee as a no-show.

**Parameters:**
- `uuid` (string, required): No-show UUID

**Example:**
```
Unmark no-show abc123
```

---

## Data Compliance

### `delete_invitee_data`

Delete all data for invitee emails (GDPR compliance).

**Parameters:**
- `emails` (array, required): Array of email addresses

**Example:**
```
Delete all data for emails ["user1@example.com", "user2@example.com"]
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

## New Features Summary

🆕 = New in v2.1.0

- Event Type Management (5 new endpoints)
- Complete CRUD operations for event types
- Availability schedule management
- Meeting location queries
- 45+ total endpoints with full API coverage

---

⭐ = Premium feature requiring paid Calendly plan
