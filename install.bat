@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo           BotServer Installation Wizard
echo ===================================================

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install it.
    pause
    exit /b 1
)

echo [1/5] Creating environment...
python -m venv .venv
call .venv\Scripts\activate

echo [2/5] Installing core components...
pip install -r requirements.txt --quiet

echo.
echo --- CONFIGURATION ---
set /p bot_token="[INPUT] Enter Telegram Bot Token: "
echo DATABASE_TYPE=sqlite > .env
echo BOT_TOKEN=!bot_token! >> .env
echo VERSION=personal >> .env

echo [3/5] Bundling application (This may take a minute)...
echo.
:: Progress bar simulation
echo [##########          ] 50%%
pyinstaller --onefile --name BotLauncher --noconsole --distpath . bot.py >nul 2>&1
echo [####################] 100%%
echo.

echo [4/5] Finalizing standalone mode...
:: Create 'files' directory
if not exist "files" mkdir "files"

echo [5/5] Cleaning up source files...
:: We move the EXE first to protect it
move BotLauncher.exe ..\ >nul 2>&1
cd ..
:: Remove the project source directory completely
:: WARNING: This removes the directory the script is in!
:: We use a temporary script to do the dirty work
echo @echo off > cleanup.bat
echo timeout /t 2 /nobreak ^>nul >> cleanup.bat
echo rd /s /q BotServer >> cleanup.bat
echo del cleanup.bat >> cleanup.bat
start /b cleanup.bat

echo.
echo ===================================================
echo           INSTALLATION SUCCESSFUL!
echo ===================================================
echo.
echo  YOUR BOT IS READY: BotLauncher.exe
echo  YOUR FILES:        /files
echo.
echo  You can now move BotLauncher.exe anywhere!
echo ===================================================
echo.

set /p launch="[INPUT] Launch the bot now? (y/n): "
if /i "!launch!"=="y" (
    start BotLauncher.exe
)
exit
