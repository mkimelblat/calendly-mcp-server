# Calendly MCP Server

A complete Model Context Protocol (MCP) server for the Calendly API. This server provides full access to all Calendly API endpoints, including **Event Type Management APIs** for creating and updating event types programmatically.

## 🆕 Latest Updates (v2.1.0)

**NEW! Complete Event Type Management:**
- ✅ **Create new event types** - Build event types programmatically
- ✅ **Update existing event types** - Modify duration, location, description, and more
- ✅ **Manage availability schedules** - Configure when event types are available
- ✅ **List meeting locations** - Get all configured meeting location options

Now includes **45+ Calendly API endpoints** with complete CRUD operations!

## Features

✅ **Complete API Coverage** - All Calendly API v2 endpoints
✅ **Event Type Management** - Create, read, update event types ⭐ NEW
✅ **Scheduling API** - Book meetings programmatically
✅ **Update Operations** - Modify event types, schedules, and settings
✅ **Delete Operations** - Remove unwanted resources
✅ **Create Operations** - Full creation capabilities
✅ **Read Operations** - Query all Calendly data
✅ **Easy Setup** - Simple configuration with your API key

## What This Enables

### Event Type Management (NEW!)
- Create new event types without using the Calendly UI
- Update event type durations, locations, and settings in bulk
- Modify availability schedules programmatically
- Configure meeting locations via API

### Scheduling & Events
- Book meetings programmatically (Scheduling API)
- Cancel and manage scheduled events
- Track invitees and no-shows
- Bulk operations on multiple events

### Organization & Users
- Manage organization memberships
- Invite and remove users
- Configure webhooks for real-time updates
- GDPR compliance tools

## Prerequisites

- Python 3.10 or higher
- A Calendly account
- A Calendly API key (Personal Access Token)

## Installation

### 1. Clone this repository

```bash
git clone https://github.com/mkimelblat/calendly-mcp-server.git
cd calendly-mcp-server
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Get your Calendly API key

1. Go to https://calendly.com
2. Log in to your account
3. Navigate to: Profile → Settings → Integrations → API & Webhooks
4. Click "Generate New Token"
5. Copy the token (keep it secure!)

### 4. Configure the server

Create a `.env` file in the project root:

```bash
CALENDLY_API_KEY=your_api_key_here
```

**Important:** Never commit your `.env` file to GitHub! It's already in `.gitignore`.

## Usage with Claude

### Option 1: Using Claude Desktop

Add this to your Claude Desktop configuration file:

**On macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**On Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "calendly": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/calendly-mcp-server/server.py"],
      "env": {
        "CALENDLY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Replace `/path/to/` with your actual paths.

### Option 2: Using with Claude API

```python
from anthropic import Anthropic

client = Anthropic(api_key="your_anthropic_api_key")

# The MCP server will be available as tools
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[...],  # MCP tools will be injected here
    messages=[
        {"role": "user", "content": "Create a new 45 minute strategy session event type"}
    ]
)
```

## Available Operations

### Event Type Management ⭐ NEW
- `create_event_type` - **Create new event types programmatically**
- `update_event_type` - **Update event type settings**
- `list_event_types` - List all event types
- `get_event_type` - Get event type details
- `list_event_type_availability_schedules` - **List availability schedules**
- `update_event_type_availability_schedule` - **Modify availability**
- `list_user_meeting_locations` - **Get meeting location options**

### Scheduled Events
- `create_event_invitee` - **Book meetings programmatically** (Scheduling API)
- `list_events` - List scheduled events
- `get_event` - Get event details
- `cancel_event` - Cancel a scheduled event
- `list_event_invitees` - Get invitee information

### Users & Organization
- `get_current_user` - Get your user information
- `get_user` - Get any user's information
- `list_organization_memberships` - List organization members
- `create_organization_invitation` - Invite users
- `delete_organization_membership` - Remove users

### Webhooks
- `create_webhook_subscription` - Set up real-time notifications
- `list_webhook_subscriptions` - List active webhooks
- `delete_webhook_subscription` - Remove webhooks

### And 30+ more!

See [API_REFERENCE.md](./API_REFERENCE.md) for complete documentation.

## Examples

### Create a new event type

```python
# Through Claude:
"Create a new 45-minute event type called 'Strategy Session' with Zoom as the location"
```

### Update an event type duration

```python
# Through Claude:
"Update my '30 min chat' event type to be 20 minutes instead"
```

### Change event type location

```python
# Through Claude:
"Change my 'Team Sync' event type location from Google Meet to Zoom"
```

### Book a meeting programmatically

```python
# Through Claude:
"Schedule a meeting for john@example.com tomorrow at 2pm using my '30 min chat' event type"
```

### Bulk update event types

```python
# Through Claude:
"Update all my 30-minute event types to 25 minutes"
```

## API Endpoint Coverage

This server provides access to **45+ Calendly API v2 endpoints**:

- ✅ Users (2 endpoints)
- ✅ Event Types (7 endpoints) - Including NEW management APIs
- ✅ Scheduled Events (5 endpoints) - Including Scheduling API
- ✅ Event Invitees (2 endpoints)
- ✅ Availability Schedules (3 endpoints)
- ✅ Organizations (7 endpoints)
- ✅ Webhooks (4 endpoints)
- ✅ Routing Forms (4 endpoints)
- ✅ Scheduling Links (1 endpoint)
- ✅ No-Shows (3 endpoints)
- ✅ Meeting Locations (1 endpoint) - NEW
- ✅ Data Compliance (1 endpoint)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security

- Never commit your API keys or `.env` file
- Use environment variables for sensitive data
- Rotate your API keys regularly
- Follow the principle of least privilege

## Troubleshooting

### "Module not found" errors
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### "Authentication failed" errors
Check that your `CALENDLY_API_KEY` is correct and hasn't expired.

### Connection issues
Ensure you have internet connectivity and can reach api.calendly.com

### Python version errors
Make sure you're using Python 3.10 or higher:
```bash
python3 --version
```

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

- Built using the [Model Context Protocol](https://modelcontextprotocol.io)
- Powered by the [Calendly API](https://developer.calendly.com)
- Created for use with [Claude](https://claude.ai)

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [Calendly API documentation](https://developer.calendly.com/api-docs)
- Review the [MCP documentation](https://modelcontextprotocol.io)

## Version History

### v2.1.0 (Current)
- Added Event Type Management APIs
- Create and update event types programmatically
- Manage event type availability schedules
- List user meeting locations
- Complete coverage of all Calendly API v2 endpoints (45+ tools)

### v1.0.0
- Initial release
- Core API endpoint coverage
- Scheduling API support

---

**Made with ❤️ for the Claude and Calendly communities**
