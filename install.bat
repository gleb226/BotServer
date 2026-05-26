@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo           BotServer Installation Wizard
echo ===================================================

:: Check for python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install it.
    pause
    exit /b 1
)

echo [1/4] Creating environment...
python -m venv .venv
call .venv\Scripts\activate

echo [2/4] Installing core components...
pip install -r requirements.txt --quiet

echo.
echo --- CONFIGURATION ---
set /p bot_token="[INPUT] Enter Telegram Bot Token: "
echo VERSION=personal > .env
echo DATABASE_TYPE=sqlite >> .env
echo BOT_TOKEN=!bot_token! >> .env

echo.
echo [3/4] Bundling application (This may take a minute)...
echo.
:: Run PyInstaller and output to the current folder
pyinstaller --onefile --name BotLauncher --noconsole --distpath . bot.py >nul 2>&1

echo [4/4] Finalizing standalone mode...
:: Create necessary folders if they don't exist
if not exist "files" mkdir "files"
if not exist "app\databases" mkdir "app\databases"

echo.
echo ===================================================
echo           INSTALLATION SUCCESSFUL!
echo ===================================================
echo.
echo  YOUR BOT IS READY: BotLauncher.exe
echo  YOUR FILES:        /files
echo  YOUR SETTINGS:     .env
echo.
echo ===================================================
echo.

set /p launch="[INPUT] Launch the bot now? (y/n): "
if /i "!launch!"=="y" (
    start BotLauncher.exe
)

:: Self-cleanup script: deletes everything except the essentials
echo @echo off > cleanup.bat
echo timeout /t 2 /nobreak ^>nul >> cleanup.bat
echo del bot.py >> cleanup.bat
echo del requirements.txt >> cleanup.bat
echo del install.sh >> cleanup.bat
echo del BotLauncher.spec >> cleanup.bat
echo rd /s /q .venv >> cleanup.bat
echo rd /s /q build >> cleanup.bat
echo rd /s /q app\common >> cleanup.bat
echo rd /s /q app\handlers >> cleanup.bat
echo rd /s /q app\keyboards >> cleanup.bat
echo rd /s /q app\utils >> cleanup.bat
echo :: Note: We keep app\databases for the bot.db >> cleanup.bat
echo del cleanup.bat >> cleanup.bat
echo exit >> cleanup.bat

:: Launch cleanup in background and close this window
start /b cleanup.bat
exit
