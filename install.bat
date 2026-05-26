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

:: 3. Install Dependencies (Using --no-cache-dir to avoid warnings)
echo [2/4] Installing dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet --no-cache-dir

:: 4. Get Token and Version
echo.
echo --- CONFIGURATION ---
set /p bot_token="[INPUT] Enter Telegram Bot Token: "
echo.
echo Choose Version:
echo 1) Personal (Standalone, Local Storage)
echo 2) Commercial (Scalable, Payments, User Isolation)
set /p v_choice="Selection [1-2]: "

set version=personal
set payment_token=

if "!v_choice!"=="2" (
    set version=commercial
    set /p payment_token="[INPUT] Enter Payment Provider Token (LikPay): "
)

(
echo VERSION=!version!
echo DATABASE_TYPE=sqlite
echo BOT_TOKEN=!bot_token!
if not "!payment_token!"=="" echo PAYMENT_TOKEN=!payment_token!
) > .env

:: 5. Compile to EXE
echo.
echo [3/4] Building standalone executable...
echo This will take about 60 seconds. Please wait...
pyinstaller --onefile --name BotLauncher --noconsole --distpath . bot.py >nul 2>&1

:: 6. Verify and Cleanup Preparation
echo [4/4] Finalizing setup...
if not exist "files" mkdir "files"

echo.
echo ===================================================
echo           INSTALLATION SUCCESSFUL!
echo ===================================================
echo.
echo  The following items are ready:
echo  1. BotLauncher.exe (Double-click to start)
echo  2. .env            (Your configuration)
echo  3. bot.db          (Database)
echo  4. /files          (Data storage)
echo.
echo  Cleaning up source files...
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
