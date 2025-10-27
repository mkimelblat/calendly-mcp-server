# Publishing to GitHub - Step by Step

This guide will walk you through publishing your Calendly MCP Server to GitHub so you can share it with others.

## 📋 Prerequisites

1. A GitHub account (free) - Sign up at https://github.com
2. Git installed on your computer
3. The calendly-mcp-server folder downloaded

## 🚀 Step-by-Step Instructions

### Step 1: Install Git (if needed)

#### Mac:
```bash
# Check if Git is already installed
git --version

# If not installed, install via Homebrew:
brew install git

# Or download from: https://git-scm.com/download/mac
```

#### Windows:
1. Download Git from: https://git-scm.com/download/win
2. Run the installer (keep all default settings)
3. Restart your computer

### Step 2: Configure Git (first time only)

Open Terminal (Mac) or Git Bash (Windows) and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Replace with your actual name and the email you used for GitHub.

### Step 3: Create a New Repository on GitHub

1. Go to https://github.com
2. Click the "+" icon in the top right
3. Click "New repository"
4. Fill in:
   - **Repository name:** `calendly-mcp-server`
   - **Description:** "Complete MCP server for the Calendly API with full CRUD support"
   - **Public** (so others can use it)
   - **Do NOT check** "Initialize with README" (we already have one)
5. Click "Create repository"
6. **Keep this page open** - you'll need it in Step 5

### Step 4: Prepare Your Local Folder

Open Terminal/Command Prompt and navigate to the folder:

```bash
cd /path/to/calendly-mcp-server
```

**Important:** Make sure your `.env` file is NOT in this folder (it should be in `.gitignore` already). Never commit API keys!

### Step 5: Initialize Git and Push to GitHub

Run these commands one by one:

```bash
# Initialize Git in this folder
git init

# Add all files to Git
git add .

# Create your first commit
git commit -m "Initial commit: Complete Calendly MCP Server"

# Set the default branch to 'main'
git branch -M main

# Connect to your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/calendly-mcp-server.git

# Push your code to GitHub
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username!

### Step 6: Verify It Worked

1. Go back to your GitHub repository page
2. Refresh the page
3. You should see all your files!

## 🎉 Success!

Your Calendly MCP Server is now on GitHub! 

### Share Your Repository

Your repository URL is:
```
https://github.com/YOUR_USERNAME/calendly-mcp-server
```

Share this with anyone who wants to use it!

## 📝 Making Updates

When you want to update your GitHub repository:

```bash
# Make your changes to files
# Then:

git add .
git commit -m "Description of what you changed"
git push
```

## 🌟 Optional: Make It Look Great

### Add Topics
1. Go to your repository on GitHub
2. Click the gear icon next to "About"
3. Add topics: `calendly`, `mcp`, `api`, `claude`, `anthropic`, `scheduling`

### Add a GitHub Actions Badge (Optional)
Create a badge to show your project is active!

### Star and Share
- Click the "Star" button on your own repo
- Share the link on social media or forums

## 🔒 Security Reminder

**Never commit these files:**
- `.env` (contains your API key)
- Any file with passwords or secrets

These are already in `.gitignore`, but always double-check!

## 📚 Next Steps

1. **Write a blog post** about building it
2. **Share on Twitter/X** with hashtags #Calendly #MCP #Claude
3. **Submit to MCP directory** (if Anthropic has one)
4. **Help others** who have questions about using it

## 🆘 Troubleshooting

### "Authentication failed" when pushing
You might need to set up a Personal Access Token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select `repo` scope
4. Copy the token
5. Use it as your password when pushing

### "Repository not found"
- Check that you replaced YOUR_USERNAME with your actual username
- Make sure the repository exists on GitHub

### Files not showing up
- Make sure you ran `git add .`
- Check that files aren't in `.gitignore`
- Try `git status` to see what's tracked

## 📞 Need Help?

- GitHub Docs: https://docs.github.com
- Git Tutorial: https://www.atlassian.com/git/tutorials
- Open an issue if you get stuck!

---

**Congratulations on publishing your first open-source project! 🎊**
