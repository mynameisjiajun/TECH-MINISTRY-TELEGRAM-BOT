#!/bin/bash

# Church Tech Ministry Telegram Bot Startup Script

echo "========================================"
echo "🙏 Church Tech Ministry Bot Launcher"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

echo "✅ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/installed.flag" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/installed.flag
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create a .env file with your configuration."
    echo "You can copy .env.example and fill in your details."
    exit 1
fi

echo "✅ Configuration file found"

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo "⚠️  WARNING: credentials.json not found!"
    echo "Make sure you have your Google Service Account credentials."
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "========================================"
echo "🚀 Starting bot..."
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the bot"
echo ""

# Run the bot
python3 main.py

