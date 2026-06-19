@echo off
title JARVIS CONVERSATIONAL AI
color 0B

cls
echo ========================================
echo    JARVIS CONVERSATIONAL AI
echo    Talk Together Like Friends
echo ========================================
echo.
echo Features:
echo  * Natural conversations
echo  * Understands context
echo  * Remembers your name
echo  * Asks follow-up questions
echo  * Works together with you
echo  * Saves conversation history
echo.
echo ========================================
echo.

echo Installing required packages...
pip install SpeechRecognition pyttsx3 pyaudio requests beautifulsoup4 --quiet

echo.
echo Starting JARVIS Conversational AI...
echo.
echo ========================================
echo  JARVIS will now have a conversation
echo  Talk naturally - JARVIS will respond!
echo  Say "exit" to end conversation
echo ========================================
echo.

python jarvis_conversational.py

pause
