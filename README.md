# Calendly MCP Server

A complete Model Context Protocol (MCP) server for the Calendly API. This server provides full access to all Calendly API endpoints, including update and delete operations not available in other integrations.

## Features

✅ **Complete API Coverage** - All Calendly API endpoints
✅ **Update Operations** - Modify event types, schedules, and settings
✅ **Delete Operations** - Remove event types and schedules
✅ **Create Operations** - Full creation capabilities
✅ **Read Operations** - Query all Calendly data
✅ **Easy Setup** - Simple configuration with your API key

## What This Enables

- Update event type durations, locations, and settings
- Modify availability schedules and working hours
- Delete unwanted event types
- Create custom scheduling workflows
- Bulk operations on multiple event types
- And much more!

## Prerequisites

- Python 3.8 or higher
- A Calendly account
- A Calendly API key (Personal Access Token)

## Installation

### 1. Clone this repository

```bash
git clone https://github.com/YOUR_USERNAME/calendly-mcp-server.git
cd calendly-mcp-server
```

### 2. Install dependencies

```bash
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
      "command": "python",
      "args": ["/path/to/calendly-mcp-server/server.py"],
      "env": {
        "CALENDLY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Option 2: Using with Claude API

```python
from anthropic import Anthropic

client = Anthropic(api_key="your_anthropic_api_key")

# The MCP server will be available as tools
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[...],  # MCP tools will be injected here
    messages=[
        {"role": "user", "content": "Update my 30 min chat event type to 20 minutes"}
    ]
)
```

## Available Operations

### Event Types
- `get_event_type` - Get details of an event type
- `list_event_types` - List all event types
- `create_event_type` - Create a new event type
- `update_event_type` - **Update event type settings** ✨
- `delete_event_type` - **Delete an event type** ✨

### Availability Schedules
- `get_user_availability_schedule` - Get schedule details
- `list_user_availability_schedules` - List all schedules
- `create_user_availability_schedule` - Create new schedule
- `update_user_availability_schedule` - **Modify schedule** ✨
- `delete_user_availability_schedule` - **Remove schedule** ✨

### Scheduled Events
- `get_event` - Get event details
- `list_events` - List scheduled events
- `cancel_event` - Cancel a scheduled event
- `list_event_invitees` - Get invitee information

### Users
- `get_current_user` - Get your user information
- `get_user` - Get any user's information

### And many more!

See [API_REFERENCE.md](./API_REFERENCE.md) for complete documentation.

## Examples

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

### Delete test event types

```python
# Through Claude:
"Delete all event types that start with 'Test'"
```

### Block Friday afternoons

```python
# Through Claude:
"Update my availability schedule to block every Friday after 2pm"
```

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

---

**Made with ❤️ for the Claude and Calendly communities**
