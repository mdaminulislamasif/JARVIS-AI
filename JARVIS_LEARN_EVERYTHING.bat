@echo off
title JARVIS AUTO-LEARNER - LEARN EVERYTHING
color 0B

echo ========================================
echo    JARVIS AUTO-LEARNER
echo    LEARN EVERYTHING MODE
echo ========================================
echo.
echo Installing required packages...
pip install requests beautifulsoup4 --quiet

echo.
echo Starting auto-learning system...
echo.

python jarvis_auto_learner.py

pause
