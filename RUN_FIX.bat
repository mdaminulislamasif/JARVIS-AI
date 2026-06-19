@echo off
title FIX JARVIS API QUOTA PROBLEM
color 0C

cls
echo ========================================
echo    FIX JARVIS API QUOTA PROBLEM
echo ========================================
echo.
echo This will fix your JARVIS to:
echo  * Auto-switch to offline brain
echo  * Handle quota errors gracefully
echo  * Continue working without API keys
echo.
echo Your files will be backed up first!
echo.
echo ========================================
echo.

python FIX_QUOTA_PROBLEM.py

echo.
echo ========================================
echo.
echo After this fix, restart your JARVIS!
echo.
echo ========================================

pause
