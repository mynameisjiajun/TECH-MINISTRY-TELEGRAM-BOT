@echo off
REM Church Tech Ministry Telegram Bot Startup Script (Windows)

echo ========================================
echo 🙏 Church Tech Ministry Bot Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if requirements are installed
if not exist "venv\installed.flag" (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\installed.flag
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already installed
)

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found!
    echo Please create a .env file with your configuration.
    echo You can copy .env.example and fill in your details.
    pause
    exit /b 1
)

echo ✅ Configuration file found

REM Check if credentials.json exists
if not exist "credentials.json" (
    echo ⚠️  WARNING: credentials.json not found!
    echo Make sure you have your Google Service Account credentials.
    echo.
    set /p continue="Do you want to continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

echo.
echo ========================================
echo 🚀 Starting bot...
echo ========================================
echo.
echo Press Ctrl+C to stop the bot
echo.

REM Run the bot
python main.py

pause

