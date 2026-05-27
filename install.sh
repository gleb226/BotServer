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
echo "Creating standalone executable..."
pyinstaller --onefile --name BotLauncher bot.py

echo ""
echo "==========================================="
echo "   Installation Complete!"
echo "==========================================="
echo "Executable created in: ./dist/BotLauncher"
echo "==========================================="
echo ""

read -p "Would you like to start the bot now? (y/N): " start_bot
if [[ "$start_bot" =~ ^[Yy]$ ]]; then
    python3 bot.py
fi