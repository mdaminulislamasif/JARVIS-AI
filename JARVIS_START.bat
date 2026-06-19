@echo off
title JARVIS
color 0A
cls
echo.
echo  ========================================================================
echo                                JARVIS
echo                          AI Assistant Active
echo  ========================================================================
echo.

pip install SpeechRecognition pyttsx3 pyaudio requests beautifulsoup4 --quiet >nul 2>&1

python JARVIS_COMPLETE.py

pause
