@echo off
echo ========================================
echo Cheng Bot Name Changer
echo ========================================
echo.
echo This will replace "Cheng Bot" with your chosen name
echo in all documentation files.
echo.
echo Options:
echo   1. ASIF
echo   2. AI
echo   3. Custom name
echo.

python CHANGE_CHENG BOT_NAME.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Python script failed!
    echo.
    echo Make sure Python is installed:
    echo   python --version
    echo.
)

pause
