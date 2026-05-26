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
pip install -r requirements.txt --quiet

:: 4. Get Token
echo.
echo --- CONFIGURATION ---
set /p bot_token="[INPUT] Enter Telegram Bot Token: "
(
echo VERSION=personal
echo DATABASE_TYPE=sqlite
echo BOT_TOKEN=!bot_token!
) > .env

:: 5. Compile to EXE
echo.
echo [3/4] Building standalone executable...
echo This will take about 60 seconds. Do not close this window.
:: We use --console for the first build so user can see errors if any, but --noconsole is requested for final.
:: I will use --noconsole as requested but ensure paths are rock solid.
pyinstaller --onefile --name BotLauncher --noconsole --distpath . bot.py >nul 2>&1

:: 6. Verify and Cleanup Preparation
echo [4/4] Finalizing files...
if not exist "files" mkdir "files"

echo.
echo ===================================================
echo           INSTALLATION SUCCESSFUL!
echo ===================================================
echo.
echo  The following items are now ready in this folder:
echo  1. BotLauncher.exe (Double-click to start)
echo  2. .env            (Contains your token)
echo  3. bot.db          (Your database)
echo  4. /files          (Folder for your data)
echo.
echo  All other source files will be removed now.
echo ===================================================
echo.

set /p launch="[INPUT] Launch the bot now? (y/n): "

:: 7. Detached Cleanup (PowerShell handles this better than CMD batch)
:: This command waits 3 seconds, then deletes everything EXCEPT the 4 essential items.
set "cleanup_cmd=Start-Sleep -s 3; Get-ChildItem -Exclude 'BotLauncher.exe','.env','bot.db','files' | Remove-Item -Recurse -Force; Write-Host 'Cleanup complete!'"

if /i "!launch!"=="y" (
    start BotLauncher.exe
)

:: Start the detached background cleanup and close THIS window immediately
start /b powershell.exe -NoProfile -Command "!cleanup_cmd!"
exit
