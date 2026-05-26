@echo off
setlocal enabledelayedexpansion

echo ===========================================
echo    BotServer Installation Wizard
echo ===========================================

:: Check for python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python could not be found. Please install Python.
    pause
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv .venv
call .venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Interactive Configuration
echo.
echo --- Configuration ---
set /p bot_token="Enter your Telegram Bot Token: "

echo Choose Database Type:
echo 1) SQLite (Default, Simple)
echo 2) MongoDB (Advanced)
set /p db_choice="Selection [1-2]: "

set db_type=sqlite
set mongo_url=

if "!db_choice!"=="2" (
    set db_type=mongodb
    set /p mongo_url="Enter MongoDB URL [mongodb://localhost:27017]: "
    if "!mongo_url!"=="" set mongo_url=mongodb://localhost:27017
)

:: Create .env file
(
echo DATABASE_TYPE=!db_type!
echo BOT_TOKEN=!bot_token!
if "!db_type!"=="mongodb" echo MONGO_URL=!mongo_url!
) > .env

echo.
echo ===========================================
echo    Installation Complete!
echo ===========================================
echo To start the bot, run: call .venv\Scripts\activate ^&^& python bot.py
echo ===========================================
pause
