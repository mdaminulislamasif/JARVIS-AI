@echo off
title JARVIS BROWSER SYSTEM
color 0A

:MENU
cls
echo.
echo  ========================================================================
echo                      JARVIS BROWSER SYSTEM
echo                   Complete Web Learning Platform
echo  ========================================================================
echo.
echo   [#]  Browser Control    [#]  Auto-Learning    [#]  Knowledge Base
echo.
echo  ========================================================================
echo.
echo 1. JARVIS Conversational (Talk Together) [NEW!]
echo 2. JARVIS Autonomous (Complete AI)
echo 3. Browser Controller (Manual Control)
echo 4. Voice Browser (Voice Control)
echo 5. Auto-Learner (Learn Everything)
echo 6. Quick Learn (15 min session)
echo 7. View Learning Summary
echo 8. Read Guide
echo 9. Install Requirements
echo 0. Exit
echo.
echo ========================================

set /p choice="Select option (0-9): "

if "%choice%"=="1" goto CONVERSATIONAL
if "%choice%"=="2" goto AUTONOMOUS
if "%choice%"=="3" goto BROWSER
if "%choice%"=="4" goto VOICEBROWSER
if "%choice%"=="5" goto AUTOLEARN
if "%choice%"=="6" goto QUICKLEARN
if "%choice%"=="7" goto SUMMARY
if "%choice%"=="8" goto GUIDE
if "%choice%"=="9" goto INSTALL
if "%choice%"=="0" goto EXIT

echo Invalid choice!
timeout /t 2 >nul
goto MENU

:CONVERSATIONAL
cls
echo ========================================
echo    JARVIS CONVERSATIONAL AI
echo    Talk Together Like Friends!
echo ========================================
echo.
echo Installing packages...
pip install SpeechRecognition pyttsx3 pyaudio requests beautifulsoup4 --quiet
echo.
echo Starting Conversational JARVIS...
echo Have natural conversations!
echo.
python jarvis_conversational.py
pause
goto MENU

:AUTONOMOUS
cls
echo ========================================
echo    JARVIS AUTONOMOUS SYSTEM
echo    Complete AI - Does Everything!
echo ========================================
echo.
echo Installing packages...
pip install SpeechRecognition pyttsx3 pyaudio requests beautifulsoup4 --quiet
echo.
echo Starting JARVIS Autonomous...
echo Speak naturally - JARVIS understands everything!
echo Say "autonomous mode" for full automation!
echo.
python jarvis_autonomous.py
pause
goto MENU

:BROWSER
cls
echo Starting Browser Controller...
python jarvis_browser_controller.py
pause
goto MENU

:VOICEBROWSER
cls
echo ========================================
echo    JARVIS VOICE BROWSER
echo ========================================
echo.
echo Installing voice packages...
pip install SpeechRecognition pyttsx3 pyaudio --quiet
echo.
echo Starting Voice Browser...
echo Speak your commands when you see "Listening..."
echo.
python jarvis_voice_browser.py
pause
goto MENU

:AUTOLEARN
cls
echo Starting Auto-Learner...
python jarvis_auto_learner.py
pause
goto MENU

:QUICKLEARN
cls
echo Starting Quick Learning Session...
echo This will learn 10 topics in 15 minutes
echo.
python -c "from jarvis_auto_learner import JarvisAutoLearner; learner = JarvisAutoLearner(); learner.auto_learn_session(15, 10)"
pause
goto MENU

:SUMMARY
cls
echo Loading Learning Summary...
python -c "from jarvis_browser_controller import JarvisBrowserController; browser = JarvisBrowserController(); browser.get_learning_summary()"
pause
goto MENU

:GUIDE
cls
type JARVIS_BROWSER_GUIDE.txt
pause
goto MENU

:INSTALL
cls
echo Installing required packages...
echo.
echo [1/3] Installing browser packages...
pip install requests beautifulsoup4
echo.
echo [2/3] Installing voice packages...
pip install SpeechRecognition pyttsx3
echo.
echo [3/3] Installing audio package...
pip install pyaudio
echo.
echo Installation complete!
echo.
echo Note: If pyaudio failed, you may need to:
echo   1. pip install pipwin
echo   2. pipwin install pyaudio
echo.
pause
goto MENU

:EXIT
cls
echo.
echo Thank you for using JARVIS Browser System!
echo.
timeout /t 2 >nul
exit
