@echo off
echo Installing dependencies...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python could not be found. Please install Python.
    pause
    exit /b
)
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
if not exist .env (
    echo Creating .env template...
    echo BOT_TOKEN=your_token_here > .env
    echo MONGO_URL=mongodb://localhost:27017 >> .env
)
echo Installation complete. Please configure your .env file and run 'python bot.py'.
pause
