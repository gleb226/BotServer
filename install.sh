#!/bin/bash

echo "==========================================="
echo "   BotServer Installation Wizard"
echo "==========================================="

# Check for python
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 could not be found. Please install Python 3."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Interactive Configuration
echo ""
echo "--- Configuration ---"
read -p "Enter your Telegram Bot Token: " bot_token

echo "Choose Database Type:"
echo "1) SQLite (Default, Simple)"
echo "2) MongoDB (Advanced)"
read -p "Selection [1-2]: " db_choice

db_type="sqlite"
mongo_url=""

if [ "$db_choice" == "2" ]; then
    db_type="mongodb"
    read -p "Enter MongoDB URL [mongodb://localhost:27017]: " mongo_url
    if [ -z "$mongo_url" ]; then
        mongo_url="mongodb://localhost:27017"
    fi
fi

# Create .env file
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
