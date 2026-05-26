@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo           BotServer Installation Wizard
echo ===================================================

:: 1. Verify Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python.
    pause
    exit /b 1
)

:: 2. Setup Environment
echo [1/4] Preparing environment...
if exist ".venv" rd /s /q .venv
python -m venv .venv >nul 2>&1
call .venv\Scripts\activate

:: 3. Install Dependencies
echo [2/4] Installing dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet --no-cache-dir

:: 4. Get Token
echo.
echo --- CONFIGURATION ---
echo To get your BOT_TOKEN, message @BotFather on Telegram.
echo.
set /p bot_token="[INPUT] Enter Telegram Bot Token: "

(
echo VERSION=personal
echo DATABASE_TYPE=sqlite
echo BOT_TOKEN=!bot_token!
) > .env

:: 5. Compile to EXE
echo.
echo [3/4] Building standalone executable...
echo This will take about 60 seconds. Please wait...
:: Added hidden imports to fix common PyInstaller issues with aiogram and other libs
pyinstaller --onefile --name BotLauncher --noconsole --distpath . ^
--hidden-import aiogram ^
--hidden-import aiogram.dispatcher ^
--hidden-import aiogram.filters ^
--hidden-import aiogram.fsm.storage.memory ^
--hidden-import motor ^
--hidden-import pymongo ^
--hidden-import tabulate ^
bot.py >nul 2>&1

:: 6. Finalizing
echo [4/4] Finalizing setup...
if not exist "files" mkdir "files"

echo.
echo ===================================================
echo           INSTALLATION SUCCESSFUL!
echo ===================================================
echo.
echo  Ready files:
echo  1. BotLauncher.exe (The App)
echo  2. .env            (Your Settings)
echo  3. bot.db          (Your Data Index)
echo  4. /files          (Storage Folder)
echo.
echo  All source code and temporary files will be removed.
echo ===================================================
echo.

set /p launch="[INPUT] Launch the bot now? (y/n): "

:: 7. Detached Cleanup (PowerShell)
set "cleanup_cmd=Start-Sleep -s 3; Get-ChildItem -Exclude 'BotLauncher.exe','.env','bot.db','files' | Remove-Item -Recurse -Force"

if /i "!launch!"=="y" (
    start BotLauncher.exe
)

start /b powershell.exe -NoProfile -Command "!cleanup_cmd!"
exit
