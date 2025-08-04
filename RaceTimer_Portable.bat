@echo off
title Race Timer - Portable
echo Starting Race Timer...
echo.
echo If you see any errors below, the executable may need additional files.
echo The executable should open in a new window.
echo.
cd /d "%~dp0"
start "" "dist\RaceTimer.exe"
echo.
echo Race Timer started! You can close this window.
echo If the application doesn't start, check:
echo - Windows Defender/Antivirus settings
echo - Required Visual C++ redistributables are installed
echo.
pause