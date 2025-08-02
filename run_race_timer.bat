@echo off
echo Starting Race Timer Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show PyQt6 >nul 2>&1
if errorlevel 1 (
    echo PyQt6 not found, installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    pip show pygame >nul 2>&1
    if errorlevel 1 (
        echo pygame not found, installing dependencies...
        pip install -r requirements.txt
        if errorlevel 1 (
            echo Error: Failed to install dependencies
            pause
            exit /b 1
        )
    )
)

REM Create recordings directory if it doesn't exist
if not exist "recordings" mkdir recordings

REM Create audio directory if it doesn't exist
if not exist "audio" mkdir audio

REM Start the application
echo Starting Race Timer...
python main.py

REM If the application exits with an error, pause to show the error
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    pause
) 