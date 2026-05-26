#!/bin/bash
echo "Installing dependencies..."
if ! command -v python3 &> /dev/null
then
    echo "python3 could not be found. Please install Python 3."
    exit
fi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
if [ ! -f .env ]; then
    echo "Creating .env template..."
    echo "BOT_TOKEN=your_token_here" > .env
    echo "MONGO_URL=mongodb://localhost:27017" >> .env
fi
echo "Installation complete. Please configure your .env file and run 'python3 bot.py'."
