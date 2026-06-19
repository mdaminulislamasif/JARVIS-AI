@echo off
title JARVIS BROWSER CONTROLLER
color 0A

echo ========================================
echo    JARVIS BROWSER CONTROLLER
echo ========================================
echo.
echo Starting browser control system...
echo.

python jarvis_browser_controller.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start browser controller
    echo Make sure Python is installed and required packages are available
    echo.
    echo Installing required packages...
    pip install requests beautifulsoup4
    echo.
    echo Retrying...
    python jarvis_browser_controller.py
)

pause
