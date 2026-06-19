@echo off
title JARVIS - NO API KEYS NEEDED
color 0A

cls
echo ========================================
echo    JARVIS - NO API KEYS NEEDED
echo    FIX FOR API QUOTA PROBLEMS
echo ========================================
echo.
echo This version works WITHOUT any API keys!
echo.
echo  * NO Gemini API needed
echo  * NO Groq API needed
echo  * NO HuggingFace API needed
echo  * NO Cohere API needed
echo  * NO Ollama needed
echo.
echo  Uses FREE services only:
echo  * Google Speech Recognition (FREE)
echo  * Local Text-to-Speech (FREE)
echo  * Local Database (FREE)
echo  * Direct Web Scraping (FREE)
echo.
echo  NO QUOTAS, NO LIMITS, NO PROBLEMS!
echo.
echo ========================================
echo.

echo Installing packages...
pip install SpeechRecognition pyttsx3 pyaudio requests beautifulsoup4 --quiet

echo.
echo Starting JARVIS (NO API KEYS)...
echo.

python jarvis_no_api_needed.py

pause
