#!/bin/bash

# Calendly MCP Server Setup Script
# This script helps you set up the server quickly

echo "🗓️  Calendly MCP Server Setup"
echo "=============================="
echo ""

# Check if Python is installed
echo "Checking for Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Found $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
    PYTHON_VERSION=$(python --version)
    echo "✅ Found $PYTHON_VERSION"
else
    echo "❌ Python not found. Please install Python 3.8 or higher."
    echo "   Download from: https://python.org/downloads"
    exit 1
fi

echo ""

# Check if pip is installed
echo "Checking for pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD=pip3
    echo "✅ Found pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD=pip
    echo "✅ Found pip"
else
    echo "❌ pip not found. Please install pip."
    exit 1
fi

echo ""

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Check for .env file
if [ -f ".env" ]; then
    echo "✅ Found .env file"
else
    echo "⚠️  No .env file found"
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "📝 IMPORTANT: Edit .env and add your Calendly API key!"
    echo "   Get your API key from: https://calendly.com/integrations/api_webhooks"
    echo ""
fi

echo ""
echo "=============================="
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Calendly API key"
echo "2. Test the server: $PYTHON_CMD server.py"
echo "3. Add to Claude Desktop config (see README.md)"
echo ""
echo "For detailed instructions, see QUICKSTART.md"
echo ""
