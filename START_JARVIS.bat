@echo off
chcp 65001 >nul
echo ================================================================
echo STARTING JARVIS PANEL
echo ================================================================
echo.

python START_JARVIS.py

if errorlevel 1 (
    echo.
    echo ================================================================
    echo ERROR: JARVIS failed to start
    echo ================================================================
    echo.
    pause
)
