@echo off
echo ================================================================
echo    JARVIS Voice Test
echo ================================================================
echo.
echo Testing JARVIS voice with different messages...
echo.

echo 1. Greeting...
python jarvis_voice_engine.py "Good day sir. All systems are operational."
timeout /t 2 >nul

echo.
echo 2. Premium activation...
python jarvis_voice_engine.py "Premium activated successfully sir."
timeout /t 2 >nul

echo.
echo 3. Dark mode...
python jarvis_voice_engine.py "Dark mode activated sir."
timeout /t 2 >nul

echo.
echo 4. API access...
python jarvis_voice_engine.py "API access granted sir."
timeout /t 2 >nul

echo.
echo ================================================================
echo    Test Complete!
echo ================================================================
echo.
echo If you heard JARVIS speak clearly, the voice engine is working!
echo.
pause
