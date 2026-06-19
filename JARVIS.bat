@echo off
title JARVIS
color 0A
cls
echo.
echo  ========================================================================
echo                                JARVIS
echo  ========================================================================
echo.
echo                         Initializing AI System...
echo.

REM Silent installation
pip install SpeechRecognition pyttsx3 pyaudio requests beautifulsoup4 --quiet >nul 2>&1

echo                         JARVIS is now active!
echo.
echo                         Speak to begin...
echo.
echo  ========================================================================
echo.

python jarvis_conversational.py

pause
