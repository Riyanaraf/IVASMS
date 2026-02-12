@echo off
REM IVASMS Bot - Windows Deployment Script

echo.
echo ========================================
echo IVASMS Telegram Bot - Deployment Script
echo ========================================
echo.

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo + Found Python %PYTHON_VERSION%
echo.

REM Check for required environment variables
echo Checking environment variables...
setlocal enabledelayedexpansion

set MISSING_VARS=0

if "!IVASMS_EMAIL!"=="" (
    echo - IVASMS_EMAIL not set
    set MISSING_VARS=1
) else (
    echo + IVASMS_EMAIL is set
)

if "!IVASMS_PASSWORD!"=="" (
    echo - IVASMS_PASSWORD not set
    set MISSING_VARS=1
) else (
    echo + IVASMS_PASSWORD is set
)

if "!BOT_TOKEN!"=="" (
    echo - BOT_TOKEN not set
    set MISSING_VARS=1
) else (
    echo + BOT_TOKEN is set
)

if "!CHAT_ID!"=="" (
    echo - CHAT_ID not set
    set MISSING_VARS=1
) else (
    echo + CHAT_ID is set
)

echo.

if %MISSING_VARS% equ 1 (
    echo ERROR: Missing required environment variables!
    echo Please set these variables in your system environment or create a .env file:
    echo   - IVASMS_EMAIL
    echo   - IVASMS_PASSWORD
    echo   - BOT_TOKEN
    echo   - CHAT_ID
    pause
    exit /b 1
)

echo + All environment variables are set
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
    echo + Virtual environment created
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/updating dependencies...
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo + Dependencies installed
echo.
echo ========================================
echo Starting IVASMS Bot...
echo ========================================
echo.

REM Run the bot
python bot.py
pause
