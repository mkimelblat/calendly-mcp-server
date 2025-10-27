# Quick Start Guide

This guide will help you get the Calendly MCP Server running in just a few minutes, even if you're not technical!

## 📋 What You'll Need

1. A computer (Mac, Windows, or Linux)
2. Your Calendly API key
3. About 10 minutes

## 🚀 Step-by-Step Setup

### Step 1: Get Your Calendly API Key

1. Go to https://calendly.com and log in
2. Click your profile picture in the top right
3. Click "Settings"
4. In the left sidebar, click "Integrations"
5. Click "API & Webhooks"
6. Click the "Generate New Token" button
7. **Copy the token** - you'll need it in Step 4!
8. Keep this tab open or save the token somewhere safe

### Step 2: Install Python (if you don't have it)

#### On Mac:
1. Open Terminal (search for "Terminal" in Spotlight)
2. Type: `python3 --version` and press Enter
3. If you see a version number (like `Python 3.11.5`), you're good! Skip to Step 3.
4. If not, go to https://python.org/downloads and install Python

#### On Windows:
1. Go to https://python.org/downloads
2. Download the latest Python installer
3. **Important:** Check the box "Add Python to PATH" during installation
4. Complete the installation

### Step 3: Download This Project

#### Option A: Using Git (if you have it)
```bash
git clone https://github.com/YOUR_USERNAME/calendly-mcp-server.git
cd calendly-mcp-server
```

#### Option B: Download ZIP
1. Click the green "Code" button at the top of this page
2. Click "Download ZIP"
3. Extract the ZIP file
4. Open Terminal/Command Prompt and navigate to the folder:
   - Mac: `cd ~/Downloads/calendly-mcp-server-main`
   - Windows: `cd %USERPROFILE%\Downloads\calendly-mcp-server-main`

### Step 4: Configure Your API Key

1. In the project folder, find the file named `.env.example`
2. Make a copy of it and rename the copy to `.env`
3. Open `.env` in a text editor (Notepad, TextEdit, etc.)
4. Replace `your_calendly_api_key_here` with your actual API key from Step 1
5. Save and close the file

**Your `.env` file should look like:**
```
CALENDLY_API_KEY=eyJraWQiOiIxY2UxZTEzNjE3ZGNm...
LOG_LEVEL=INFO
```

### Step 5: Install Dependencies

Open Terminal (Mac) or Command Prompt (Windows) in the project folder and run:

```bash
pip install -r requirements.txt
```

Or if that doesn't work, try:
```bash
pip3 install -r requirements.txt
```

Wait for it to finish installing (should take 1-2 minutes).

### Step 6: Test It Works

Run this command:
```bash
python server.py
```

Or try:
```bash
python3 server.py
```

If you see "Calendly MCP Server starting..." - success! Press `Ctrl+C` to stop it.

## 🔌 Connect to Claude

### Using Claude Desktop

1. Find your Claude Desktop config file:
   - **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. Open it in a text editor

3. Add this configuration (replace `/path/to/` with your actual path):

```json
{
  "mcpServers": {
    "calendly": {
      "command": "python3",
      "args": ["/path/to/calendly-mcp-server/server.py"],
      "env": {
        "CALENDLY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

4. Save the file

5. Restart Claude Desktop

6. You should now see "Calendly MCP" in your available tools!

## ✅ Verify It's Working

Try asking Claude:
```
"List my active Calendly event types"
```

If you see your event types, everything is working! 🎉

## 🆘 Troubleshooting

### "Python not found" error
- Make sure Python is installed (Step 2)
- Try using `python3` instead of `python`

### "Module not found" error
- Run the install command again: `pip install -r requirements.txt`
- Make sure you're in the right folder

### "Authentication failed" error
- Double-check your API key in the `.env` file
- Make sure there are no extra spaces
- Try generating a new API key

### Claude doesn't see the MCP server
- Make sure you restarted Claude Desktop
- Check that the path in the config file is correct
- Make sure the `.env` file has your API key

## 🎯 What You Can Do Now

Try these commands with Claude:

- "Update my '30 min chat' event type to 20 minutes"
- "Change my Team Sync event to use Zoom instead of Google Meet"
- "List all my event types and their durations"
- "Delete all test event types"
- "Show me my availability schedule"
- "Block Friday afternoons after 2pm"

## 📚 Next Steps

- Read the [API Reference](API_REFERENCE.md) for all available commands
- Check out the [README](README.md) for more details
- Customize the server for your needs

## 💬 Need Help?

- Open an issue on GitHub
- Check the [Calendly API docs](https://developer.calendly.com)
- Review the [MCP documentation](https://modelcontextprotocol.io)

Happy scheduling! 🗓️
