@echo off
setlocal enabledelayedexpansion

echo ===========================================
echo    BotServer Installation Wizard
echo ===========================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python could not be found. Please install Python.
    pause
    exit /b 1
)

echo Creating virtual environment...
python -m venv .venv
call .venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo --- Configuration ---
set /p bot_token="Enter your Telegram Bot Token: "

(
echo DATABASE_TYPE=sqlite
echo BOT_TOKEN=!bot_token!
) > .env

echo.
echo Creating standalone executable...
pyinstaller --onefile --name BotLauncher bot.py

echo.
echo ===========================================
echo    Installation Complete!
echo ===========================================
echo Executable created in: .\dist\BotLauncher.exe
echo ===========================================
echo.

set /p start_bot="Would you like to start the bot now? (y/N): "
if /i "!start_bot!"=="y" (
    python bot.py
) else (
    echo.
    echo To start the bot later, simply run BotLauncher.exe from the dist folder.
    pause
)
