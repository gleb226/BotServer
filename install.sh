#!/bin/bash

echo "==========================================="
echo "   BotServer Installation Wizard"
echo "==========================================="

if ! command -v python3 &> /dev/null
then
    echo "Error: python3 could not be found. Please install Python 3."
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "--- Configuration ---"
read -p "Enter your Telegram Bot Token: " bot_token

echo "DATABASE_TYPE=sqlite" > .env
echo "BOT_TOKEN=$bot_token" >> .env

echo ""
echo "==========================================="
echo "   Installation Complete!"
echo "==========================================="
echo "To start the bot, run: source .venv/bin/activate && python3 bot.py"
echo "==========================================="
