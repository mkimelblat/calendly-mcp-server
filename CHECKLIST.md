# ✅ Getting Started Checklist

Use this checklist to get your Calendly MCP Server up and running!

## 📥 Phase 1: Download & Setup (5 minutes)

- [ ] Download the `calendly-mcp-server` folder
- [ ] Extract it to a location you'll remember
- [ ] Open Terminal (Mac) or Command Prompt (Windows)
- [ ] Navigate to the folder: `cd /path/to/calendly-mcp-server`

## 🔑 Phase 2: Get Your API Key (3 minutes)

- [ ] Go to https://calendly.com
- [ ] Log in to your account
- [ ] Click your profile picture → Settings
- [ ] Navigate to Integrations → API & Webhooks
- [ ] Click "Generate New Token"
- [ ] Copy the token (save it somewhere safe!)

## 🐍 Phase 3: Install Python (if needed) (5 minutes)

- [ ] Check if Python is installed: `python --version` or `python3 --version`
- [ ] If not installed:
  - [ ] Mac: Download from https://python.org/downloads
  - [ ] Windows: Download from https://python.org/downloads
  - [ ] **Windows users:** Check "Add Python to PATH"
- [ ] Restart Terminal/Command Prompt after installation

## ⚙️ Phase 4: Configure the Server (2 minutes)

- [ ] Copy `.env.example` to `.env`
- [ ] Open `.env` in a text editor
- [ ] Replace `your_calendly_api_key_here` with your actual API key
- [ ] Save the file

**Quick way:**
```bash
cp .env.example .env
# Then edit .env with your API key
```

## 📦 Phase 5: Install Dependencies (2 minutes)

Run this command:
```bash
pip install -r requirements.txt
```

Or try:
```bash
pip3 install -r requirements.txt
```

Or use the automated script:
```bash
./setup.sh
```

Wait for installation to complete.

## 🧪 Phase 6: Test It Works (1 minute)

- [ ] Run: `python server.py` or `python3 server.py`
- [ ] Look for: "Calendly MCP Server starting..."
- [ ] If you see it: Success! Press Ctrl+C to stop
- [ ] If you see errors: Check the Troubleshooting section below

## 🔌 Phase 7: Connect to Claude Desktop (5 minutes)

- [ ] Find your Claude Desktop config file:
  - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- [ ] Open it in a text editor
- [ ] Add the MCP server configuration (see README.md)
- [ ] Save the file
- [ ] Restart Claude Desktop
- [ ] Verify it's connected (you should see new tools available)

## 🎉 Phase 8: Test with Claude (2 minutes)

Try these commands in Claude:

- [ ] "List my active Calendly event types"
- [ ] "Show me my availability schedule"
- [ ] "Get my user information"

If these work, you're all set! 🎊

## 🐙 Phase 9: (Optional) Publish to GitHub (10 minutes)

- [ ] Read GITHUB_SETUP.md
- [ ] Create a GitHub account (if needed)
- [ ] Install Git (if needed)
- [ ] Create a new repository
- [ ] Push your code
- [ ] Share the repository URL!

## 📚 Bonus: Learn More (Ongoing)

- [ ] Read API_REFERENCE.md to see all available commands
- [ ] Experiment with updating event types
- [ ] Try creating custom availability schedules
- [ ] Explore webhook integrations
- [ ] Contribute improvements back to the project

---

## 🆘 Troubleshooting

### Python not found
- Reinstall Python with "Add to PATH" checked
- Restart your Terminal/Command Prompt
- Try `python3` instead of `python`

### pip not found
- Python installation should include pip
- Try `pip3` instead of `pip`
- Or: `python -m pip install -r requirements.txt`

### Module not found errors
- Make sure you ran the install command
- Check you're in the right directory
- Try: `pip install --upgrade -r requirements.txt`

### Authentication failed
- Double-check your API key in `.env`
- Make sure there are no extra spaces
- Verify the key hasn't expired
- Try generating a new key

### Server won't start
- Check that port isn't already in use
- Look at error messages carefully
- Make sure `.env` file exists
- Verify Python version is 3.8+

### Claude doesn't see the server
- Restart Claude Desktop completely
- Check config file syntax (valid JSON)
- Verify the path in config is correct
- Look at Claude Desktop console for errors

---

## ⏱️ Total Time Estimate

- **Minimum:** 15 minutes (if everything works perfectly)
- **Typical:** 25 minutes (with some troubleshooting)
- **Maximum:** 45 minutes (if installing Python + Git)

## 🎯 You're Done When...

✅ The server starts without errors
✅ Claude can see your Calendly data
✅ You can update an event type
✅ You're excited to share it!

## 📞 Need Help?

- Check QUICKSTART.md for detailed instructions
- Review API_REFERENCE.md for usage examples
- Open an issue on GitHub
- Ask the Claude community

---

**Remember:** It's okay if something doesn't work the first time. That's part of learning! The troubleshooting section and documentation are here to help. 💪

**Good luck! You've got this! 🚀**
