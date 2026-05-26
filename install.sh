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

echo ""
read -p "Use MongoDB instead of SQLite? (y/N): " use_mongo

db_type="sqlite"
mongo_url=""

if [[ "$use_mongo" =~ ^[Yy]$ ]]; then
    db_type="mongodb"
    read -p "Enter MongoDB URL [mongodb://localhost:27017]: " mongo_url
    if [ -z "$mongo_url" ]; then
        mongo_url="mongodb://localhost:27017"
    fi
fi

echo "DATABASE_TYPE=$db_type" > .env
echo "BOT_TOKEN=$bot_token" >> .env
if [ "$db_type" == "mongodb" ]; then
    echo "MONGO_URL=$mongo_url" >> .env
fi

echo ""
echo "==========================================="
echo "   Installation Complete!"
echo "==========================================="
echo "To start the bot, run: source .venv/bin/activate && python3 bot.py"
echo "==========================================="
