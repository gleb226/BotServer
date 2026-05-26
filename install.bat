@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo           BotServer Installation Wizard
echo ===================================================

:: 1. Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install it.
    pause
    exit /b 1
)

:: 2. Setup Environment
echo [1/4] Creating environment...
python -m venv .venv >nul 2>&1
call .venv\Scripts\activate

:: 3. Install Requirements
echo [2/4] Installing core components...
pip install -r requirements.txt --quiet

:: 4. Configuration
echo.
echo --- CONFIGURATION ---
set /p bot_token="[INPUT] Enter Telegram Bot Token: "
(
echo VERSION=personal
echo DATABASE_TYPE=sqlite
echo BOT_TOKEN=!bot_token!
) > .env

:: 5. Build Executable
echo.
echo [3/4] Bundling application...
echo This may take a minute. Please wait...
pyinstaller --onefile --name BotLauncher --noconsole --distpath . bot.py >nul 2>&1

:: 6. Create Storage
echo [4/4] Finalizing setup...
if not exist "files" mkdir "files"

echo.
echo ===================================================
echo           INSTALLATION SUCCESSFUL!
echo ===================================================
echo.
echo  FOLDER:  %CD%
echo  FILES:   BotLauncher.exe, .env, bot.db, /files
echo.
echo ===================================================
echo.

:: 7. Self-Cleanup logic (moved to a safe external script)
:: We create a script that waits for THIS batch to exit, then cleans up.
(
echo @echo off
echo timeout /t 2 /nobreak ^>nul
echo del bot.py
echo del requirements.txt
echo del install.sh
echo del BotLauncher.spec
echo rd /s /q .venv
echo rd /s /q build
echo rd /s /q app
echo del "%%~f0"
) > finalize.bat

set /p launch="[INPUT] Launch the bot now? (y/n): "
if /i "!launch!"=="y" (
    start BotLauncher.exe
)

:: Launch the external finalizer and exit this script immediately
start /b finalize.bat
exit
