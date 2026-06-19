@echo off
title JARVIS VOICE BROWSER
color 0B

echo ========================================
echo    JARVIS VOICE BROWSER
echo    Control Browser with Voice
echo ========================================
echo.
echo Installing required packages...
echo.

pip install SpeechRecognition pyttsx3 pyaudio --quiet

if errorlevel 1 (
    echo.
    echo Note: If pyaudio fails, trying alternative installation...
    pip install pipwin --quiet
    pipwin install pyaudio --quiet
)

echo.
echo Starting voice browser...
echo.

python jarvis_voice_browser.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Voice browser failed to start
    echo ========================================
    echo.
    echo Troubleshooting:
    echo 1. Make sure microphone is connected
    echo 2. Check microphone permissions
    echo 3. Try manual installation:
    echo    pip install SpeechRecognition
    echo    pip install pyttsx3
    echo    pip install pyaudio
    echo.
)

pause
