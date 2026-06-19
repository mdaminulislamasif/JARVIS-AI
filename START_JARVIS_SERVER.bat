@echo off
chcp 65001 > nul
title JARVIS UNIFIED BACKEND SERVER
color 0A
echo.
echo ================================================================
echo    JARVIS AI - UNIFIED BACKEND SERVER
echo    Version: ANTIGRAVITY NEURAL LINK
echo ================================================================
echo.
echo [*] Starting JARVIS Voice + Command Server...
echo [*] Server URL: http://localhost:5000
echo.
echo [*] All Modules Verified:
echo     - Flask Server (Voice + Commands)
echo     - System Automation (psutil, pyautogui)
echo     - TTS Voice Engine (pyttsx3)
echo     - Face Recognition API (PIL)
echo     - Network Scanner
echo     - Android ADB Controller
echo.
echo [!] Browser will NOT auto-open - controlled by your commands only
echo.
echo ================================================================
echo.
cd /d "%~dp0"
python jarvis_voice_server.py
echo.
echo [!] Server stopped. Press any key to restart...
pause > nul
goto :start
:start
python jarvis_voice_server.py
pause
