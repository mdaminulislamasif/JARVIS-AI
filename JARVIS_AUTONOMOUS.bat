@echo off
title JARVIS AUTONOMOUS SYSTEM
color 0A

cls
echo ========================================
echo    JARVIS AUTONOMOUS SYSTEM
echo    Complete AI - Does Everything
echo ========================================
echo.
echo Features:
echo  * Voice Recognition (NO API KEY)
echo  * Text-to-Speech (NO API KEY)
echo  * Automatic Search
echo  * Automatic Website Usage
echo  * Understands User Needs
echo  * Self-Learning
echo  * Self-Updating
echo  * Fully Autonomous Mode
echo.
echo ========================================
echo.

echo Installing required packages...
pip install SpeechRecognition pyttsx3 pyaudio requests beautifulsoup4 --quiet

if errorlevel 1 (
    echo.
    echo Note: If pyaudio fails, trying alternative...
    pip install pipwin --quiet
    pipwin install pyaudio --quiet
)

echo.
echo Starting JARVIS Autonomous System...
echo.
echo ========================================
echo  JARVIS will now listen and respond
echo  Speak naturally - no commands needed!
echo  Say "autonomous mode" for full auto
echo  Say "exit" to quit
echo ========================================
echo.

python jarvis_autonomous.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: JARVIS failed to start
    echo ========================================
    echo.
    echo Troubleshooting:
    echo 1. Check microphone connection
    echo 2. Check microphone permissions
    echo 3. Try manual installation:
    echo    pip install SpeechRecognition
    echo    pip install pyttsx3
    echo    pip install pyaudio
    echo    pip install requests
    echo    pip install beautifulsoup4
    echo.
)

pause
