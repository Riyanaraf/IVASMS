#!/bin/bash

# IVASMS Bot - Universal Deployment Script
# Works on Pterodactyl Panel, VPS, Linux servers, and any Python environment

set -e

echo "========================================"
echo "IVASMS Telegram Bot - Deployment Script"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Check for required environment variables
echo "Checking environment variables..."
MISSING_VARS=0

if [ -z "$IVASMS_EMAIL" ]; then
    echo "⚠ IVASMS_EMAIL not set"
    MISSING_VARS=1
else
    echo "✓ IVASMS_EMAIL is set"
fi

if [ -z "$IVASMS_PASSWORD" ]; then
    echo "⚠ IVASMS_PASSWORD not set"
    MISSING_VARS=1
else
    echo "✓ IVASMS_PASSWORD is set"
fi

if [ -z "$BOT_TOKEN" ]; then
    echo "⚠ BOT_TOKEN not set"
    MISSING_VARS=1
else
    echo "✓ BOT_TOKEN is set"
fi

if [ -z "$CHAT_ID" ]; then
    echo "⚠ CHAT_ID not set"
    MISSING_VARS=1
else
    echo "✓ CHAT_ID is set"
fi

echo ""

if [ $MISSING_VARS -eq 1 ]; then
    echo "ERROR: Missing required environment variables!"
    echo "Please set these variables in your environment or .env file:"
    echo "  - IVASMS_EMAIL"
    echo "  - IVASMS_PASSWORD"
    echo "  - BOT_TOKEN"
    echo "  - CHAT_ID"
    exit 1
fi

echo "✓ All environment variables are set"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""
echo "========================================"
echo "Starting IVASMS Bot..."
echo "========================================"
echo ""

# Run the bot
python3 bot.py
